<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useBoardStore, useSidebarStore, useTeamStore, useUserStore } from "../../stores";

const emit = defineEmits<{
  (e: "createBoard"): void;
}>();

const router = useRouter();
const boardStore = useBoardStore();
const sidebarStore = useSidebarStore();
const teamStore = useTeamStore();
const userStore = useUserStore();
const showUserMenu = ref(false);

const boards = boardStore.boardList;
const categories = sidebarStore.categoryAttributes;

function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  userStore.clearMe();
  router.push("/login");
}
</script>

<template>
  <aside class="sidebar d-flex flex-column bg-light border-end" style="width: 240px; height: 100vh;">
    <div class="p-3 border-bottom d-flex align-items-center justify-content-between">
      <h6 class="mb-0 text-truncate">{{ teamStore.current?.title || "Nexo" }}</h6>
    </div>

    <div class="p-2">
      <button class="btn btn-primary btn-sm w-100" @click="emit('createBoard')">
        + New Board
      </button>
    </div>

    <div class="flex-grow-1 overflow-auto px-2 mt-2">
      <div v-if="boards.length === 0" class="text-center text-muted small py-4">
        No boards yet. Click "+ New Board" to start.
      </div>
      <div v-else>
        <div class="small text-muted px-2 py-1 fw-semibold">Boards</div>
        <div
          v-for="board in boards"
          :key="board.id"
          class="d-flex align-items-center px-3 py-1 small rounded cursor-pointer"
          :class="{ 'bg-primary bg-opacity-10 text-primary': boardStore.current === board.id }"
          @click="router.push(`/board/${board.id}`)"
        >
          <span class="me-1">{{ board.icon || "📋" }}</span>
          <span class="text-truncate">{{ board.title }}</span>
        </div>
      </div>

      <div v-if="categories.length > 0" class="mt-3">
        <div class="small text-muted px-2 py-1 fw-semibold">Categories</div>
        <div v-for="cat in categories" :key="cat.id" class="mb-1">
          <div class="px-2 py-1 small text-muted">{{ cat.name }}</div>
        </div>
      </div>
    </div>

    <div class="p-2 border-top position-relative">
      <button class="btn btn-outline-secondary btn-sm w-100 text-start d-flex align-items-center gap-2" @click="showUserMenu = !showUserMenu">
        <span class="rounded-circle bg-secondary text-white d-inline-flex align-items-center justify-content-center" style="width: 20px; height: 20px; font-size: 11px;">
          {{ userStore.me?.username?.charAt(0).toUpperCase() || "?" }}
        </span>
        <span class="text-truncate small">{{ userStore.me?.username || "User" }}</span>
      </button>
      <div v-if="showUserMenu" class="position-absolute bottom-100 start-0 w-100 p-1" style="z-index: 10;">
        <div class="bg-white border rounded shadow-sm">
          <button class="dropdown-item small py-2 px-3" @click="router.push('/change_password')">Change Password</button>
          <hr class="my-1">
          <button class="dropdown-item small py-2 px-3 text-danger" @click="logout">Logout</button>
        </div>
      </div>
    </div>
  </aside>
</template>
