"""Bounded optional provider work, separate from saving and exercise access."""
import asyncio
import json
import httpx
from .domain import PROMPT_VERSION, QUESTIONS, allowed_references, render_fragments


INVALID_STAGES = frozenset({"input-size", "response-size", "response-json", "response-envelope",
                            "model-identity", "content-missing", "content-empty", "content-size",
                            "content-json", "content-truncated", "fragment-schema", "tool-calls",
                            "tool-envelope", "tool-name", "tool-arguments-missing", "tool-arguments-size",
                            "tool-arguments-json", "tool-arguments-truncated", "unexpected-prose"})
FINISH_REASONS = frozenset({"stop", "length", "content_filter", "tool_calls", "error", "other"})
ACKNOWLEDGMENT_TOOL = "acknowledge_current_rule"


def safe_diagnostic(value):
    """Retain fixed categories and bounded integers, never provider strings."""
    diagnostic = {}
    if value.get("invalid_stage") in INVALID_STAGES:
        diagnostic["invalid_stage"] = value["invalid_stage"]
    if value.get("finish_reason") in FINISH_REASONS:
        diagnostic["finish_reason"] = value["finish_reason"]
    for name, lower, upper in (("http_status", 100, 599), ("completion_tokens", 0, 1000000),
                               ("reasoning_tokens", 0, 1000000)):
        number = value.get(name)
        if isinstance(number, int) and not isinstance(number, bool) and lower <= number <= upper:
            diagnostic[name] = number
    return diagnostic


class InvalidProviderResponse(ValueError):
    def __init__(self, stage, diagnostic=None):
        self.diagnostic = safe_diagnostic({**(diagnostic or {}), "invalid_stage": stage})
        super().__init__("Provider response failed application validation")


def response_diagnostic(value, status):
    metadata = {"http_status": status}
    if isinstance(value, dict):
        usage = value.get("usage")
        if isinstance(usage, dict):
            metadata["completion_tokens"] = usage.get("completion_tokens")
            details = usage.get("completion_tokens_details")
            if isinstance(details, dict):
                metadata["reasoning_tokens"] = details.get("reasoning_tokens")
        choices = value.get("choices")
        if isinstance(choices, list) and choices and isinstance(choices[0], dict):
            reason = choices[0].get("finish_reason")
            if reason is not None:
                metadata["finish_reason"] = reason if isinstance(reason, str) and reason in FINISH_REASONS else "other"
    return safe_diagnostic(metadata)


