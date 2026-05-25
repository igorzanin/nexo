import { defineStore } from "pinia";
import { ref } from "vue";
import type { Board } from "../types/board";

export const useTemplateStore = defineStore("templates", () => {
  const value = ref<Board[]>([]);

  function setTemplates(templates: Board[]) {
    value.value = templates;
  }

  return { value, setTemplates };
});
