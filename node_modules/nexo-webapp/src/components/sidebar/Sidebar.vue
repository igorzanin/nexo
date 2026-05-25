<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { useBoardStore, useSidebarStore, useTeamStore, useUserStore } from "../../stores";
import SidebarCategory from "./SidebarCategory.vue";
import SidebarBoardItem from "./SidebarBoardItem.vue";
import CreateCategory from "./CreateCategory.vue";
import SidebarSettingsMenu from "./SidebarSettingsMenu.vue";
import SidebarUserMenu from "./SidebarUserMenu.vue";

const emit = defineEmits<{
  (e: "createBoard"): void;
}>();

const router = useRouter();
const boardStore = useBoardStore();
const sidebarStore = useSidebarStore();
const teamStore = useTeamStore();
const userStore = useUserStore();

const { boardList } = storeToRefs(boardStore);
const categories = computed(() => sidebarStore.categoryAttributes);

async function handleCreateCategory(name: string) {
  if (teamStore.currentId) {
    await sidebarStore.createCategory(teamStore.currentId, name);
  }
}

async function handleRenameCategory(id: string, name: string) {
  await sidebarStore.renameCategory(id, name);
}

async function handleDeleteCategory(id: string) {
  await sidebarStore.deleteCategory(id);
}

function handleChangeTeam() {
  router.push("/");
}
</script>

<template>
  <aside class="sidebar d-flex flex-column bg-light border-end" style="width: 240px; height: 100vh;">
    <div class="p-3 border-bottom d-flex align-items-center justify-content-between">
      <h6 class="mb-0 text-truncate">{{ teamStore.current?.title || "Nexo" }}</h6>
    </div>

    <div class="p-2">
      <button class="btn btn-primary btn-sm w-100" @click="emit('createBoard')">
        <i class="bi bi-plus me-1"></i> New Board
      </button>
    </div>

    <div class="flex-grow-1 overflow-auto px-2 mt-2">
      <div v-if="boardList.length === 0" class="text-center text-muted small py-4">
        No boards yet. Click "+ New Board" to start.
      </div>
      <div v-else>
        <div class="small text-muted px-2 py-1 fw-semibold">Boards</div>
        <SidebarBoardItem
          v-for="board in boardList"
          :key="board.id"
          :board="board"
          :active="boardStore.current === board.id"
        />
      </div>

      <div v-if="categories.length > 0" class="mt-3">
        <SidebarCategory
          v-for="cat in categories"
          :key="cat.id"
          :category="cat"
          :boards="[]"
          @rename="handleRenameCategory"
          @delete="handleDeleteCategory"
        />
      </div>

      <div class="mt-2">
        <CreateCategory @create="handleCreateCategory" />
      </div>
    </div>

    <div class="p-2 border-top d-flex flex-column gap-1">
      <SidebarSettingsMenu @change-team="handleChangeTeam" />
      <SidebarUserMenu :username="userStore.me?.username || 'User'" />
    </div>
  </aside>
</template>
