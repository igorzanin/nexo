<script setup lang="ts">
// features/boards/pages/TeamSettingsPage.vue
// Configurações do time: renomear, token de convite, deletar.
import { ref, onMounted } from "vue";
import AppLayout from "../../../shared/layouts/AppLayout.vue";
import http from "../../../shared/api/client";
import { useTeamsStore } from "../stores/teams.store";

const teamStore = useTeamsStore();

const teamName = ref("");
const signupToken = ref("");
const loading = ref(false);
const saving = ref(false);
const error = ref("");
const success = ref("");

onMounted(async () => {
  loading.value = true;
  try {
    if (!teamStore.currentId) await teamStore.fetchTeams();
    if (teamStore.currentTeam) {
      teamName.value = teamStore.currentTeam.title;
      signupToken.value = teamStore.currentTeam.signupToken || "";
    }
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Failed to load team settings";
  } finally {
    loading.value = false;
  }
});

async function saveSettings() {
  if (!teamName.value.trim()) {
    error.value = "Team name cannot be empty.";
    return;
  }
  saving.value = true;
  error.value = "";
  success.value = "";
  try {
    const res = await http.patch(`/teams/${teamStore.currentId}`, {
      title: teamName.value.trim(),
      signup_token: signupToken.value,
    });
    teamStore.setCurrent(teamStore.currentId);
    if (teamStore.allTeams) {
      const idx = teamStore.allTeams.findIndex((t) => t.id === teamStore.currentId);
      if (idx !== -1) {
        teamStore.allTeams[idx] = res.data;
        teamStore.setCurrent(res.data.id);
      }
    }
    success.value = "Settings saved.";
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Failed to save settings";
  } finally {
    saving.value = false;
  }
}

function regenerateToken() {
  signupToken.value = crypto.randomUUID();
}
</script>

<template>
  <AppLayout>
    <div class="container py-4" style="max-width: 560px;">
      <h4 class="mb-4">Team Settings</h4>

      <div v-if="loading" class="text-center text-muted py-5">
        <div class="spinner-border spinner-border-sm me-2"></div>
        Loading…
      </div>

      <form v-else @submit.prevent="saveSettings">
        <div v-if="error" class="alert alert-danger mb-3">{{ error }}</div>
        <div v-if="success" class="alert alert-success mb-3">{{ success }}</div>

        <div class="mb-3">
          <label class="form-label fw-semibold">Team name</label>
          <input
            v-model="teamName"
            type="text"
            class="form-control"
            :disabled="saving"
          />
        </div>

        <div class="mb-4">
          <label class="form-label fw-semibold">Signup token</label>
          <div class="input-group">
            <input
              v-model="signupToken"
              type="text"
              class="form-control font-monospace small"
              readonly
            />
            <button
              type="button"
              class="btn btn-outline-secondary"
              @click="regenerateToken"
            >
              Regenerate
            </button>
          </div>
          <div class="form-text">Share this token with users you want to invite to the team.</div>
        </div>

        <button
          type="submit"
          class="btn btn-primary"
          :disabled="saving"
        >
          <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
          Save settings
        </button>
      </form>
    </div>
  </AppLayout>
</template>
