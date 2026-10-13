<script setup>
defineProps({ value: Number, label: String, selected: Boolean, disabled: Boolean });
defineEmits(['choose']);
</script>
<template>
  <button class="face-option" :class="{ selected }" :aria-pressed="selected" :disabled="disabled" @keydown="e => { if (e.repeat) e.preventDefault(); }" @click="e => { if (e.detail < 2) $emit('choose', value); }">
    <svg viewBox="0 0 80 80" aria-hidden="true" :class="['face', 'face-' + value]">
      <circle cx="40" cy="40" r="35" />
      <g class="face-lines"><circle cx="29" cy="32" r="2"/><circle cx="51" cy="32" r="2"/>
        <path v-if="value === 0" d="M26 45 Q40 62 54 45"/><path v-else-if="value === 1" d="M26 51 H54"/><path v-else d="M26 56 Q40 39 54 56"/>
      </g>
    </svg>
    <span>{{ label }}</span><span class="selection-mark" aria-hidden="true">{{ selected ? '✓' : '' }}</span>
  </button>
</template>
