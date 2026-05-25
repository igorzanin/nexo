/**
 * shared/api/useMutator.ts
 * Borda única de mutações do frontend (ADR-008 / BR-MIGRAR-012).
 * Componentes não chamam API diretamente — usam este composable.
 */
import { useBoardStore, useCardStore, useViewStore } from "../../stores";
import * as api from "../../api";
import { createBlock } from "../../types/block";
import type { Block, BlockPatch } from "../../types/block";
import type { Board, BoardPatch } from "../../types/board";

export function useMutator() {
  const boardStore = useBoardStore();
  const cardStore = useCardStore();
  const viewStore = useViewStore();

  async function insertBlock(board: Board, partial?: Partial<Block>): Promise<Block> {
    const block = createBlock({ boardId: board.id, ...partial });
    const created = await api.createBlock(board.id, block);
    if (created.type === "card") {
      cardStore.setCard(created);
    } else if (created.type === "view") {
      viewStore.setView(created as any);
    }
    return created;
  }

  async function patchBlock(boardId: string, blockId: string, patch: BlockPatch, undoPatch: BlockPatch) {
    const updated = await api.patchBlock(boardId, blockId, patch);
    return { updated, undoPatch };
  }

  async function deleteBlock(boardId: string, blockId: string) {
    await api.deleteBlock(boardId, blockId);
    cardStore.removeCard(blockId);
    viewStore.removeView(blockId);
  }

  async function patchBoard(boardId: string, patch: BoardPatch, undoPatch: BoardPatch) {
    const updated = await api.patchBoard(boardId, patch);
    boardStore.setBoard(updated);
    return { updated, undoPatch };
  }

  return { insertBlock, patchBlock, deleteBlock, patchBoard };
}
