<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import * as api from "../api";

const router = useRouter();

const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const error = ref("");
const loading = ref(false);

async function handleRegister() {
  error.value = "";
  if (password.value !== confirmPassword.value) {
    error.value = "Passwords do not match";
    return;
  }
  loading.value = true;
  try {
    const res = await api.register(username.value, email.value, password.value);
    localStorage.setItem("access_token", res.access_token);
    localStorage.setItem("refresh_token", res.refresh_token);
    router.push("/board");
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Registration failed";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="d-flex align-items-center justify-content-center vh-100 bg-light">
    <div class="card shadow" style="width: 400px;">
      <div class="card-body p-4">
        <h4 class="card-title text-center mb-4">Create Account</h4>
        <form @submit.prevent="handleRegister">
          <div class="mb-3">
            <input v-model="username" type="text" class="form-control" placeholder="Username" required />
          </div>
          <div class="mb-3">
            <input v-model="email" type="email" class="form-control" placeholder="Email" required />
          </div>
          <div class="mb-3">
            <input v-model="password" type="password" class="form-control" placeholder="Password (min 8 chars)" required minlength="8" />
          </div>
          <div class="mb-3">
            <input v-model="confirmPassword" type="password" class="form-control" placeholder="Confirm password" required />
          </div>
          <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>
          <button type="submit" class="btn btn-primary w-100" :disabled="loading">
            {{ loading ? "Creating..." : "Create account" }}
          </button>
          <div class="text-center mt-3 small">
            <router-link to="/login">Already have an account? Sign in</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
