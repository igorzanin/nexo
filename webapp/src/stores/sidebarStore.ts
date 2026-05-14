import { defineStore } from "pinia";
import { ref } from "vue";
import type { CategoryBoards } from "../types/category";
import * as api from "../api";

export const useSidebarStore = defineStore("sidebar", () => {
  const categoryAttributes = ref<CategoryBoards[]>([]);
  const hiddenBoardIDs = ref<string[]>([]);

  function setCategories(categories: CategoryBoards[]) {
    categoryAttributes.value = categories;
  }

  function hideBoard(boardId: string) {
    if (!hiddenBoardIDs.value.includes(boardId)) {
      hiddenBoardIDs.value.push(boardId);
    }
  }

  function showBoard(boardId: string) {
    hiddenBoardIDs.value = hiddenBoardIDs.value.filter((id) => id !== boardId);
  }

  async function fetchCategories(teamId: string) {
    const data = await api.getCategories(teamId);
    const mapped: CategoryBoards[] = data.map((cat) => ({
      id: cat.id,
      name: cat.name,
      userID: cat.userID,
      teamID: cat.teamID,
      createAt: cat.createAt,
      updateAt: cat.updateAt,
      deleteAt: cat.deleteAt,
      collapsed: cat.collapsed,
      sortOrder: cat.sortOrder,
      type: cat.type,
      boardMetadata: [],
    }));
    categoryAttributes.value = mapped;
  }

  return {
    categoryAttributes, hiddenBoardIDs,
    setCategories, hideBoard, showBoard, fetchCategories,
  };
});
