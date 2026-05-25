import { defineStore } from "pinia";
import { ref } from "vue";
import api from "../api/client";

export interface ClientConfig {
  telemetry: boolean;
  enablePublicSharedBoards: boolean;
  [key: string]: unknown;
}

export const useConfigStore = defineStore("config", () => {
  const value = ref<ClientConfig>({
    telemetry: false,
    enablePublicSharedBoards: false,
  });

  async function fetchConfig() {
    try {
      const res = await api.get("/clientConfig");
      value.value = res.data;
    } catch {
      // use defaults
    }
  }

  function setConfig(config: Partial<ClientConfig>) {
    value.value = { ...value.value, ...config };
  }

  return { value, fetchConfig, setConfig };
});
