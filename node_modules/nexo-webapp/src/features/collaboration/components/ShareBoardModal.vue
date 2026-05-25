<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import type { BoardMember } from "../../../types/board";
import * as api from "../../../api";
import { useSharingStore } from "../stores/sharing.store";

const props = defineProps<{
  boardId: string;
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

const sharingStore = useSharingStore();

const status = ref<"idle" | "loading" | "error">("loading");
const errorMessage = ref("");
const liveMessage = ref("");
const searchQuery = ref("");
const isPublicSharing = ref(false);
const shareToken = ref("");
const members = ref<BoardMember[]>([]);

const shareUrl = computed(() => `${window.location.origin}/shared/${props.boardId}${shareToken.value ? `?token=${shareToken.value}` : ""}`);
const filteredMembers = computed(() => members.value.filter((member) => {
  const query = searchQuery.value.toLowerCase();
  if (!query) return true;
  return member.userId.toLowerCase().includes(query);
}));

function roleLabel(member: BoardMember) {
  if (member.schemeAdmin) return "Admin";
  if (member.schemeEditor) return "Editor";
  if (member.schemeCommenter) return "Commenter";
  return "Viewer";
}

async function loadSharing() {
  status.value = "loading";
  errorMessage.value = "";
  try {
    const [sharing, boardMembers] = await Promise.all([
      sharingStore.fetchSharing(props.boardId),
      api.getMembers(props.boardId),
    ]);
    isPublicSharing.value = sharing.enabled;
    shareToken.value = sharing.token;
    members.value = boardMembers;
    status.value = "idle";
  } catch (error: unknown) {
    errorMessage.value = error instanceof Error ? error.message : "Failed to load sharing settings";
    status.value = "error";
  }
}

async function toggleSharing() {
  const updated = await sharingStore.updateSharing(props.boardId, isPublicSharing.value, shareToken.value);
  isPublicSharing.value = updated.enabled;
  shareToken.value = updated.token;
  liveMessage.value = "Sharing settings updated.";
}

async function copyLink() {
  await navigator.clipboard.writeText(shareUrl.value);
  liveMessage.value = "Sharing settings updated.";
}

onMounted(loadSharing);
</script>

<template>
  <div class="modal fade show d-block" tabindex="-1" style="z-index: 1055;" aria-modal="true" role="dialog">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Share Board</h5>
          <button type="button" class="btn-close" aria-label="Close" @click="emit('close')"></button>
        </div>
        <div class="modal-body">
          <div v-if="status === 'loading'" class="text-muted">Loading sharing settings...</div>
          <div v-else-if="status === 'error'" class="alert alert-danger mb-0">{{ errorMessage }}</div>
          <div v-else class="vstack gap-3">
            <input v-model="searchQuery" type="search" class="form-control" placeholder="Search for people" />
            <div class="form-check form-switch">
              <input id="allow-sharing" v-model="isPublicSharing" class="form-check-input" type="checkbox" role="switch" @change="toggleSharing" />
              <label class="form-check-label" for="allow-sharing">Allow sharing</label>
            </div>
            <div class="input-group">
              <input :value="shareUrl" type="text" class="form-control" readonly />
              <button type="button" class="btn btn-primary" @click="copyLink">Copy link</button>
            </div>
            <table class="table mb-0">
              <thead>
                <tr>
                  <th>Member</th>
                  <th>Role</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="member in filteredMembers" :key="member.userId">
                  <td>{{ member.userId }}</td>
                  <td>{{ roleLabel(member) }}</td>
                </tr>
              </tbody>
            </table>
            <div v-if="liveMessage" class="visually-hidden" aria-live="polite">{{ liveMessage }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-backdrop fade show" style="z-index: 1050;" @click="emit('close')"></div>
</template>
