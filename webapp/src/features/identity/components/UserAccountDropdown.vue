<script setup lang="ts">
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth.store";

const props = defineProps<{
  user: {
    username: string;
    initials: string;
  };
}>();

const emit = defineEmits<{
  (e: "invite-users"): void;
}>();

const router = useRouter();
const auth = useAuthStore();

async function handleLogout() {
  auth.logout();
  await router.push("/login");
}
</script>

<template>
  <div class="dropup">
    <button
      type="button"
      class="btn btn-outline-secondary w-100 d-flex align-items-center gap-2 text-start"
      data-bs-toggle="dropdown"
      data-bs-auto-close="true"
      aria-expanded="false"
    >
      <span
        class="rounded-circle bg-secondary text-white d-inline-flex align-items-center justify-content-center flex-shrink-0"
        style="width: 20px; height: 20px; font-size: 11px;"
      >
        {{ user.initials }}
      </span>
      <span class="text-truncate small flex-grow-1">{{ user.username }}</span>
    </button>

    <ul class="dropdown-menu w-100">
      <li>
        <div class="dropdown-header d-flex align-items-center gap-2">
          <span
            class="rounded-circle bg-secondary text-white d-inline-flex align-items-center justify-content-center flex-shrink-0"
            style="width: 20px; height: 20px; font-size: 11px;"
          >
            {{ user.initials }}
          </span>
          <span class="text-truncate small">{{ user.username }}</span>
        </div>
      </li>
      <li>
        <button type="button" class="dropdown-item" @click="router.push('/change-password')">
          Change password
        </button>
      </li>
      <li>
        <button type="button" class="dropdown-item" @click="emit('invite-users')">
          Invite users
        </button>
      </li>
      <li><hr class="dropdown-divider" /></li>
      <li>
        <button type="button" class="dropdown-item text-danger" @click="handleLogout">
          Log out
        </button>
      </li>
    </ul>
  </div>
</template>
