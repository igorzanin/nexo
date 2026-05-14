import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { Block } from "../types/block";
import { CONTENT_BLOCK_TYPES } from "../types/contentBlock";

export const useContentStore = defineStore("contents", () => {
  const contents = ref<Record<string, Block>>({});

  const contentList = computed(() => Object.values(contents.value));

  const contentsByCard = computed(() => {
    const map: Record<string, Block[]> = {};
    for (const content of contentList.value) {
      const parentId = content.parentId;
      if (!map[parentId]) map[parentId] = [];
      map[parentId].push(content);
    }
    return map;
  });

  function setContent(content: Block) {
    contents.value[content.id] = content;
  }

  function removeContent(contentId: string) {
    delete contents.value[contentId];
  }

  function setContentsFromBlocks(blocks: Block[]) {
    for (const block of blocks) {
      if (CONTENT_BLOCK_TYPES.includes(block.type as typeof CONTENT_BLOCK_TYPES[number])) {
        setContent(block);
      }
    }
  }

  return {
    contents, contentList, contentsByCard,
    setContent, removeContent, setContentsFromBlocks,
  };
});
