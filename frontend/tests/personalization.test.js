import test from 'node:test';
import assert from 'node:assert/strict';
import { createSSRApp, nextTick } from 'vue';
import { renderToString } from 'vue/server-renderer';
import { usePrototype } from '../src/usePrototype.js';
import { createColorPreference, COLOR_PREFERENCE_KEY } from '../src/preferences.js';

globalThis.window = { scrollTo() {} };
globalThis.document = { querySelector() { return null; } };
globalThis.sessionStorage = { setItem() {}, removeItem() {} };
globalThis.cancelAnimationFrame = () => {};

function memoryStorage(initial) {
  const values = new Map(initial === undefined ? [] : [[COLOR_PREFERENCE_KEY, initial]]);
  return { values, getItem: key => values.get(key) ?? null, setItem: (key, value) => values.set(key, value), removeItem: key => values.delete(key) };
}
async function harness({ storage = memoryStorage(), respond = async () => ({}) } = {}) {
  const calls = [], frames = [];
  globalThis.requestAnimationFrame = callback => frames.push(callback);
  const request = async (path, options = {}) => { calls.push({ path, ...structuredClone(options) }); return respond(path, options); };
  let p;
  await renderToString(createSSRApp({ setup() { p = usePrototype({ request, colorPreference: createColorPreference(() => storage) }); return () => null; } }));
  const paintReady = async () => { await nextTick(); frames.shift()?.(performance.now()); await new Promise(resolve => setImmediate(resolve)); };
  return { p, calls, storage, paintReady };
}
function assertSupportAccess(p, expectedScreen) {
  p.supportDialog.value ??= { open: false, showModal() { this.open = true; }, close() { this.open = false; } };
  assert.equal(p.screen.value, expectedScreen);
  p.openSupport();
  assert.equal(p.supportDialog.value.open, true);
  assert.equal(p.screen.value, expectedScreen);
  p.closeSupport();
  assert.equal(p.supportDialog.value.open, false);
}

test('[S08] explicit colour survives return and a fresh controller without storing session data', async () => {
  const storage = memoryStorage();
  const first = await harness({ storage });
  first.p.directEntry(); first.p.choose('breathing'); first.p.chooseColor('pearl'); first.p.go('home');
  assert.equal(first.p.color.value, 'pearl');
  assert.equal(first.p.saveState.value, 'unsaved');
  assert.equal(first.calls.length, 0);
  assert.deepEqual([...storage.values], [[COLOR_PREFERENCE_KEY, 'pearl']]);
  const afterReload = await harness({ storage });
  assert.equal(afterReload.p.color.value, 'pearl');
  assert.equal(afterReload.p.saveEnabled.value, false);
  assert.deepEqual(afterReload.p.answers.value, Array(5).fill(null));
});

test('[S08 B3] saved sessions record the current explicit colour without changing the preference payload', async () => {
  const { p, calls, storage, paintReady } = await harness();
  p.saveEnabled.value = true; p.directEntry(); p.choose('breathing'); p.chooseColor('red');
  await paintReady();
  const snapshots = calls.filter(call => call.method === 'PUT');
  assert.equal(snapshots.at(-1).body.color, 'red');
  assert.equal(snapshots.at(-1).body.color_explicit, true);
  assert.equal(p.saveState.value, 'saved');
  assert.deepEqual([...storage.values], [[COLOR_PREFERENCE_KEY, 'red']]);
});

test('[S08] invalid or unavailable browser storage falls back safely and never blocks unsaved practice', async () => {
  const invalid = await harness({ storage: memoryStorage('{"answers":[2,2,2,2,2]}') });
  assert.equal(invalid.p.color.value, 'pink');
  invalid.p.chooseColor('unsupported');
  assert.equal(invalid.p.color.value, 'pink');
  const blocked = await harness({ storage: { getItem() { throw Error('Blocked'); }, setItem() { throw Error('Blocked'); } } });
  blocked.p.directEntry(); blocked.p.choose('grounding'); blocked.p.chooseColor('red'); blocked.p.startExercise();
  assert.equal(blocked.p.screen.value, 'grounding');
  assert.equal(blocked.p.color.value, 'red');
  assert.match(blocked.p.colorStorageError.value, /could not remember/);
  assert.equal(blocked.calls.length, 0);
});

