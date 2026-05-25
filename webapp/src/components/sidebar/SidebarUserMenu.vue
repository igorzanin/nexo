<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "../../stores";

const props = defineProps<{
  username: string;
}>();

const router = useRouter();
const userStore = useUserStore();
const isOpen = ref(false);

function toggle() {
  isOpen.value = !isOpen.value;
}

function logout() {
  isOpen.value = false;
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  userStore.clearMe();
  router.push("/login");
}

function goToSettings() {
  isOpen.value = false;
  router.push("/change_password");
}
</script>

<template>
  <div class="position-relative">
    <button class="btn btn-outline-secondary btn-sm w-100 text-start d-flex align-items-center gap-2" @click="toggle">
      <span class="rounded-circle bg-secondary text-white d-inline-flex align-items-center justify-content-center" style="width: 20px; height: 20px; font-size: 11px;">
        {{ username.charAt(0).toUpperCase() || "?" }}
      </span>
      <span class="text-truncate small flex-grow-1">{{ username || "User" }}</span>
      <i class="bi" :class="isOpen ? 'bi-chevron-down' : 'bi-chevron-up'" style="font-size: 10px;"></i>
    </button>
    <div v-if="isOpen" class="position-absolute bottom-100 start-0 w-100 p-1" style="z-index: 10;">
      <div class="bg-white border rounded shadow-sm">
        <div class="px-3 py-2 small text-muted border-bottom">
          Signed in as <strong>{{ username }}</strong>
        </div>
        <button class="dropdown-item small py-2 px-3" @click="goToSettings">
          <i class="bi bi-gear me-2"></i> Settings
        </button>
        <hr class="my-1">
        <button class="dropdown-item small py-2 px-3 text-danger" @click="logout">
          <i class="bi bi-box-arrow-right me-2"></i> Logout
        </button>
      </div>
    </div>
  </div>
</template>
