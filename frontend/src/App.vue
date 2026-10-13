<script setup>
import { computed } from 'vue';
import { objectsFor } from './assets.js';
import { questions, senses, fictionalSessions } from './data.js';
import { usePrototype } from './usePrototype.js';
import FaceOption from './components/FaceOption.vue';
import DecorativeObject from './components/DecorativeObject.vue';
import BalloonPacer from './components/BalloonPacer.vue';
const p = usePrototype();
const { screen, questionIndex, answers, result, exercise, origin, selecting, senseIndex, color, reducedMotion, timing, paused, pauseReason, sessionStatus, supportDialog } = p;
const question = computed(() => questions[questionIndex.value]);
const sense = computed(() => senses[senseIndex.value]);
const title = computed(() => exercise.value === 'breathing' ? 'A gentle breathing rhythm.' : 'A little more here.');
function directEntry() { origin.value = 'direct'; result.value = null; p.go('choice'); }
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
        <div class="opening-copy"><span class="eyebrow">PEYCE · PRONOUNCED “PACE”</span><h1 tabindex="-1">A moment<br>at your <em>pace.</em></h1><p class="lead">A gentle rhythm. A little grounding.<br>Room to choose what fits right now.</p><div class="opening-actions"><button class="primary" @click="p.beginCheckin">Find an exercise <span aria-hidden="true">→</span></button><button class="secondary" @click="directEntry">Choose an exercise</button></div><p class="fine-print">Five optional questions, or go straight to a practice.<br>No typing. No account. You can leave at any time.</p></div>
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
        <div class="ready-copy"><button class="back-button" @click="p.readyBack">← Back</button><span class="eyebrow">{{ result?.code === 'direct-choice' ? 'YOUR CHOICE' : 'ONE OPTION FOR THIS MOMENT' }}</span><h1 tabindex="-1">{{ title }}</h1><p class="reason">{{ result?.reason }}</p><p class="lead exercise-intro" v-if="exercise === 'breathing'">Follow the balloon with a comfortable breath. In through your nose as it grows, then gently out through your mouth as it softens. No need to force it.</p><p class="lead exercise-intro" v-else>Notice five things you can see, then four you can feel, three you can hear, two you can smell, and one you can taste. Keep them to yourself. You can skip any sense.</p>
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
        <div class="practice-top"><button class="back-button" @click="senseIndex > 0 ? (senseIndex--, p.go('grounding')) : p.go('ready')">← Back</button><span class="eyebrow">GROUNDING · {{ senseIndex + 1 }} OF 5</span><button class="text-button" @click="p.stop">Stop</button></div><div class="sense-count" aria-hidden="true">{{ sense.quantity }}</div><span class="eyebrow sense-label">{{ sense.sense }}</span><h1 tabindex="-1">{{ sense.title }}</h1><p class="lead">{{ sense.guidance }}</p><div class="quantity-markers" aria-hidden="true"><span v-for="n in sense.quantity" :key="n"></span></div><p class="question-note">Notice privately. No need to type or name them here.</p><button class="primary" @click="p.nextSense">{{ senseIndex === 4 ? 'Finish grounding' : 'Next sense' }} <span aria-hidden="true">→</span></button><button class="text-button" @click="p.nextSense">Skip this sense</button><button class="text-button" @click="p.stop(); p.choose('breathing')">Switch to breathing</button>
      </section>

      <section v-else-if="screen === 'done'" class="center-stage narrow ending-stage"><span class="eyebrow">{{ sessionStatus === 'completed' ? 'EXERCISE COMPLETE' : 'EXERCISE STOPPED' }}</span><div class="end-mark" aria-hidden="true">—</div><h1 tabindex="-1">A moment, taken.</h1><p class="lead">You can finish here.<br>There is nothing else you need to do.</p><button class="primary" @click="p.go('home')">Finish <span aria-hidden="true">→</span></button><button class="text-button" @click="p.choose(exercise === 'breathing' ? 'grounding' : 'breathing')">Try the other exercise</button><p class="fine-print">This ending does not assess how you feel.</p></section>

      <section v-else-if="screen === 'history'" class="center-stage history-stage"><button class="back-button" @click="p.go('home')">← Back</button><span class="eyebrow">FICTIONAL DESIGN EXAMPLE</span><h1 tabindex="-1">Past sessions.</h1><p class="lead">A quiet record, without a score.</p><div class="session-list"><article v-for="s in fictionalSessions" :key="s.date"><span class="session-date">{{ s.date }}</span><div><h2>{{ s.exercise }}</h2><span>{{ s.status }}</span></div><p>{{ s.detail }}</p></article></div><p class="fine-print">These two records are fictional. This prototype saves no sessions.<br>Your choices here stay in memory and disappear on reload.</p><button class="text-button" @click="p.go('failure')">View scripted explanation failure</button></section>

      <section v-else-if="screen === 'failure'" class="center-stage narrow"><button class="back-button" @click="p.go('history')">← Back</button><span class="eyebrow">SCRIPTED FAILURE EXAMPLE</span><h1 tabindex="-1">Your choices<br>are still here.</h1><p class="lead">An explanation is unavailable. You can choose an exercise without waiting.</p><p class="notice">No model is connected in this prototype. In the planned design, a delayed or invalid explanation falls back to approved copy and never blocks access.</p><button class="primary" @click="directEntry">Choose an exercise <span aria-hidden="true">→</span></button><button class="text-button" @click="p.go('home')">Finish for now</button></section>
    </main>

    <footer class="site-footer"><span>Coursework design prototype · fictional use only</span><span>No person is monitoring. <span class="footer-scripted">Responses are scripted.</span></span></footer>

    <dialog ref="supportDialog" class="support-dialog" aria-labelledby="support-title" @keydown="p.dialogKey">
      <div class="dialog-heading"><span class="eyebrow">CRISIS SUPPORT · UNITED STATES</span><button class="close-button" aria-label="Close crisis support" @click="p.closeSupport">×</button></div><h2 id="support-title">Reach a real person.</h2><p>Peyce is a coursework prototype. No person is monitoring this prototype, and it is not a support service.</p><div class="support-resource"><h3>988 Suicide &amp; Crisis Lifeline</h3><p>United States and territories.</p><div class="resource-actions"><a href="tel:988?oai_link_source=model_response_hotline">Call 988</a><a href="sms:988?oai_link_source=model_response_hotline">Text 988</a><a href="https://988lifeline.org/chat/?oai_link_source=model_response_hotline" target="_blank" rel="noopener noreferrer">Open 988 chat ↗</a></div></div><div class="support-resource"><h3>Immediate danger · United States</h3><p>For an emergency requiring police, fire, or ambulance.</p><div class="resource-actions"><a href="tel:911">Call 911</a></div></div><p class="fine-print">Outside the United States, contact local emergency or crisis services. This prototype has no worldwide resource directory.</p><button class="secondary" @click="p.closeSupport">Return to prototype</button>
    </dialog>
  </div>
</template>
