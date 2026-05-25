<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import AuthLayout from "../../../shared/layouts/AuthLayout.vue";
import { useAuthStore } from "../stores/auth.store";

const router = useRouter();
const route = useRoute();
const auth = useAuthStore();

const usernameOrEmail = ref("");
const password = ref("");
const submitted = ref(false);

const errorMessage = computed(() => auth.error);

async function handleSubmit() {
  submitted.value = false;
  auth.clearError();
  try {
    await auth.login(usernameOrEmail.value, password.value);
    submitted.value = true;
    const redirect = typeof route.query.r === "string" ? route.query.r : "/boards";
    router.push(redirect);
  } catch {
    submitted.value = false;
  }
}
</script>

<template>
  <AuthLayout>
    <div class="card shadow" style="width: 100%; max-width: 420px;">
      <div class="card-body p-4">
        <div class="vstack gap-3">
          <h1 class="h4 mb-0">Nexo</h1>
          <form class="vstack gap-3" @submit.prevent="handleSubmit">
            <div>
              <label for="login-username" class="form-label">Username</label>
              <input
                id="login-username"
                v-model="usernameOrEmail"
                type="text"
                class="form-control"
                placeholder="Enter username"
                autocomplete="username"
              />
            </div>
            <div>
              <label for="login-password" class="form-label">Password</label>
              <input
                id="login-password"
                v-model="password"
                type="password"
                class="form-control"
                placeholder="Enter password"
                autocomplete="current-password"
              />
            </div>
            <button type="submit" class="btn btn-primary w-100" :disabled="auth.loading">
              {{ auth.loading ? "Logging in..." : "Log in" }}
            </button>
            <div v-if="errorMessage" class="alert alert-danger mb-0">{{ errorMessage }}</div>
            <div v-if="submitted" class="visually-hidden" aria-live="polite">Redirecting...</div>
          </form>
          <button type="button" class="btn btn-link p-0 align-self-start" @click="router.push('/register')">
            create an account
          </button>
        </div>
      </div>
    </div>
  </AuthLayout>
</template>
