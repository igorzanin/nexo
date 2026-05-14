<script setup lang="ts">
import { useRouter } from "vue-router";

const props = defineProps<{
  board: { id: string; title: string; icon?: string };
  active?: boolean;
}>();

const emit = defineEmits<{
  (e: "click", id: string): void;
}>();

const router = useRouter();

function handleClick() {
  router.push(`/board/${props.board.id}`);
  emit("click", props.board.id);
}
</script>

<template>
  <div
    class="d-flex align-items-center px-3 py-1 small rounded cursor-pointer sidebar-board-item"
    :class="{ 'bg-primary bg-opacity-10 text-primary': active }"
    @click="handleClick"
  >
    <span class="me-1">{{ board.icon || "📋" }}</span>
    <span class="text-truncate flex-grow-1">{{ board.title }}</span>
  </div>
</template>

<style scoped>
.sidebar-board-item:hover {
  background-color: rgba(0, 0, 0, 0.04);
}
</style>
