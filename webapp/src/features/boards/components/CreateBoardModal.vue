<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import type { Board } from "../../../types/board";
import { useBoardsStore } from "../stores/boards.store";
import { useTeamsStore } from "../stores/teams.store";

const emit = defineEmits<{
  (e: "close"): void;
  (e: "created", boardId: string): void;
}>();

const router = useRouter();
const boardsStore = useBoardsStore();
const teamsStore = useTeamsStore();

const boardName = ref("");
const selectedTemplateId = ref<string | null>(null);
const status = ref<"idle" | "loading" | "error" | "success">("idle");
const errorMessage = ref("");

const templates = computed(() => boardsStore.templateList);
const selectedTemplate = computed(() => templates.value.find((template) => template.id === selectedTemplateId.value) || null);
const preview = computed(() => selectedTemplate.value?.description || selectedTemplate.value?.title || "Select a template to preview it.");

onMounted(async () => {
  if (!teamsStore.currentId) {
    await teamsStore.fetchTeams();
  }
  if (teamsStore.currentId && !boardsStore.boardList.length && !boardsStore.templateList.length) {
    await boardsStore.fetchBoards(teamsStore.currentId);
  }
});

async function createBoard(useTemplate: boolean) {
  if (!boardName.value.trim()) {
    errorMessage.value = "Board name is required.";
    status.value = "error";
    return;
  }

  status.value = "loading";
  errorMessage.value = "";

  try {
    const payload = {
      teamId: teamsStore.currentId,
      title: boardName.value.trim(),
      ...(useTemplate && selectedTemplateId.value ? { templateId: selectedTemplateId.value } : {}),
    } as Partial<Board> & Record<string, unknown>;

    const board = await boardsStore.createBoard(payload);
    boardsStore.current = board.id;
    status.value = "success";
    emit("created", board.id);
    emit("close");
    router.push(`/board/${board.id}`);
  } catch (error: unknown) {
    errorMessage.value = error instanceof Error ? error.message : "Failed to create board";
    status.value = "error";
  }
}
</script>

<template>
  <Teleport to="#app-modal">
  <div class="modal fade show d-block" style="z-index: 1055;" tabindex="-1" aria-modal="true" role="dialog">
    <div class="modal-dialog modal-xl modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Create a board</h5>
          <button type="button" class="btn-close" aria-label="Close" @click="emit('close')"></button>
        </div>
        <div class="modal-body">
          <div class="vstack gap-3">
            <div v-if="status === 'loading'" class="text-muted">Creating board...</div>
            <div v-if="status === 'error' && errorMessage" class="alert alert-danger mb-0">{{ errorMessage }}</div>
            <div v-if="status === 'success'" class="visually-hidden" aria-live="polite">Board created.</div>

            <div>
              <label for="board-name" class="form-label">Board name</label>
              <input id="board-name" v-model="boardName" type="text" class="form-control" />
            </div>

            <div class="row g-3">
              <div class="col-lg-5">
                <div class="list-group">
                  <button
                    v-for="template in templates"
                    :key="template.id"
                    type="button"
                    class="list-group-item list-group-item-action"
                    :class="{ active: selectedTemplateId === template.id }"
                    @click="selectedTemplateId = template.id"
                  >
                    {{ template.title }}
                  </button>
                </div>
              </div>
              <div class="col-lg-7">
                <div class="card h-100">
                  <div class="card-header">Preview</div>
                  <div class="card-body text-muted">{{ preview }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-outline-secondary" :disabled="status === 'loading'" @click="createBoard(false)">
            Create empty board
          </button>
          <button
            type="button"
            class="btn btn-primary"
            :disabled="status === 'loading' || !selectedTemplateId"
            @click="createBoard(true)"
          >
            Use this template
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-backdrop fade show" style="z-index: 1050;" @click="emit('close')"></div>
  </Teleport>
</template>
