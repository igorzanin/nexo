<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { createBlock } from "../../../types/block";
import type { Block } from "../../../types/block";
import type { IPropertyTemplate } from "../../../types/board";
import type { ContentBlockType } from "../../../types/contentBlock";
import { useBoardStore } from "../../../stores/boardStore";
import { useCommentStore, useContentStore } from "../stores/content.store";
import * as api from "../../../api";
import ContentRegistry from "./ContentRegistry.vue";
import PropertyValueElement from "./PropertyValueElement.vue";

const props = defineProps<{
  boardId: string;
  cardId: string;
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

const boardStore = useBoardStore();
const contentStore = useContentStore();
const commentStore = useCommentStore();

const PROPERTY_TYPES: { value: string; label: string }[] = [
  { value: "text",            label: "Texto" },
  { value: "number",          label: "Número" },
  { value: "email",           label: "Email" },
  { value: "phone",           label: "Telefone" },
  { value: "url",             label: "URL" },
  { value: "select",          label: "Selecionar" },
  { value: "multiselect",     label: "Seleção múltipla" },
  { value: "date",            label: "Data" },
  { value: "person",          label: "Pessoa" },
  { value: "multiperson",     label: "Múltiplas pessoas" },
  { value: "checkbox",        label: "Caixa de seleção" },
  { value: "createdTime",     label: "Horário de criação" },
  { value: "createdBy",       label: "Criado por" },
  { value: "updatedTime",     label: "Atualizado pela última vez em" },
  { value: "updatedBy",       label: "Atualizado pela última vez por" },
];

const CONTENT_TYPES: { value: ContentBlockType; label: string; icon: string }[] = [
  { value: "text",      label: "texto",          icon: "bi-text-left" },
  { value: "image",     label: "imagem",         icon: "bi-image" },
  { value: "divider",   label: "Divisor",        icon: "bi-dash-lg" },
  { value: "checkbox",  label: "caixa de seleção", icon: "bi-check2-square" },
];

const status = ref<"idle" | "loading" | "error">("loading");
const errorMessage = ref("");
const liveMessage = ref("");
const card = ref<Block | null>(null);
const title = ref("");
const newComment = ref("");
const titleEditing = ref(false);

const cardContents = computed(() => contentStore.contentsByCard[props.cardId] ?? []);
const comments = computed(() => commentStore.commentsByCard[props.cardId] ?? []);
const boardProperties = computed(() => boardStore.boards[props.boardId]?.cardProperties ?? []);
const cardIcon = computed(() => (card.value?.fields as Record<string, unknown>)?.icon as string | undefined);

function propertyValue(propertyId: string) {
  return ((card.value?.fields?.properties as Record<string, unknown>) ?? {})[propertyId] ?? "";
}

async function loadCard() {
  status.value = "loading";
  errorMessage.value = "";
  try {
    if (!boardStore.boards[props.boardId]) {
      await boardStore.fetchBoard(props.boardId);
    }
    const blocks = await api.getBlocks(props.boardId);
    card.value = blocks.find((b) => b.id === props.cardId) ?? null;
    title.value = card.value?.title || "";
    contentStore.setContentsFromBlocks(blocks);
    commentStore.setCommentsFromBlocks(blocks);
    status.value = "idle";
  } catch (err: unknown) {
    errorMessage.value = err instanceof Error ? err.message : "Failed to load card";
    status.value = "error";
  }
}

async function saveTitle() {
  titleEditing.value = false;
  if (!card.value || title.value === card.value.title) return;
  const updated = await api.patchBlock(props.boardId, card.value.id, { title: title.value });
  card.value = updated;
  liveMessage.value = "Card updated.";
}

async function updateProperty(propertyId: string, value: unknown) {
  if (!card.value) return;
  const updated = await api.patchBlock(props.boardId, card.value.id, {
    fields: {
      ...card.value.fields,
      properties: {
        ...((card.value.fields?.properties as Record<string, unknown>) ?? {}),
        [propertyId]: value,
      },
    },
  });
  card.value = updated;
  liveMessage.value = "Card updated.";
}

async function addBlock(type: ContentBlockType) {
  const created = await api.createBlock(props.boardId, createBlock({ boardId: props.boardId, parentId: props.cardId, type }));
  contentStore.setContent(created);
}

async function updateBlock(block: Block, blockTitle: string) {
  const updated = await api.patchBlock(props.boardId, block.id, { title: blockTitle });
  contentStore.setContent(updated);
}

async function toggleCheckbox(block: Block, checked: boolean) {
  const updated = await api.patchBlock(props.boardId, block.id, { fields: { ...block.fields, checked } });
  contentStore.setContent(updated);
}

async function addComment() {
  if (!newComment.value.trim()) return;
  const created = await api.createBlock(props.boardId, createBlock({
    boardId: props.boardId,
    parentId: props.cardId,
    type: "comment",
    title: newComment.value.trim(),
  }));
  commentStore.setComment(created);
  newComment.value = "";
  liveMessage.value = "Card updated.";
}

async function addBoardProperty(type: string) {
  const board = boardStore.boards[props.boardId];
  if (!board) return;
  const newProp: IPropertyTemplate = {
    id: crypto.randomUUID(),
    name: PROPERTY_TYPES.find((t) => t.value === type)?.label ?? type,
    type,
    options: [],
  };
  const updatedBoard = await api.patchBoard(props.boardId, {
    cardProperties: [...board.cardProperties, newProp],
  });
  boardStore.setBoard(updatedBoard);
  liveMessage.value = "Propriedade adicionada.";
}

onMounted(loadCard);
watch(() => props.cardId, loadCard);
</script>

<template>
  <Teleport to="#app-modal">
    <div class="modal fade show d-block" tabindex="-1" style="z-index:1055;" aria-modal="true" role="dialog" @click.self="emit('close')">
    <div class="modal-dialog modal-xl modal-dialog-scrollable" style="max-width: 750px;">
      <div class="modal-content" style="min-height: 500px;">

        <!-- Minimal toolbar -->
        <div class="d-flex align-items-center justify-content-end gap-1 px-3 pt-2 pb-1">
          <button type="button" class="btn btn-sm btn-outline-secondary border-0 text-muted" title="Attach">
            <i class="bi bi-paperclip me-1"></i>Attach
          </button>
          <div class="dropdown">
            <button type="button" class="btn btn-sm btn-outline-secondary border-0 text-muted" data-bs-toggle="dropdown" title="More options">
              <i class="bi bi-three-dots"></i>
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
              <li><button type="button" class="dropdown-item text-danger small">Delete card</button></li>
            </ul>
          </div>
          <button type="button" class="btn btn-sm btn-outline-secondary border-0 text-muted" @click="emit('close')" title="Close">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>

        <div class="modal-body pt-1 pb-4 px-4">
          <div v-if="status === 'loading'" class="text-muted py-5 text-center">
            <div class="spinner-border spinner-border-sm me-2" role="status"></div>Loading card...
          </div>
          <div v-else-if="status === 'error'" class="alert alert-danger">{{ errorMessage }}</div>
          <template v-else-if="card">

            <!-- Icon + Title -->
            <div class="mb-3">
              <div v-if="cardIcon" class="mb-2" style="font-size: 3rem; line-height: 1;">{{ cardIcon }}</div>
              <div v-else class="mb-2 text-muted" style="font-size: 1.5rem; opacity:0.3;">
                <i class="bi bi-card-text"></i>
              </div>
              <textarea
                v-model="title"
                class="form-control border-0 shadow-none fw-bold p-0"
                style="font-size: 1.6rem; line-height: 1.3; resize: none; overflow: hidden; min-height: 2.5rem;"
                rows="1"
                placeholder="Untitled"
                @blur="saveTitle"
                @keydown.enter.prevent="saveTitle"
                @input="($event.target as HTMLTextAreaElement).style.height = 'auto'; ($event.target as HTMLTextAreaElement).style.height = ($event.target as HTMLTextAreaElement).scrollHeight + 'px'"
              ></textarea>
            </div>

            <!-- Properties -->
            <div class="mb-1">
              <PropertyValueElement
                v-for="property in boardProperties"
                :key="property.id"
                :label="property.name"
                :type="property.type as any"
                :options="property.options"
                :model-value="propertyValue(property.id)"
                @update:model-value="updateProperty(property.id, $event)"
              />
              <!-- + Adicionar propriedade -->
              <div class="dropdown mt-1">
                <button
                  type="button"
                  class="btn btn-sm btn-link text-muted text-decoration-none px-0"
                  style="font-size: 0.8125rem;"
                  data-bs-toggle="dropdown"
                >
                  <i class="bi bi-plus me-1"></i>Adicionar propriedade
                </button>
                <ul class="dropdown-menu" style="min-width: 220px;">
                  <li class="px-3 py-1">
                    <small class="text-muted fw-semibold text-uppercase" style="font-size: 0.7rem; letter-spacing: 0.05em;">
                      Selecione o tipo de propriedade
                    </small>
                  </li>
                  <li><hr class="dropdown-divider my-1"></li>
                  <li v-for="pt in PROPERTY_TYPES" :key="pt.value">
                    <button type="button" class="dropdown-item small" @click="addBoardProperty(pt.value)">
                      {{ pt.label }}
                    </button>
                  </li>
                </ul>
              </div>
            </div>

            <!-- Separator -->
            <hr class="my-3">

            <!-- Comments (before content blocks, as in original) -->
            <div class="mb-3">
              <!-- New comment input -->
              <div class="d-flex align-items-center gap-2 mb-3">
                <div
                  class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center flex-shrink-0"
                  style="width: 28px; height: 28px; font-size: 11px;"
                >
                  <i class="bi bi-person"></i>
                </div>
                <input
                  v-model="newComment"
                  type="text"
                  class="form-control form-control-sm border-0 border-bottom rounded-0 shadow-none px-0"
                  placeholder="Adicionar um comentário..."
                  style="background: transparent;"
                  @keydown.enter.prevent="addComment"
                />
              </div>
              <!-- Existing comments -->
              <div
                v-for="comment in comments"
                :key="comment.id"
                class="d-flex align-items-start gap-2 mb-2"
              >
                <div
                  class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center flex-shrink-0"
                  style="width: 28px; height: 28px; font-size: 11px;"
                >
                  {{ comment.createdBy?.slice(0, 2)?.toUpperCase() || "?" }}
                </div>
                <div class="small pt-1">{{ comment.title }}</div>
              </div>
            </div>

            <!-- Content blocks -->
            <div class="mb-2">
              <ContentRegistry
                :content="cardContents"
                editable
                @add-block="addBlock"
                @update-block="updateBlock"
                @toggle-checkbox="toggleCheckbox"
              />
            </div>

            <!-- + Adicionar conteúdo -->
            <div class="dropdown">
              <button
                type="button"
                class="btn btn-sm btn-outline-secondary"
                style="font-size: 0.8125rem;"
                data-bs-toggle="dropdown"
              >
                Adicionar conteúdo
              </button>
              <ul class="dropdown-menu">
                <li v-for="ct in CONTENT_TYPES" :key="ct.value">
                  <button type="button" class="dropdown-item small d-flex align-items-center gap-2" @click="addBlock(ct.value)">
                    <i :class="`bi ${ct.icon}`" style="width: 16px;"></i>{{ ct.label }}
                  </button>
                </li>
              </ul>
            </div>

          </template>
        </div>
      </div>
    </div>
    <div aria-live="polite" class="visually-hidden">{{ liveMessage }}</div>
  </div>
  <div class="modal-backdrop fade show" style="z-index:1050;" @click="emit('close')"></div>
  </Teleport>
</template>
