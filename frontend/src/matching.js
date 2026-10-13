export const POLICY_VERSION = 'peyce-routing-1.0';
export function matchExercise(answers, directChoice = null) {
  if (directChoice && ['breathing', 'grounding'].includes(directChoice)) return { exercise: directChoice, code: 'direct-choice', reason: 'You chose this exercise. You can change your mind at any time.' };
  const [body, thought, present, breath, ground] = answers;
  if (breath === 2 && ground === 2) return { exercise: null, code: 'both-declined', reason: 'You would rather not try either exercise. You can finish here, or explore only if you choose.' };
  if (breath === 0 && ground !== 0) return { exercise: 'breathing', code: 'breathing-comfort', reason: 'You said a gentle breathing rhythm sounds comfortable. You can choose something else.' };
  if (ground === 0 && breath !== 0) return { exercise: 'grounding', code: 'grounding-comfort', reason: 'You said noticing things around you sounds comfortable. You can choose something else.' };
  if (breath === 0 && ground === 0 && [body, thought, present].every(v => v !== null)) {
    const external = Math.max(thought, present);
    if (body > external) return { exercise: 'breathing', code: 'body-cue', reason: `You said softening your shoulders and jaw is “${questionsLabel(0, body)}”, and breathing sounds comfortable. A gentle rhythm is one option.` };
    if (body < external) return { exercise: 'grounding', code: 'present-cue', reason: `You described ${thought >= present ? `a repeating thought as “${questionsLabel(1, thought)}”` : `your connection to what is around you as “${questionsLabel(2, present)}”`}, and noticing your surroundings sounds comfortable.` };
  }
  return { exercise: null, code: 'equal-choice', reason: 'There is no clear suggestion from these answers. You can choose either exercise, or finish here.' };
}
function questionsLabel(q, answer) {
  return [['easy', 'takes some effort', 'hard right now'], ['easy', 'it comes back', 'it keeps pulling me in'], ['present', 'a little distracted', 'far away']][q][answer];
}
