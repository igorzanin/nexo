<script setup lang="ts">
import http from "../../../shared/api/client";
import { useBoardsStore } from "../stores/boards.store";

const props = defineProps<{
  boardId?: string;
}>();

const boardsStore = useBoardsStore();

function downloadFile(data: BlobPart, fileName: string) {
  const blob = new Blob([data]);
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = fileName;
  link.click();
  URL.revokeObjectURL(url);
}

async function exportCsv() {
  const boardId = props.boardId || boardsStore.current;
  if (!boardId) return;
  const response = await http.get(`/boards/${boardId}/export/csv`, { responseType: "blob" });
  downloadFile(response.data, `board-${boardId}.csv`);
}

async function exportArchive() {
  const boardId = props.boardId || boardsStore.current;
  if (!boardId) return;
  const response = await http.get(`/boards/${boardId}/export/archive`, { responseType: "blob" });
  downloadFile(response.data, `board-${boardId}.boardarchive`);
}
</script>

<template>
  <div class="dropdown">
    <button type="button" class="btn btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">...</button>
    <ul class="dropdown-menu">
      <li><button type="button" class="dropdown-item" @click="exportCsv">Export to CSV</button></li>
      <li><button type="button" class="dropdown-item" @click="exportArchive">Export Archive (.boardarchive)</button></li>
    </ul>
  </div>
</template>
