import { defineStore } from "pinia";
import { ref } from "vue";

export const useSearchStore = defineStore("search", () => {
  const value = ref("");

  function setSearch(text: string) {
    value.value = text;
  }

  function clearSearch() {
    value.value = "";
  }

  return { value, setSearch, clearSearch };
});
