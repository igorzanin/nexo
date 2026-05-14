<script setup lang="ts">
import { ref } from "vue";

const emit = defineEmits<{
  (e: "exportBoard"): void;
  (e: "duplicateBoard"): void;
  (e: "deleteBoard"): void;
}>();

const isOpen = ref(false);

function toggle() {
  isOpen.value = !isOpen.value;
}

function handle(action: string) {
  isOpen.value = false;
  if (action === "export") emit("exportBoard");
  if (action === "duplicate") emit("duplicateBoard");
  if (action === "delete") emit("deleteBoard");
}
</script>

<template>
  <div class="position-relative">
    <button class="btn btn-sm btn-outline-secondary border-0" @click="toggle">
      <i class="bi bi-three-dots-vertical"></i>
    </button>
    <div v-if="isOpen" class="position-absolute end-0 mt-1 bg-white border rounded shadow-sm" style="z-index: 100; min-width: 160px;">
      <button class="dropdown-item small py-1 px-3" @click="handle('export')">
        <i class="bi bi-download me-2"></i> Export Board
      </button>
      <button class="dropdown-item small py-1 px-3" @click="handle('duplicate')">
        <i class="bi bi-files me-2"></i> Duplicate Board
      </button>
      <hr class="my-1">
      <button class="dropdown-item small py-1 px-3 text-danger" @click="handle('delete')">
        <i class="bi bi-trash me-2"></i> Delete Board
      </button>
    </div>
  </div>
</template>
