<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useBoardStore, useTeamStore, useViewStore } from "../../stores";
import Sidebar from "../sidebar/Sidebar.vue";
import CenterPanel from "../centerPanel/CenterPanel.vue";
import * as api from "../../api";

const props = defineProps<{
  boardId?: string;
}>();

const router = useRouter();
const boardStore = useBoardStore();
const teamStore = useTeamStore();
const loading = ref(false);
const error = ref("");

async function createBoard() {
  if (!teamStore.currentId) return;
  loading.value = true;
  error.value = "";
  try {
    const board = await boardStore.createBoard({ team_id: teamStore.currentId, title: "New Board", type: "P" });
    router.push(`/board/${board.id}`);
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Failed to create board";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="workspace d-flex" style="height: 100vh;">
    <Sidebar @create-board="createBoard" />
    <div v-if="error" class="d-flex align-items-center justify-content-center flex-grow-1">
      <div class="text-center">
        <p class="text-danger small">{{ error }}</p>
      </div>
    </div>
    <CenterPanel v-else-if="boardId || boardStore.current" :board-id="boardId || boardStore.current" />
    <div v-else class="d-flex flex-column align-items-center justify-content-center flex-grow-1 bg-body-secondary">
      <h2 class="mb-3">Welcome to Nexo</h2>
      <p class="text-muted mb-4">Create your first board to get started.</p>
      <button class="btn btn-primary btn-lg" :disabled="loading" @click="createBoard">
        {{ loading ? "Creating..." : "+ Create Board" }}
      </button>
    </div>
  </div>
</template>
