<script setup lang="ts">
withDefaults(defineProps<{
  variant?: "primary" | "secondary" | "danger" | "outline-secondary" | "outline-primary";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  loading?: boolean;
  type?: "button" | "submit" | "reset";
}>(), {
  variant: "primary",
  size: "md",
  disabled: false,
  loading: false,
  type: "button",
});
</script>

<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="['btn', `btn-${variant}`, size !== 'md' ? `btn-${size}` : '']"
  >
    <span v-if="loading" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true" />
    <slot />
  </button>
</template>
