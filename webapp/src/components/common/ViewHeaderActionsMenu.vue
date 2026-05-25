<script setup lang="ts">
const emit = defineEmits<{
  (e: "exportBoard"): void;
  (e: "duplicateBoard"): void;
  (e: "deleteBoard"): void;
}>();
</script>

<template>
  <div class="dropdown">
    <button class="btn btn-sm btn-outline-secondary border-0 dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
      <i class="bi bi-three-dots-vertical"></i>
    </button>
    <ul class="dropdown-menu dropdown-menu-end">
      <li><button class="dropdown-item" @click="emit('exportBoard')"><i class="bi bi-download me-2"></i> Export Board</button></li>
      <li><button class="dropdown-item" @click="emit('duplicateBoard')"><i class="bi bi-files me-2"></i> Duplicate Board</button></li>
      <li><hr class="dropdown-divider"></li>
      <li><button class="dropdown-item text-danger" @click="emit('deleteBoard')"><i class="bi bi-trash me-2"></i> Delete Board</button></li>
    </ul>
  </div>
</template>