test('[S08 B2 B3] repeating a finished record creates a fresh unknown-answer session and waits for Start', async () => {
  const old = { id: '4ec92b1a-b12f-4c37-bb50-b3ae71478f67', status: 'finished', exercise: 'breathing', color: 'red', color_explicit: true, answers: [2, 0, 0, 0, 0], answered: [true, true, true, true, true], timing: { counted_ms: 80000 }, explanations: [{ text: 'Earlier model wording' }] };
  const { p, calls, paintReady } = await harness({ storage: memoryStorage('pearl'), respond: async path => path.endsWith(old.id) ? structuredClone(old) : {} });
  p.saveEnabled.value = true;
  await p.openSession(old.id);
  assert.equal(p.repeatSession(), true);
  assert.equal(p.screen.value, 'ready');
  assert.equal(p.sessionStatus.value, 'ready');
  assert.equal(p.exercise.value, 'breathing');
  assert.equal(p.color.value, 'pearl');
  assert.equal(p.selectedSession.value, null);
  assert.equal(p.explanationText.value, '');
  assert.equal(p.timing.value.elapsed, 0);
  assert.deepEqual(p.answers.value, Array(5).fill(null));
  await paintReady();
  const writes = calls.filter(call => call.method === 'PUT');
  const ids = new Set(writes.map(call => call.path.split('/')[2]));
  assert.equal(ids.size, 1);
  assert.notEqual([...ids][0], old.id);
  assert.ok(writes.every(call => call.body.answered.every(answered => !answered)));
  assert.ok(writes.every(call => call.body.timing === null));
  assert.ok(writes.every(call => !call.body.events.some(event => ['start', 'complete', 'finish'].includes(event.kind))));
  assert.equal(writes.at(-1).body.direct_choice, 'breathing');
  assert.equal(old.explanations[0].text, 'Earlier model wording');
  p.choose('grounding');
  assert.equal(p.exercise.value, 'grounding');
  assert.equal(p.result.value.code, 'direct-choice');
});

test('[S08 B2] repeating does not silently opt into saving or resume an unfinished record', async () => {
  let record = { id: 'old-record', status: 'finished', exercise: 'grounding' };
  const { p, calls, paintReady } = await harness({ respond: async () => record });
  await p.openSession(record.id); p.repeatSession(); await paintReady();
  assert.equal(p.saveEnabled.value, false);
  assert.equal(p.saveState.value, 'unsaved');
  assert.equal(p.screen.value, 'ready');
  assert.equal(calls.filter(call => call.method === 'PUT' || call.path.endsWith('/explanation')).length, 0);
  record = { id: 'stopped-record', status: 'stopped', exercise: 'breathing' };
  await p.openSession(record.id);
  assert.equal(p.repeatSession(), false);
  assert.equal(p.screen.value, 'session-detail');
});

test('[S16 B3] cancel preserves history and colour; only confirmed clearing deletes and resets them', async () => {
  const { p, calls, storage } = await harness({ storage: memoryStorage('red') });
  p.historyItems.value = [{ id: 'saved-record' }];
  p.requestHistoryClear(); p.cancelHistoryClear();
  assert.equal(await p.clearHistory(), false);
  assert.equal(calls.length, 0);
  assert.equal(p.historyItems.value.length, 1);
  assert.equal(storage.getItem(COLOR_PREFERENCE_KEY), 'red');
  p.requestHistoryClear();
  assert.equal(await p.clearHistory(), true);
  assert.equal(calls.filter(call => call.method === 'DELETE').length, 1);
  assert.deepEqual(p.historyItems.value, []);
  assert.equal(p.color.value, 'pink');
  assert.equal(storage.getItem(COLOR_PREFERENCE_KEY), null);
  assert.equal(p.confirmingClear.value, false);
});

