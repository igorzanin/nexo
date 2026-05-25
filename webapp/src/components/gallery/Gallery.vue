<script setup lang="ts">
import type { Block } from "../../types/block";

defineProps<{
  cards: Block[];
}>();

const emit = defineEmits<{
  (e: "openCard", cardId: string): void;
}>();
</script>

<template>
  <div class="gallery-view overflow-auto flex-grow-1 p-3">
    <div v-if="cards.length === 0" class="text-center text-muted py-5">
      <i class="bi bi-images fs-1 d-block mb-2"></i>
      <p class="small">No cards to display.</p>
    </div>
    <div v-else class="row g-3">
      <div
        v-for="card in cards"
        :key="card.id"
        class="col-xl-3 col-lg-4 col-md-6 col-sm-12"
        style="cursor: pointer;"
        @click="emit('openCard', card.id)"
      >
        <div class="card shadow-sm h-100 border-0">
          <div class="card-body p-3">
            <div v-if="card.fields?.icon" class="fs-2 mb-2">{{ card.fields.icon }}</div>
            <h6 class="card-title small">{{ card.title || "Untitled" }}</h6>
            <p v-if="card.fields?.description" class="card-text small text-muted text-truncate">{{ card.fields.description }}</p>
            <div v-if="card.fields?.properties" class="mt-2 d-flex flex-wrap gap-1">
              <span v-for="(val, key) in card.fields.properties" :key="key" v-if="val" class="badge bg-secondary-subtle text-secondary fw-normal" style="font-size: 10px;">
                {{ val }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
