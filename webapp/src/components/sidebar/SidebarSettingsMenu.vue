<script setup lang="ts">
import { useRouter } from "vue-router";

const emit = defineEmits<{
  (e: "changeTeam"): void;
}>();

const router = useRouter();
</script>

<template>
  <div class="dropup">
    <button class="btn btn-link btn-sm text-muted w-100 text-start px-2 py-1 dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
      <i class="bi bi-gear me-1"></i> Settings
    </button>
    <ul class="dropdown-menu w-100">
      <li><button class="dropdown-item" @click="emit('changeTeam')"><i class="bi bi-people me-2"></i> Change Team</button></li>
      <li><button class="dropdown-item" @click="router.push('/change_password')"><i class="bi bi-key me-2"></i> Change Password</button></li>
    </ul>
  </div>
</template>
