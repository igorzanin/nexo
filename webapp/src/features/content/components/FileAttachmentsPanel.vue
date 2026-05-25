<template>
  <div class="file-attachments-panel">
    <h6 class="text-muted small mb-2">Attachments</h6>

    <!-- Loading -->
    <div v-if="filesStore.uploading" class="text-muted small">Uploading...</div>

    <!-- Error -->
    <div v-if="filesStore.error" class="alert alert-danger py-1 small">{{ filesStore.error }}</div>

    <!-- File list -->
    <ul class="list-group list-group-flush mb-2">
      <li
        v-for="file in cardFiles"
        :key="file.id"
        class="list-group-item px-0 d-flex align-items-center gap-2"
      >
        <i class="bi bi-paperclip text-muted" />
        <a
          :href="fileUrl(file)"
          target="_blank"
          rel="noopener noreferrer"
          class="text-truncate small flex-grow-1"
        >{{ fileName(file) }}</a>
        <button
          v-if="canEdit"
          type="button"
          class="btn btn-sm btn-link text-danger p-0"
          title="Delete"
          @click="deleteFile(file)"
        >
          <i class="bi bi-trash" />
        </button>
      </li>
      <li v-if="!cardFiles.length" class="list-group-item px-0 text-muted small">No attachments.</li>
    </ul>

    <!-- Upload control -->
    <div v-if="canEdit">
      <label class="btn btn-outline-secondary btn-sm w-100">
        <i class="bi bi-upload me-1" /> Upload file
        <input type="file" class="d-none" @change="onFileChange" />
      </label>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { Block } from "../../../types/block";
import { useFilesStore } from "../stores/files.store";

const props = defineProps<{
  boardId: string;
  cardId: string;
  canEdit?: boolean;
}>();

const filesStore = useFilesStore();

const cardFiles = computed(() => filesStore.filesByCard[props.cardId] ?? []);

function fileName(file: Block): string {
  return (file.fields?.originalName as string) ?? file.title ?? file.id;
}

function fileUrl(file: Block): string {
  return (file.fields?.url as string) ?? "#";
}

async function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  if (!file) return;
  await filesStore.uploadFile(props.boardId, props.cardId, file);
  input.value = "";
}

async function deleteFile(file: Block) {
  if (!confirm(`Delete "${fileName(file)}"?`)) return;
  await filesStore.deleteFile(props.boardId, file.id);
}
</script>
