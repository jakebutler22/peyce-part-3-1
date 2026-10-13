<script setup>
import { decorativeObjects } from '../assets.js';
defineProps({ objectId: { type: String, default: 'satin-bow' } });
</script>
<template><img v-if="decorativeObjects[objectId]" :src="decorativeObjects[objectId].source" :width="decorativeObjects[objectId].width" alt="" aria-hidden="true" class="decorative-object" /></template>
