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
  <div class="comments-list">
    <strong class="small text-muted d-block mb-2">Comments</strong>

    <div v-if="comments.length === 0" class="text-muted small mb-3">
      No comments yet.
    </div>

    <div v-for="comment in comments" :key="comment.id" class="border-bottom py-2 mb-2">
      <div class="d-flex align-items-start gap-2">
        <span class="rounded-circle bg-secondary text-white d-inline-flex align-items-center justify-content-center" style="width: 24px; height: 24px; font-size: 10px; flex-shrink: 0;">
          {{ comment.fields?.createdBy?.charAt(0)?.toUpperCase() || "?" }}
        </span>
        <div>
          <div class="small">{{ comment.title }}</div>
          <div class="small text-muted" style="font-size: 10px;">
            {{ new Date(comment.createAt).toLocaleString() }}
          </div>
        </div>
      </div>
    </div>

    <div class="d-flex gap-2 mt-2">
      <input
        v-model="newComment"
        type="text"
        class="form-control form-control-sm"
        placeholder="Write a comment..."
        @keyup.enter="postComment"
      />
      <button class="btn btn-primary btn-sm" :disabled="!newComment.trim() || posting" @click="postComment">
        {{ posting ? "..." : "Post" }}
      </button>
    </div>
  </div>
</template>
