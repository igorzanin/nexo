<script setup lang="ts">
import type { Block } from "../../types/block";
import CardBadges from "./CardBadges.vue";

defineProps<{
  card: Block;
}>();
</script>

<template>
  <div class="kanban-card card shadow-sm border-0 mb-2 cursor-pointer" @click="$emit('click')">
    <div class="card-body p-2">
      <div v-if="card.fields?.icon" class="fs-6 mb-1">{{ card.fields.icon }}</div>
      <h6 class="card-title small mb-0">{{ card.title || "Untitled" }}</h6>
      <div v-if="card.fields?.properties" class="mt-1 d-flex flex-wrap gap-1">
        <span v-for="(val, key) in card.fields.properties" :key="key" v-if="val" class="small text-muted" style="font-size: 10px;">
          {{ val }}
        </span>
      </div>
      <CardBadges :card="card" />
    </div>
  </div>
</template>
