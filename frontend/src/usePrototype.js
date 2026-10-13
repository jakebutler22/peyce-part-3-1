import { ref, nextTick, onMounted, onUnmounted } from 'vue';
import { matchExercise } from './matching.js';
import { PhaseClock, phaseAt } from './clock.js';

export function usePrototype() {
  const screen = ref('home'), questionIndex = ref(0), answers = ref(Array(5).fill(null));
  const result = ref(null), exercise = ref('breathing'), origin = ref('direct'), selecting = ref(false);
  const senseIndex = ref(0), color = ref('pink'), reducedMotion = ref(false), paused = ref(false), pauseReason = ref('');
  const timing = ref(phaseAt(0)), sessionStatus = ref('completed'), supportDialog = ref(null);
  let frame, lockUntil = 0, senseLockUntil = 0, selectTimeout, supportReturnFocus, supportInterruptedSelection = false;
  const clock = new PhaseClock();
  function focusHeading() { nextTick(() => { window.scrollTo({ top: 0, left: 0, behavior: 'instant' }); document.querySelector('main h1')?.focus({ preventScroll: true }); }); }
  function go(next) { if (screen.value === 'checkin' && next !== 'checkin') { clearTimeout(selectTimeout); selecting.value = false; } screen.value = next; focusHeading(); }
  function beginCheckin() { answers.value = Array(5).fill(null); result.value = null; origin.value = 'checkin'; questionIndex.value = 0; go('intro'); }
  function answer(value) {
    if (selecting.value || performance.now() < lockUntil) return;
    selecting.value = true; lockUntil = performance.now() + 850;
    answers.value[questionIndex.value] = value; result.value = null;
    selectTimeout = setTimeout(() => { if (screen.value !== 'checkin') return; selecting.value = false; if (questionIndex.value < 4) { questionIndex.value++; focusHeading(); } else finishCheckin(); }, 360);
  }
  function finishCheckin() { result.value = matchExercise(answers.value); if (result.value.exercise) { exercise.value = result.value.exercise; go('ready'); } else go('choice'); }
  function skipAll() { clearTimeout(selectTimeout); selecting.value = false; answers.value = Array(5).fill(null); result.value = null; origin.value = 'direct'; go('choice'); }
  function backQuestion() { if (selecting.value) return; result.value = null; if (questionIndex.value > 0) { questionIndex.value--; focusHeading(); } else go('intro'); }
  function choose(skill) { exercise.value = skill; result.value = matchExercise(answers.value, skill); go('ready'); }
  function readyBack() { if (origin.value === 'checkin') { questionIndex.value = 4; go('checkin'); } else go('choice'); }
  function tick(now) {
    if (screen.value !== 'breathing') return;
    timing.value = clock.sample(now);
    if (timing.value.done) { sessionStatus.value = 'completed'; go('done'); return; }
    frame = requestAnimationFrame(tick);
  }
  function startExercise() {
    sessionStatus.value = 'completed';
    if (exercise.value === 'breathing') { paused.value = false; pauseReason.value = ''; clock.start(performance.now()); timing.value = phaseAt(0); go('breathing'); frame = requestAnimationFrame(tick); }
    else { senseIndex.value = 0; go('grounding'); }
  }
  function pause(reason = '') { if (screen.value !== 'breathing' || paused.value) return; clock.pause(performance.now()); timing.value = clock.sample(performance.now()); paused.value = true; pauseReason.value = reason; }
  function resume() { clock.resume(performance.now()); paused.value = false; pauseReason.value = ''; }
  function stop() { cancelAnimationFrame(frame); clock.pause(performance.now()); sessionStatus.value = 'stopped'; go('done'); }
  function nextSense() { if (performance.now() < senseLockUntil) return; senseLockUntil = performance.now() + 500; if (senseIndex.value < 4) { senseIndex.value++; focusHeading(); } else { sessionStatus.value = 'completed'; go('done'); } }
  function openSupport() { supportReturnFocus = document.activeElement; supportInterruptedSelection = selecting.value; if (supportInterruptedSelection) { clearTimeout(selectTimeout); selecting.value = false; } pause('Paused while support is open.'); supportDialog.value.showModal(); }
  function closeSupport() { supportDialog.value.close(); supportReturnFocus?.focus(); if (supportInterruptedSelection && screen.value === 'checkin') { supportInterruptedSelection = false; lockUntil = 0; answer(answers.value[questionIndex.value]); } }
  function onVisibility() { if (document.hidden) pause('Paused when this tab moved into the background. Resume when you are ready.'); }
  function dialogKey(event) {
    if (event.key === 'Escape') { event.preventDefault(); closeSupport(); }
    if (event.key === 'Tab') {
      const controls = [...supportDialog.value.querySelectorAll('button, a[href]')];
      const first = controls[0], last = controls.at(-1);
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
  }
  onMounted(() => { reducedMotion.value = matchMedia('(prefers-reduced-motion: reduce)').matches; document.addEventListener('visibilitychange', onVisibility); });
  onUnmounted(() => { clearTimeout(selectTimeout); cancelAnimationFrame(frame); document.removeEventListener('visibilitychange', onVisibility); });
  return { screen, questionIndex, answers, result, exercise, origin, selecting, senseIndex, color, reducedMotion, timing, paused, pauseReason, sessionStatus, supportDialog, go, beginCheckin, answer, skipAll, backQuestion, choose, readyBack, startExercise, pause, resume, stop, nextSense, openSupport, closeSupport, dialogKey };
}
