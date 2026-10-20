import test from 'node:test';
import assert from 'node:assert/strict';
import { SequenceTimer } from '../src/sequence.js';
import { SaveQueue } from '../src/api.js';

test('whole sequence includes reading, pacing and deliberate Finish', () => {
  const t = new SequenceTimer(); t.showInstructions(21000); t.showInstructions(25000);
  const result = t.finish(99000);
  assert.equal(result.entry_ms, 21000); assert.equal(result.counted_ms, 78000);
  assert.equal(t.finish(120000).finish_ms, 99000);
});
test('overlapping user/support intervals are subtracted once; background has no exclusion', () => {
  const t = new SequenceTimer(); t.showInstructions(1000);
  t.exclude('user', 5000); t.exclude('support', 7000); t.include('user', 10000); t.include('support', 12000);
  const r = t.finish(21000); assert.equal(r.raw_ms, 20000); assert.equal(r.excluded_ms, 7000); assert.equal(r.counted_ms, 13000);
});
test('an open pause is clipped at Finish and pre-instruction time is separate', () => {
  const t = new SequenceTimer(); t.exclude('support', 100); t.showInstructions(1000);
  const r = t.finish(4000); assert.equal(r.excluded_ms, 3000); assert.equal(r.counted_ms, 0);
});
test('save queue captures values, preserves order and recovers after a failed write', async () => {
  const seen = []; const queue = new SaveQueue(async v => { seen.push(v.revision); if (v.revision === 1) throw Error('controlled'); return v; });
  const payload = { revision: 1 }; const first = queue.enqueue(payload); payload.revision = 99;
  const second = queue.enqueue({ revision: 2 });
  await assert.rejects(first); assert.equal((await second).revision, 2); assert.deepEqual(seen, [1, 2]);
});
