<script setup lang="ts">
import { onMounted, ref } from "vue";
import type { Block } from "../../../types/block";
import * as api from "../../../api";

const props = defineProps<{
  boardId: string;
}>();

const emit = defineEmits<{
  (e: "select", templateId: string | null): void;
}>();

const templates = ref<Block[]>([]);
const status = ref<"idle" | "loading" | "error" | "success">("idle");
const errorMessage = ref("");

onMounted(async () => {
  status.value = "loading";
  try {
    const blocks = await api.getBlocks(props.boardId);
    templates.value = blocks.filter((block) => block.type === "card" && Boolean(block.fields?.isTemplate));
    status.value = "success";
  } catch (error: unknown) {
    errorMessage.value = error instanceof Error ? error.message : "Failed to load templates";
    status.value = "error";
  }
});
</script>

<template>
  <div class="dropdown">
    <button type="button" class="btn btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">New ▾</button>
    <ul class="dropdown-menu">
      <li><h6 class="dropdown-header">Select a template</h6></li>
      <li>
        <button type="button" class="dropdown-item" @click="emit('select', null)">
          □ Empty Card
        </button>
      </li>
      <li v-if="status === 'loading'"><span class="dropdown-item-text">Loading templates...</span></li>
      <li v-else-if="status === 'error'"><span class="dropdown-item-text text-danger">{{ errorMessage }}</span></li>
      <li v-for="template in templates" :key="template.id">
        <button type="button" class="dropdown-item" @click="emit('select', template.id)">
          {{ template.title }}
        </button>
      </li>
    </ul>
  </div>
</template>
