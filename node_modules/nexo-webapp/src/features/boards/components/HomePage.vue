<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import AppLayout from "../../../shared/layouts/AppLayout.vue";
import CreateBoardModal from "./CreateBoardModal.vue";
import { useBoardsStore } from "../stores/boards.store";
import { useTeamsStore } from "../stores/teams.store";

const router = useRouter();
const boardsStore = useBoardsStore();
const teamsStore = useTeamsStore();

const showCreateModal = ref(false);
const status = ref<"idle" | "loading" | "error" | "success">("idle");
const errorMessage = ref("");

const teamName = computed(() => teamsStore.current?.title || "Nexo");
const boards = computed(() => boardsStore.boardList);

onMounted(async () => {
  status.value = "loading";
  errorMessage.value = "";
  try {
    if (!teamsStore.currentId) {
      await teamsStore.fetchTeams();
    }
    if (teamsStore.currentId) {
      await boardsStore.fetchBoards(teamsStore.currentId);
    }
    status.value = "success";
  } catch (error: unknown) {
    errorMessage.value = error instanceof Error ? error.message : "Failed to load boards";
    status.value = "error";
  }
});

function openBoard(boardId: string) {
  boardsStore.current = boardId;
  router.push(`/board/${boardId}`);
}
</script>

<template>
  <AppLayout :brand-text="'Nexo'" :team-name="teamName" :boards="boards" @create-board="showCreateModal = true">
    <div class="container-fluid p-4">
      <div class="vstack gap-4">
        <div class="d-flex align-items-center justify-content-between">
          <h1 class="mb-0">Boards</h1>
          <button type="button" class="btn btn-primary" @click="showCreateModal = true">+ Add board</button>
        </div>

        <div v-if="status === 'loading'" class="d-flex align-items-center gap-2 text-muted">
          <div class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></div>
          <span>Loading boards...</span>
        </div>

        <div v-else-if="status === 'error'" class="alert alert-danger mb-0">{{ errorMessage }}</div>

        <div v-else>
          <div class="visually-hidden" aria-live="polite">Boards loaded.</div>
          <div class="row g-3">
            <div v-for="board in boards" :key="board.id" class="col-md-6 col-xl-4">
              <div class="card shadow-sm h-100">
                <div class="card-body d-flex flex-column gap-2">
                  <h2 class="h5 mb-0">{{ board.title }}</h2>
                  <p class="text-muted mb-0 flex-grow-1">{{ board.description }}</p>
                  <button type="button" class="btn btn-link p-0 align-self-start" @click="openBoard(board.id)">
                    Open
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <CreateBoardModal v-if="showCreateModal" @close="showCreateModal = false" @created="showCreateModal = false" />
  </AppLayout>
</template>
