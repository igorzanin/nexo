<script setup lang="ts">
import { computed } from "vue";
import type { Block } from "../../types/block";

defineProps<{
  cards: Block[];
}>();

const emit = defineEmits<{
  (e: "openCard", cardId: string): void;
}>();

// Simple calendar grid implementation
const today = new Date();
const currentMonth = today.getMonth();
const currentYear = today.getFullYear();

const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
const firstDayOfWeek = new Date(currentYear, currentMonth, 1).getDay();

const days = computed(() => {
  const result = [];
  for (let i = 0; i < firstDayOfWeek; i++) {
    result.push(null);
  }
  for (let d = 1; d <= daysInMonth; d++) {
    result.push(d);
  }
  return result;
});

const dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

function cardsForDay(day: number | null): Block[] {
  if (!day) return [];
  const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
  return []; // Would filter cards by date property
}

function isToday(day: number | null): boolean {
  if (!day) return false;
  return day === today.getDate() && currentMonth === today.getMonth() && currentYear === today.getFullYear();
}
</script>

<template>
  <div class="calendar-view overflow-auto flex-grow-1 p-3">
    <div class="d-flex align-items-center justify-content-between mb-3">
      <h5 class="mb-0">{{ new Date(currentYear, currentMonth).toLocaleDateString("default", { month: "long", year: "numeric" }) }}</h5>
    </div>
    <div class="border rounded">
      <div class="row g-0 border-bottom">
        <div v-for="day in dayNames" :key="day" class="col text-center small fw-semibold text-muted py-2">
          {{ day }}
        </div>
      </div>
      <div class="row g-0">
        <div v-for="(day, idx) in days" :key="idx" class="col border-bottom border-end" style="min-height: 80px;">
          <div v-if="day" class="p-1">
            <span
              class="d-inline-flex align-items-center justify-content-center rounded-circle"
              :class="isToday(day) ? 'bg-primary text-white' : ''"
              style="width: 24px; height: 24px; font-size: 12px; cursor: pointer;"
            >
              {{ day }}
            </span>
            <div class="mt-1">
              <div
                v-for="card in cardsForDay(day)"
                :key="card.id"
                class="small text-truncate bg-primary bg-opacity-10 rounded px-1 mb-1"
                style="font-size: 10px; cursor: pointer;"
                @click="emit('openCard', card.id)"
              >
                {{ card.title }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
