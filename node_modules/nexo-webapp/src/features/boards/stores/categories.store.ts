/**
 * features/boards/stores/categories.store.ts
 * Store Pinia para categorias de board (feature-scoped).
 * Wrap sobre sidebarStore com API de categorias exposta.
 */
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import http from "../../../shared/api/client";
import type { Category, CategoryBoards } from "../../../types/category";

export const useCategoriesStore = defineStore("boards/categories", () => {
  const categories = ref<CategoryBoards[]>([]);
  const loading = ref(false);
  const error = ref("");

  const sortedCategories = computed(() =>
    [...categories.value].sort((a, b) => a.sortOrder - b.sortOrder)
  );

  async function fetchCategories(teamId: string): Promise<void> {
    loading.value = true;
    error.value = "";
    try {
      const res = await http.get<Category[]>(`/teams/${teamId}/categories`);
      categories.value = res.data.map((cat) => ({
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
    } catch (e: any) {
      error.value = e.response?.data?.detail || "Failed to load categories";
    } finally {
      loading.value = false;
    }
  }

  async function createCategory(teamId: string, name: string): Promise<void> {
    const res = await http.post<Category>(`/teams/${teamId}/categories`, { name });
    categories.value.push({ ...res.data, boardMetadata: [] });
  }

  async function renameCategory(teamId: string, categoryId: string, name: string): Promise<void> {
    await http.put(`/teams/${teamId}/categories/${categoryId}`, { name });
    const cat = categories.value.find((c) => c.id === categoryId);
    if (cat) cat.name = name;
  }

  async function deleteCategory(teamId: string, categoryId: string): Promise<void> {
    await http.delete(`/teams/${teamId}/categories/${categoryId}`);
    categories.value = categories.value.filter((c) => c.id !== categoryId);
  }

  async function moveBoardToCategory(
    teamId: string,
    categoryId: string,
    boardId: string
  ): Promise<void> {
    await http.post(`/teams/${teamId}/categories/${categoryId}/boards/${boardId}`);
  }

  return {
    categories, sortedCategories, loading, error,
    fetchCategories, createCategory, renameCategory, deleteCategory, moveBoardToCategory,
  };
});
