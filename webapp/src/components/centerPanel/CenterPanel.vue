<script setup lang="ts">
import { computed, ref } from "vue";
import { useBoardStore, useCardStore, useViewStore } from "../../stores";
import { useMutator } from "../../composables/useMutator";
import ViewHeader from "../common/ViewHeader.vue";
import CardDialog from "../cardDetail/CardDialog.vue";
import { useFlashMessage } from "../../composables/useFlashMessage";
import Kanban from "../kanban/Kanban.vue";
import Table from "../table/Table.vue";
import CalendarView from "../calendar/Calendar.vue";
import GalleryView from "../gallery/Gallery.vue";

const props = defineProps<{
  boardId: string;
}>();

const boardStore = useBoardStore();
const cardStore = useCardStore();
const viewStore = useViewStore();
const mutator = useMutator();
const { show } = useFlashMessage();
const creating = ref(false);
const openCardId = ref<string | null>(null);

const cards = computed(() => Object.values(cardStore.cards).filter((c) => c.boardId === props.boardId));
const views = computed(() => Object.values(viewStore.views).filter((v) => v.boardId === props.boardId));
const activeView = computed(() => viewStore.views[viewStore.current]);
const board = computed(() => boardStore.boards[props.boardId]);

async function addCard() {
  if (!board.value || creating.value) return;
  creating.value = true;
  try {
    const card = await mutator.insertBlock(board.value, { type: "card", title: "New card" });
    openCardId.value = card.id;
  } catch (e: any) {
    show(e.response?.data?.detail || "Failed to create card", "error");
  } finally {
    creating.value = false;
  }
}

function openCard(cardId: string) {
  openCardId.value = cardId;
}

function closeCard() {
  openCardId.value = null;
}

const visiblePropertyIds = computed(() => {
  const v = activeView.value?.fields?.visiblePropertyIds;
  if (v && v.length > 0) return v;
  return board.value?.cardProperties?.map((p) => p.id) || [];
});

const currentSort = computed(() => activeView.value?.fields?.sortOptions?.[0] || null);
const currentGroupBy = computed(() => activeView.value?.fields?.groupById || null);
</script>

<template>
  <div class="center-panel d-flex flex-column flex-grow-1 overflow-hidden">
    <ViewHeader
      v-if="board && activeView"
      :board="board"
      :view="activeView"
      :views="views"
      :properties="board.cardProperties || []"
      :visible-property-ids="visiblePropertyIds"
      :current-sort="currentSort"
      :current-group-by="currentGroupBy"
      @add-card="addCard"
      @rename-view="(name) => mutator.patchBlock(board.id, viewStore.current, { title: name } as any, {} as any)"
      @delete-view="async (id) => { await mutator.deleteBlock(board.id, id); if (viewStore.current === id) viewStore.current = ''; }"
      @switch-view="(id) => viewStore.current = id"
      @switch-view-type="async (type) => { if (activeView) { const patch = { fields: { ...activeView.fields, viewType: type } }; await mutator.patchBlock(board.id, activeView.id, patch, {} as any); } }"
    />

    <div v-if="!board" class="d-flex align-items-center justify-content-center flex-grow-1 bg-body-secondary">
      <div class="text-center text-muted">
        <h5>Board not found</h5>
        <p class="small">Select a board from the sidebar.</p>
      </div>
    </div>

    <Kanban
      v-else-if="activeView?.fields?.viewType === 'board' || activeView?.fields?.viewType === 'kanban'"
      :board="board"
      :view="activeView"
      :cards="cards"
      @open-card="openCard"
      @add-card="addCard"
    />
    <Table
      v-else-if="activeView?.fields?.viewType === 'table'"
      :board="board"
      :view="activeView"
      :cards="cards"
      @open-card="openCard"
    />
    <CalendarView
      v-else-if="activeView?.fields?.viewType === 'calendar'"
      :cards="cards"
      @open-card="openCard"
    />
    <GalleryView
      v-else-if="activeView?.fields?.viewType === 'gallery'"
      :cards="cards"
      @open-card="openCard"
    />
    <div v-else class="flex-grow-1 overflow-auto p-3">
      <div v-if="cards.length === 0" class="text-center text-muted py-5">
        <p class="mb-2 fs-4"><i class="bi bi-kanban"></i></p>
        <p class="mb-2">This board is empty</p>
        <p class="small mb-3">Add your first card to get started.</p>
        <button class="btn btn-primary" :disabled="creating" @click="addCard">
          {{ creating ? "Creating..." : "+ Add Card" }}
        </button>
      </div>
      <div v-else class="row g-2">
        <div
          v-for="card in cards"
          :key="card.id"
          class="col-4 col-md-3"
          style="cursor: pointer;"
          @click="openCard(card.id)"
        >
          <div class="card shadow-sm h-100 border-0 bg-body-secondary">
            <div class="card-body p-2">
              <h6 class="card-title small mb-0 text-truncate">{{ card.title || "Untitled" }}</h6>
            </div>
          </div>
        </div>
      </div>
    </div>

    <CardDialog
      v-if="openCardId"
      :card-id="openCardId"
      :board-id="boardId"
      @close="closeCard"
    />
  </div>
</template>
