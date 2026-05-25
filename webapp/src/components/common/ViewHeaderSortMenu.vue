<script setup lang="ts">
const props = defineProps<{
  properties: { id: string; name: string }[];
  currentSort?: { propertyId: string; direction: "asc" | "desc" } | null;
}>();

const emit = defineEmits<{
  (e: "sort", value: { propertyId: string; direction: "asc" | "desc" }): void;
  (e: "clearSort"): void;
}>();

function selectSort(propertyId: string) {
  const direction = props.currentSort?.propertyId === propertyId && props.currentSort.direction === "asc" ? "desc" : "asc";
  emit("sort", { propertyId, direction });
}

function clearSort() {
  emit("clearSort");
}
</script>

<template>
  <div class="dropdown">
    <button class="btn btn-sm btn-outline-secondary border-0 dropdown-toggle" :class="{ 'text-primary': currentSort }" data-bs-toggle="dropdown" aria-expanded="false">
      <i class="bi bi-arrow-up-down"></i>
    </button>
    <ul class="dropdown-menu">
      <li><h6 class="dropdown-header">Sort by</h6></li>
      <li v-for="prop in properties" :key="prop.id">
        <button class="dropdown-item d-flex align-items-center justify-content-between" @click="selectSort(prop.id)">
          {{ prop.name }}
          <i v-if="currentSort?.propertyId === prop.id" class="bi ms-2" :class="currentSort.direction === 'asc' ? 'bi-sort-up' : 'bi-sort-down'"></i>
        </button>
      </li>
      <li><hr class="dropdown-divider"></li>
      <li><button class="dropdown-item text-muted" @click="clearSort"><i class="bi bi-x me-1"></i> Clear sort</button></li>
    </ul>
  </div>
</template>
