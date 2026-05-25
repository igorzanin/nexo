<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import * as api from "../api";

const router = useRouter();
const oldPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const error = ref("");
const success = ref("");
const loading = ref(false);

async function handleChange() {
  error.value = "";
  success.value = "";
  if (newPassword.value !== confirmPassword.value) {
    error.value = "Passwords do not match";
    return;
  }
  loading.value = true;
  try {
    const token = localStorage.getItem("access_token") || "";
    const payload = JSON.parse(atob(token.split(".")[1]));
    const userId = payload?.sub || "me";
    await api.changePassword(userId, oldPassword.value, newPassword.value);
    success.value = "Password changed successfully";
    setTimeout(() => router.push("/board"), 2000);
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Failed to change password";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="d-flex align-items-center justify-content-center vh-100 bg-body-secondary">
    <div class="card shadow" style="width: 400px;">
      <div class="card-body p-4">
        <h4 class="card-title text-center mb-4">Change Password</h4>
        <form @submit.prevent="handleChange">
          <div class="mb-3">
            <input v-model="oldPassword" type="password" class="form-control" placeholder="Current password" required />
          </div>
          <div class="mb-3">
            <input v-model="newPassword" type="password" class="form-control" placeholder="New password (min 8 chars)" required minlength="8" />
          </div>
          <div class="mb-3">
            <input v-model="confirmPassword" type="password" class="form-control" placeholder="Confirm new password" required />
          </div>
          <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>
          <div v-if="success" class="alert alert-success py-2 small">{{ success }}</div>
          <button type="submit" class="btn btn-primary w-100" :disabled="loading">
            {{ loading ? "Changing..." : "Change password" }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
