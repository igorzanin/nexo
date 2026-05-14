<script setup lang="ts">
import { ref } from "vue";

const props = defineProps<{
  properties: { id: string; name: string }[];
  currentSort?: { propertyId: string; direction: "asc" | "desc" } | null;
}>();

const emit = defineEmits<{
  (e: "sort", propertyId: string, direction: "asc" | "desc"): void;
  (e: "clearSort"): void;
}>();

const isOpen = ref(false);

function toggle() {
  isOpen.value = !isOpen.value;
}

function selectSort(propertyId: string) {
  const dir = props.currentSort?.propertyId === propertyId && props.currentSort.direction === "asc" ? "desc" : "asc";
  emit("sort", propertyId, dir);
  isOpen.value = false;
}

function clearSort() {
  emit("clearSort");
  isOpen.value = false;
}
</script>

<template>
  <div class="position-relative">
    <button class="btn btn-sm btn-outline-secondary border-0" :class="{ 'text-primary': currentSort }" @click="toggle">
      <i class="bi bi-arrow-up-down"></i>
    </button>
    <div v-if="isOpen" class="position-absolute start-0 mt-1 bg-white border rounded shadow-sm" style="z-index: 100; min-width: 200px;">
      <div class="px-3 py-1 small fw-semibold text-muted">Sort by</div>
      <button
        v-for="prop in properties"
        :key="prop.id"
        class="dropdown-item small py-1 px-3 d-flex align-items-center justify-content-between"
        @click="selectSort(prop.id)"
      >
        {{ prop.name }}
        <i v-if="currentSort?.propertyId === prop.id" class="bi" :class="currentSort.direction === 'asc' ? 'bi-sort-up' : 'bi-sort-down'"></i>
      </button>
      <hr class="my-1">
      <button class="dropdown-item small py-1 px-3 text-muted" @click="clearSort">
        <i class="bi bi-x me-1"></i> Clear sort
      </button>
    </div>
  </div>
</template>
