<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import AuthLayout from "../../../shared/layouts/AuthLayout.vue";
import { useAuthStore } from "../stores/auth.store";

const router = useRouter();
const auth = useAuthStore();

const currentPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const localError = ref("");
const success = ref(false);

const errorMessage = computed(() => localError.value || auth.error);

async function handleSubmit() {
  localError.value = "";
  success.value = false;
  auth.clearError();

  if (newPassword.value !== confirmPassword.value) {
    localError.value = "Passwords do not match";
    return;
  }

  try {
    await auth.changePassword(currentPassword.value, newPassword.value);
    success.value = true;
  } catch {
    success.value = false;
  }
}

function handleCancel() {
  router.back();
}
</script>

<template>
  <AuthLayout>
    <div class="card shadow" style="width: 100%; max-width: 420px;">
      <div class="card-body p-4">
        <div class="vstack gap-3">
          <h1 class="h4 mb-0">Change password</h1>
          <form class="vstack gap-3" @submit.prevent="handleSubmit">
            <div>
              <label for="current-password" class="form-label">Current password</label>
              <input
                id="current-password"
                v-model="currentPassword"
                type="password"
                class="form-control"
                autocomplete="current-password"
              />
            </div>
            <div>
              <label for="new-password" class="form-label">New password</label>
              <input id="new-password" v-model="newPassword" type="password" class="form-control" autocomplete="new-password" />
            </div>
            <div>
              <label for="confirm-new-password" class="form-label">Confirm new password</label>
              <input
                id="confirm-new-password"
                v-model="confirmPassword"
                type="password"
                class="form-control"
                autocomplete="new-password"
              />
            </div>
            <div class="btn-group">
              <button type="button" class="btn btn-outline-secondary" :disabled="auth.loading" @click="handleCancel">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary" :disabled="auth.loading">
                {{ auth.loading ? "Changing password..." : "Change password" }}
              </button>
            </div>
            <div v-if="errorMessage" class="alert alert-danger mb-0">{{ errorMessage }}</div>
            <div v-if="success" class="alert alert-success mb-0">Password changed successfully.</div>
          </form>
        </div>
      </div>
    </div>
  </AuthLayout>
</template>
