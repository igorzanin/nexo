<script setup lang="ts">
// features/boards/pages/BoardMembersPage.vue
// Gerencia membros de um board: lista, adiciona, altera role, remove.
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import AppLayout from "../../../shared/layouts/AppLayout.vue";
import http from "../../../shared/api/client";
import type { BoardMember } from "../../../types/board";
import type { MemberRole } from "../../../types/board";
import { useHasPermissions } from "../composables/useHasPermissions";
import { useBoardsStore } from "../stores/boards.store";

const route = useRoute();
const boardStore = useBoardsStore();
const boardId = route.params.boardId as string;

const members = ref<BoardMember[]>([]);
const loading = ref(false);
const error = ref("");
const newUserEmail = ref("");
const newRole = ref<MemberRole>("editor");
const saving = ref(false);

const board = boardStore.boards[boardId] || null;
const myMember = boardStore.myBoardMemberships[boardId] || null;
const { canManageRoles } = useHasPermissions(board, myMember);

const roles: MemberRole[] = ["viewer", "commenter", "editor", "admin"];

onMounted(async () => {
  loading.value = true;
  error.value = "";
  try {
    const res = await http.get<BoardMember[]>(`/boards/${boardId}/members`);
    members.value = res.data;
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Failed to load members";
  } finally {
    loading.value = false;
  }
});

function effectiveRole(m: BoardMember): string {
  if (m.schemeAdmin) return "admin";
  if (m.schemeEditor) return "editor";
  if (m.schemeCommenter) return "commenter";
  if (m.schemeViewer) return "viewer";
  return m.minimumRole || "viewer";
}

async function changeRole(member: BoardMember, role: MemberRole) {
  try {
    await http.put(`/boards/${boardId}/members/${member.userId}`, { role });
    const idx = members.value.findIndex((m) => m.userId === member.userId);
    if (idx !== -1) {
      members.value[idx] = { ...member, minimumRole: role };
    }
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Failed to update role";
  }
}

async function removeMember(userId: string) {
  if (!confirm("Remove this member from the board?")) return;
  try {
    await http.delete(`/boards/${boardId}/members/${userId}`);
    members.value = members.value.filter((m) => m.userId !== userId);
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Failed to remove member";
  }
}

async function addMember() {
  if (!newUserEmail.value.trim()) return;
  saving.value = true;
  error.value = "";
  try {
    const res = await http.post<BoardMember>(`/boards/${boardId}/members`, {
      email: newUserEmail.value.trim(),
      role: newRole.value,
    });
    members.value.push(res.data);
    newUserEmail.value = "";
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Failed to add member";
  } finally {
    saving.value = false;
  }
}
</script>

<template>
  <AppLayout>
    <div class="container py-4" style="max-width: 720px;">
      <h4 class="mb-4">Board Members</h4>

      <div v-if="error" class="alert alert-danger mb-3">{{ error }}</div>

      <!-- Add member form -->
      <div v-if="canManageRoles" class="card mb-4">
        <div class="card-body">
          <div class="row g-2 align-items-end">
            <div class="col-sm-6">
              <label class="form-label small fw-semibold">Email or username</label>
              <input
                v-model="newUserEmail"
                type="email"
                class="form-control form-control-sm"
                placeholder="user@example.com"
                :disabled="saving"
                @keyup.enter="addMember"
              />
            </div>
            <div class="col-sm-3">
              <label class="form-label small fw-semibold">Role</label>
              <select v-model="newRole" class="form-select form-select-sm" :disabled="saving">
                <option v-for="r in roles" :key="r" :value="r">{{ r }}</option>
              </select>
            </div>
            <div class="col-sm-3">
              <button
                class="btn btn-primary btn-sm w-100"
                :disabled="saving || !newUserEmail.trim()"
                @click="addMember"
              >
                <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
                Add
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Members list -->
      <div v-if="loading" class="text-center text-muted py-4">
        <div class="spinner-border spinner-border-sm me-2"></div>
        Loading members…
      </div>

      <div v-else class="list-group">
        <div
          v-for="m in members"
          :key="m.userId"
          class="list-group-item d-flex align-items-center justify-content-between gap-2"
        >
          <span class="small text-truncate flex-grow-1">{{ m.userId }}</span>
          <select
            v-if="canManageRoles"
            :value="effectiveRole(m)"
            class="form-select form-select-sm"
            style="width: 120px;"
            @change="changeRole(m, ($event.target as HTMLSelectElement).value as MemberRole)"
          >
            <option v-for="r in roles" :key="r" :value="r">{{ r }}</option>
          </select>
          <span v-else class="badge bg-secondary">{{ effectiveRole(m) }}</span>
          <button
            v-if="canManageRoles"
            class="btn btn-outline-danger btn-sm"
            @click="removeMember(m.userId)"
          >
            Remove
          </button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>
