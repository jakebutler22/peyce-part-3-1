from typing import Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, model_validator
from .domain import match_exercise

Skill = Literal["breathing", "grounding"]
Status = Literal["checkin", "choice", "ready", "active", "paused", "completed", "stopped", "interrupted", "finished"]


def merged_spans(spans, lower, upper):
    """Clip and merge spans; equivalent split/overlap representations are valid."""
    result = []
    for start, end in sorted((max(lower, start), min(upper, end)) for start, end in spans):
        if end <= start:
            continue
        if result and start <= result[-1][1] + 1:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result


def observed_exclusions(events, finish):
    """Only explicit user pauses/support suspend counted sequence time.

    Background pauses stop pacing, but remain in whole-sequence timing.
    Open permitted intervals close at the final action, as the client timer does.
    """
    spans = {"user": [], "support": []}
    opened = {}
    for event in events:
        if event.at_ms > finish + 1:
            break
        if event.kind == "pause" and event.cause == "user":
            opened.setdefault("user", event.at_ms)
        elif event.kind == "support_open" and event.cause == "support":
            opened.setdefault("support", event.at_ms)
        closing = []
        if event.kind in ("resume", "stop", "finish"):
            closing.append("user")
        if event.kind in ("support_close", "finish"):
            closing.append("support")
        for cause in closing:
            if cause in opened:
                spans[cause].append((opened.pop(cause), min(finish, event.at_ms)))
    for cause, start in opened.items():
        spans[cause].append((start, finish))
    return spans


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Event(StrictModel):
    id: UUID
    kind: Literal["instruction_visible", "start", "pause", "resume", "support_open", "support_close", "background_pause", "sense_next", "sense_skip", "complete", "stop", "finish", "leave"]
    at_ms: float = Field(ge=0, le=604800000, allow_inf_nan=False)
    active_ms: float = Field(ge=0, le=604800000, allow_inf_nan=False)
    cause: Literal["user", "support", "background", "navigation", "clock"]


class ExcludedInterval(StrictModel):
    start_ms: float = Field(ge=0, allow_inf_nan=False)
    end_ms: float = Field(ge=0, allow_inf_nan=False)
    cause: Literal["user", "support"]

    @model_validator(mode="after")
    def interval_order(self):
        if self.end_ms < self.start_ms:
            raise ValueError("An excluded interval ends before it begins")
        return self


class Timing(StrictModel):
    raw_ms: float = Field(ge=0, le=604800000, allow_inf_nan=False)
    counted_ms: float = Field(ge=0, le=604800000, allow_inf_nan=False)
    excluded_ms: float = Field(ge=0, le=604800000, allow_inf_nan=False)
    excluded_intervals: list[ExcludedInterval] = Field(max_length=200)
    instruction_ms: float = Field(ge=0, le=604800000, allow_inf_nan=False)
    finish_ms: float = Field(ge=0, le=604800000, allow_inf_nan=False)
    entry_ms: float = Field(ge=0, le=604800000, allow_inf_nan=False)

    @model_validator(mode="after")
    def arithmetic(self):
        if abs(self.raw_ms - (self.finish_ms - self.instruction_ms)) > 1:
            raise ValueError("Raw timing must include first instruction through final planned action")
        spans = sorted((max(self.instruction_ms, p.start_ms), min(self.finish_ms, p.end_ms)) for p in self.excluded_intervals)
        union = 0.0
        edge = self.instruction_ms
        for start, end in spans:
            if end > max(start, edge):
                union += end - max(start, edge)
                edge = end
        if abs(self.excluded_ms - union) > 1 or abs(self.counted_ms - (self.raw_ms - union)) > 1:
            raise ValueError("Excluded time must be the union of user/support intervals, without double subtraction")
        return self


