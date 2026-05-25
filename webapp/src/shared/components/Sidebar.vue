<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import type { Board } from "../../types/board";
import type { CategoryBoards } from "../../types/category";
import { useBoardStore, useTeamStore, useUserStore } from "../../stores";
import { useCategoriesStore } from "../../features/boards/stores/categories.store";
import SettingsAppMenu from "../../features/boards/components/SettingsAppMenu.vue";
import SidebarCategoryContextMenu from "../../features/boards/components/SidebarCategoryContextMenu.vue";
import UserAccountDropdown from "../../features/identity/components/UserAccountDropdown.vue";

const props = withDefaults(defineProps<{
  brandText?: string;
  teamName?: string;
  boards?: Board[];
  activeBoard?: string;
  footerSettingsLabel?: string;
}>(), {
  brandText: "Nexo",
  teamName: "",
  boards: () => [],
  activeBoard: "",
  footerSettingsLabel: "Settings",
});

const emit = defineEmits<{
  (e: "createBoard"): void;
}>();

const router = useRouter();
const boardStore = useBoardStore();
const teamStore = useTeamStore();
const userStore = useUserStore();
const categoriesStore = useCategoriesStore();

const contextCategory = ref<CategoryBoards | null>(null);
const contextPosition = ref({ x: 0, y: 0 });

const boardItems = computed(() => (props.boards.length ? props.boards : boardStore.boardList));
const sidebarTeamName = computed(() => props.teamName || teamStore.current?.title || props.brandText);
const categories = computed(() => categoriesStore.sortedCategories);
const activeBoardValue = computed(() => props.activeBoard || boardStore.current || "");
const userInfo = computed(() => {
  const username = userStore.me?.username || "User";
  const initials = username.slice(0, 2).toUpperCase() || "US";
  return { username, initials };
});

async function loadCategories(teamId: string) {
  if (!teamId) return;
  try {
    await categoriesStore.fetchCategories(teamId);
  } catch {
    // mant├®m sidebar utiliz├ível mesmo sem categorias
  }
}

function openBoard(boardId: string) {
  boardStore.current = boardId;
  router.push(`/board/${boardId}`);
}

function isBoardActive(board: Board) {
  return activeBoardValue.value === board.id || activeBoardValue.value === board.title;
}

function openCategoryMenu(category: CategoryBoards, event: MouseEvent) {
  event.preventDefault();
  contextCategory.value = category;
  contextPosition.value = { x: event.clientX, y: event.clientY };
}

function closeCategoryMenu() {
  contextCategory.value = null;
}

async function renameCategory(category: CategoryBoards) {
  const teamId = teamStore.currentId;
  const name = window.prompt("Rename", category.name)?.trim();
  if (!teamId || !name || name === category.name) return;
  await categoriesStore.renameCategory(teamId, category.id, name);
  closeCategoryMenu();
}

async function deleteCategory(category: CategoryBoards) {
  const teamId = teamStore.currentId;
  if (!teamId) return;
  await categoriesStore.deleteCategory(teamId, category.id);
  closeCategoryMenu();
}

function handleDocumentClick() {
  closeCategoryMenu();
}

onMounted(() => {
  document.addEventListener("click", handleDocumentClick);
  if (teamStore.currentId) {
    loadCategories(teamStore.currentId);
  }
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleDocumentClick);
});

watch(() => teamStore.currentId, (teamId) => {
  if (teamId) {
    loadCategories(teamId);
  }
}, { immediate: true });
</script>

<template>
  <aside class="nexo-sidebar d-flex flex-column border-end" style="width: 240px; min-width: 240px; max-width: 240px; height: 100vh;">
    <div class="p-3 border-bottom nexo-sidebar-divider">
      <div class="nexo-sidebar-brand">{{ brandText }}</div>
      <div class="nexo-sidebar-team">{{ sidebarTeamName }}</div>
    </div>

    <div class="flex-grow-1 overflow-auto p-2">
      <div class="d-flex align-items-center justify-content-between mb-1 px-1 mt-2">
        <span class="nexo-sidebar-section-label">Boards</span>
        <button type="button" class="nexo-sidebar-add-btn" @click="emit('createBoard')" title="New board">
          <i class="bi bi-plus"></i>
        </button>
      </div>

      <div class="vstack gap-0">
        <button
          v-for="board in boardItems"
          :key="board.id"
          type="button"
          class="nexo-board-item"
          :class="{ active: isBoardActive(board) }"
          @click="openBoard(board.id)"
        >
          <span>{{ board.icon || '📋' }}</span>
          <span class="text-truncate flex-grow-1">{{ board.title }}</span>
        </button>
      </div>

      <div v-if="categories.length" class="mt-3">
        <div class="d-flex align-items-center justify-content-between mb-1 px-1">
          <span class="nexo-sidebar-section-label">Categories</span>
        </div>
        <div class="vstack gap-0">
          <div
            v-for="category in categories"
            :key="category.id"
            class="nexo-category-item"
            @contextmenu="openCategoryMenu(category, $event)"
          >
            <span class="text-truncate flex-grow-1">{{ category.name }}</span>
            <button type="button" class="nexo-sidebar-add-btn" style="font-size: 0.9rem;" @click.stop="openCategoryMenu(category, $event)">
              <i class="bi bi-three-dots"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="border-top nexo-sidebar-divider p-2 vstack gap-1">
      <SettingsAppMenu :label="footerSettingsLabel" />
      <UserAccountDropdown :user="userInfo" />
    </div>

    <SidebarCategoryContextMenu
      v-if="contextCategory"
      :show="true"
      :x="contextPosition.x"
      :y="contextPosition.y"
      @rename="renameCategory(contextCategory)"
      @move-to="closeCategoryMenu"
      @delete="deleteCategory(contextCategory)"
      @close="closeCategoryMenu"
    />
  </aside>
</template>