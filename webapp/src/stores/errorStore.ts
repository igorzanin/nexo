import { defineStore } from "pinia";
import { ref } from "vue";

export const useErrorStore = defineStore("error", () => {
  const value = ref("");

  function setError(msg: string) {
    value.value = msg;
  }

  function clearError() {
    value.value = "";
  }

  return { value, setError, clearError };
});
