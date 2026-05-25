<script setup lang="ts">
import type { Board } from "../../types/board";
import type { BoardView } from "../../types/boardView";

defineProps<{
  board: Board;
  view: BoardView;
}>();

const emit = defineEmits<{
  (e: "addCard"): void;
  (e: "addView"): void;
}>();
</script>

<template>
  <div class="view-header d-flex align-items-center justify-content-between px-3 py-2 border-bottom bg-white">
    <div class="d-flex align-items-center gap-2">
      <span class="fs-5">{{ board.icon }}</span>
      <h5 class="mb-0">{{ board.title }}</h5>
      <span class="badge bg-secondary">{{ view.fields.viewType }}</span>
    </div>

    <div class="d-flex gap-2">
      <button class="btn btn-sm btn-outline-primary" @click="emit('addCard')">+ Card</button>
      <button class="btn btn-sm btn-outline-secondary" @click="emit('addView')">+ View</button>
    </div>
  </div>
</template>
