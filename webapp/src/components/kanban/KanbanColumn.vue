<script setup lang="ts">
defineProps<{
  column: { id: string; title: string; color?: string };
  collapsed?: boolean;
}>();

const emit = defineEmits<{
  (e: "toggleCollapse"): void;
  (e: "addCard"): void;
}>();
</script>

<template>
  <div class="kanban-column d-flex flex-column bg-light rounded border flex-grow-1">
    <div class="kanban-column-header d-flex align-items-center justify-content-between px-3 py-2 border-bottom bg-white rounded-top">
      <div class="d-flex align-items-center gap-2">
        <button class="btn btn-sm p-0 border-0" @click="emit('toggleCollapse')">
          <i class="bi" :class="collapsed ? 'bi-chevron-right' : 'bi-chevron-down'" style="font-size: 10px;"></i>
        </button>
        <span v-if="column.color" class="rounded-circle d-inline-block" :style="{ backgroundColor: column.color, width: 10, height: 10 }"></span>
        <span class="small fw-semibold text-truncate">{{ column.title }}</span>
      </div>
      <button class="btn btn-sm p-0 border-0 text-muted" @click="emit('addCard')">
        <i class="bi bi-plus"></i>
      </button>
    </div>
    <slot name="cards" />
    <div v-if="collapsed" class="text-center text-muted small py-2">
      {{ $slots.cards?.().length || 0 }} cards
    </div>
  </div>
</template>
