import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { ITeam } from "../types/team";
import * as api from "../api";

export const useTeamStore = defineStore("teams", () => {
  const currentId = ref("");
  const currentTeam = ref<ITeam | null>(null);
  const allTeams = ref<ITeam[]>([]);

  const current = computed(() => currentTeam.value);

  async function fetchTeams() {
    const data = await api.getTeams();
    allTeams.value = data;
    if (data.length > 0 && !currentId.value) {
      currentId.value = data[0].id;
      currentTeam.value = data[0];
    }
  }

  function setCurrent(teamId: string) {
    currentId.value = teamId;
    currentTeam.value = allTeams.value.find((t) => t.id === teamId) ?? null;
  }

  return {
    currentId, currentTeam, allTeams, current,
    fetchTeams, setCurrent,
  };
});
