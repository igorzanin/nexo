<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import type { Category } from "../../types/category";

const props = defineProps<{
  category: Category;
  boards: { id: string; title: string; icon?: string }[];
  collapsed?: boolean;
}>();

const emit = defineEmits<{
  (e: "toggleCollapse", id: string): void;
  (e: "rename", id: string, name: string): void;
  (e: "delete", id: string): void;
  (e: "reorder", boardId: string, categoryId: string): void;
}>();

const router = useRouter();
const isCollapsed = ref(props.collapsed ?? false);
const isEditing = ref(false);
const newName = ref(props.category.name);

function toggle() {
  isCollapsed.value = !isCollapsed.value;
  emit("toggleCollapse", props.category.id);
}

function startRename() {
  newName.value = props.category.name;
  isEditing.value = true;
}

function saveRename() {
  if (newName.value.trim()) {
    emit("rename", props.category.id, newName.value.trim());
  }
  isEditing.value = false;
}
</script>

<template>
  <div class="sidebar-category mb-1">
    <div class="d-flex align-items-center px-2 py-1 small text-muted cursor-pointer" @click="toggle">
      <i class="bi" :class="isCollapsed ? 'bi-chevron-right' : 'bi-chevron-down'" style="font-size: 10px;"></i>
      <span v-if="!isEditing" class="ms-1 text-truncate fw-semibold">{{ category.name }}</span>
      <input
        v-else
        v-model="newName"
        class="form-control form-control-sm ms-1"
        style="height: 20px; font-size: 11px;"
        @blur="saveRename"
        @keyup.enter="saveRename"
        @keyup.escape="isEditing = false"
        autofocus
      />
      <div class="ms-auto d-flex gap-1">
        <i class="bi bi-pencil text-muted" style="font-size: 10px; cursor: pointer;" @click.stop="startRename"></i>
        <i class="bi bi-trash text-muted" style="font-size: 10px; cursor: pointer;" @click.stop="emit('delete', category.id)"></i>
      </div>
    </div>
    <div v-if="!isCollapsed" class="ms-2">
      <div
        v-for="board in boards"
        :key="board.id"
        class="d-flex align-items-center px-2 py-1 small rounded cursor-pointer"
        @click="router.push(`/board/${board.id}`)"
      >
        <span class="me-1">{{ board.icon || "📋" }}</span>
        <span class="text-truncate">{{ board.title }}</span>
      </div>
    </div>
  </div>
</template>
