<script setup lang="ts">
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import * as api from "../api";
import { useUserStore } from "../stores";

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const username = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

async function handleLogin() {
  error.value = "";
  loading.value = true;
  try {
    const res = await api.login(username.value, password.value);
    localStorage.setItem("access_token", res.access_token);
    localStorage.setItem("refresh_token", res.refresh_token);
    userStore.setMe({ id: "", username: username.value, email: "", createAt: 0, updateAt: 0, deleteAt: 0 });
    const redirect = (route.query.r as string) || "/board";
    router.push(redirect);
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Invalid credentials";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="d-flex align-items-center justify-content-center vh-100 bg-body-secondary">
    <div class="card shadow" style="width: 400px;">
      <div class="card-body p-4">
        <h4 class="card-title text-center mb-4">Nexo</h4>
        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <input v-model="username" type="text" class="form-control" placeholder="Username or email" required />
          </div>
          <div class="mb-3">
            <input v-model="password" type="password" class="form-control" placeholder="Password" required />
          </div>
          <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>
          <button type="submit" class="btn btn-primary w-100" :disabled="loading">
            {{ loading ? "Signing in..." : "Sign in" }}
          </button>
          <div class="text-center mt-3 small">
            <router-link to="/register">Create account</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
