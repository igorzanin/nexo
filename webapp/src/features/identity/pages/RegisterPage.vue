<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import AuthLayout from "../../../shared/layouts/AuthLayout.vue";
import { useAuthStore } from "../stores/auth.store";

const router = useRouter();
const auth = useAuthStore();

const email = ref("");
const username = ref("");
const password = ref("");
const confirmPassword = ref("");
const localError = ref("");
const submitted = ref(false);

const errorMessage = computed(() => localError.value || auth.error);

async function handleSubmit() {
  localError.value = "";
  submitted.value = false;
  auth.clearError();

  if (password.value !== confirmPassword.value) {
    localError.value = "Passwords do not match";
    return;
  }

  try {
    await auth.register(username.value, email.value, password.value);
    submitted.value = true;
    router.push("/boards");
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
          <h1 class="h4 mb-0">Create an account</h1>
          <form class="vstack gap-3" @submit.prevent="handleSubmit">
            <div>
              <label for="register-email" class="form-label">Email</label>
              <input id="register-email" v-model="email" type="email" class="form-control" autocomplete="email" />
            </div>
            <div>
              <label for="register-username" class="form-label">Username</label>
              <input id="register-username" v-model="username" type="text" class="form-control" autocomplete="username" />
            </div>
            <div>
              <label for="register-password" class="form-label">Password</label>
              <input id="register-password" v-model="password" type="password" class="form-control" autocomplete="new-password" />
            </div>
            <div>
              <label for="register-confirm-password" class="form-label">Confirm password</label>
              <input
                id="register-confirm-password"
                v-model="confirmPassword"
                type="password"
                class="form-control"
                autocomplete="new-password"
              />
            </div>
            <button type="submit" class="btn btn-primary w-100" :disabled="auth.loading">
              {{ auth.loading ? "Creating account..." : "Create account" }}
            </button>
            <div v-if="errorMessage" class="alert alert-danger mb-0">{{ errorMessage }}</div>
            <div v-if="submitted" class="visually-hidden" aria-live="polite">Redirecting...</div>
          </form>
          <button type="button" class="btn btn-link p-0 align-self-start" @click="router.push('/login')">
            Log in
          </button>
        </div>
      </div>
    </div>
  </AuthLayout>
</template>
