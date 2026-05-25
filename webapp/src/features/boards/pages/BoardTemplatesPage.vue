<script setup lang="ts">
// features/boards/pages/BoardTemplatesPage.vue
// Lista e gerencia templates de board disponíveis para o time.
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import AppLayout from "../../../shared/layouts/AppLayout.vue";
import { useBoardsStore } from "../stores/boards.store";
import { useTeamsStore } from "../stores/teams.store";
import type { Board } from "../../../types/board";

const router = useRouter();
const boardStore = useBoardsStore();
const teamStore = useTeamsStore();

const loading = ref(false);
const error = ref("");
const creating = ref(false);

onMounted(async () => {
  loading.value = true;
  try {
    if (!teamStore.currentId) await teamStore.fetchTeams();
    if (teamStore.currentId) await boardStore.fetchBoards(teamStore.currentId);
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Failed to load templates";
  } finally {
    loading.value = false;
  }
});

async function useTemplate(template: Board) {
  creating.value = true;
  error.value = "";
  try {
    const board = await boardStore.createBoard({
      teamId: teamStore.currentId,
      title: `Copy of ${template.title}`,
      isTemplate: false,
    });
    router.push(`/board/${board.id}`);
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Failed to use template";
  } finally {
    creating.value = false;
  }
}
</script>

<template>
  <AppLayout>
    <div class="container py-4">
      <h4 class="mb-4">Board Templates</h4>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-if="loading" class="text-center text-muted py-5">
        <div class="spinner-border spinner-border-sm me-2"></div>
        Loading templates…
      </div>

      <div v-else-if="boardStore.templateList.length === 0" class="text-center text-muted py-5">
        No templates available.
      </div>

      <div v-else class="row g-3">
        <div
          v-for="template in boardStore.templateList"
          :key="template.id"
          class="col-md-6 col-xl-4"
        >
          <div class="card h-100 shadow-sm">
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">
                {{ template.icon || "📋" }} {{ template.title }}
              </h5>
              <p class="card-text text-muted small flex-grow-1">
                {{ template.description || "No description" }}
              </p>
              <button
                class="btn btn-primary btn-sm mt-2"
                :disabled="creating"
                @click="useTemplate(template)"
              >
                <span v-if="creating" class="spinner-border spinner-border-sm me-1"></span>
                Use template
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>
