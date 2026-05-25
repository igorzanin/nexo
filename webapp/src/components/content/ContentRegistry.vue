<script setup lang="ts">
import { ref } from "vue";
import type { Block } from "../../types/block";
import * as api from "../../api";

const props = defineProps<{
  block: Block;
  boardId: string;
}>();

const editingText = ref(false);
const editValue = ref("");

function startEdit() {
  editValue.value = props.block.title || "";
  editingText.value = true;
}

async function saveText() {
  editingText.value = false;
  if (editValue.value === props.block.title) return;
  try {
    await api.patchBlock(props.boardId, props.block.id, { title: editValue.value });
    props.block.title = editValue.value;
  } catch {}
}

async function toggleCheckbox() {
  const checked = !(props.block.fields?.checked as boolean);
  try {
    await api.patchBlock(props.boardId, props.block.id, {
      fields: { ...props.block.fields, checked },
    });
    if (props.block.fields) props.block.fields.checked = checked;
  } catch {}
}
</script>

<template>
  <div class="content-element py-1">
    <template v-if="block.type === 'text'">
      <div v-if="!editingText" class="content-text small" @click="startEdit">
        <span v-if="block.title">{{ block.title }}</span>
        <span v-else class="text-muted fst-italic">Clique para adicionar texto...</span>
      </div>
      <textarea
        v-else
        v-model="editValue"
        class="form-control form-control-sm"
        rows="3"
        autofocus
        @blur="saveText"
        @keyup.escape="editingText = false"
      />
    </template>

    <div v-else-if="block.type === 'image'">
      <img v-if="block.title" :src="block.title" alt="image" class="img-fluid rounded" style="max-height: 300px;" />
      <div v-else class="text-muted small fst-italic border rounded p-3 text-center">
        <i class="bi bi-image me-1"></i>Imagem não disponível
      </div>
    </div>

    <hr v-else-if="block.type === 'divider'" />

    <div v-else-if="block.type === 'checkbox'" class="d-flex align-items-center gap-2">
      <input
        type="checkbox"
        class="form-check-input mt-0 flex-shrink-0"
        style="cursor:pointer;"
        :checked="block.fields?.checked as boolean"
        @change="toggleCheckbox"
      />
      <template v-if="editingText">
        <input
          v-model="editValue"
          type="text"
          class="form-control form-control-sm border-0 p-0"
          style="font-size: 14px;"
          autofocus
          @blur="saveText"
          @keyup.enter="saveText"
          @keyup.escape="editingText = false"
        />
      </template>
      <span
        v-else
        class="small checkbox-label"
        :class="{ 'text-decoration-line-through text-muted': block.fields?.checked }"
        @click="startEdit"
      >
        {{ block.title || 'Item de lista' }}
      </span>
    </div>

    <div v-else-if="block.type === 'attachment'">
      <a :href="block.title" target="_blank" class="btn btn-sm btn-outline-secondary">
        📎 {{ block.title }}
      </a>
    </div>

    <div v-else-if="['h1', 'h2', 'h3'].includes(block.type)" :class="`fs-${block.type.slice(1)}`">
      {{ block.title }}
    </div>

    <div v-else class="text-muted small">
      {{ block.type }}: {{ block.title }}
    </div>
  </div>
</template>

<style scoped>
.content-text {
  min-height: 24px;
  padding: 4px 6px;
  border-radius: 4px;
  cursor: text;
  white-space: pre-wrap;
  word-break: break-word;
}
.content-text:hover {
  background-color: var(--bs-secondary-bg);
}
.checkbox-label {
  cursor: text;
  flex: 1;
  min-height: 20px;
}
.checkbox-label:hover {
  text-decoration: underline dotted;
}
</style>
