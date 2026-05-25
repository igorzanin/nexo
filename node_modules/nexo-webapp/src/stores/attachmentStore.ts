import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { Block } from "../types/block";

export const useAttachmentStore = defineStore("attachments", () => {
  const attachments = ref<Record<string, Block>>({});

  const attachmentList = computed(() => Object.values(attachments.value));

  const attachmentsByCard = computed(() => {
    const map: Record<string, Block[]> = {};
    for (const att of attachmentList.value) {
      const parentId = att.parentId;
      if (!map[parentId]) map[parentId] = [];
      map[parentId].push(att);
    }
    return map;
  });

  function setAttachment(attachment: Block) {
    attachments.value[attachment.id] = attachment;
  }

  function removeAttachment(attachmentId: string) {
    delete attachments.value[attachmentId];
  }

  function setAttachmentsFromBlocks(blocks: Block[]) {
    for (const block of blocks) {
      if (block.type === "attachment") {
        setAttachment(block);
      }
    }
  }

  return {
    attachments, attachmentList, attachmentsByCard,
    setAttachment, removeAttachment, setAttachmentsFromBlocks,
  };
});
