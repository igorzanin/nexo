<script setup lang="ts">
import { ref } from "vue";

defineProps<{
  text: string;
}>();

const visible = ref(false);

function show() { visible.value = true; }
function hide() { visible.value = false; }
</script>

<template>
  <span class="position-relative d-inline-flex" @mouseenter="show" @mouseleave="hide">
    <slot />
    <span
      v-if="visible"
      class="position-absolute bg-dark text-white small px-2 py-1 rounded shadow-sm text-nowrap"
      style="z-index: 1080; bottom: 100%; left: 50%; transform: translateX(-50%); margin-bottom: 4px; font-size: 11px;"
    >
      {{ text }}
    </span>
  </span>
</template>
