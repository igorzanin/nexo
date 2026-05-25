<script setup lang="ts">
defineProps<{
  modelValue: string;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
  (e: "save"): void;
}>();
</script>

<template>
  <div class="dropdown">
    <div class="small" style="cursor: pointer;" data-bs-toggle="dropdown" aria-expanded="false">
      <span v-if="modelValue" class="d-flex align-items-center gap-1">
        <span class="rounded-circle bg-secondary text-white d-inline-flex align-items-center justify-content-center" style="width: 18px; height: 18px; font-size: 9px;">
          {{ modelValue.charAt(0).toUpperCase() }}
        </span>
        {{ modelValue }}
      </span>
      <span v-else class="text-muted">No one</span>
    </div>
    <div class="dropdown-menu p-2" style="min-width: 200px;">
      <div class="small text-muted">User selection placeholder</div>
    </div>
  </div>
</template>
