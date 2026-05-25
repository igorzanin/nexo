<script setup lang="ts">
import { ref } from "vue";

const emit = defineEmits<{
  (e: "create", name: string): void;
}>();

const isOpen = ref(false);
const name = ref("");

function open() {
  name.value = "";
  isOpen.value = true;
}

function close() {
  isOpen.value = false;
  name.value = "";
}

function submit() {
  if (name.value.trim()) {
    emit("create", name.value.trim());
    close();
  }
}
</script>

<template>
  <div>
    <button v-if="!isOpen" class="btn btn-link btn-sm text-muted w-100 text-start px-2 py-1 small" @click="open">
      <i class="bi bi-folder-plus me-1"></i> New Category
    </button>
    <div v-else class="px-2 py-1">
      <div class="input-group input-group-sm">
        <input
          v-model="name"
          type="text"
          class="form-control"
          placeholder="Category name"
          @keyup.enter="submit"
          @keyup.escape="close"
          autofocus
        />
        <button class="btn btn-primary btn-sm" :disabled="!name.trim()" @click="submit">
          <i class="bi bi-check"></i>
        </button>
        <button class="btn btn-outline-secondary btn-sm" @click="close">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
  </div>
</template>
