"""Bounded optional provider work, separate from saving and exercise access."""
import asyncio
import json
import httpx
from .domain import PROMPT_VERSION, QUESTIONS, allowed_references, render_fragments


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
            return {"reason_code": "invented", "text": "unapproved text"}, "peyce-mock-1.0"
        eligible = allowed_references(snapshot, result)
        if self.settings.model_mode == "mock":
            # Deliberate deterministic variation tests construction; it is
            # labeled mock throughout, never evidence of a live contribution.
            answered_total = sum(a for a in snapshot["answers"] if a is not None)
            return {"reason_code": result["code"], "opening_id": "reflect" if answered_total % 2 == 0 else "notice", "reference_ids": eligible[:2], "closing_id": "choice" if answered_total % 2 == 0 else "change"}, "peyce-mock-1.0"
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
        messages = [{"role": "system", "content": "Peyce (pronounced peace) is a fictional coursework interface. Return exactly ONE JSON object, with no Markdown fences, commentary, thinking, extra keys or prose. Choose only JSON phrase IDs and eligible current-turn references to acknowledge the actual selections. Do not choose an exercise, assess risk, diagnose, score, add prose or instructions. The approved rule result is fixed. Reflect acknowledges a selection directly; notice gently acknowledges it. Choice offers choosing or finishing; change reminds that the person may change their mind. Reference the most relevant eligible answer(s), never a skip. Enforced application schema: " + json.dumps(schema, separators=(",", ":")) + ". Valid shape example (choose IDs/references appropriate to the actual turns): " + json.dumps(example, separators=(",", ":")) + ". Current approved context: " + json.dumps(context, ensure_ascii=False)}, *turns]
        if len(json.dumps(messages, ensure_ascii=False).encode()) > 5000:
            raise ValueError("Input context exceeded its fixed budget")
        # Reserve before any outbound attempt, including a rejected request.
        if not self.repository.reserve_live_attempt(self.settings):
            raise PermissionError("live-attempt-or-budget-cap")
        body = {"model": self.settings.model_id, "messages": messages, "stream": False,
                "max_tokens": 1000, "temperature": 0.2,
                # The authorized model's current catalog does not advertise
                # response_format. Ask for exact JSON in context, then enforce
                # the entire grammar locally before displaying any text.
                "provider": {"require_parameters": True, "allow_fallbacks": False,
                             "max_price": {"prompt": 0, "completion": 0}}}
        async with httpx.AsyncClient(timeout=self.settings.model_timeout_seconds, follow_redirects=False) as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", json=body,
                                         headers={"Authorization": "Bearer " + self.settings.api_key,
                                                  "Content-Type": "application/json", "X-Title": "Peyce Part 3.2 fictional coursework"})
            response.raise_for_status()
            if len(response.content) > 16000:
                raise ValueError("Provider response exceeded safe bounds")
            value = response.json()
        content = value["choices"][0]["message"]["content"]
        if not isinstance(content, str) or len(content) > 2000:
            raise ValueError("Missing or excessive model content")
        actual_model = value.get("model", self.settings.model_id)
        if actual_model not in (self.settings.model_id, self.settings.model_id.removesuffix(":free")):
            raise ValueError("Provider returned an unapproved model identity")
        return json.loads(content), actual_model

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
            fragments, actual_model = await asyncio.wait_for(self.provider_fragments(snapshot, result, fault), timeout=self.settings.model_timeout_seconds)
            text = render_fragments(fragments, snapshot, result)
            response.update(status="validated", text=text, fragments=fragments, references=fragments["reference_ids"], model_id=actual_model)
            outcome = "validated"
        except (asyncio.TimeoutError, httpx.TimeoutException):
            outcome = "fallback-timeout"
        except PermissionError:
            outcome = "fallback-unavailable"
        except (ValueError, KeyError, TypeError, IndexError):
            outcome = "fallback-invalid"
        except httpx.HTTPStatusError as error:
            # Retain only bounded numeric diagnostics, never provider prose,
            # payloads, headers, URLs, credentials or exception representations.
            outcome = f"fallback-provider-http-{error.response.status_code}"
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
