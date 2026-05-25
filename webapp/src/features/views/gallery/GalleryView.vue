<template>
  <div class="gallery-view d-flex flex-column h-100">
    <!-- Toolbar -->
    <div class="d-flex align-items-center gap-2 px-3 py-2 border-bottom bg-body-secondary">
      <button class="btn btn-sm btn-outline-secondary" @click="showFilter = !showFilter">
        <i class="bi bi-funnel" /> Filter
        <span v-if="filterClauses.length" class="badge bg-secondary ms-1">{{ filterClauses.length }}</span>
      </button>
      <div class="ms-auto">
        <input
          v-model="searchQuery"
          type="search"
          placeholder="Search cards…"
          class="form-control form-control-sm"
          style="min-width: 180px;"
        />
      </div>
    </div>

    <FilterPanel
      v-if="showFilter && board"
      :properties="properties"
      :clauses="filterClauses as any"
      @update:clauses="filterClauses = ($event as any)"
      @close="showFilter = false"
    />

    <div v-if="status === 'loading'" class="flex-grow-1 d-flex align-items-center justify-content-center">
      <div class="spinner-border text-primary" />
    </div>
    <div v-else-if="status === 'error'" class="alert alert-danger m-3">{{ errorMessage }}</div>

    <div v-else class="flex-grow-1 overflow-auto p-3">
      <div class="row row-cols-2 row-cols-sm-3 row-cols-md-4 g-3">
        <div
          v-for="card in filteredCards"
          :key="card.id"
          class="col"
        >
          <div
            class="card h-100 shadow-sm cursor-pointer"
            @click="openCard(card)"
          >
            <img
              v-if="getCoverUrl(card)"
              :src="getCoverUrl(card)!"
              class="card-img-top object-fit-cover"
              style="height: 140px;"
              :alt="card.title"
            />
            <div class="card-body py-2 px-3">
              <p class="card-title fw-semibold mb-0 small text-truncate">{{ card.title || "(Untitled)" }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <CardDetailModal
      v-if="detailCard && board"
      :boardId="detailCard.boardId"
      :cardId="detailCard.id"
      @close="detailCard = null"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRoute } from "vue-router";
import type { Block } from "../../../types/block";
import FilterPanel from "../components/FilterPanel.vue";
import CardDetailModal from "../../content/components/CardDetailModal.vue";
import { useViewData } from "../composables/useViewData";

const route = useRoute();
const boardId = route.params.boardId as string;

const {
  status, errorMessage, board, properties,
  filteredCards, searchQuery, showFilter, filterClauses,
} = useViewData(boardId);

const detailCard = ref<Block | null>(null);

function openCard(card: Block) {
  detailCard.value = card;
}

function getCoverUrl(card: Block): string | null {
  const cover = (card.fields as Record<string, unknown>)?.coverUrl;
  return typeof cover === "string" ? cover : null;
}
</script>

<style scoped>
.cursor-pointer { cursor: pointer; }
</style>
