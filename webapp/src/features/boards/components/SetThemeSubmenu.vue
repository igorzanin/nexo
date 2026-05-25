<script setup lang="ts">
defineProps<{
  currentTheme: "default" | "dark" | "light";
}>();

const emit = defineEmits<{
  (e: "back"): void;
  (e: "select-theme", theme: "default" | "dark" | "light"): void;
}>();
</script>

<template>
  <li>
    <button type="button" class="dropdown-item" @click.stop="emit('back')">← Back</button>
  </li>
  <li>
    <button type="button" class="dropdown-item d-flex justify-content-between" @click.stop="emit('select-theme', 'default')">
      <span>Default</span><i v-if="currentTheme === 'default'" class="bi bi-check"></i>
    </button>
  </li>
  <li>
    <button type="button" class="dropdown-item d-flex justify-content-between" @click.stop="emit('select-theme', 'dark')">
      <span>Dark</span><i v-if="currentTheme === 'dark'" class="bi bi-check"></i>
    </button>
  </li>
  <li>
    <button type="button" class="dropdown-item d-flex justify-content-between" @click.stop="emit('select-theme', 'light')">
      <span>Light</span><i v-if="currentTheme === 'light'" class="bi bi-check"></i>
    </button>
  </li>
</template>