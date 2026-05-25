<script setup lang="ts">
import { ref, watch } from "vue";

const emit = defineEmits<{
  (e: "search", query: string): void;
}>();

const query = ref("");
const isOpen = ref(false);
let debounceTimer: ReturnType<typeof setTimeout> | null = null;

function onInput(value: string) {
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    emit("search", value);
  }, 300);
}

function toggle() {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    setTimeout(() => {
      const el = document.getElementById("view-search-input");
      el?.focus();
    }, 50);
  }
}

watch(query, onInput);
</script>

<template>
  <div class="position-relative">
    <button v-if="!isOpen" class="btn btn-sm btn-outline-secondary border-0" @click="toggle">
      <i class="bi bi-search"></i>
    </button>
    <div v-else class="d-flex align-items-center">
      <input
        id="view-search-input"
        v-model="query"
        type="text"
        class="form-control form-control-sm"
        style="width: 180px;"
        placeholder="Search cards..."
        @keyup.escape="toggle"
      />
      <button class="btn btn-sm btn-link text-muted" @click="toggle">
        <i class="bi bi-x"></i>
      </button>
    </div>
  </div>
</template>