def parse_fragment_json(arguments):
    """Reject ambiguous duplicate keys and non-JSON constants as well as prose."""
    def object_fields(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate fragment field")
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError("Non-JSON constant")

    return json.loads(arguments, object_pairs_hook=object_fields, parse_constant=invalid_constant)


class ModelService:
    def __init__(self, settings, repository):
        self.settings, self.repository = settings, repository

    def identity(self):
        if self.settings.model_mode == "mock":
            return "mock", "peyce-mock-1.0"
        return self.settings.model_mode, self.settings.model_id or "unconfigured"

    async def provider_fragments(self, snapshot, result, fault=None):
        """Exactly one provider request; tests use an entirely local mock."""
        if fault == "timeout":
            await asyncio.sleep(self.settings.model_timeout_seconds + 1)
        if fault == "provider":
            raise RuntimeError("injected-provider-failure")
        if fault == "invalid":
            return {"reason_code": "invented", "text": "unapproved text"}, "peyce-mock-1.0", {}
        eligible = allowed_references(snapshot, result)
        if self.settings.model_mode == "mock":
            # Deliberate deterministic variation tests construction; it is
            # labeled mock throughout, never evidence of a live contribution.
            answered_total = sum(a for a in snapshot["answers"] if a is not None)
            return {"reason_code": result["code"], "opening_id": "reflect" if answered_total % 2 == 0 else "notice", "reference_ids": eligible[:2], "closing_id": "choice" if answered_total % 2 == 0 else "change"}, "peyce-mock-1.0", {}
        if self.settings.model_mode != "openrouter" or not self.settings.live_configured:
            raise PermissionError("live-configuration-unavailable")
        turns = []
        for index, (qid, question, labels) in enumerate(QUESTIONS):
            if snapshot["answered"][index]:
                answer = snapshot["answers"][index]
                turns.extend([{"role": "assistant", "content": question}, {"role": "user", "content": "Skipped this question" if answer is None else labels[answer]}])
        context = {"prompt_version": PROMPT_VERSION, "approved_rule_result": result,
                   "deliberate_exercise": snapshot["exercise"], "direct_choice": snapshot["direct_choice"],
                   "eligible_current_question_ids": eligible}
        schema = {"type": "object", "additionalProperties": False,
                  "required": ["reason_code", "opening_id", "reference_ids", "closing_id"],
                  "properties": {"reason_code": {"type": "string", "enum": [result["code"]]},
                                 "opening_id": {"type": "string", "enum": ["reflect", "notice"]},
                                 "reference_ids": {"type": "array", "items": {"type": "string", "enum": eligible or ["__none_allowed__"]}, "minItems": 1 if eligible else 0, "maxItems": min(2, len(eligible))},
                                 "closing_id": {"type": "string", "enum": ["choice", "change"]}}}
        example = {"reason_code": result["code"], "opening_id": "reflect", "reference_ids": eligible[:2], "closing_id": "choice"}
        tools = [{"type": "function", "function": {"name": ACKNOWLEDGMENT_TOOL,
                  "description": "Acknowledge the approved rule using only permitted phrase IDs and current answer references. This selects data; no external action is executed.",
                  "parameters": schema}}]
        messages = [{"role": "system", "content": "Peyce (pronounced peace) is a fictional coursework interface. Call acknowledge_current_rule exactly ONCE, with no Markdown fences, commentary, thinking, extra keys or prose. Choose only JSON phrase IDs and eligible current-turn references to acknowledge the actual selections. Do not choose an exercise, assess risk, diagnose, score, add prose or instructions. The approved rule result is fixed. Reflect acknowledges a selection directly; notice gently acknowledges it. Choice offers choosing or finishing; change reminds that the person may change their mind. Reference the most relevant eligible answer(s), never a skip. Use the supplied function parameter schema. Valid argument shape example (choose IDs/references appropriate to the actual turns): " + json.dumps(example, separators=(",", ":")) + ". Current approved context: " + json.dumps(context, ensure_ascii=False)}, *turns]
        if len(json.dumps({"messages": messages, "tools": tools}, ensure_ascii=False).encode()) > 5000:
            raise InvalidProviderResponse("input-size")
        # Reserve before any outbound attempt, including a rejected request.
        if not self.repository.reserve_live_attempt(self.settings):
            raise PermissionError("live-attempt-or-budget-cap")
        body = {"model": self.settings.model_id, "messages": messages, "stream": False,
                "max_tokens": 1000, "temperature": 0.2,
                # The verified free model supports optional reasoning. Keep
                # the fixed output budget for the approved phrase IDs.
                "reasoning": {"enabled": False, "exclude": True},
                "tools": tools,
                "tool_choice": {"type": "function", "function": {"name": ACKNOWLEDGMENT_TOOL}},
                # A named data-only call transports the existing grammar.
                # No function or follow-up provider request is executed.
                "provider": {"require_parameters": True, "allow_fallbacks": False,
                             "max_price": {"prompt": 0, "completion": 0}}}
        async with httpx.AsyncClient(timeout=self.settings.model_timeout_seconds, follow_redirects=False) as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", json=body,
                                         headers={"Authorization": "Bearer " + self.settings.api_key,
                                                  "Content-Type": "application/json", "X-Title": "Peyce Part 3.2 fictional coursework"})
            response.raise_for_status()
            if len(response.content) > 16000:
                raise InvalidProviderResponse("response-size", {"http_status": response.status_code})
            try:
                value = response.json()
            except ValueError:
                raise InvalidProviderResponse("response-json", {"http_status": response.status_code}) from None
        diagnostic = response_diagnostic(value, response.status_code)
        if not isinstance(value, dict) or not isinstance(value.get("choices"), list) or not value["choices"] or not isinstance(value["choices"][0], dict) or not isinstance(value["choices"][0].get("message"), dict):
            raise InvalidProviderResponse("response-envelope", diagnostic)
        actual_model = value.get("model")
        if actual_model not in (self.settings.model_id, self.settings.model_id.removesuffix(":free")):
            raise InvalidProviderResponse("model-identity", diagnostic)
        message = value["choices"][0]["message"]
        content = message.get("content")
        if content is not None and (not isinstance(content, str) or content.strip()):
            raise InvalidProviderResponse("unexpected-prose", diagnostic)
        calls = message.get("tool_calls")
        if not isinstance(calls, list) or len(calls) != 1:
            raise InvalidProviderResponse("tool-calls", diagnostic)
        call = calls[0]
        if not isinstance(call, dict) or call.get("type") != "function" or not isinstance(call.get("function"), dict):
            raise InvalidProviderResponse("tool-envelope", diagnostic)
        function = call["function"]
        if function.get("name") != ACKNOWLEDGMENT_TOOL:
            raise InvalidProviderResponse("tool-name", diagnostic)
        arguments = function.get("arguments")
        if not isinstance(arguments, str):
            raise InvalidProviderResponse("tool-arguments-missing", diagnostic)
        if len(arguments) > 2000:
            raise InvalidProviderResponse("tool-arguments-size", diagnostic)
        try:
            fragments = parse_fragment_json(arguments)
        except ValueError:
            raise InvalidProviderResponse("tool-arguments-truncated" if diagnostic.get("finish_reason") == "length" else "tool-arguments-json", diagnostic) from None
        return fragments, actual_model, diagnostic

    async def explain(self, session_id, request, fault=None):
        mode, model_id = self.identity()
        current, replay = self.repository.begin_explanation(session_id, request, mode, model_id)
        if replay is not None:
            return replay
        snapshot, result = current
        response = dict(session_id=session_id, revision=request.revision, request_id=str(request.request_id),
                        mode=mode, model_id=model_id, status="fallback", text=result["reason"], fragments=None, references=[], stale=False)
        outcome = "fallback-unavailable"
        try:
            if fault == "late":
                # Deliberate test-only latency before the bounded adapter call.
                await asyncio.sleep(self.settings.test_late_seconds)
            fragments, actual_model, diagnostic = await asyncio.wait_for(self.provider_fragments(snapshot, result, fault), timeout=self.settings.model_timeout_seconds)
            if diagnostic:
                response["diagnostic"] = safe_diagnostic(diagnostic)
            text = render_fragments(fragments, snapshot, result)
            response.update(status="validated", text=text, fragments=fragments, references=fragments["reference_ids"], model_id=actual_model)
            outcome = "validated"
        except (asyncio.TimeoutError, httpx.TimeoutException):
            outcome = "fallback-timeout"
        except PermissionError:
            outcome = "fallback-unavailable"
        except InvalidProviderResponse as error:
            response["diagnostic"] = error.diagnostic
            outcome = "fallback-invalid"
        except (ValueError, KeyError, TypeError, IndexError):
            response["diagnostic"] = safe_diagnostic({**response.get("diagnostic", {}), "invalid_stage": "fragment-schema"})
            outcome = "fallback-invalid"
        except httpx.HTTPStatusError as error:
            # Retain only bounded numeric diagnostics, never provider prose,
            # payloads, headers, URLs, credentials or exception representations.
            outcome = f"fallback-provider-http-{error.response.status_code}"
            response["diagnostic"] = safe_diagnostic({"http_status": error.response.status_code})
            if len(error.response.content) <= 16000:
                try:
                    upstream_code = error.response.json().get("error", {}).get("code")
                    if isinstance(upstream_code, int) and not isinstance(upstream_code, bool) and 0 <= upstream_code <= 999999:
                        outcome += f"-code-{upstream_code}"
                except (ValueError, AttributeError, TypeError):
                    pass
        except httpx.RequestError as error:
            names = {"ConnectError", "ReadError", "WriteError", "CloseError", "NetworkError",
                     "ProxyError", "ProtocolError", "LocalProtocolError", "RemoteProtocolError",
                     "UnsupportedProtocol", "TooManyRedirects", "RequestError"}
            category = type(error).__name__ if type(error).__name__ in names else "RequestError"
            outcome = "fallback-provider-" + category
        except (httpx.HTTPError, RuntimeError):
            outcome = "fallback-provider"
        return self.repository.finish_explanation(session_id, request, response, outcome)
