<!-- features/identity/pages/UserPreferencesPage.vue -->
<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import AppLayout from "../../../shared/layouts/AppLayout.vue";
import BaseButton from "../../../shared/components/BaseButton.vue";
import { useUserStore } from "../../../stores/userStore";
import { useConfigStore } from "../../../stores/configStore";

const router = useRouter();
const userStore = useUserStore();
const configStore = useConfigStore();

const theme = ref((configStore as any).theme || "default");
const language = ref((configStore as any).language || "en");
const success = ref("");

async function save() {
  (configStore as any).theme = theme.value;
  (configStore as any).language = language.value;
  success.value = "Preferences saved";
  setTimeout(() => (success.value = ""), 2500);
}
</script>

<template>
  <AppLayout>
    <div class="container-fluid p-4" style="max-width: 600px;">
      <h5 class="mb-4">User Preferences</h5>

      <div class="mb-3">
        <label class="form-label fw-semibold small">Username</label>
        <p class="form-control-plaintext small">{{ userStore.me?.username }}</p>
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold small">Email</label>
        <p class="form-control-plaintext small">{{ userStore.me?.email }}</p>
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold small">Theme</label>
        <select v-model="theme" class="form-select form-select-sm">
          <option value="default">Default</option>
          <option value="dark">Dark</option>
          <option value="light">Light</option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold small">Language</label>
        <select v-model="language" class="form-select form-select-sm">
          <option value="en">English</option>
          <option value="pt">Português</option>
          <option value="es">Español</option>
        </select>
      </div>

      <div v-if="success" class="alert alert-success py-2 small">{{ success }}</div>

      <div class="d-flex gap-2">
        <BaseButton type="button" @click="save">Save</BaseButton>
        <BaseButton variant="outline-secondary" type="button" @click="router.push('/board')">Cancel</BaseButton>
      </div>
    </div>
  </AppLayout>
</template>
