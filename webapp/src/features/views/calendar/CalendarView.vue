<template>
  <div class="calendar-view d-flex flex-column h-100">
    <!-- Toolbar -->
    <div class="d-flex align-items-center gap-2 px-3 py-2 border-bottom bg-light">
      <button class="btn btn-sm btn-outline-secondary" @click="prevMonth">&lt;</button>
      <span class="fw-semibold">{{ monthLabel }}</span>
      <button class="btn btn-sm btn-outline-secondary" @click="nextMonth">&gt;</button>

      <select
        v-if="dateProperties.length"
        v-model="datePropId"
        class="form-select form-select-sm ms-auto"
        style="max-width: 160px;"
      >
        <option v-for="p in dateProperties" :key="p.id" :value="p.id">{{ p.name }}</option>
      </select>
    </div>

    <div v-if="status === 'loading'" class="flex-grow-1 d-flex align-items-center justify-content-center">
      <div class="spinner-border text-primary" />
    </div>
    <div v-else-if="status === 'error'" class="alert alert-danger m-3">{{ errorMessage }}</div>

    <div v-else class="flex-grow-1 overflow-auto p-3">
      <!-- Week header -->
      <div class="row row-cols-7 g-0 mb-1">
        <div v-for="d in ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']" :key="d" class="col text-center small fw-semibold text-muted py-1">{{ d }}</div>
      </div>

      <!-- Calendar grid -->
      <div class="row row-cols-7 g-0 border-top border-start">
        <div
          v-for="cell in calendarCells"
          :key="cell.key"
          class="col border-bottom border-end p-1"
          style="min-height: 100px;"
          :class="{ 'bg-light': !cell.currentMonth }"
        >
          <div class="text-end small" :class="cell.isToday ? 'fw-bold text-primary' : 'text-muted'">{{ cell.day }}</div>
          <div class="d-flex flex-column gap-1 mt-1">
            <div
              v-for="card in cell.cards"
              :key="card.id"
              class="badge text-bg-primary text-truncate cursor-pointer w-100 text-start"
              @click="openCard(card)"
            >
              {{ card.title || "(Untitled)" }}
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
import { ref, computed } from "vue";
import { useRoute } from "vue-router";
import type { Block } from "../../../types/block";
import CardDetailModal from "../../content/components/CardDetailModal.vue";
import { useViewData } from "../composables/useViewData";

const route = useRoute();
const boardId = route.params.boardId as string;

const {
  status, errorMessage, board, properties, allCards,
} = useViewData(boardId);

const detailCard = ref<Block | null>(null);

const now = new Date();
const currentYear = ref(now.getFullYear());
const currentMonth = ref(now.getMonth()); // 0-based

const dateProperties = computed(() => properties.value.filter((p) => p.type === "date"));
const datePropId = ref("");
const resolvedDatePropId = computed(() => datePropId.value || dateProperties.value[0]?.id || "");

const monthLabel = computed(() =>
  new Date(currentYear.value, currentMonth.value, 1).toLocaleString("default", { month: "long", year: "numeric" })
);

function prevMonth() {
  if (currentMonth.value === 0) { currentYear.value--; currentMonth.value = 11; }
  else currentMonth.value--;
}

function nextMonth() {
  if (currentMonth.value === 11) { currentYear.value++; currentMonth.value = 0; }
  else currentMonth.value++;
}

interface CalendarCell {
  key: string;
  day: number;
  currentMonth: boolean;
  isToday: boolean;
  cards: Block[];
}

const calendarCells = computed<CalendarCell[]>(() => {
  const firstDay = new Date(currentYear.value, currentMonth.value, 1);
  const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0);
  const today = new Date();

  const cells: CalendarCell[] = [];

  // Leading days from prev month
  for (let i = 0; i < firstDay.getDay(); i++) {
    const d = new Date(currentYear.value, currentMonth.value, 1 - (firstDay.getDay() - i));
    cells.push({ key: d.toISOString(), day: d.getDate(), currentMonth: false, isToday: false, cards: [] });
  }

  // Days in current month
  for (let d = 1; d <= lastDay.getDate(); d++) {
    const date = new Date(currentYear.value, currentMonth.value, d);
    const isToday =
      date.getDate() === today.getDate() &&
      date.getMonth() === today.getMonth() &&
      date.getFullYear() === today.getFullYear();

    const cards = resolvedDatePropId.value
      ? allCards.value.filter((c) => {
          const val = (c.fields?.properties as Record<string, unknown>)?.[resolvedDatePropId.value];
          if (!val) return false;
          const cardDate = new Date(String(val));
          return (
            cardDate.getFullYear() === currentYear.value &&
            cardDate.getMonth() === currentMonth.value &&
            cardDate.getDate() === d
          );
        })
      : [];

    cells.push({ key: date.toISOString(), day: d, currentMonth: true, isToday, cards });
  }

  // Trailing days
  const remaining = 7 - (cells.length % 7);
  if (remaining < 7) {
    for (let i = 1; i <= remaining; i++) {
      const d = new Date(currentYear.value, currentMonth.value + 1, i);
      cells.push({ key: d.toISOString(), day: d.getDate(), currentMonth: false, isToday: false, cards: [] });
    }
  }

  return cells;
});

function openCard(card: Block) {
  detailCard.value = card;
}
</script>

<style scoped>
.cursor-pointer { cursor: pointer; }
</style>
