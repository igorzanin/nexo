<script setup lang="ts">
import { computed, ref } from "vue";
import { useBoardStore, useCardStore, useViewStore } from "../../stores";
import { useMutator } from "../../composables/useMutator";
import ViewHeader from "../common/ViewHeader.vue";
import CardDialog from "../cardDetail/CardDialog.vue";
import { useFlashMessage } from "../../composables/useFlashMessage";

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
</script>

<template>
  <div class="center-panel d-flex flex-column flex-grow-1 overflow-hidden">
    <ViewHeader v-if="board && activeView" :board="board" :view="activeView" @add-card="addCard" />

    <div v-if="!board" class="d-flex align-items-center justify-content-center flex-grow-1 bg-light">
      <div class="text-center text-muted">
        <h5>Board not found</h5>
        <p class="small">Select a board from the sidebar.</p>
      </div>
    </div>

    <div v-else class="flex-grow-1 overflow-auto p-3">
      <div class="d-flex align-items-center justify-content-between mb-3">
        <span class="text-muted small">{{ cards.length }} cards</span>
        <button class="btn btn-sm btn-outline-primary" :disabled="creating" @click="addCard">
          {{ creating ? "Creating..." : "+ Add Card" }}
        </button>
      </div>

      <div v-if="cards.length === 0" class="text-center text-muted py-5">
        <p class="mb-2 fs-5">This board is empty</p>
        <p class="small">Click "+ Add Card" to create your first card.</p>
      </div>

      <div v-else class="row g-2">
        <div
          v-for="card in cards"
          :key="card.id"
          class="col-4 col-md-3"
          style="cursor: pointer;"
          @click="openCard(card.id)"
        >
          <div class="card shadow-sm h-100 border-0 bg-light">
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
