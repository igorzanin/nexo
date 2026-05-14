<script setup lang="ts">
const props = defineProps<{
  modelValue: boolean;
  disabled?: boolean;
  label?: string;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
}>();
</script>

<template>
  <div class="form-check form-switch">
    <input
      type="checkbox"
      class="form-check-input"
      :checked="modelValue"
      :disabled="disabled"
      @change="emit('update:modelValue', ($event.target as HTMLInputElement).checked)"
    />
    <label v-if="label" class="form-check-label small">{{ label }}</label>
  </div>
</template>
