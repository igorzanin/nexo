<script setup lang="ts">
import type { Block } from "../../types/block";
import { CONTENT_BLOCK_TYPES } from "../../types/contentBlock";

defineProps<{
  block: Block;
}>();
</script>

<template>
  <div class="content-element py-1">
    <div v-if="block.type === 'text'">{{ block.title }}</div>
    <div v-else-if="block.type === 'image'">
      <img :src="block.title" alt="image" class="img-fluid rounded" style="max-height: 300px;" />
    </div>
    <div v-else-if="block.type === 'divider'">
      <hr />
    </div>
    <div v-else-if="block.type === 'checkbox'" class="form-check">
      <input type="checkbox" class="form-check-input" :checked="block.fields?.checked as boolean" />
      <label class="form-check-label">{{ block.title }}</label>
    </div>
    <div v-else-if="block.type === 'attachment'">
      <a :href="block.title" target="_blank" class="btn btn-sm btn-outline-secondary">
        📎 {{ block.title }}
      </a>
    </div>
    <div v-else-if="['h1', 'h2', 'h3'].includes(block.type)" :class="`fs-${block.type.slice(1)}`">
      {{ block.title }}
    </div>
    <div v-else class="text-muted small">
      {{ block.type }}: {{ block.title }}
    </div>
  </div>
</template>
