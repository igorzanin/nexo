<script setup lang="ts">
import { ref, computed } from "vue";
import { useCommentStore } from "../../stores";
import { useMutator } from "../../composables/useMutator";
import { useFlashMessage } from "../../composables/useFlashMessage";
import * as api from "../../api";

const props = defineProps<{
  cardId: string;
  boardId: string;
}>();

const commentStore = useCommentStore();
const mutator = useMutator();
const { show } = useFlashMessage();
const newComment = ref("");
const posting = ref(false);

const comments = computed(() =>
  Object.values(commentStore.comments).filter((c) => c.parentId === props.cardId)
);

async function postComment() {
  if (!newComment.value.trim() || posting.value) return;
  posting.value = true;
  try {
    await mutator.insertBlock(
      { id: props.boardId } as any,
      { type: "comment", title: newComment.value.trim(), parentId: props.cardId, boardId: props.boardId }
    );
    newComment.value = "";
    const blocks = await api.getBlocks(props.boardId).catch(() => []);
    commentStore.setCommentsFromBlocks(blocks);
  } catch (e: any) {
    show(e.response?.data?.detail || "Failed to post comment", "error");
  } finally {
    posting.value = false;
  }
}
</script>

<template>
  <div class="comments-section">
    <div v-for="comment in comments" :key="comment.id" class="d-flex gap-2 mb-3">
      <span class="avatar-circle flex-shrink-0">
        {{ comment.fields?.createdBy?.charAt(0)?.toUpperCase() || "?" }}
      </span>
      <div>
        <span class="fw-semibold small me-2">{{ comment.fields?.createdBy || "?" }}</span>
        <span class="text-muted small">{{ new Date(comment.createAt).toLocaleString() }}</span>
        <div class="small mt-1">{{ comment.title }}</div>
      </div>
    </div>

    <div class="d-flex gap-2 align-items-center mt-1">
      <span class="avatar-circle flex-shrink-0">?</span>
      <input
        v-model="newComment"
        type="text"
        class="form-control form-control-sm border-0 bg-body-secondary rounded-pill"
        placeholder="Adicionar um comentário..."
        @keyup.enter="postComment"
      />
    </div>
  </div>
</template>

<style scoped>
.avatar-circle {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background-color: var(--bs-secondary);
  color: white;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
}
</style>
