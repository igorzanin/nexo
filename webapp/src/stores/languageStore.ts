import { defineStore } from "pinia";
import { ref } from "vue";

export const useLanguageStore = defineStore("language", () => {
  const value = ref<"en" | "pt-BR" | "es">(navigator.language?.startsWith("pt") ? "pt-BR" : "en");

  function setLanguage(lang: "en" | "pt-BR" | "es") {
    value.value = lang;
  }

  return { value, setLanguage };
});