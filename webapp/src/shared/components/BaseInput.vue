<script setup lang="ts">
defineProps<{
  modelValue: string;
  label?: string;
  placeholder?: string;
  type?: string;
  disabled?: boolean;
  error?: string;
}>();
defineEmits<{ (e: "update:modelValue", value: string): void }>();
</script>

<template>
  <div class="mb-3">
    <label v-if="label" class="form-label fw-semibold small">{{ label }}</label>
    <input
      :value="modelValue"
      :type="type || 'text'"
      :placeholder="placeholder"
      :disabled="disabled"
      :class="['form-control', error ? 'is-invalid' : '']"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <div v-if="error" class="invalid-feedback">{{ error }}</div>
  </div>
</template>
