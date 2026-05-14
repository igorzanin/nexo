import { ref } from "vue";
import { useBoardStore, useCardStore, useViewStore } from "../stores";
import * as api from "../api";
import { createBlock } from "../types/block";
import type { Block, BlockPatch } from "../types/block";
import type { Board, BoardPatch } from "../types/board";

interface UndoAction {
  type: "insert" | "patch" | "delete" | "boardPatch";
  boardId: string;
  blockId?: string;
  undoPatch?: BlockPatch;
  undoBoardPatch?: BoardPatch;
  timestamp: number;
}

export function useMutator() {
  const boardStore = useBoardStore();
  const cardStore = useCardStore();
  const viewStore = useViewStore();

  const undoStack = ref<UndoAction[]>([]);
  const maxUndo = 50;

  function pushUndo(action: UndoAction) {
    undoStack.value.push(action);
    if (undoStack.value.length > maxUndo) {
      undoStack.value.shift();
    }
  }

  function popUndo(): UndoAction | undefined {
    return undoStack.value.pop();
  }

  function canUndo(): boolean {
    return undoStack.value.length > 0;
  }

  async function insertBlock(board: Board, partial?: Partial<Block>): Promise<Block> {
    const block = createBlock({ boardId: board.id, ...partial });
    const isCard = partial?.type === "card" || block.type === "card";
    const created = isCard
      ? await api.createCard(board.id, block)
      : await api.createBlock(board.id, block);
    if (created.type === "card") {
      cardStore.setCard(created);
    } else if (created.type === "view") {
      viewStore.setView(created as any);
    }
    pushUndo({ type: "insert", boardId: board.id, blockId: created.id, timestamp: Date.now() });
    return created;
  }

  async function patchBlock(boardId: string, blockId: string, patch: BlockPatch, undoPatch: BlockPatch) {
    const updated = await api.patchBlock(boardId, blockId, patch);
    pushUndo({ type: "patch", boardId, blockId, undoPatch, timestamp: Date.now() });
    return { updated, undoPatch };
  }

  async function deleteBlock(boardId: string, blockId: string) {
    const block = cardStore.cards[blockId] || viewStore.views[blockId];
    const undoPatch: BlockPatch = block ? { title: block.title, type: block.type, fields: block.fields } : {};
    await api.deleteBlock(boardId, blockId);
    cardStore.removeCard(blockId);
    viewStore.removeView(blockId);
    pushUndo({ type: "delete", boardId, blockId, undoPatch, timestamp: Date.now() });
  }

  async function patchBoard(boardId: string, patch: BoardPatch, undoPatch: BoardPatch) {
    const updated = await api.patchBoard(boardId, patch);
    pushUndo({ type: "boardPatch", boardId, undoBoardPatch: undoPatch, timestamp: Date.now() });
    return { updated, undoPatch };
  }

  async function undo() {
    const action = popUndo();
    if (!action) return;
    try {
      if (action.type === "insert" && action.blockId) {
        await api.deleteBlock(action.boardId, action.blockId);
        cardStore.removeCard(action.blockId);
        viewStore.removeView(action.blockId);
      } else if (action.type === "patch" && action.blockId && action.undoPatch) {
        await api.patchBlock(action.boardId, action.blockId, action.undoPatch);
      } else if (action.type === "delete" && action.blockId && action.undoPatch) {
        const restored = await api.createBlock(action.boardId, {
          id: action.blockId, title: action.undoPatch.title || "", type: action.undoPatch.type || "unknown", fields: action.undoPatch.fields || {},
        } as any);
        if (restored.type === "card") cardStore.setCard(restored);
        if (restored.type === "view") viewStore.setView(restored as any);
      } else if (action.type === "boardPatch" && action.undoBoardPatch) {
        await api.patchBoard(action.boardId, action.undoBoardPatch);
      }
    } catch {
      // undo failed silently
    }
  }

  return { insertBlock, patchBlock, deleteBlock, patchBoard, undo, canUndo, undoStack };
}
