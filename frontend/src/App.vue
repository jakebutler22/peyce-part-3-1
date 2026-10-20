<script setup>
import { computed, ref } from 'vue';
import { objectsFor } from './assets.js';
import { questions, senses } from './data.js';
import { usePrototype } from './usePrototype.js';
import FaceOption from './components/FaceOption.vue';
import DecorativeObject from './components/DecorativeObject.vue';
import BalloonPacer from './components/BalloonPacer.vue';
const p = usePrototype();
const {
  screen, questionIndex, answers, result, exercise, origin, selecting, senseIndex,
  color, reducedMotion, timing, paused, pauseReason, sessionStatus, supportDialog,
  saveEnabled, saveState, saveMessage, historyItems, historyLoading, historyError,
  selectedSession, explanationText, explanationLabel, verificationMode, providerFault, saveFault,
} = p;
const question = computed(() => questions[questionIndex.value]);
const sense = computed(() => senses[senseIndex.value]);
const title = computed(() => exercise.value === 'breathing' ? 'A gentle breathing rhythm.' : 'A little more here.');
const confirmingClear = ref(false);
const detail = computed(() => {
  const record = selectedSession.value;
  return record ? { ...record.session, ...record.snapshot, ...record } : null;
});
const footerMessage = computed(() => {
  if (!['history', 'session-detail'].includes(screen.value) || saveState.value === 'error') return saveMessage.value;
  if (historyLoading.value) return 'Loading saved history…';
  return historyError.value ? 'Local support and new exercises remain available.' : 'Only confirmed saves are shown in history.';
});
const currentTurns = computed(() => {
  const turns = (detail.value?.turns || []).filter(turn => !turn.superseded && (turn.source === 'structured-turn' || turn.question_id));
  const unique = new Map();
  for (const turn of turns) unique.set(`${turn.role}:${turn.question_id || turn.id}`, turn);
  return [...unique.values()];
});
const earlierTurnGroups = computed(() => {
  const revisions = new Map();
  for (const turn of detail.value?.turns || []) {
    if (!turn.superseded) continue;
    if (!revisions.has(turn.revision)) revisions.set(turn.revision, []);
    revisions.get(turn.revision).push(turn);
  }
  return [...revisions].map(([revision, turns]) => ({ revision, turns }));
});
function displayDate(value) {
  if (!value) return 'Date unavailable';
  const date = new Date(value);
  return Number.isNaN(date.valueOf()) ? value : date.toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
}
function displaySkill(value) { return value === 'breathing' ? 'Breathing' : value === 'grounding' ? 'Grounding' : 'Check-in'; }
function displayStatus(value) {
  return ({ checkin: 'Check-in', choice: 'Choosing', ready: 'Ready', active: 'In progress', paused: 'Paused', completed: 'Completed', stopped: 'Stopped', interrupted: 'Interrupted', finished: 'Finished' })[value] || 'Status unavailable';
}
function seconds(value) { return value !== null && value !== undefined && Number.isFinite(Number(value)) ? `${(Number(value) / 1000).toFixed(1)} s` : 'Not recorded'; }
function explanationSource(item) {
  if ((item.outcome || item.status || '').startsWith('fallback')) return 'Local fallback';
  if (item.mode === 'mock') return 'Mock model';
  return ['openai', 'openrouter', 'live'].includes(item.mode) ? 'Model-assisted' : 'Local fallback';
}
function turnText(turn) { return turn.text || turn.content || turn.question_text || turn.answer_label || (turn.kind === 'skip' ? 'Skipped this question' : 'Recorded turn'); }
function eventLabel(kind) {
  return ({ instruction_visible: 'Instructions shown', start: 'Started', pause: 'Paused', resume: 'Resumed', support_open: 'Support opened', support_close: 'Support closed', background_pause: 'Paused in background', sense_next: 'Next sense', sense_skip: 'Sense skipped', complete: 'Exercise completed', stop: 'Stopped', finish: 'Finished', leave: 'Left exercise' })[kind] || kind;
}
async function clearSavedHistory() {
  await p.clearHistory();
  if (!historyError.value) confirmingClear.value = false;
}
</script>

