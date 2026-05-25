<script setup lang="ts">
import { useRouter } from "vue-router";
import { useUserStore } from "../../stores";

defineProps<{
  username: string;
}>();

const router = useRouter();
const userStore = useUserStore();

function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  userStore.clearMe();
  router.push("/login");
}

function goToSettings() {
  router.push("/change_password");
}
</script>

<template>
  <div class="dropup">
    <button class="btn btn-outline-secondary btn-sm w-100 text-start d-flex align-items-center gap-2" data-bs-toggle="dropdown" aria-expanded="false">
      <span class="rounded-circle bg-secondary text-white d-inline-flex align-items-center justify-content-center flex-shrink-0" style="width: 20px; height: 20px; font-size: 11px;">
        {{ username.charAt(0).toUpperCase() || "?" }}
      </span>
      <span class="text-truncate small flex-grow-1">{{ username || "User" }}</span>
    </button>
    <ul class="dropdown-menu w-100">
      <li>
        <div class="dropdown-header small text-muted">Signed in as <strong>{{ username }}</strong></div>
      </li>
      <li><button class="dropdown-item" @click="goToSettings"><i class="bi bi-gear me-2"></i> Settings</button></li>
      <li><hr class="dropdown-divider"></li>
      <li><button class="dropdown-item text-danger" @click="logout"><i class="bi bi-box-arrow-right me-2"></i> Logout</button></li>
    </ul>
  </div>
</template>