test('[S16 B3] a failed deletion retains the explicit preference and a newer choice outranks pending clearing', async () => {
  const failed = await harness({ storage: memoryStorage('red'), respond: async () => { throw Error('Controlled outage'); } });
  failed.p.requestHistoryClear();
  assert.equal(await failed.p.clearHistory(), false);
  assert.equal(failed.storage.getItem(COLOR_PREFERENCE_KEY), 'red');
  assert.equal(failed.p.confirmingClear.value, true);
  let finish;
  const pending = await harness({ storage: memoryStorage('red'), respond: () => new Promise(resolve => { finish = resolve; }) });
  pending.p.requestHistoryClear(); const clearing = pending.p.clearHistory();
  pending.p.chooseColor('pearl'); finish({ deleted: true }); await clearing;
  assert.equal(pending.p.color.value, 'pearl');
  assert.equal(pending.storage.getItem(COLOR_PREFERENCE_KEY), 'pearl');
});

test('[S16 B3] clearing does not claim the browser preference was removed when storage rejects removal', async () => {
  const storage = memoryStorage('red');
  storage.removeItem = () => { throw Error('Controlled browser storage failure'); };
  const { p } = await harness({ storage });
  p.historyItems.value = [{ id: 'saved-record' }]; p.requestHistoryClear();
  assert.equal(await p.clearHistory(), false);
  assert.deepEqual(p.historyItems.value, []);
  assert.equal(storage.getItem(COLOR_PREFERENCE_KEY), 'red');
  assert.equal(p.color.value, 'red');
  assert.match(p.historyError.value, /history was cleared.*could not clear the remembered colour/);
});

test('[B1 S04 S09 S10 S11] local support stays reachable across entry, both skills, stopping and history outage', async () => {
  const { p, calls, paintReady } = await harness({ respond: async () => { throw Error('Controlled backend outage'); } });
  assertSupportAccess(p, 'home');
  p.directEntry(); assertSupportAccess(p, 'choice');
  p.choose('breathing'); await paintReady(); assertSupportAccess(p, 'ready');
  p.startExercise(); assertSupportAccess(p, 'breathing');
  assert.equal(p.paused.value, true);
  p.resume(); assert.equal(p.paused.value, false);
  p.stop(); assertSupportAccess(p, 'done');
  p.choose('grounding'); p.startExercise(); assertSupportAccess(p, 'grounding');
  p.stop(); p.go('home'); p.go('history');
  await new Promise(resolve => setImmediate(resolve));
  assert.match(p.historyError.value, /could not be loaded/);
  assertSupportAccess(p, 'history');
  assert.equal(calls.filter(call => call.method === 'PUT' || call.path.endsWith('/explanation')).length, 0);
  assert.equal(p.saveState.value, 'unsaved');
});

test('[B1 S12] optional wording loading and provider failure never gate local support or direct choice', async () => {
  let rejectProvider;
  const { p, paintReady } = await harness({ respond: (path) => path.endsWith('/explanation') ? new Promise((_, reject) => { rejectProvider = reject; }) : Promise.resolve({ saved: true }) });
  p.saveEnabled.value = true; p.directEntry(); p.choose('breathing'); await paintReady();
  assert.match(p.explanationLabel.value, /loading/);
  assertSupportAccess(p, 'ready');
  rejectProvider(new Error('Controlled provider rejection'));
  await new Promise(resolve => setImmediate(resolve));
  assert.match(p.explanationLabel.value, /fallback/);
  assertSupportAccess(p, 'ready');
  p.choose('grounding'); p.startExercise();
  assert.equal(p.screen.value, 'grounding');
  assert.equal(p.result.value.code, 'direct-choice');
});

