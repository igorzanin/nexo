<template>
  <div class="comments-panel d-flex flex-column gap-3">
    <h6 class="fw-semibold mb-1">Comments</h6>

    <div v-if="status === 'loading'" class="text-center py-2">
      <div class="spinner-border spinner-border-sm text-secondary" />
    </div>
    <div v-else-if="status === 'error'" class="alert alert-danger py-2 small">{{ errorMessage }}</div>

    <div v-else class="d-flex flex-column gap-2">
      <div
        v-for="comment in comments"
        :key="comment.id"
        class="p-2 rounded border bg-body-secondary"
      >
        <div class="d-flex align-items-center justify-content-between mb-1">
          <span class="small fw-semibold text-primary">{{ comment.createdBy }}</span>
          <span class="small text-muted">{{ formatDate(comment.createAt) }}</span>
        </div>
        <p class="mb-0 small" style="white-space: pre-wrap;">{{ comment.title }}</p>
        <button
          v-if="comment.createdBy === currentUserId"
          type="button"
          class="btn btn-link btn-sm text-danger p-0 mt-1"
          @click="deleteComment(comment.id)"
        >
          Delete
        </button>
      </div>

      <div v-if="!comments.length" class="text-muted small">No comments yet.</div>
    </div>

    <!-- New comment form -->
    <div class="d-flex gap-2">
      <textarea
        v-model="newText"
        rows="2"
        placeholder="Write a comment…"
        class="form-control form-control-sm flex-grow-1"
        @keydown.ctrl.enter="submitComment"
      />
      <button
        type="button"
        class="btn btn-primary btn-sm align-self-end"
        :disabled="!newText.trim() || submitting"
        @click="submitComment"
      >
        <span v-if="submitting" class="spinner-border spinner-border-sm" />
        <span v-else>Send</span>
      </button>
    </div>
    <p class="text-muted" style="font-size: 0.75rem;">Ctrl+Enter to send</p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import type { Block } from "../../../types/block";
import { useWebSocket } from "../../../shared/ws/useWebSocket";
import { useUserStore } from "../../../stores/userStore";
import * as api from "../../../api";

const props = defineProps<{
  boardId: string;
  cardId: string;
}>();

const userStore = useUserStore();
const currentUserId = computed(() => userStore.me?.id ?? "");

const status = ref<"idle" | "loading" | "error">("loading");
const errorMessage = ref("");
const comments = ref<Block[]>([]);
const newText = ref("");
const submitting = ref(false);

const { onMessage } = useWebSocket();
let unsubWs: (() => void) | null = null;

function formatDate(ts: number): string {
  return new Date(ts).toLocaleString();
}

async function loadComments() {
  status.value = "loading";
  try {
    const blocks = await api.getBlocks(props.boardId);
    comments.value = blocks.filter(
      (b) => b.type === "comment" && b.parentId === props.cardId
    );
    status.value = "idle";
  } catch (e: unknown) {
    errorMessage.value = e instanceof Error ? e.message : "Failed to load";
    status.value = "error";
  }
}

async function submitComment() {
  const text = newText.value.trim();
  if (!text) return;
  submitting.value = true;
  try {
    const created = await api.createBlock(props.boardId, {
      type: "comment",
      parentId: props.cardId,
      boardId: props.boardId,
      title: text,
    });
    comments.value.push(created);
    newText.value = "";
  } finally {
    submitting.value = false;
  }
}

async function deleteComment(commentId: string) {
  await api.deleteBlock(props.boardId, commentId);
  comments.value = comments.value.filter((c) => c.id !== commentId);
}

onMounted(async () => {
  await loadComments();

  // Listen for real-time block updates via WS
  unsubWs = onMessage((data) => {
    const msg = data as { action?: string; block?: Block };
    if (!msg.block || msg.block.type !== "comment") return;
    if (msg.block.parentId !== props.cardId) return;

    if (msg.action === "UPDATE_BLOCK") {
      const idx = comments.value.findIndex((c) => c.id === msg.block!.id);
      if (idx >= 0) comments.value[idx] = msg.block;
      else comments.value.push(msg.block);
    } else if (msg.action === "DELETE_BLOCK") {
      comments.value = comments.value.filter((c) => c.id !== msg.block!.id);
    }
  });
});

onUnmounted(() => {
  unsubWs?.();
});
</script>
