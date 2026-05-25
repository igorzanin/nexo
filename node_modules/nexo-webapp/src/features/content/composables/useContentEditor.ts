/**
 * useContentEditor — composable for editing card content blocks.
 * Content blocks (text, image, etc.) are managed through the API and
 * reflected in the global contentStore.
 */
import type { Ref } from "vue";
import type { Block, BlockPatch } from "../../../types/block";
import { createContentBlock, type ContentBlockType } from "../../../types/contentBlock";
import { useContentStore } from "../../../stores/contentStore";
import * as api from "../../../api";

export function useContentEditor(boardId: Ref<string>, cardId: Ref<string>) {
  const contentStore = useContentStore();

  async function addBlock(type: ContentBlockType, title = ""): Promise<Block> {
    const block = createContentBlock(type, {
      boardId: boardId.value,
      parentId: cardId.value,
      title,
    });
    const created = await api.createBlock(boardId.value, block);
    contentStore.setContent(created);
    return created;
  }

  async function updateBlock(block: Block, patch: BlockPatch): Promise<void> {
    const updated = await api.patchBlock(boardId.value, block.id, patch);
    contentStore.setContent(updated);
  }

  async function deleteBlock(block: Block): Promise<void> {
    await api.deleteBlock(boardId.value, block.id);
    contentStore.removeContent(block.id);
  }

  return { addBlock, updateBlock, deleteBlock };
}