class Snapshot(StrictModel):
    operation_id: UUID
    revision: StrictInt = Field(ge=1, le=1000000)
    answers: list[StrictInt | None] = Field(min_length=5, max_length=5)
    answered: list[StrictBool] = Field(min_length=5, max_length=5)
    direct_choice: Skill | None = None
    exercise: Skill | None = None
    status: Status = "checkin"
    color: Literal["pink", "red", "pearl"] = "pink"
    color_explicit: StrictBool = False
    events: list[Event] = Field(default_factory=list, max_length=200)
    timing: Timing | None = None

    @model_validator(mode="after")
    def consistent(self):
        if any(a is not None and a not in (0, 1, 2) for a in self.answers):
            raise ValueError("Answers must be 0, 1, 2 or unknown")
        if any(not received and answer is not None for received, answer in zip(self.answered, self.answers)):
            raise ValueError("Unanswered questions remain null")
        if self.status in ("ready", "active", "paused", "completed") and self.exercise is None:
            raise ValueError("Exercise state requires an explicit selected exercise")
        if self.exercise is not None and self.exercise != match_exercise(self.answers, self.direct_choice)["exercise"]:
            raise ValueError("Selected exercise must match the approved rule or an explicit direct choice")
        if len({e.id for e in self.events}) != len(self.events) or any(b.at_ms < a.at_ms for a, b in zip(self.events, self.events[1:])):
            raise ValueError("Lifecycle event identifiers are unique and offsets monotonic")
        if any(e.active_ms > e.at_ms + 1 for e in self.events):
            raise ValueError("Active exercise time cannot exceed the recorded session span")
        if self.exercise is not None and self.status in ("completed", "finished"):
            completions = [i for i, e in enumerate(self.events) if e.kind == "complete"
                           and (self.exercise != "breathing" or e.active_ms >= 60000)]
            if not completions or not any(e.kind == "start" for e in self.events[:completions[0]]):
                raise ValueError("Exercise completion requires Start followed by an explicit completion")
            if self.status == "finished" and not any(e.kind == "finish" for e in self.events[completions[0] + 1:]):
                raise ValueError("A finished exercise requires Finish after completion")
        if self.exercise == "breathing" and self.status in ("completed", "finished") and not any(e.kind == "complete" and e.active_ms >= 60000 for e in self.events):
            raise ValueError("Breathing completion requires six actual active cycles")
        if self.exercise == "breathing" and self.status in ("completed", "finished"):
            complete = next(e for e in self.events if e.kind == "complete" and e.active_ms >= 60000)
            starts = [e for e in self.events if e.kind == "start" and e.at_ms <= complete.at_ms]
            if not starts or complete.at_ms - starts[0].at_ms < 59999:
                raise ValueError("Breathing completion must follow a full recorded pacing span")
        if self.status == "finished" and not any(e.kind == "finish" for e in self.events):
            raise ValueError("Finished status requires an explicit final action")
        if self.timing is not None and not any(e.kind == "instruction_visible" for e in self.events):
            raise ValueError("Timing requires a recorded first instruction")
        if self.timing is not None:
            instruction = next(e for e in self.events if e.kind == "instruction_visible")
            if abs(instruction.at_ms - self.timing.instruction_ms) > 1:
                raise ValueError("Timing must refer to the actual first instruction event")
            if self.status == "finished" and abs(next(e for e in reversed(self.events) if e.kind == "finish").at_ms - self.timing.finish_ms) > 1:
                raise ValueError("Timing must include the actual final Finish event")
            observed = observed_exclusions(self.events, self.timing.finish_ms)
            for cause in ("user", "support"):
                expected = merged_spans(observed[cause], self.timing.instruction_ms, self.timing.finish_ms)
                claimed = merged_spans(((p.start_ms, p.end_ms) for p in self.timing.excluded_intervals if p.cause == cause), self.timing.instruction_ms, self.timing.finish_ms)
                if len(expected) != len(claimed) or any(abs(a - b) > 1 for observed_span, claimed_span in zip(expected, claimed) for a, b in zip(observed_span, claimed_span)):
                    raise ValueError("Timing exclusions must match recorded user-pause/support intervals")
        return self


class ExplanationRequest(StrictModel):
    revision: StrictInt = Field(ge=1, le=1000000)
    request_id: UUID


class InterruptRequest(StrictModel):
    revision: StrictInt = Field(ge=1, le=1000000)
    operation_id: UUID
