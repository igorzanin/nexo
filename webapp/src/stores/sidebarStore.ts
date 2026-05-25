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

  async function createCategory(teamId: string, name: string) {
    const cat = await api.createCategory(teamId, name);
    if (cat) {
      categoryAttributes.value.push({
        id: cat.id,
        name: cat.name,
        userID: cat.userID,
        teamID: cat.teamID,
        createAt: cat.createAt,
        updateAt: cat.updateAt,
        deleteAt: cat.deleteAt,
        collapsed: false,
        sortOrder: cat.sortOrder || 0,
        type: "custom",
        boardMetadata: [],
      });
    }
  }

  async function renameCategory(id: string, name: string) {
    await api.renameCategory(id, name);
    const cat = categoryAttributes.value.find((c) => c.id === id);
    if (cat) cat.name = name;
  }

  async function deleteCategory(id: string) {
    await api.deleteCategory(id);
    categoryAttributes.value = categoryAttributes.value.filter((c) => c.id !== id);
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
    setCategories, hideBoard, showBoard, fetchCategories, createCategory, renameCategory, deleteCategory,
  };
});
