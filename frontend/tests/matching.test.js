import test from 'node:test';
import assert from 'node:assert/strict';
import { matchExercise, POLICY_VERSION } from '../src/matching.js';
import { questions, QUESTION_VERSION, senses } from '../src/data.js';

const routingExamples = [
  ['body-tension path', [2, 0, 0, 0, 0], 'breathing', 'body-cue'],
  ['present-focus path', [0, 2, 1, 0, 0], 'grounding', 'present-cue'],
  ['preference overrides body cue', [2, 0, 0, 2, 0], 'grounding', 'grounding-comfort'],
  ['preference overrides present cue', [0, 2, 2, 0, 2], 'breathing', 'breathing-comfort'],
  ['both activities declined', [2, 2, 2, 2, 2], null, 'both-declined'],
  ['all skipped', [null, null, null, null, null], null, 'equal-choice'],
  ['all comfortable cue answers', [0, 0, 0, 0, 0], null, 'equal-choice'],
  ['nonzero tie', [2, 2, 1, 0, 0], null, 'equal-choice'],
  ['missing body cue', [null, 0, 0, 0, 0], null, 'equal-choice'],
  ['missing thought cue', [2, null, 0, 0, 0], null, 'equal-choice'],
  ['missing present cue', [2, 0, null, 0, 0], null, 'equal-choice'],
  ['only breathing comfortable, grounding unsure', [null, null, null, 0, 1], 'breathing', 'breathing-comfort'],
  ['only grounding comfortable, breathing unsure', [null, null, null, 1, 0], 'grounding', 'grounding-comfort'],
  ['grounding unknown, expressed breathing comfort', [null, null, null, 0, null], 'breathing', 'breathing-comfort'],
  ['breathing unknown, expressed grounding comfort', [null, null, null, null, 0], 'grounding', 'grounding-comfort'],
  ['breathing declined, grounding unknown', [2, 0, 0, 2, null], null, 'equal-choice'],
  ['grounding declined, breathing unknown', [0, 2, 2, null, 2], null, 'equal-choice'],
  ['breathing declined, grounding unsure', [2, 0, 0, 2, 1], null, 'equal-choice'],
  ['grounding declined, breathing unsure', [0, 2, 2, 1, 2], null, 'equal-choice'],
  ['both activities unsure', [2, 0, 0, 1, 1], null, 'equal-choice'],
  ['cue answers cannot supply missing willingness', [2, 0, 0, null, null], null, 'equal-choice'],
];

for (const [name, answers, exercise, code] of routingExamples) {
  test(`routing: ${name}`, () => {
    const snapshot = [...answers];
    const result = matchExercise(Object.freeze(answers));
    assert.equal(result.exercise, exercise);
    assert.equal(result.code, code);
    assert.deepEqual(answers, snapshot, 'routing must not rewrite answers');
    assert.ok(result.reason.length > 0);
  });
}

test('a deliberate current exercise choice overrides any offered suggestion or refusal', () => {
  for (const chosen of ['breathing', 'grounding']) {
    for (const answers of [[2, 0, 0, 0, 0], [0, 2, 2, 0, 0], [2, 2, 2, 2, 2], Array(5).fill(null)]) {
      const result = matchExercise(answers, chosen);
      assert.equal(result.exercise, chosen);
      assert.equal(result.code, 'direct-choice');
      assert.match(result.reason, /You chose this exercise/);
    }
  }
});

test('unrecognized direct choice cannot bypass the approved choices', () => {
  for (const chosen of ['diagnose', 'score', 'unknown', 1]) {
    const result = matchExercise(Array(5).fill(null), chosen);
    assert.equal(result.exercise, null);
    assert.equal(result.code, 'equal-choice');
  }
});

test('explanations cite the selected content and activity comfort', () => {
  const body = matchExercise([2, 0, 0, 0, 0]);
  assert.match(body.reason, /hard right now/);
  assert.match(body.reason, /breathing sounds comfortable/);
  const thought = matchExercise([0, 2, 1, 0, 0]);
  assert.match(thought.reason, /it keeps pulling me in/);
  assert.match(thought.reason, /noticing your surroundings sounds comfortable/);
  const present = matchExercise([0, 1, 2, 0, 0]);
  assert.match(present.reason, /far away/);
});

