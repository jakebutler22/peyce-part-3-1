<script setup>
import { pacingObject } from '../assets.js';
defineProps({ inflation: { type: Number, default: 0.5 }, color: { type: String, default: 'pink' }, reducedMotion: Boolean });
</script>
<template>
  <div class="balloon-stage" :class="{ minimal: reducedMotion }">
    <img :src="pacingObject.source" :alt="color + ' latex balloon, a visual timing metaphor'" class="balloon" :class="'balloon-' + color" :style="{ transform: `scale(${reducedMotion ? .85 : .62 + inflation * .38}, ${reducedMotion ? .85 : .72 + inflation * .28})` }" />
    <div class="balloon-shadow" :style="{ opacity: reducedMotion ? .12 : .11 + inflation * .08, transform: `scaleX(${reducedMotion ? 1 : .7 + inflation * .3})` }"></div>
  </div>
</template>
