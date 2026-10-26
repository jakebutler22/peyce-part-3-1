"""Pure versioned routing and approved model grammar. No clinical inference."""
QUESTION_VERSION = "peyce-original-1.0"
POLICY_VERSION = "peyce-routing-1.0"
PROMPT_VERSION = "peyce-acknowledgment-1.1"
CONTENT_VERSION = "peyce-skills-1.0"
QUESTIONS = [
    ("body", "How easy is it to let your shoulders and jaw soften right now?", ["Easy", "Takes some effort", "Hard right now"]),
    ("thought", "How easy is it to set a repeating thought aside for a moment?", ["Easy", "It comes back", "It keeps pulling me in"]),
    ("present", "How connected do you feel to what's around you?", ["Present", "A little distracted", "Far away"]),
    ("breathing", "How does following a gentle breathing rhythm sound right now?", ["Comfortable", "Not sure", "I'd rather not"]),
    ("grounding", "How does noticing a few things around you sound right now?", ["Comfortable", "Not sure", "I'd rather not"]),
]


def match_exercise(answers, direct_choice=None):
    if direct_choice in ("breathing", "grounding"):
        return dict(exercise=direct_choice, code="direct-choice", reason="You chose this exercise. You can change your mind at any time.")
    body, thought, present, breath, ground = answers
    if breath == 2 and ground == 2:
        return dict(exercise=None, code="both-declined", reason="You would rather not try either exercise. You can finish here, or explore only if you choose.")
    if breath == 0 and ground != 0:
        return dict(exercise="breathing", code="breathing-comfort", reason="You said a gentle breathing rhythm sounds comfortable. You can choose something else.")
    if ground == 0 and breath != 0:
        return dict(exercise="grounding", code="grounding-comfort", reason="You said noticing things around you sounds comfortable. You can choose something else.")
    if breath == 0 and ground == 0 and all(v is not None for v in (body, thought, present)):
        if body > max(thought, present):
            label = QUESTIONS[0][2][body].lower()
            return dict(exercise="breathing", code="body-cue", reason=f"You said softening your shoulders and jaw is “{label}”, and breathing sounds comfortable. A gentle rhythm is one option.")
        if body < max(thought, present):
            detail = f'a repeating thought as “{QUESTIONS[1][2][thought].lower()}”' if thought >= present else f'your connection to what is around you as “{QUESTIONS[2][2][present].lower()}”'
            return dict(exercise="grounding", code="present-cue", reason=f"You described {detail}, and noticing your surroundings sounds comfortable.")
    return dict(exercise=None, code="equal-choice", reason="There is no clear suggestion from these answers. You can choose either exercise, or finish here.")


def allowed_references(snapshot, result):
    code = result["code"]
    if code == "body-cue":
        return ["body", "breathing"]
    if code == "present-cue":
        return ["thought" if snapshot["answers"][1] >= snapshot["answers"][2] else "present", "grounding"]
    if code == "breathing-comfort":
        return ["breathing"]
    if code == "grounding-comfort":
        return ["grounding"]
    if code == "both-declined":
        return ["breathing", "grounding"]
    if code == "equal-choice" and all(snapshot["answers"][i] is not None for i in range(5)) and snapshot["answers"][3:] == [0, 0]:
        return ["body", "thought", "present"]
    return []


def render_fragments(fragments, snapshot, result):
    """Validate an enforceable phrase grammar; never render provider prose."""
    if set(fragments) != {"reason_code", "opening_id", "reference_ids", "closing_id"}:
        raise ValueError("Unknown or missing fragment fields")
    if fragments["reason_code"] != result["code"] or fragments["opening_id"] not in ("reflect", "notice") or fragments["closing_id"] not in ("choice", "change"):
        raise ValueError("Fragment does not belong to the committed rule result")
    references = fragments["reference_ids"]
    eligible = allowed_references(snapshot, result)
    if not isinstance(references, list) or len(references) > 2 or len(set(references)) != len(references) or any(r not in eligible for r in references):
        raise ValueError("Unsupported reference")
    if eligible and not references:
        raise ValueError("Relevant current-turn references required")
    labels = {q[0]: (i, q[2]) for i, q in enumerate(QUESTIONS)}
    contexts = dict(body="shoulders/jaw", thought="repeating thought", present="connection", breathing="breathing", grounding="grounding")
    acknowledgment = []
    for reference in references:
        i, options = labels[reference]
        answer = snapshot["answers"][i]
        if not snapshot["answered"][i] or answer is None:
            raise ValueError("Skipped or absent turn cannot support an explanation")
        acknowledgment.append(f'{contexts[reference]}: “{options[answer]}”')
    opening = "You selected " if fragments["opening_id"] == "reflect" else "You noted "
    if acknowledgment:
        prefix = opening + "; ".join(acknowledgment) + ". "
    elif result["code"] == "direct-choice":
        prefix = ("You chose " if fragments["opening_id"] == "reflect" else "Your choice is ") + result["exercise"] + ". "
    else:
        prefix = "There is no clear suggestion from these answers. " if fragments["opening_id"] == "reflect" else "Either option is available if you want it. "
    action = {"body-cue": "A gentle breathing rhythm is one option. ", "present-cue": "Noticing your surroundings is one option. ", "breathing-comfort": "Breathing is one option. ", "grounding-comfort": "Grounding is one option. ", "both-declined": "You can finish here. "}.get(result["code"], "")
    closing = "You can choose or finish." if fragments["closing_id"] == "choice" else "You can change your mind."
    text = prefix + action + closing
    if len(text) > 240:
        raise ValueError("Rendered acknowledgment exceeds 240 characters")
    return text