<template>
  <div class="app-shell" :class="['screen-' + screen, { practicing: ['breathing', 'grounding'].includes(screen) }]">
    <a class="skip-link" href="#main">Skip to current task</a>
    <header class="site-header">
      <button class="wordmark" aria-label="Peyce home" @click="['breathing','grounding'].includes(screen) ? p.stop() : p.go('home')"><span>P</span><span>e</span><span>y</span><span>c</span><span>e</span><i aria-hidden="true">•</i></button>
      <div class="header-actions"><button v-if="screen === 'home'" class="text-button history-link" @click="p.go('history')">Past sessions</button><button class="support-button" @click="p.openSupport"><span aria-hidden="true">↗</span> Crisis support</button></div>
    </header>

    <main id="main">
      <section v-if="screen === 'home'" class="home-layout">
        <div class="opening-art"><DecorativeObject v-for="object in objectsFor('opening')" :key="object.id" :object-id="object.id"/><div class="art-rule"></div><span class="art-caption">One small moment.<br>Your own pace.</span></div>
        <div class="opening-copy">
          <span class="eyebrow">PEYCE · PRONOUNCED “PEACE”</span><h1 tabindex="-1">A moment<br>at your <em>pace.</em></h1>
          <p class="lead">A gentle rhythm. A little grounding.<br>Room to choose what fits right now.</p>
          <div class="save-choice"><label><input type="checkbox" v-model="saveEnabled"> <span>Save this fictional session on this device</span></label><p>Fictional coursework only. Saved answers and activity stay on this computer until you clear past sessions.</p></div>
          <div class="opening-actions"><button class="primary" @click="p.beginCheckin">Find an exercise <span aria-hidden="true">→</span></button><button class="secondary" @click="p.directEntry">Choose an exercise</button></div>
          <p class="fine-print">Five optional questions, or go straight to a practice.<br>No typing. No account. You can leave at any time.</p>
        </div>
      </section>

      <section v-else-if="screen === 'intro'" class="center-stage narrow">
        <button class="back-button" @click="p.go('home')">← Back</button><span class="eyebrow">A SHORT, OPTIONAL CHECK-IN</span><h1 tabindex="-1">What fits<br>this moment?</h1><p class="lead">Five questions about what feels comfortable right now.</p><div class="notice"><p><strong>Choosing a face moves to the next question.</strong> Your choice appears briefly first. Use Back to change it, or skip any question.</p><p>These original questions are not an anxiety test. Suggestions use simple design rules, not a clinical assessment.</p></div><button class="primary" @click="p.go('checkin')">Begin check-in <span aria-hidden="true">→</span></button><button class="text-button" @click="p.skipAll">Skip all · choose an exercise</button>
      </section>

      <section v-else-if="screen === 'checkin'" class="checkin-stage">
        <div class="section-top"><button class="back-button" :disabled="selecting" @click="p.backQuestion">← Back</button><span class="eyebrow">{{ questionIndex + 1 }} OF 5</span><DecorativeObject v-for="object in objectsFor('checkin')" :key="object.id" :object-id="object.id" class="quiet-bow"/></div>
        <div class="question-progress" aria-hidden="true"><span v-for="n in 5" :key="n" :class="{ current: n === questionIndex + 1, passed: n < questionIndex + 1 }"></span></div>
        <h1 tabindex="-1" :key="question.id">{{ question.text }}</h1><p class="question-note">Choose what fits. There is no right answer.</p>
        <div class="face-options"><FaceOption v-for="(label, value) in question.labels" :key="value" :value="value" :label="label" :selected="answers[questionIndex] === value" :disabled="selecting" @choose="p.answer"/></div>
        <div class="skip-actions"><button class="text-button" :disabled="selecting" @click="p.answer(null)">Skip this question</button><span aria-hidden="true">/</span><button class="text-button" :disabled="selecting" @click="p.skipAll">Skip all</button></div><p class="sr-only" aria-live="polite">{{ selecting ? 'Selection recorded. Moving to the next screen.' : '' }}</p>
      </section>

      <section v-else-if="screen === 'choice'" class="center-stage choices-stage">
        <button class="back-button" @click="origin === 'checkin' ? p.readyBack() : p.go('home')">← Back</button><span class="eyebrow">YOUR CHOICE</span><h1 tabindex="-1">Room to choose.</h1><p class="lead choice-reason">{{ result?.reason || 'No check-in needed. Try what appeals to you, or finish here.' }}</p>
        <button v-if="result?.code === 'both-declined'" class="primary finish-neither" @click="p.go('home')">Finish</button>
        <div class="exercise-choices"><button class="exercise-choice" @click="p.choose('breathing')"><span class="choice-symbol" aria-hidden="true">◌</span><span class="choice-title">Breathing</span><span>A soft balloon rhythm.<br>Four seconds in, six seconds out.</span><span class="choice-duration">60 seconds of pacing <b aria-hidden="true">→</b></span></button><button class="exercise-choice" @click="p.choose('grounding')"><span class="choice-symbol grounding-symbol" aria-hidden="true">✳</span><span class="choice-title">Grounding</span><span>Notice your surroundings,<br>one sense at a time.</span><span class="choice-duration">At your pace · about 90 seconds <b aria-hidden="true">→</b></span></button></div>
        <button v-if="result?.code !== 'both-declined'" class="text-button" @click="p.go('home')">Finish for now</button><p class="fine-print">A design heuristic, not a treatment recommendation.<br>{{ result?.code === 'both-declined' ? 'The exercises above are voluntary exploration only.' : 'Either choice is yours to change.' }}</p>
      </section>

      <section v-else-if="screen === 'ready'" class="ready-layout">
        <div class="ready-copy"><button class="back-button" @click="p.readyBack">← Back</button><span class="eyebrow">{{ result?.code === 'direct-choice' ? 'YOUR CHOICE' : 'ONE OPTION FOR THIS MOMENT' }}</span><h1 tabindex="-1">{{ title }}</h1>
          <div class="explanation-block"><p class="reason">{{ explanationText || result?.reason }}</p><span class="explanation-source">{{ explanationLabel }}</span></div>
          <p class="lead exercise-intro" v-if="exercise === 'breathing'">Follow the balloon with a comfortable breath. In through your nose as it grows, then gently out through your mouth as it softens. No need to force it.</p><p class="lead exercise-intro" v-else>Notice five things you can see, then four you can feel, three you can hear, two you can smell, and one you can taste. Keep them to yourself. You can skip any sense.</p>
          <div v-if="exercise === 'breathing'" class="visual-settings"><span class="setting-label">Balloon colour</span><div class="swatches"><button v-for="c in ['pink','red','pearl']" :key="c" :aria-label="c + ' balloon'" :aria-pressed="color === c" :class="['swatch', c, { chosen: color === c }]" @click="color = c"><span aria-hidden="true">{{ color === c ? '✓' : '' }}</span></button></div><label class="motion-choice"><input type="checkbox" v-model="reducedMotion"> Minimal motion</label></div>
          <button class="primary" @click="p.startExercise">Start {{ exercise }} <span aria-hidden="true">→</span></button><button class="text-button" @click="p.choose(exercise === 'breathing' ? 'grounding' : 'breathing')">Try {{ exercise === 'breathing' ? 'grounding' : 'breathing' }} instead</button><button class="text-button finish-ready" @click="p.go('home')">Finish for now</button><p class="fine-print">{{ exercise === 'breathing' ? 'Six cycles · no breath hold · 60 seconds of pacing.' : 'One Next action per sense. About 90 seconds, at your pace.' }}<br>You can stop or switch at any time.</p></div>
        <div class="ready-visual" aria-hidden="true"><BalloonPacer v-if="exercise === 'breathing'" :inflation=".7" :color="color" :reduced-motion="reducedMotion"/><div v-else class="sense-art"><span>5</span><span>4</span><span>3</span><span>2</span><span>1</span><small>here, one sense at a time</small></div></div>
      </section>

      <section v-else-if="screen === 'breathing'" class="practice-stage">
        <div class="practice-top"><button class="back-button" @click="p.stop">← Stop</button><span class="eyebrow">BREATHING · {{ timing.cycle }} OF 6</span></div><h1 tabindex="-1" class="breath-cue" aria-live="polite" aria-atomic="true">{{ paused ? 'Take your time.' : timing.phase === 'inhale' ? 'Breathe in gently' : 'Breathe out slowly' }}</h1><p class="practice-sub">{{ paused ? pauseReason || 'Paused. Breathe normally until you are ready.' : 'A comfortable breath is enough.' }}</p>
        <BalloonPacer :inflation="timing.inflation" :color="color" :reduced-motion="reducedMotion"/>
        <div class="phase-track" aria-hidden="true"><span :style="{ width: (timing.elapsed / 60000 * 100) + '%' }"></span></div><div class="practice-actions"><button class="secondary" @click="paused ? p.resume() : p.pause()">{{ paused ? 'Resume' : 'Pause' }}</button><button class="text-button" @click="p.stop">Stop · breathe normally</button><button class="text-button" @click="p.stop(); p.choose('grounding')">Switch to grounding</button></div><p class="fine-print">The balloon shows time. It does not measure your breathing.</p>
      </section>

      <section v-else-if="screen === 'grounding'" class="center-stage grounding-stage" @keydown="e => { if (e.repeat && ['Enter', ' '].includes(e.key)) e.preventDefault(); }">
        <div class="practice-top"><button class="back-button" :disabled="paused || senseIndex === 0" @click="p.backSense">← Back</button><span class="eyebrow">GROUNDING · {{ senseIndex + 1 }} OF 5</span><button class="text-button" @click="p.stop">Stop</button></div><div class="sense-count" aria-hidden="true">{{ sense.quantity }}</div><span class="eyebrow sense-label">{{ sense.sense }}</span><h1 tabindex="-1">{{ paused ? 'Take your time.' : sense.title }}</h1><p class="lead">{{ paused ? pauseReason || 'Paused. Continue when you are ready.' : sense.guidance }}</p><div class="quantity-markers" aria-hidden="true"><span v-for="n in sense.quantity" :key="n"></span></div><p class="question-note">Notice privately. No need to type or name them here.</p><button class="primary" :disabled="paused" @click="p.nextSense()">{{ senseIndex === 4 ? 'Finish grounding' : 'Next sense' }} <span aria-hidden="true">→</span></button><button class="text-button" :disabled="paused" @click="p.nextSense(true)">Skip this sense</button><button class="text-button" @click="paused ? p.resume() : p.pause()">{{ paused ? 'Resume' : 'Pause' }}</button><button class="text-button" @click="p.stop(); p.choose('breathing')">Switch to breathing</button>
      </section>

      <section v-else-if="screen === 'done'" class="center-stage narrow ending-stage"><span class="eyebrow">{{ sessionStatus === 'completed' ? 'EXERCISE COMPLETE' : 'EXERCISE STOPPED' }}</span><div class="end-mark" aria-hidden="true">—</div><h1 tabindex="-1">A moment, taken.</h1><p class="lead">You can finish here.<br>There is nothing else you need to do.</p><button class="primary" @click="p.go('home')">Finish <span aria-hidden="true">→</span></button><button class="text-button" @click="p.choose(exercise === 'breathing' ? 'grounding' : 'breathing')">Try the other exercise</button><p class="fine-print">This ending does not assess how you feel.</p></section>

      <section v-else-if="screen === 'history'" class="center-stage history-stage">
        <button class="back-button" @click="p.go('home')">← Back</button><span class="eyebrow">SAVED ON THIS COMPUTER</span><h1 tabindex="-1">Past sessions.</h1><p class="lead">A quiet record, without a score.</p>
        <div v-if="historyLoading" class="history-notice" role="status">Loading saved sessions…</div>
        <div v-else-if="historyError" class="history-notice" role="status"><p>{{ historyError }}</p><button class="text-button" @click="p.refreshHistory">Try again</button></div>
        <div v-else-if="!historyItems.length" class="history-notice"><h2>No saved sessions yet.</h2><p>Sessions appear here only when you choose to save and saving succeeds.</p></div>
        <div v-else class="session-list"><article v-for="s in historyItems" :key="s.id"><span class="session-date">{{ displayDate(s.created_at) }}</span><div><h2>{{ displaySkill(s.exercise) }}</h2><span>{{ displayStatus(s.status) }}</span></div><p v-if="s.result?.reason">{{ s.result.reason }}</p><button class="text-button session-open" @click="p.openSession(s.id)">View session <span class="sr-only">from {{ displayDate(s.created_at) }}</span> <span aria-hidden="true">→</span></button></article></div>
        <p class="fine-print">Only fictional sessions you chose to save are shown. Records stay on this computer until cleared. This is a record of actions, not an assessment.</p>
        <div class="history-actions"><button class="text-button" @click="p.refreshHistory">Refresh history</button><button v-if="historyItems.length && !confirmingClear" class="text-button" @click="confirmingClear = true">Clear saved history</button></div>
        <div v-if="confirmingClear" class="clear-confirmation" role="group" aria-labelledby="clear-title"><h2 id="clear-title">Clear all saved fictional sessions?</h2><p>This removes their saved answers and activity from this computer.</p><div><button class="secondary" @click="confirmingClear = false">Keep history</button><button class="primary" @click="clearSavedHistory">Yes, clear history</button></div></div>
      </section>

      <section v-else-if="screen === 'session-detail'" class="center-stage history-stage session-detail-stage">
        <button class="back-button" @click="p.go('history')">← Past sessions</button><span class="eyebrow">SAVED FICTIONAL SESSION</span><h1 tabindex="-1">A moment, recorded.</h1>
        <div v-if="historyLoading" class="history-notice" role="status">Loading this session…</div><div v-else-if="historyError" class="history-notice" role="status">{{ historyError }}</div>
        <template v-else-if="detail">
          <dl class="session-summary"><div><dt>Exercise</dt><dd>{{ displaySkill(detail.exercise) }}</dd></div><div><dt>Recorded status</dt><dd>{{ displayStatus(detail.status) }}</dd></div><div><dt>Started</dt><dd>{{ displayDate(detail.created_at) }}</dd></div><div><dt>Last saved</dt><dd>{{ displayDate(detail.updated_at) }}</dd></div></dl>
          <section class="record-section" aria-labelledby="record-choice"><h2 id="record-choice">Choice and explanation</h2><p>{{ detail.result?.reason || 'No exercise suggestion recorded.' }}</p><p v-if="detail.direct_choice" class="fine-print">Your deliberate choice: {{ displaySkill(detail.direct_choice) }}.</p><ol v-if="detail.explanations?.length" class="explanation-records"><li v-for="(item, i) in detail.explanations" :key="item.request_id || i"><p v-if="item.text">{{ item.text }}</p><span class="record-provenance">{{ explanationSource(item) }} · {{ item.outcome || item.status || 'Recorded' }}<template v-if="item.model_id"> · {{ item.model_id }}</template><template v-if="item.revision !== undefined"> · revision {{ item.revision }}{{ item.superseded ? ' (earlier)' : '' }}</template></span></li></ol></section>
          <section class="record-section" aria-labelledby="record-conversation">
            <h2 id="record-conversation">Check-in conversation</h2>
            <p v-if="currentTurns.length" class="record-context">The answers in this saved revision.</p>
            <ol v-if="currentTurns.length" class="conversation-records"><li v-for="(turn, i) in currentTurns" :key="turn.id || i" :class="{ 'user-record': turn.role === 'user' }"><span>{{ turn.role === 'user' ? 'Your response' : 'Peyce' }}</span><p>{{ turnText(turn) }}</p></li></ol><p v-else>Entered without check-in answers.</p>
            <details v-if="earlierTurnGroups.length" class="earlier-records"><summary>Earlier revisions · {{ earlierTurnGroups.length }} saved snapshots</summary><p>Historical snapshots preserve the conversation as it was saved. They may repeat unchanged answers and do not replace the answers above.</p><details v-for="group in earlierTurnGroups" :key="group.revision" class="revision-record"><summary>Revision {{ group.revision }} · {{ group.turns.length }} recorded turns</summary><ol class="conversation-records"><li v-for="(turn, i) in group.turns" :key="turn.id || i" :class="{ 'user-record': turn.role === 'user' }"><span>{{ turn.role === 'user' ? 'Your response' : 'Peyce' }}</span><p>{{ turnText(turn) }}</p></li></ol></details></details>
          </section>
          <section class="record-section" aria-labelledby="record-timing"><h2 id="record-timing">Time and activity</h2><dl v-if="detail.timing" class="timing-summary"><div><dt>{{ detail.timing.finish_ms !== null && detail.timing.finish_ms !== undefined ? 'Instructions through Finish' : 'Recorded span from instructions' }}</dt><dd>{{ seconds(detail.timing.raw_ms) }}</dd></div><div><dt>Chosen pause / support time</dt><dd>{{ seconds(detail.timing.excluded_ms) }}</dd></div><div><dt>Counted sequence</dt><dd>{{ seconds(detail.timing.counted_ms) }}</dd></div></dl><p v-else class="fine-print">A finished sequence duration has not been recorded.</p><ol v-if="detail.lifecycle?.length" class="lifecycle-records"><li v-for="(event, i) in detail.lifecycle" :key="event.id || i"><span>{{ eventLabel(event.kind) }}</span><span>{{ seconds(event.at_ms) }} from entry</span></li></ol><p class="fine-print">These records describe interface actions. They do not measure wellbeing or breathing.</p></section>
        </template><div v-else class="history-notice">This saved session is unavailable.</div>
      </section>
    </main>

    <footer class="site-footer"><div><span>Coursework prototype · fictional use only</span><span>No person is monitoring. This is not a support service.</span></div><div class="save-status" :class="'save-state-' + saveState"><span role="status" aria-live="polite">{{ footerMessage }}</span><button v-if="saveState === 'error'" class="text-button" @click="p.retrySave">Retry saving</button></div></footer>

    <details v-if="verificationMode" class="verification-tools"><summary>Coursework verification controls</summary><p>Controlled faults for local checks. Exercises and support remain available.</p><label>Explanation fault <select v-model="providerFault"><option value="">None</option><option value="timeout">Timeout</option><option value="invalid">Invalid output</option><option value="late">Late response</option><option value="provider">Provider error</option></select></label><label><input type="checkbox" v-model="saveFault"> Simulate database failure (save/history)</label><div><button class="secondary" @click="p.refreshHistory">Refresh saved history</button><button class="secondary" @click="p.retrySave">Retry saving</button></div></details>

    <dialog ref="supportDialog" class="support-dialog" aria-labelledby="support-title" @keydown="p.dialogKey">
      <div class="dialog-heading"><span class="eyebrow">CRISIS SUPPORT · UNITED STATES</span><button class="close-button" aria-label="Close crisis support" @click="p.closeSupport">×</button></div><h2 id="support-title">Reach a real person.</h2><p>Peyce is a coursework prototype. No person is monitoring this prototype, and it is not a support service.</p><div class="support-resource"><h3>988 Suicide &amp; Crisis Lifeline</h3><p>United States and territories.</p><div class="resource-actions"><a href="tel:988?oai_link_source=model_response_hotline">Call 988</a><a href="sms:988?oai_link_source=model_response_hotline">Text 988</a><a href="https://988lifeline.org/chat/?oai_link_source=model_response_hotline" target="_blank" rel="noopener noreferrer">Open 988 chat ↗</a></div></div><div class="support-resource"><h3>Immediate danger · United States</h3><p>For an emergency requiring police, fire, or ambulance.</p><div class="resource-actions"><a href="tel:911">Call 911</a></div></div><p class="fine-print">Outside the United States, contact local emergency or crisis services. This prototype has no worldwide resource directory.</p><button class="secondary" @click="p.closeSupport">Return to prototype</button>
    </dialog>
  </div>
</template>
