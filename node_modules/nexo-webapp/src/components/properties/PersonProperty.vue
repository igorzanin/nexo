<script setup lang="ts">
import { ref } from "vue";

defineProps<{
  modelValue: string;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
  (e: "save"): void;
}>();

const isOpen = ref(false);
</script>

<template>
  <div class="position-relative">
    <div class="small" style="cursor: pointer;" @click="isOpen = !isOpen">
      <span v-if="modelValue" class="d-flex align-items-center gap-1">
        <span class="rounded-circle bg-secondary text-white d-inline-flex align-items-center justify-content-center" style="width: 18px; height: 18px; font-size: 9px;">
          {{ modelValue.charAt(0).toUpperCase() }}
        </span>
        {{ modelValue }}
      </span>
      <span v-else class="text-muted">No one</span>
    </div>
    <div v-if="isOpen" class="position-absolute start-0 mt-1 bg-white border rounded shadow-sm" style="z-index: 100; min-width: 200px;">
      <div class="px-3 py-1 small text-muted">User selection placeholder</div>
    </div>
  </div>
</template>
