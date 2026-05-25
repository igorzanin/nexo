<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from "vue";
import { Modal } from "bootstrap";
import { useBoardStore, useCardStore, useContentStore, useTeamStore } from "../../stores";
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
const teamStore = useTeamStore();
const mutator = useMutator();

const card = computed(() => cardStore.cards[props.cardId]);
const board = computed(() => boardStore.boards[props.boardId]);
const contents = computed(() =>
  Object.values(contentStore.contents).filter((c) => c.parentId === props.cardId)
);
const editing = ref(false);
const editTitle = ref("");
const saving = ref(false);
const uploadingImage = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);
const modalEl = ref<HTMLElement | null>(null);
let bsModal: Modal | null = null;

function onHidden() {
  emit("close");
}

onMounted(async () => {
  await nextTick();
  if (modalEl.value) {
    bsModal = new Modal(modalEl.value, { backdrop: true, keyboard: true });
    modalEl.value.addEventListener("hidden.bs.modal", onHidden);
    bsModal.show();
  }
  const blocks = await api.getBlocks(props.boardId).catch(() => [] as any[]);
  contentStore.setContentsFromBlocks(blocks);
});

onBeforeUnmount(() => {
  if (modalEl.value) {
    modalEl.value.removeEventListener("hidden.bs.modal", onHidden);
  }
  bsModal?.dispose();
  // Bootstrap cannot clean up after itself when Vue removes the element from DOM.
  // Manually remove any leftover Bootstrap modal state so subsequent pages are interactive.
  document.body.classList.remove("modal-open");
  document.body.style.removeProperty("overflow");
  document.body.style.removeProperty("padding-right");
  document.querySelectorAll(".modal-backdrop").forEach((el) => el.remove());
});

function close() {
  bsModal?.hide();
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
  } finally {
    saving.value = false;
  }
}

async function addContentBlock(type: string) {
  if (type === "image") {
    fileInput.value?.click();
    return;
  }
  mutator.insertBlock(
    { id: props.boardId } as any,
    { type, title: "", parentId: props.cardId, boardId: props.boardId }
  ).then(async () => {
    const blocks = await api.getBlocks(props.boardId).catch(() => []);
    contentStore.setContentsFromBlocks(blocks);
  }).catch(() => {});
}

async function onFileSelected(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (!file) return;
  uploadingImage.value = true;
  try {
    const teamId = board.value?.teamId || teamStore.currentId;
    if (!teamId) throw new Error("No teamId");
    const { url } = await api.uploadFile(teamId, props.boardId, file);
    const block = await api.createBlock(props.boardId, {
      type: "image",
      title: url,
      parentId: props.cardId,
      boardId: props.boardId,
    });
    contentStore.setContent(block);
  } catch (err) {
    console.error("Image upload failed:", err);
  } finally {
    uploadingImage.value = false;
    if (fileInput.value) fileInput.value.value = "";
  }
}

function deleteCard() {
  mutator.deleteBlock(props.boardId, props.cardId).then(() => close()).catch(() => {});
}
</script>

<template>
  <Teleport to="body">
    <div ref="modalEl" class="modal fade" tabindex="-1" aria-modal="true" role="dialog">
      <div class="modal-dialog modal-xl modal-dialog-scrollable modal-dialog-centered" style="max-width: 975px;">
        <div class="modal-content">
          <div class="d-flex align-items-center justify-content-end gap-1 px-3 pt-2 pb-1">
            <div class="flex-grow-1" />
            <button class="btn btn-sm btn-outline-secondary border-0 py-1" @click="deleteCard" title="Delete">
              <i class="bi bi-trash"></i>
            </button>
            <button class="btn btn-sm btn-outline-secondary border-0 py-1" data-bs-dismiss="modal" title="Close">
              <i class="bi bi-x-lg"></i>
            </button>
          </div>

          <div v-if="card" class="modal-body px-4 pb-4">
            <div class="d-flex align-items-start gap-2 mb-2">
              <div class="flex-grow-1">
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

            <div class="octo-propertylist mb-3">
              <CardDetailProperties
                v-if="board"
                :card="card"
                :properties="board.cardProperties || []"
                :board-id="boardId"
              />
            </div>

            <div class="mb-4">
              <CommentsList :card-id="cardId" :board-id="boardId" />
            </div>

            <div class="content-blocks">
              <div v-for="block in contents" :key="block.id" class="py-1">
                <ContentRegistry :block="block" :board-id="boardId" />
              </div>
              <div class="mt-2">
                <div class="dropdown">
                  <button class="btn btn-sm btn-outline-secondary" data-bs-toggle="dropdown">
                    <i class="bi bi-plus-lg me-1"></i>Adicionar conteúdo
                  </button>
                  <ul class="dropdown-menu">
                    <li><button class="dropdown-item small" @click="addContentBlock('text')"><i class="bi bi-text-left me-2"></i>texto</button></li>
                    <li><button class="dropdown-item small" :disabled="uploadingImage" @click="addContentBlock('image')"><i class="bi bi-image me-2"></i>imagem<span v-if="uploadingImage"> (enviando...)</span></button></li>
                    <li><button class="dropdown-item small" @click="addContentBlock('divider')"><i class="bi bi-dash-lg me-2"></i>Divisor</button></li>
                    <li><button class="dropdown-item small" @click="addContentBlock('checkbox')"><i class="bi bi-check-square me-2"></i>caixa de seleção</button></li>
                  </ul>
                </div>
                <input ref="fileInput" type="file" accept="image/*" class="d-none" @change="onFileSelected" />
              </div>
            </div>
          </div>

          <div v-else class="modal-body">
            <div class="alert alert-danger mb-0">This card doesn't exist or is inaccessible.</div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
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
</style>