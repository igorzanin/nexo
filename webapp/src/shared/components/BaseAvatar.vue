<script setup lang="ts">
// BaseAvatar — círculo com inicial (SCR-017 layout.avatar.size)
withDefaults(defineProps<{
  username?: string;
  size?: number;
}>(), { size: 32 });
</script>

<template>
  <span
    class="rounded-circle bg-secondary text-white d-inline-flex align-items-center justify-content-center fw-semibold"
    :style="{ width: `${size}px`, height: `${size}px`, fontSize: `${Math.round(size * 0.4)}px`, flexShrink: '0' }"
  >
    {{ username?.charAt(0).toUpperCase() || "?" }}
  </span>
</template>
