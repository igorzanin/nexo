import { clone, currentTimestamp, generateId } from "./utils";

export interface Block {
  id: string;
  boardId: string;
  parentId: string;
  createdBy: string;
  modifiedBy: string;
  schema: number;
  type: string;
  title: string;
  fields: Record<string, unknown>;
  createAt: number;
  updateAt: number;
  deleteAt: number;
}

export interface BlockPatch {
  parentId?: string;
  schema?: number;
  type?: string;
  title?: string;
  fields?: Record<string, unknown>;
}

export interface BlockPatchBatch {
  blockIds: string[];
  blockPatches: BlockPatch[];
}

export function createBlock(partial?: Partial<Block>): Block {
  const now = currentTimestamp();
  return {
    id: partial?.id ?? generateId(),
    boardId: partial?.boardId ?? "",
    parentId: partial?.parentId ?? "",
    createdBy: partial?.createdBy ?? "",
    modifiedBy: partial?.modifiedBy ?? "",
    schema: partial?.schema ?? 1,
    type: partial?.type ?? "unknown",
    title: partial?.title ?? "",
    fields: partial?.fields ?? {},
    createAt: partial?.createAt ?? now,
    updateAt: partial?.updateAt ?? now,
    deleteAt: partial?.deleteAt ?? 0,
  };
}

export interface Patches<T> {
  updatePatch: T;
  undoPatch: T;
}

export function createPatchesFromBlocks(
  oldBlocks: Block[],
  newBlocks: Block[]
): Patches<BlockPatch[]> {
  const updatePatches: BlockPatch[] = [];
  const undoPatches: BlockPatch[] = [];

  for (const newBlock of newBlocks) {
    const oldBlock = oldBlocks.find((b) => b.id === newBlock.id);
    if (oldBlock) {
      const updatePatch: BlockPatch = {};
      const undoPatch: BlockPatch = {};

      for (const key of ["title", "type", "schema"] as const) {
        if (newBlock[key] !== oldBlock[key]) {
          (updatePatch as Record<string, unknown>)[key] = newBlock[key];
          (undoPatch as Record<string, unknown>)[key] = oldBlock[key];
        }
      }
      if (JSON.stringify(newBlock.fields) !== JSON.stringify(oldBlock.fields)) {
        updatePatch.fields = clone(newBlock.fields);
        undoPatch.fields = clone(oldBlock.fields);
      }

      if (Object.keys(updatePatch).length > 0) {
        updatePatches.push(updatePatch);
        undoPatches.push(undoPatch);
      }
    }
  }

  return { updatePatch: updatePatches, undoPatch: undoPatches };
}
