import { Block, BlockPatch, createBlock } from "./block";
import { clone, currentTimestamp } from "./utils";

export type BoardType = "O" | "P";
export type MemberRole = "" | "viewer" | "commenter" | "editor" | "admin";

export interface IPropertyOption {
  id: string;
  value: string;
  color: string;
}

export interface IPropertyTemplate {
  id: string;
  name: string;
  type: string;
  options: IPropertyOption[];
}

export interface Board {
  id: string;
  teamId: string;
  channelId: string;
  type: BoardType;
  title: string;
  description: string;
  icon: string;
  showDescription: boolean;
  isTemplate: boolean;
  templateVersion: number;
  minimumRole: MemberRole;
  cardProperties: IPropertyTemplate[];
  createAt: number;
  updateAt: number;
  deleteAt: number;
}

export interface BoardPatch {
  type?: BoardType;
  title?: string;
  description?: string;
  icon?: string;
  showDescription?: boolean;
  minimumRole?: MemberRole;
  channelId?: string;
}

export interface BoardMember {
  boardId: string;
  userId: string;
  minimumRole: MemberRole;
  schemeAdmin: boolean;
  schemeEditor: boolean;
  schemeCommenter: boolean;
  schemeViewer: boolean;
}

export function createBoard(partial?: Partial<Board>): Board {
  const now = currentTimestamp();
  return {
    id: partial?.id ?? "",
    teamId: partial?.teamId ?? "",
    channelId: partial?.channelId ?? "",
    type: partial?.type ?? "P",
    title: partial?.title ?? "",
    description: partial?.description ?? "",
    icon: partial?.icon ?? "",
    showDescription: partial?.showDescription ?? false,
    isTemplate: partial?.isTemplate ?? false,
    templateVersion: partial?.templateVersion ?? 0,
    minimumRole: partial?.minimumRole ?? "",
    cardProperties: partial?.cardProperties ?? [],
    createAt: partial?.createAt ?? now,
    updateAt: partial?.updateAt ?? now,
    deleteAt: partial?.deleteAt ?? 0,
  };
}

export interface BoardsAndBlocks {
  boards: Board[];
  blocks: Block[];
}

export function createPatchesFromBoards(
  oldBoards: Board[],
  newBoards: Board[]
): { updatePatch: BoardPatch[]; undoPatch: BoardPatch[] } {
  const updatePatches: BoardPatch[] = [];
  const undoPatches: BoardPatch[] = [];

  for (const newBoard of newBoards) {
    const oldBoard = oldBoards.find((b) => b.id === newBoard.id);
    if (oldBoard) {
      const updatePatch: BoardPatch = {};
      const undoPatch: BoardPatch = {};

      for (const key of ["title", "description", "icon", "showDescription", "minimumRole", "type", "channelId"] as const) {
        if (newBoard[key] !== oldBoard[key]) {
          (updatePatch as Record<string, unknown>)[key] = newBoard[key];
          (undoPatch as Record<string, unknown>)[key] = oldBoard[key];
        }
      }

      if (Object.keys(updatePatch).length > 0) {
        updatePatches.push(updatePatch);
        undoPatches.push(undoPatch);
      }
    }
  }

  return { updatePatch: updatePatches, undoPatch: undoPatches };
}

export function createCardPropertiesPatches(
  oldProps: IPropertyTemplate[],
  newProps: IPropertyTemplate[]
): { updatePatch: { cardProperties: IPropertyTemplate[] }; undoPatch: { cardProperties: IPropertyTemplate[] } } {
  return {
    updatePatch: { cardProperties: clone(newProps) },
    undoPatch: { cardProperties: clone(oldProps) },
  };
}
