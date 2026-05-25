<template>
  <div class="block-history-panel">
    <h6 class="text-muted small mb-2">Block History</h6>

    <!-- Loading -->
    <div v-if="status === 'loading'" class="text-muted small">Loading history...</div>

    <!-- Error -->
    <div v-else-if="status === 'error'" class="alert alert-danger py-1 small">{{ errorMessage }}</div>

    <!-- History list -->
    <div v-else>
      <ul v-if="history.length" class="list-group list-group-flush">
        <li
          v-for="entry in history"
          :key="entry.id"
          class="list-group-item px-0"
        >
          <div class="d-flex justify-content-between align-items-start">
            <span class="small text-muted">{{ formatDate(entry.action_at) }}</span>
            <span class="badge bg-secondary small">{{ entry.action }}</span>
          </div>
          <p v-if="entry.title" class="mb-0 small text-truncate">{{ entry.title }}</p>
        </li>
      </ul>
      <p v-else class="text-muted small mb-0">No history available.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import client from "../../../shared/api/client";

interface HistoryEntry {
  id: string;
  block_id: string;
  action: string;
  action_at: number;
  title?: string;
  fields?: Record<string, unknown>;
}

const props = defineProps<{
  boardId: string;
  blockId: string;
}>();

const history = ref<HistoryEntry[]>([]);
const status = ref<"idle" | "loading" | "error">("loading");
const errorMessage = ref("");

async function load() {
  status.value = "loading";
  errorMessage.value = "";
  try {
    const res = await client.get(`/boards/${props.boardId}/blocks/${props.blockId}/history`);
    history.value = res.data ?? [];
    status.value = "idle";
  } catch (e: unknown) {
    errorMessage.value = e instanceof Error ? e.message : "Failed to load history";
    status.value = "error";
  }
}

onMounted(load);
watch(() => props.blockId, load);

function formatDate(ts: number): string {
  return new Date(ts).toLocaleString();
}
</script>
