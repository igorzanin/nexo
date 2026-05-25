<script setup lang="ts">
import { ref } from "vue";

const props = defineProps<{
  properties: { id: string; name: string }[];
  currentGroupBy?: string | null;
}>();

const emit = defineEmits<{
  (e: "groupBy", propertyId: string | null): void;
}>();

const isOpen = ref(false);

function toggle() {
  isOpen.value = !isOpen.value;
}

function select(propertyId: string) {
  emit("groupBy", propertyId);
  isOpen.value = false;
}

function clearGroup() {
  emit("groupBy", null);
  isOpen.value = false;
}
</script>

<template>
  <div class="position-relative">
    <button class="btn btn-sm btn-outline-secondary border-0" :class="{ 'text-primary': currentGroupBy }" @click="toggle">
      <i class="bi bi-layers"></i>
    </button>
    <div v-if="isOpen" class="position-absolute start-0 mt-1 bg-white border rounded shadow-sm" style="z-index: 100; min-width: 200px;">
      <div class="px-3 py-1 small fw-semibold text-muted">Group by</div>
      <button
        v-for="prop in properties"
        :key="prop.id"
        class="dropdown-item small py-1 px-3 d-flex align-items-center justify-content-between"
        @click="select(prop.id)"
      >
        {{ prop.name }}
        <i v-if="currentGroupBy === prop.id" class="bi bi-check text-primary"></i>
      </button>
      <hr class="my-1">
      <button class="dropdown-item small py-1 px-3 text-muted" @click="clearGroup">
        <i class="bi bi-x me-1"></i> No grouping
      </button>
    </div>
  </div>
</template>
