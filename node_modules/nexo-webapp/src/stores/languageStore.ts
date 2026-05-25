import { defineStore } from "pinia";
import { ref } from "vue";

export const useLanguageStore = defineStore("language", () => {
  const value = ref(navigator.language?.startsWith("pt") ? "pt" : "en");

  function setLanguage(lang: string) {
    value.value = lang;
  }

  return { value, setLanguage };
});
