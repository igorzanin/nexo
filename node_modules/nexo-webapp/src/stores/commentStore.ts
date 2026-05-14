import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { Block } from "../types/block";

export const useCommentStore = defineStore("comments", () => {
  const comments = ref<Record<string, Block>>({});

  const commentList = computed(() => Object.values(comments.value));

  const commentsByCard = computed(() => {
    const map: Record<string, Block[]> = {};
    for (const comment of commentList.value) {
      const parentId = comment.parentId;
      if (!map[parentId]) map[parentId] = [];
      map[parentId].push(comment);
    }
    return map;
  });

  function setComment(comment: Block) {
    comments.value[comment.id] = comment;
  }

  function removeComment(commentId: string) {
    delete comments.value[commentId];
  }

  function setCommentsFromBlocks(blocks: Block[]) {
    for (const block of blocks) {
      if (block.type === "comment") {
        setComment(block);
      }
    }
  }

  return {
    comments, commentList, commentsByCard,
    setComment, removeComment, setCommentsFromBlocks,
  };
});
