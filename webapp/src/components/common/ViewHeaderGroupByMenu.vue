<script setup lang="ts">
const props = defineProps<{
  properties: { id: string; name: string }[];
  currentGroupBy?: string | null;
}>();

const emit = defineEmits<{
  (e: "groupBy", propertyId: string | null): void;
}>();
</script>

<template>
  <div class="dropdown">
    <button class="btn btn-sm btn-outline-secondary border-0 dropdown-toggle" :class="{ 'text-primary': currentGroupBy }" data-bs-toggle="dropdown" aria-expanded="false">
      <i class="bi bi-layers"></i>
    </button>
    <ul class="dropdown-menu">
      <li><h6 class="dropdown-header">Group by</h6></li>
      <li v-for="prop in properties" :key="prop.id">
        <button class="dropdown-item d-flex align-items-center justify-content-between" @click="emit('groupBy', prop.id)">
          {{ prop.name }}
          <i v-if="currentGroupBy === prop.id" class="bi bi-check text-primary ms-2"></i>
        </button>
      </li>
      <li><hr class="dropdown-divider"></li>
      <li><button class="dropdown-item text-muted" @click="emit('groupBy', null)"><i class="bi bi-x me-1"></i> No grouping</button></li>
    </ul>
  </div>
</template>
