<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

const emit = defineEmits<{
  (e: "changeTeam"): void;
}>();

const router = useRouter();
const isOpen = ref(false);

function toggle() {
  isOpen.value = !isOpen.value;
}

function handleAction(action: string) {
  isOpen.value = false;
  if (action === "change-team") emit("changeTeam");
  if (action === "settings") router.push("/change_password");
}
</script>

<template>
  <div class="position-relative">
    <button class="btn btn-link btn-sm text-muted w-100 text-start px-2 py-1" @click="toggle">
      <i class="bi bi-gear me-1"></i> Settings
    </button>
    <div v-if="isOpen" class="position-absolute start-0 w-100 bg-white border rounded shadow-sm" style="z-index: 105; bottom: 100%;">
      <button class="dropdown-item small py-1 px-3" @click="handleAction('change-team')">
        <i class="bi bi-people me-2"></i> Change Team
      </button>
      <button class="dropdown-item small py-1 px-3" @click="handleAction('settings')">
        <i class="bi bi-key me-2"></i> Change Password
      </button>
    </div>
  </div>
</template>