test('[B2 S07 S10 S11 S13] late wording cannot change an active choice, resume Stop or manufacture completion', async () => {
  let reply;
  const { p, calls, paintReady } = await harness({ respond: path => path.endsWith('/explanation') ? new Promise(resolve => { reply = resolve; }) : Promise.resolve({ saved: true }) });
  p.saveEnabled.value = true; p.directEntry(); p.choose('breathing'); await paintReady();
  p.startExercise(); p.pause(); p.resume(); p.stop();
  reply({ status: 'validated', mode: 'openrouter', text: 'Controlled late wording', stale: false });
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(p.screen.value, 'done');
  assert.equal(p.sessionStatus.value, 'stopped');
  assert.equal(p.exercise.value, 'breathing');
  assert.equal(p.explanationText.value, '');
  p.resume();
  assert.equal(p.sessionStatus.value, 'stopped');
  const stopped = calls.filter(call => call.method === 'PUT').at(-1).body;
  assert.equal(stopped.status, 'stopped');
  assert.ok(stopped.events.some(event => event.kind === 'stop'));
  assert.ok(!stopped.events.some(event => event.kind === 'complete'));
  p.choose('grounding');
  assert.equal(p.screen.value, 'ready');
  assert.equal(p.exercise.value, 'grounding');
  assert.deepEqual(p.answers.value, Array(5).fill(null));
});

test('[S05 S18 B2] Back cancels a pending first-answer transition and permits an immediate intentional correction', async () => {
  const { p } = await harness();
  p.beginCheckin(); p.go('checkin'); p.answer(2);
  assert.equal(p.selecting.value, true);
  p.backQuestion();
  assert.equal(p.screen.value, 'intro');
  assert.equal(p.selecting.value, false);
  assert.equal(p.answers.value[0], 2);
  await new Promise(resolve => setTimeout(resolve, 400));
  assert.equal(p.screen.value, 'intro');
  p.go('checkin'); p.answer(0); p.answer(1);
  assert.equal(p.answers.value[0], 0);
  assert.equal(p.selecting.value, true);
  p.go('home');
});

test('[S05 S18 B2] pending Back preserves answers and a corrected answer advances once instead of replaying both callbacks', async () => {
  const { p } = await harness();
  p.beginCheckin(); p.go('checkin'); p.answer(0);
  await new Promise(resolve => setTimeout(resolve, 900));
  assert.equal(p.questionIndex.value, 1);
  p.answer(2); p.backQuestion();
  assert.equal(p.screen.value, 'checkin');
  assert.equal(p.questionIndex.value, 0);
  assert.deepEqual(p.answers.value.slice(0, 2), [0, 2]);
  p.answer(1); p.answer(2);
  assert.equal(p.answers.value[0], 1);
  await new Promise(resolve => setTimeout(resolve, 400));
  assert.equal(p.questionIndex.value, 1);
  assert.deepEqual(p.answers.value.slice(0, 2), [1, 2]);
  p.go('home');
});

test('[S14 B3] successful save retry removes the stale saving-unavailable label without requesting wording', async () => {
  let unavailable = true;
  const { p, calls, paintReady } = await harness({ respond: async () => {
    if (unavailable) throw Error('Controlled database failure');
    return { saved: true };
  } });
  p.saveEnabled.value = true; p.directEntry(); p.choose('grounding'); await paintReady();
  assert.equal(p.saveState.value, 'error');
  assert.equal(p.explanationLabel.value, 'Local rule · saving unavailable');
  unavailable = false;
  await p.retrySave();
  assert.equal(p.saveState.value, 'saved');
  assert.equal(p.explanationLabel.value, 'Local rule · optional wording not requested');
  assert.equal(p.screen.value, 'ready');
  assert.equal(calls.filter(call => call.path.endsWith('/explanation')).length, 0);
});
