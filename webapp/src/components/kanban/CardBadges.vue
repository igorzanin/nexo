<script setup lang="ts">
import type { Block } from "../../types/block";

const props = defineProps<{
  card: Block;
}>();
</script>

<template>
  <div class="card-badges d-flex gap-1 mt-1">
    <span v-if="card.fields?.commentCount" class="badge bg-secondary-subtle text-secondary fw-normal d-flex align-items-center gap-1" style="font-size: 10px;">
      <i class="bi bi-chat"></i> {{ card.fields.commentCount }}
    </span>
    <span v-if="card.fields?.description" class="badge bg-secondary-subtle text-secondary fw-normal" style="font-size: 10px;">
      <i class="bi bi-card-heading"></i>
    </span>
    <span v-if="card.fields?.imageCount" class="badge bg-secondary-subtle text-secondary fw-normal d-flex align-items-center gap-1" style="font-size: 10px;">
      <i class="bi bi-image"></i> {{ card.fields.imageCount }}
    </span>
  </div>
</template>
