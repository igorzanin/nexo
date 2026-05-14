<script setup lang="ts">
import { ref, onMounted } from "vue";
import * as api from "../../api";

const props = defineProps<{
  boardId: string;
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

const sharing = ref<{ enabled: boolean; token: string } | null>(null);
const copied = ref(false);

onMounted(async () => {
  try {
    sharing.value = await api.getSharing(props.boardId);
  } catch {
    sharing.value = { enabled: false, token: "" };
  }
});

  async function toggleSharing() {
    if (!sharing.value) return;
    sharing.value = await api.postSharing(props.boardId, {
      enabled: !sharing.value.enabled,
      token: sharing.value.token,
    });
  }

function copyLink() {
  if (sharing.value?.token) {
    navigator.clipboard.writeText(`${window.location.origin}/share/${sharing.value.token}`);
    copied.value = true;
    setTimeout(() => (copied.value = false), 2000);
  }
}
</script>

<template>
  <Teleport to="#app-modal">
    <div class="modal-backdrop fade show" @click="emit('close')" />
    <div class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Share Board</h5>
            <button type="button" class="btn-close" @click="emit('close')" />
          </div>
          <div class="modal-body">
            <div class="form-check form-switch mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                :checked="sharing?.enabled"
                @change="toggleSharing"
              />
              <label class="form-check-label">Public access</label>
            </div>
            <div v-if="sharing?.enabled" class="input-group">
              <input type="text" class="form-control" :value="sharing?.token" readonly />
              <button class="btn btn-outline-secondary" @click="copyLink">
                {{ copied ? "Copied!" : "Copy" }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>
