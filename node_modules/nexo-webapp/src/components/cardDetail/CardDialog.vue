<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useBoardStore, useCardStore, useContentStore } from "../../stores";
import { useMutator } from "../../composables/useMutator";
import ContentRegistry from "../content/ContentRegistry.vue";
import CardDetailProperties from "./CardDetailProperties.vue";
import CommentsList from "./CommentsList.vue";
import * as api from "../../api";

const props = defineProps<{
  cardId: string;
  boardId: string;
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

const boardStore = useBoardStore();
const cardStore = useCardStore();
const contentStore = useContentStore();
const mutator = useMutator();

const card = computed(() => cardStore.cards[props.cardId]);
const board = computed(() => boardStore.boards[props.boardId]);
const contents = computed(() =>
  Object.values(contentStore.contents).filter((c) => c.parentId === props.cardId)
);
const editing = ref(false);
const editTitle = ref("");
const saving = ref(false);
const showContentMenu = ref(false);

onMounted(async () => {
  const blocks = await api.getBlocks(props.boardId).catch(() => [] as any[]);
  contentStore.setContentsFromBlocks(blocks);
});

function onKeydown(e: KeyboardEvent) {
  if (e.key === "Escape") emit("close");
}

function startEdit() {
  editTitle.value = card.value?.title || "";
  editing.value = true;
}

async function saveTitle() {
  if (!editTitle.value.trim() || saving.value) return;
  saving.value = true;
  try {
    await api.patchBlock(props.boardId, props.cardId, { title: editTitle.value.trim() });
    if (card.value) card.value.title = editTitle.value.trim();
    editing.value = false;
  } catch {
    // silently fail
  } finally {
    saving.value = false;
  }
}

function addContentBlock(type: string) {
  showContentMenu.value = false;
  mutator.insertBlock(
    { id: props.boardId } as any,
    { type, title: "", parentId: props.cardId, boardId: props.boardId }
  ).then(async () => {
    const blocks = await api.getBlocks(props.boardId).catch(() => []);
    contentStore.setContentsFromBlocks(blocks);
  }).catch(() => {});
}

function deleteCard() {
  mutator.deleteBlock(props.boardId, props.cardId).then(() => emit("close")).catch(() => {});
}
</script>

<template>
  <Teleport to="#app-modal">
    <div class="Dialog" @click.self="emit('close')">
      <div class="backdrop" />
      <div class="wrapper" @mousedown.self="emit('close')">
        <div class="dialog cardDialog" role="dialog" @click.stop>
          <div class="toolbar">
            <div />
            <div class="toolbar--right">
              <button class="btn btn-sm btn-outline-secondary border-0 py-1" @click="deleteCard" title="Delete">
                <i class="bi bi-trash"></i>
              </button>
              <button class="dialog__close btn btn-sm btn-outline-secondary border-0 py-1" @click="emit('close')" title="Close">
                <i class="bi bi-x-lg"></i>
              </button>
            </div>
          </div>

          <div v-if="card" class="CardDetail px-4 pb-4">
            <div class="d-flex align-items-start gap-2 mb-2">
              <div class="flex-grow-1" style="max-width: 600px;">
                <span v-if="card.fields?.icon" class="d-inline-block mb-1" style="font-size: 24px;">{{ card.fields.icon }}</span>
                <input
                  v-if="editing"
                  v-model="editTitle"
                  class="form-control border-0 px-0 title-input"
                  @keyup.enter="saveTitle"
                  @keyup.escape="editing = false"
                  @blur="saveTitle"
                  autofocus
                />
                <div v-else class="title" @click="startEdit">
                  {{ card.title || "Untitled" }}
                </div>
              </div>
            </div>

            <div class="octo-propertylist mb-3" style="max-width: 600px;">
              <CardDetailProperties
                v-if="board"
                :card="card"
                :properties="board.cardProperties || []"
                :board-id="boardId"
              />
            </div>

            <div class="content-blocks position-relative" style="max-width: 600px;">
              <div v-for="block in contents" :key="block.id" class="py-1">
                <ContentRegistry :block="block" />
              </div>
              <div class="add-buttons position-relative">
                <div class="d-flex align-items-center gap-2">
                  <div class="text-muted cursor-pointer d-flex align-items-center gap-1 add-content-trigger" @click="showContentMenu = !showContentMenu">
                    <i class="bi bi-plus-lg"></i>
                    <span class="small">Add content</span>
                  </div>
                  <div v-if="showContentMenu" class="position-absolute start-0 mt-4 bg-white border rounded shadow-sm" style="z-index: 100; min-width: 160px;">
                    <button class="dropdown-item small py-1 px-3" @click="addContentBlock('text')"><i class="bi bi-type me-2"></i>Text</button>
                    <button class="dropdown-item small py-1 px-3" @click="addContentBlock('image')"><i class="bi bi-image me-2"></i>Image</button>
                    <button class="dropdown-item small py-1 px-3" @click="addContentBlock('checkbox')"><i class="bi bi-check-square me-2"></i>Checkbox</button>
                    <button class="dropdown-item small py-1 px-3" @click="addContentBlock('divider')"><i class="bi bi-hr me-2"></i>Divider</button>
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-4" style="max-width: 600px;">
              <CommentsList :card-id="cardId" :board-id="boardId" />
            </div>
          </div>

          <div v-else class="banner error px-4 py-3">
            This card doesn't exist or is inaccessible.
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.Dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1040;
}
.backdrop {
  position: fixed;
  width: 100%;
  height: 100%;
  background-color: rgba(63, 67, 80, 0.5);
  z-index: -1;
}
.wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.dialog {
  position: relative;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  box-shadow: rgba(63, 67, 80, 0.1) 0 0 0 1px, rgba(63, 67, 80, 0.1) 0 2px 4px;
  border-radius: 8px;
  overflow-x: hidden;
  overflow-y: auto;
  max-width: 975px;
  width: 100%;
  height: calc(100% - 144px);
  margin: 72px auto;
}
.toolbar {
  display: flex;
  flex-direction: row;
  padding: 24px 32px;
  justify-content: space-between;
  align-items: flex-start;
  flex-shrink: 0;
}
.toolbar--right {
  display: flex;
  gap: 8px;
  align-items: center;
}
.dialog__close {
  color: rgba(63, 67, 80, 0.56);
}
.dialog__close:hover {
  background-color: rgba(63, 67, 80, 0.08);
}
.CardDetail {
  flex: 1;
}
.title {
  width: 100%;
  font-size: 32px;
  line-height: 40px;
  font-weight: 600;
  cursor: pointer;
}
.title-input {
  font-size: 32px;
  line-height: 40px;
  font-weight: 600;
  padding: 0;
}
.octo-propertylist {
  display: flex;
  flex-direction: column;
  width: 100%;
}
.add-buttons {
  min-height: 32px;
  color: rgba(63, 67, 80, 0.4);
  width: 100%;
  display: flex;
  align-items: flex-start;
}
.add-content-trigger {
  opacity: 0;
  transition: opacity 0.1s;
}
.content-blocks:hover .add-content-trigger,
.content-blocks:focus-within .add-content-trigger {
  opacity: 1;
}
.banner {
  background-color: rgba(230, 192, 192, 0.9);
  text-align: center;
  padding: 10px;
  color: #222;
}
</style>
