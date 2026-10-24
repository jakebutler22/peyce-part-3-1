import test from 'node:test';
import assert from 'node:assert/strict';
import { createSSRApp, nextTick } from 'vue';
import { renderToString } from 'vue/server-renderer';
import { usePrototype } from '../src/usePrototype.js';

// Exercise the real controller with controlled local requests. SSR registers its
// lifecycle hooks without installing browser listeners or contacting a service.
globalThis.window = { scrollTo() {} };
globalThis.document = { querySelector() { return null; } };

async function controller() {
  const pending = [];
  const request = (path, options = {}) => new Promise((resolve, reject) => pending.push({ path, options, resolve, reject }));
  let p;
  await renderToString(createSSRApp({ setup() { p = usePrototype({ request }); return () => null; } }));
  return { p, pending };
}

test('a delayed saved-session response cannot undo a deliberate Home action', async () => {
  const { p, pending } = await controller();
  const opening = p.openSession('earlier-session');
  p.go('home');
  pending[0].resolve({ id: 'earlier-session', status: 'finished' });
  await opening;
  assert.equal(p.screen.value, 'home');
  assert.equal(p.selectedSession.value, null);
  assert.equal(p.historyLoading.value, false);
});

test('an older saved-session response cannot replace the latest requested session', async () => {
  const { p, pending } = await controller();
  const first = p.openSession('first-session');
  const latest = p.openSession('latest-session');
  pending[1].resolve({ id: 'latest-session', status: 'stopped' });
  await latest;
  pending[0].resolve({ id: 'first-session', status: 'finished' });
  await first;
  assert.equal(p.screen.value, 'session-detail');
  assert.equal(p.selectedSession.value.id, 'latest-session');
  assert.equal(p.historyError.value, '');
});

test('a stale detail failure cannot replace the successful current detail with an error', async () => {
  const { p, pending } = await controller();
  const first = p.openSession('first-session');
  const latest = p.openSession('latest-session');
  pending[1].resolve({ id: 'latest-session', status: 'finished' });
  await latest;
  pending[0].reject(new Error('Controlled stale failure'));
  await first;
  assert.equal(p.selectedSession.value.id, 'latest-session');
  assert.equal(p.historyError.value, '');
});

test('a history response started before clearing cannot resurrect deleted rows', async () => {
  const { p, pending } = await controller();
  const reading = p.refreshHistory();
  const clearing = p.clearHistory();
  pending[1].resolve({ cleared: true });
  await clearing;
  pending[0].resolve({ sessions: [{ id: 'deleted-session' }] });
  await reading;
  assert.deepEqual(p.historyItems.value, []);
  assert.equal(p.historyLoading.value, false);
});

test('a delayed history read cannot overwrite a newer successful refresh', async () => {
  const { p, pending } = await controller();
  const first = p.refreshHistory();
  const latest = p.refreshHistory();
  pending[1].resolve({ sessions: [{ id: 'current-session' }] });
  await latest;
  pending[0].reject(new Error('Controlled stale failure'));
  await first;
  assert.equal(p.historyItems.value[0].id, 'current-session');
  assert.equal(p.historyError.value, '');
  assert.equal(p.historyLoading.value, false);
});

test('saved timing boundaries exactly match lifecycle even when clock sampling is delayed', async () => {
  const original = { performance: globalThis.performance, requestAnimationFrame: globalThis.requestAnimationFrame, cancelAnimationFrame: globalThis.cancelAnimationFrame, sessionStorage: globalThis.sessionStorage };
  const frames = [], snapshots = [];
  let now = 0;
  globalThis.performance = { now() { now += 7; return now; } };
  globalThis.requestAnimationFrame = callback => frames.push(callback);
  globalThis.cancelAnimationFrame = () => {};
  globalThis.sessionStorage = { setItem() {}, removeItem() {} };
  try {
    let p;
    const request = async (path, options) => { if (options?.method === 'PUT') snapshots.push(structuredClone(options.body)); return {}; };
    await renderToString(createSSRApp({ setup() { p = usePrototype({ request }); return () => null; } }));
    p.saveEnabled.value = true;
    p.directEntry();
    p.choose('grounding');
    await nextTick();
    frames.shift()();
    p.startExercise();
    p.pause();
    p.supportDialog.value = { open: false, showModal() { this.open = true; }, close() { this.open = false; } };
    p.openSupport();
    p.closeSupport();
    p.resume();
    p.stop();
    p.go('home');
    await new Promise(resolve => setImmediate(resolve));
    const saved = snapshots.at(-1);
    const at = kind => saved.events.find(event => event.kind === kind).at_ms;
    assert.equal(saved.status, 'stopped');
    assert.equal(saved.timing.instruction_ms, at('instruction_visible'));
    assert.equal(saved.timing.finish_ms, at('finish'));
    const user = saved.timing.excluded_intervals.find(interval => interval.cause === 'user');
    const support = saved.timing.excluded_intervals.find(interval => interval.cause === 'support');
    assert.deepEqual([user.start_ms, user.end_ms], [at('pause'), at('resume')]);
    assert.deepEqual([support.start_ms, support.end_ms], [at('support_open'), at('support_close')]);
  } finally {
    for (const [name, value] of Object.entries(original)) {
      if (value === undefined) delete globalThis[name]; else globalThis[name] = value;
    }
  }
});