test('recomputing after a Back edit produces a fresh result without altering the earlier result', () => {
  const answers = [2, 0, 0, 0, 0];
  const earlierResult = matchExercise(answers);
  const earlierSnapshot = structuredClone(earlierResult);
  assert.equal(earlierResult.exercise, 'breathing');
  answers[3] = 2; // Fictional Back edit: breathing is now declined.
  const updatedResult = matchExercise(answers);
  assert.notStrictEqual(updatedResult, earlierResult);
  assert.equal(updatedResult.exercise, 'grounding');
  assert.equal(updatedResult.code, 'grounding-comfort');
  assert.deepEqual(earlierResult, earlierSnapshot);
  answers[4] = null; // A subsequent skip removes the remaining comfort preference.
  const skippedResult = matchExercise(answers);
  assert.equal(skippedResult.exercise, null);
  assert.equal(skippedResult.code, 'equal-choice');
  assert.deepEqual(earlierResult, earlierSnapshot);
});

test('all 4^5 answer tuples satisfy refusal, unknown-answer, and no-score safety invariants', () => {
  const values = [null, 0, 1, 2];
  let checked = 0;
  for (const body of values) for (const thought of values) for (const present of values) {
    for (const breath of values) for (const ground of values) {
      const answers = Object.freeze([body, thought, present, breath, ground]);
      const context = JSON.stringify(answers);
      const result = matchExercise(answers);
      assert.deepEqual(Object.keys(result).sort(), ['code', 'exercise', 'reason'], context);
      assert.ok([null, 'breathing', 'grounding'].includes(result.exercise), context);
      assert.doesNotMatch(result.reason, /undefined|\bnull\b|diagnos|anxiety score/i, context);
      // Automatic suggestions always require today's explicit comfort with that activity.
      if (result.exercise === 'breathing') assert.equal(breath, 0, context);
      if (result.exercise === 'grounding') assert.equal(ground, 0, context);
      if (breath === 2 && ground === 2) {
        assert.equal(result.exercise, null, context);
        assert.equal(result.code, 'both-declined', context);
      }
      // Unknown or unsure willingness cannot be upgraded into permission by the cues.
      if (breath !== 0 && ground !== 0) assert.equal(result.exercise, null, context);
      // Cue routing needs all three current cue answers; a skip cannot justify it.
      if (breath === 0 && ground === 0 && answers.slice(0, 3).includes(null)) {
        assert.equal(result.exercise, null, context);
        assert.equal(result.code, 'equal-choice', context);
      }
      if (breath === 0 && ground === 0 && body === Math.max(thought, present)) {
        assert.equal(result.exercise, null, context);
      }
      assert.deepEqual(matchExercise(answers), result, `deterministic policy: ${context}`);
      checked += 1;
    }
  }
  assert.equal(checked, 1024);
});

test('the original five questions and ordered question-specific labels are exact and versioned', () => {
  assert.equal(POLICY_VERSION, 'peyce-routing-1.0');
  assert.equal(QUESTION_VERSION, 'peyce-original-1.0');
  assert.deepEqual(questions.map(({ id, text, labels }) => ({ id, text, labels })), [
    { id: 'body', text: 'How easy is it to let your shoulders and jaw soften right now?', labels: ['Easy', 'Takes some effort', 'Hard right now'] },
    { id: 'thought', text: 'How easy is it to set a repeating thought aside for a moment?', labels: ['Easy', 'It comes back', 'It keeps pulling me in'] },
    { id: 'present', text: "How connected do you feel to what's around you?", labels: ['Present', 'A little distracted', 'Far away'] },
    { id: 'breathing', text: 'How does following a gentle breathing rhythm sound right now?', labels: ['Comfortable', 'Not sure', "I'd rather not"] },
    { id: 'grounding', text: 'How does noticing a few things around you sound right now?', labels: ['Comfortable', 'Not sure', "I'd rather not"] },
  ]);
});

test('grounding preserves the five private noticing steps and does not require eating or drinking', () => {
  assert.deepEqual(senses.map(({ quantity, sense }) => [quantity, sense]), [[5, 'see'], [4, 'feel'], [3, 'hear'], [2, 'smell'], [1, 'taste']]);
  assert.match(senses[4].guidance, /do not need to eat or drink/);
  assert.match(senses[3].guidance, /safely around you/);
  assert.match(senses[3].guidance, /skip/);
});
