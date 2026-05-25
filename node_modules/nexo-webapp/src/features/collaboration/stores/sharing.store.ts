import { defineStore } from "pinia";
import { ref } from "vue";
import type { ISharing } from "../../../types/sharing";
import type { BoardMember } from "../../../types/board";
import * as api from "../../../api";

export const useSharingStore = defineStore("sharing", () => {
  const sharingByBoard = ref<Record<string, ISharing>>({});

  async function fetchSharing(boardId: string): Promise<ISharing> {
    const data = await api.getSharing(boardId);
    sharingByBoard.value[boardId] = data;
    return data;
  }

  async function updateSharing(
    boardId: string,
    enabled: boolean,
    token: string
  ): Promise<ISharing> {
    const data = await api.postSharing(boardId, { enabled, token });
    sharingByBoard.value[boardId] = data;
    return data;
  }

  return { sharingByBoard, fetchSharing, updateSharing };
});
