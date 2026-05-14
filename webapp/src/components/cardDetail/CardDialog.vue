<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useCardStore, useContentStore } from "../../stores";
import { useMutator } from "../../composables/useMutator";
import { useFlashMessage } from "../../composables/useFlashMessage";
import ContentRegistry from "../content/ContentRegistry.vue";
import * as api from "../../api";

const props = defineProps<{
  cardId: string;
  boardId: string;
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

const cardStore = useCardStore();
const contentStore = useContentStore();
const mutator = useMutator();
const { show } = useFlashMessage();

const card = computed(() => cardStore.cards[props.cardId]);
const contents = computed(() =>
  Object.values(contentStore.contents).filter((c) => c.parentId === props.cardId)
);
const editing = ref(false);
const editTitle = ref("");
const saving = ref(false);

onMounted(async () => {
  const blocks = await api.getBlocks(props.boardId).catch(() => [] as any[]);
  contentStore.setContentsFromBlocks(blocks);
});

function startEdit() {
  editTitle.value = card.value?.title || "";
  editing.value = true;
}

async function saveTitle() {
  if (!editTitle.value.trim() || saving.value) return;
  saving.value = true;
  try {
    await api.patchBlock(props.boardId, props.cardId, { title: editTitle.value.trim() });
    if (card.value) {
      card.value.title = editTitle.value.trim();
    }
    editing.value = false;
    show("Title updated", "success");
  } catch (e: any) {
    show(e.response?.data?.detail || "Failed to update title", "error");
  } finally {
    saving.value = false;
  }
}

async function addTextBlock() {
  try {
    await mutator.insertBlock(
      { id: props.boardId } as any,
      { type: "text", title: "", parentId: props.cardId, boardId: props.boardId }
    );
    const blocks = await api.getBlocks(props.boardId).catch(() => [] as any[]);
    contentStore.setContentsFromBlocks(blocks);
    show("Text block added", "success");
  } catch (e: any) {
    show(e.response?.data?.detail || "Failed to add text", "error");
  }
}

async function deleteCard() {
  try {
    await mutator.deleteBlock(props.boardId, props.cardId);
    emit("close");
    show("Card deleted", "success");
  } catch (e: any) {
    show(e.response?.data?.detail || "Failed to delete card", "error");
  }
}
</script>

<template>
  <Teleport to="#app-modal">
    <div class="modal-backdrop fade show" @click="emit('close')" />
    <div class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <div class="flex-grow-1">
              <input
                v-if="editing"
                v-model="editTitle"
                class="form-control form-control-sm"
                @keyup.enter="saveTitle"
                @keyup.escape="editing = false"
                autofocus
              />
              <h5 v-else class="modal-title" style="cursor: pointer;" @click="startEdit">
                {{ card?.title || "Untitled" }}
                <span class="text-muted small fw-normal ms-2">✏️</span>
              </h5>
            </div>
            <button type="button" class="btn-close" @click="emit('close')" />
          </div>

          <div class="modal-body">
            <div class="mb-3">
              <strong class="small text-muted">Content</strong>
              <div v-if="contents.length === 0" class="text-muted small py-2">
                No content yet. Add a text block below.
              </div>
              <div v-for="block in contents" :key="block.id" class="border-bottom py-1">
                <ContentRegistry :block="block" />
              </div>
            </div>
          </div>

          <div class="modal-footer d-flex justify-content-between">
            <div class="d-flex gap-1">
              <button class="btn btn-sm btn-outline-secondary" @click="addTextBlock">+ Text</button>
            </div>
            <div>
              <button class="btn btn-sm btn-outline-danger" @click="deleteCard">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>
