<script setup lang="ts">
// features/boards/pages/CategoryManagerPage.vue
// CRUD de categorias do time: criar, renomear, excluir.
import { ref, onMounted } from "vue";
import AppLayout from "../../../shared/layouts/AppLayout.vue";
import { useCategoriesStore } from "../stores/categories.store";
import { useTeamsStore } from "../stores/teams.store";

const categoriesStore = useCategoriesStore();
const teamStore = useTeamsStore();

const newCategoryName = ref("");
const editingId = ref<string | null>(null);
const editingName = ref("");
const saving = ref(false);
const error = ref("");

onMounted(async () => {
  if (!teamStore.currentId) await teamStore.fetchTeams();
  if (teamStore.currentId) {
    await categoriesStore.fetchCategories(teamStore.currentId);
  }
});

async function addCategory() {
  if (!newCategoryName.value.trim()) return;
  saving.value = true;
  error.value = "";
  try {
    await categoriesStore.createCategory(teamStore.currentId, newCategoryName.value.trim());
    newCategoryName.value = "";
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Failed to create category";
  } finally {
    saving.value = false;
  }
}

function startEdit(id: string, name: string) {
  editingId.value = id;
  editingName.value = name;
}

async function saveEdit() {
  if (!editingId.value || !editingName.value.trim()) return;
  saving.value = true;
  error.value = "";
  try {
    await categoriesStore.renameCategory(teamStore.currentId, editingId.value, editingName.value.trim());
    editingId.value = null;
    editingName.value = "";
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Failed to rename category";
  } finally {
    saving.value = false;
  }
}

function cancelEdit() {
  editingId.value = null;
  editingName.value = "";
}

async function deleteCategory(id: string, name: string) {
  if (!confirm(`Delete category "${name}"? Boards in it will become uncategorized.`)) return;
  error.value = "";
  try {
    await categoriesStore.deleteCategory(teamStore.currentId, id);
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Failed to delete category";
  }
}
</script>

<template>
  <AppLayout>
    <div class="container py-4" style="max-width: 600px;">
      <h4 class="mb-4">Manage Categories</h4>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <!-- Add new category -->
      <div class="input-group mb-4">
        <input
          v-model="newCategoryName"
          type="text"
          class="form-control"
          placeholder="New category name…"
          :disabled="saving"
          @keyup.enter="addCategory"
        />
        <button
          class="btn btn-primary"
          :disabled="saving || !newCategoryName.trim()"
          @click="addCategory"
        >
          <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
          Add
        </button>
      </div>

      <!-- Loading -->
      <div v-if="categoriesStore.loading" class="text-center text-muted py-4">
        <div class="spinner-border spinner-border-sm me-2"></div>
        Loading categories…
      </div>

      <!-- Empty -->
      <div v-else-if="categoriesStore.sortedCategories.length === 0" class="text-muted text-center py-4">
        No categories yet.
      </div>

      <!-- List -->
      <div v-else class="list-group">
        <div
          v-for="cat in categoriesStore.sortedCategories"
          :key="cat.id"
          class="list-group-item d-flex align-items-center gap-2"
        >
          <!-- Edit mode -->
          <template v-if="editingId === cat.id">
            <input
              v-model="editingName"
              type="text"
              class="form-control form-control-sm flex-grow-1"
              @keyup.enter="saveEdit"
              @keyup.escape="cancelEdit"
            />
            <button class="btn btn-primary btn-sm" :disabled="saving" @click="saveEdit">Save</button>
            <button class="btn btn-outline-secondary btn-sm" @click="cancelEdit">Cancel</button>
          </template>

          <!-- View mode -->
          <template v-else>
            <span class="flex-grow-1 small">{{ cat.name }}</span>
            <span class="badge bg-secondary-subtle text-secondary border small">{{ cat.type }}</span>
            <button class="btn btn-outline-secondary btn-sm" @click="startEdit(cat.id, cat.name)">
              Rename
            </button>
            <button class="btn btn-outline-danger btn-sm" @click="deleteCategory(cat.id, cat.name)">
              Delete
            </button>
          </template>
        </div>
      </div>
    </div>
  </AppLayout>
</template>
