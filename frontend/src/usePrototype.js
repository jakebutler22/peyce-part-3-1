import { ref, nextTick, onMounted, onUnmounted, watch } from 'vue';
import { matchExercise } from './matching.js';
import { PhaseClock, phaseAt } from './clock.js';
import { SequenceTimer } from './sequence.js';
import { api, SaveQueue } from './api.js';

export function usePrototype() {
  const screen = ref('home'), questionIndex = ref(0), answers = ref(Array(5).fill(null));
  const result = ref(null), exercise = ref('breathing'), origin = ref('direct'), selecting = ref(false);
  const senseIndex = ref(0), color = ref('pink'), reducedMotion = ref(false), paused = ref(false), pauseReason = ref('');
  const timing = ref(phaseAt(0)), sessionStatus = ref('checkin'), supportDialog = ref(null);
  const saveEnabled = ref(false), saveState = ref('unsaved'), saveMessage = ref('Not saved · choose saving before starting.');
  const historyItems = ref([]), historyLoading = ref(false), historyError = ref(''), selectedSession = ref(null);
  const explanationText = ref(''), explanationLabel = ref('Local rule · your choice stays available');
  const verificationMode = import.meta.env.DEV && new URLSearchParams(location.search).has('verify');
  const providerFault = ref(''), saveFault = ref(false);
  let current = null, frame, lockUntil = 0, senseLockUntil = 0, selectTimeout, supportReturnFocus, pendingAdvance = false;
  let generation = 0, explanationAbort, groundElapsed = 0, groundAnchor = null;
  const clock = new PhaseClock();
  const id = () => crypto.randomUUID();
  const offset = () => current ? performance.now() - current.anchor : 0;
  const activeMs = () => exercise.value === 'breathing' ? clock.sample(performance.now()).elapsed : groundElapsed + (groundAnchor === null ? 0 : Math.max(0, performance.now() - groundAnchor));
  const acknowledged = new Set();
  const queue = new SaveQueue(async ({ sessionId, snapshot, bootstrap, fault }) => {
    if (!acknowledged.has(sessionId) && snapshot.revision > 1) await api(`/sessions/${sessionId}/snapshot`, { method: 'PUT', body: bootstrap, fault });
    const response = await api(`/sessions/${sessionId}/snapshot`, { method: 'PUT', body: snapshot, fault });
    acknowledged.add(sessionId); return response;
  });
  function invalidate() { generation++; explanationAbort?.abort(); explanationText.value = ''; explanationLabel.value = 'Local rule · your choice stays available'; }
  function event(kind, cause = 'user') {
    if (!current || current.final) return;
    current.events.push({ id: id(), kind, at_ms: offset(), active_ms: current.started ? activeMs() : 0, cause });
  }
  function focusHeading() { nextTick(() => { window.scrollTo({ top: 0, left: 0, behavior: 'instant' }); document.querySelector('main h1')?.focus({ preventScroll: true }); }); }
  function show(next) { screen.value = next; focusHeading(); }
  function setStatus(value) { sessionStatus.value = value; if (current) current.status = value; }
  function newSession(direct = false) {
    invalidate(); cancelAnimationFrame(frame); clearTimeout(selectTimeout);
    current = { id: id(), anchor: performance.now(), revision: 0, events: [], timer: new SequenceTimer(), answered: Array(5).fill(false), direct: null, exercise: null, status: direct ? 'choice' : 'checkin', save: saveEnabled.value, final: false, started: false, colorExplicit: false };
    answers.value = Array(5).fill(null); result.value = null; questionIndex.value = 0; senseIndex.value = 0; selecting.value = false;
    paused.value = false; timing.value = phaseAt(0); clock.elapsed = 0; clock.anchor = null; groundElapsed = 0; groundAnchor = null;
    sessionStatus.value = current.status; origin.value = direct ? 'direct' : 'checkin';
    saveState.value = 'unsaved'; saveMessage.value = current.save ? 'Saving when this session changes…' : 'Not saved · this session stays in memory.';
    persist();
  }
  function snapshot() {
    current.revision++;
    return { operation_id: id(), revision: current.revision, answers: [...answers.value], answered: [...current.answered], direct_choice: current.direct, exercise: current.exercise, status: current.status, color: color.value, color_explicit: current.colorExplicit, events: structuredClone(current.events), timing: current.timer.result };
  }
  async function write(captured, target) {
    if (current === target) { saveState.value = 'saving'; saveMessage.value = 'Saving on this computer…'; }
    try {
      const response = await queue.enqueue(captured);
      if (current === target && captured.snapshot.revision === target.revision) {
        saveState.value = 'saved'; saveMessage.value = 'Saved on this computer.';
        if (['active', 'paused'].includes(target.status)) sessionStorage.setItem('peyce-active-id', target.id);
        else sessionStorage.removeItem('peyce-active-id');
      }
      return response;
    } catch {
      if (current === target && captured.snapshot.revision === target.revision) { saveState.value = 'error'; saveMessage.value = 'Not confirmed saved. You can continue, or retry saving.'; }
      return null;
    }
  }
  function persist() {
    if (!current?.save) return Promise.resolve(null);
    const captured = { sessionId: current.id, snapshot: snapshot(), fault: verificationMode && saveFault.value ? 'database' : '' };
    if (!current.initial) current.initial = structuredClone(captured.snapshot);
    captured.bootstrap = current.initial; current.last = captured;
    return write(captured, current);
  }
  async function retrySave() {
    if (!current?.last) return;
    const target = current;
    await write({ ...target.last, fault: verificationMode && saveFault.value ? 'database' : '' }, target);
  }
  async function explain(target, revision, context) {
    if (target !== current || context !== generation || screen.value !== 'ready' || revision !== target.revision) return;
    explanationLabel.value = 'Optional wording loading · Start is ready';
    const controller = new AbortController(); explanationAbort = controller;
    const timeout = setTimeout(() => controller.abort(), 20000);
    try {
      const response = await api(`/sessions/${target.id}/explanation`, { method: 'POST', body: { revision, request_id: id() }, signal: controller.signal, fault: verificationMode ? providerFault.value : '' });
      if (target !== current || context !== generation || screen.value !== 'ready' || revision !== target.revision || response.stale || response.status === 'obsolete') return;
      explanationText.value = response.text || '';
      explanationLabel.value = response.status === 'validated' ? (response.mode === 'mock' ? 'Mock wording · approved local rule' : 'Model-assisted wording · approved local rule') : 'Local fallback · your choice stays available';
    } catch {
      if (target === current && context === generation && screen.value === 'ready') explanationLabel.value = 'Local fallback · your choice stays available';
    } finally { clearTimeout(timeout); }
  }
  function ready() {
    invalidate(); setStatus('ready'); current.exercise = exercise.value; show('ready');
    const target = current, context = generation;
    nextTick(() => requestAnimationFrame(async () => {
      if (target !== current || context !== generation || screen.value !== 'ready') return;
      if (target.timer.instruction === null) { target.timer.showInstructions(offset()); event('instruction_visible'); }
      const pending = persist(), revision = target.revision;
      if (!target.save) { explanationLabel.value = 'Local rule · session not saved'; return; }
      if (await pending) explain(target, revision, context);
      else if (target === current && context === generation) explanationLabel.value = 'Local rule · saving unavailable';
    }));
  }
  function finishRecord() {
    if (!current || current.final) return;
    invalidate(); cancelAnimationFrame(frame);
    if (['active','paused'].includes(current.status)) { freeze(); current.timer.include('user', offset()); event('stop'); setStatus('stopped'); }
    if (current.timer.instruction !== null) { event('finish'); current.timer.finish(offset()); }
    if (current.status === 'completed') setStatus('finished');
    else if (['checkin','choice','ready'].includes(current.status)) { event('leave', 'navigation'); setStatus('stopped'); }
    current.finalSave = persist(); current.final = true; sessionStorage.removeItem('peyce-active-id');
  }
  function go(next) {
    if (screen.value === 'checkin' && next !== 'checkin') { clearTimeout(selectTimeout); selecting.value = false; pendingAdvance = false; }
    if (['home','history'].includes(next)) finishRecord();
    if (next === 'checkin' && current) { invalidate(); setStatus('checkin'); persist(); }
    show(next); if (next === 'history') { historyLoading.value = true; Promise.resolve(current?.finalSave).then(refreshHistory); }
  }
  function beginCheckin() { finishRecord(); newSession(); show('intro'); }
  function directEntry() { finishRecord(); newSession(true); show('choice'); }
  function advance() {
    if (screen.value !== 'checkin') return;
    selecting.value = false; pendingAdvance = false;
    if (questionIndex.value < 4) { questionIndex.value++; focusHeading(); } else finishCheckin();
  }
  function answer(value) {
    if (!current || selecting.value || performance.now() < lockUntil) return;
    invalidate(); selecting.value = true; lockUntil = performance.now() + 850;
    answers.value[questionIndex.value] = value; current.answered[questionIndex.value] = true; current.direct = null; current.exercise = null; result.value = null;
    persist(); pendingAdvance = true; selectTimeout = setTimeout(advance, 360);
  }
  function finishCheckin() { result.value = matchExercise(answers.value); if (result.value.exercise) { exercise.value = result.value.exercise; ready(); } else { setStatus('choice'); persist(); show('choice'); } }
  function skipAll() {
    clearTimeout(selectTimeout); selecting.value = false; pendingAdvance = false; invalidate();
    answers.value = Array(5).fill(null); current.answered = Array(5).fill(false); current.direct = null; current.exercise = null; result.value = null; origin.value = 'direct'; setStatus('choice'); persist(); show('choice');
  }
  function backQuestion() { if (selecting.value) return; invalidate(); result.value = null; if (questionIndex.value > 0) { questionIndex.value--; focusHeading(); } else show('intro'); }
  function choose(skill) {
    if (!current || current.final || screen.value === 'done') { finishRecord(); newSession(true); }
    invalidate(); exercise.value = skill; current.direct = skill; result.value = matchExercise(answers.value, skill); ready();
  }
  function readyBack() { invalidate(); if (origin.value === 'checkin') { questionIndex.value = 4; setStatus('checkin'); current.direct = null; current.exercise = null; persist(); show('checkin'); } else { setStatus('choice'); current.exercise = null; persist(); show('choice'); } }
  function tick(now) {
    if (screen.value !== 'breathing') return;
    timing.value = clock.sample(now);
    if (timing.value.done) { event('complete', 'clock'); setStatus('completed'); persist(); show('done'); return; }
    frame = requestAnimationFrame(tick);
  }
  function startExercise() {
    if (!current || current.final) return;
    // A deliberate Start cannot outrun the first painted instruction boundary.
    if (current.timer.instruction === null) { current.timer.showInstructions(offset()); event('instruction_visible'); }
    invalidate(); current.started = true; paused.value = false; pauseReason.value = ''; setStatus('active');
    if (exercise.value === 'breathing') { clock.start(performance.now()); timing.value = phaseAt(0); show('breathing'); frame = requestAnimationFrame(tick); }
    else { groundElapsed = 0; groundAnchor = performance.now(); senseIndex.value = 0; show('grounding'); }
    event('start'); persist();
  }
  function freeze() { if (exercise.value === 'breathing') { clock.pause(performance.now()); timing.value = clock.sample(performance.now()); } else if (groundAnchor !== null) { groundElapsed += performance.now() - groundAnchor; groundAnchor = null; } }
  function pause(reason = '', cause = 'user') {
    if (!['breathing','grounding'].includes(screen.value) || paused.value) return;
    freeze(); paused.value = true; pauseReason.value = typeof reason === 'string' ? reason : '';
    if (cause === 'user') current.timer.exclude('user', offset());
    event(cause === 'background' ? 'background_pause' : 'pause', cause); setStatus('paused'); persist();
  }
  function resume() {
    if (!current || !paused.value || supportDialog.value?.open) return;
    current.timer.include('user', offset());
    if (exercise.value === 'breathing') clock.resume(performance.now()); else groundAnchor = performance.now();
    paused.value = false; pauseReason.value = ''; event('resume'); setStatus('active'); persist();
  }
  function stop() { if (!current) return; invalidate(); cancelAnimationFrame(frame); freeze(); current.timer.include('user', offset()); paused.value = false; event('stop'); setStatus('stopped'); persist(); show('done'); }
  function backSense() { if (paused.value || senseIndex.value === 0) return; senseIndex.value--; focusHeading(); }
  function nextSense(skip = false) {
    if (paused.value || performance.now() < senseLockUntil) return;
    senseLockUntil = performance.now() + 500; event(skip ? 'sense_skip' : 'sense_next');
    if (senseIndex.value < 4) { senseIndex.value++; persist(); focusHeading(); }
    else { freeze(); event('complete'); setStatus('completed'); persist(); show('done'); }
  }
  function openSupport() {
    supportReturnFocus = document.activeElement;
    if (selecting.value) { clearTimeout(selectTimeout); selecting.value = false; }
    if (current && !current.final) { current.timer.exclude('support', offset()); event('support_open', 'support'); }
    pause('Paused while support is open. Resume when you are ready.', 'support');
    if (current && !current.final) persist(); supportDialog.value?.showModal();
  }
  function closeSupport() {
    supportDialog.value?.close(); supportReturnFocus?.focus();
    if (current && !current.final) { current.timer.include('support', offset()); event('support_close', 'support'); persist(); }
    if (pendingAdvance && screen.value === 'checkin') { selecting.value = true; selectTimeout = setTimeout(advance, 360); }
  }
  function onVisibility() { if (document.hidden) pause('Paused when this tab moved into the background. Resume when you are ready.', 'background'); }
  function onPageHide() {
    if (current?.save && ['active','paused'].includes(current.status)) {
      fetch(`/api/sessions/${current.id}/interrupt`, { method: 'POST', keepalive: true, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ revision: current.revision, operation_id: id() }) }).catch(() => {});
    }
  }
  function dialogKey(event) {
    if (event.key === 'Escape') { event.preventDefault(); closeSupport(); }
    if (event.key === 'Tab') {
      const controls = [...supportDialog.value.querySelectorAll('button, a[href]')], first = controls[0], last = controls.at(-1);
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
  }
  async function refreshHistory() {
    historyLoading.value = true; historyError.value = '';
    try { historyItems.value = (await api('/sessions', { fault: verificationMode && saveFault.value ? 'database' : '' })).sessions; }
    catch { historyItems.value = []; historyError.value = 'Past sessions could not be loaded. Support and new exercises are still available.'; }
    finally { historyLoading.value = false; }
  }
  async function openSession(sessionId) {
    historyError.value = ''; selectedSession.value = null;
    try { selectedSession.value = await api(`/sessions/${sessionId}`, { fault: verificationMode && saveFault.value ? 'database' : '' }); show('session-detail'); }
    catch { historyError.value = 'This saved session could not be opened. Try again later.'; }
  }
  async function clearHistory() {
    historyError.value = '';
    try { await api('/sessions', { method: 'DELETE' }); historyItems.value = []; selectedSession.value = null; }
    catch { historyError.value = 'Past sessions could not be cleared. Please try again.'; }
  }
  watch(color, () => { if (current && !current.final) { current.colorExplicit = true; invalidate(); persist(); } });
  onMounted(async () => {
    reducedMotion.value = matchMedia('(prefers-reduced-motion: reduce)').matches;
    document.addEventListener('visibilitychange', onVisibility); window.addEventListener('pagehide', onPageHide);
    const interruptedId = sessionStorage.getItem('peyce-active-id');
    if (interruptedId) {
      sessionStorage.removeItem('peyce-active-id');
      try { const previous = await api(`/sessions/${interruptedId}`); if (['active','paused'].includes(previous.status)) await api(`/sessions/${interruptedId}/interrupt`, { method: 'POST', body: { revision: previous.revision, operation_id: id() } }); } catch { /* Unload/recovery is best effort; restart reconciliation also interrupts. */ }
    }
  });
  onUnmounted(() => { invalidate(); clearTimeout(selectTimeout); cancelAnimationFrame(frame); document.removeEventListener('visibilitychange', onVisibility); window.removeEventListener('pagehide', onPageHide); });
  return { screen, questionIndex, answers, result, exercise, origin, selecting, senseIndex, color, reducedMotion, timing, paused, pauseReason, sessionStatus, supportDialog, saveEnabled, saveState, saveMessage, historyItems, historyLoading, historyError, selectedSession, explanationText, explanationLabel, verificationMode, providerFault, saveFault, go, beginCheckin, directEntry, answer, skipAll, backQuestion, choose, readyBack, startExercise, pause, resume, stop, backSense, nextSense, openSupport, closeSupport, dialogKey, refreshHistory, openSession, clearHistory, retrySave };
}
