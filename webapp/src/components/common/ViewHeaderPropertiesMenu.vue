<script setup lang="ts">
import type { IPropertyTemplate } from "../../types/board";

const props = defineProps<{
  properties: IPropertyTemplate[];
  visibleProperties: string[];
}>();

const emit = defineEmits<{
  (e: "toggleProperty", propertyId: string): void;
  (e: "addProperty"): void;
}>();

function isVisible(id: string) {
  return props.visibleProperties.includes(id);
}
</script>

<template>
  <div class="dropdown">
    <button class="btn btn-sm btn-outline-secondary border-0 dropdown-toggle" data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false">
      <i class="bi bi-list-columns"></i>
    </button>
    <div class="dropdown-menu" style="min-width: 220px;">
      <h6 class="dropdown-header">Properties</h6>
      <label v-for="prop in properties" :key="prop.id" class="dropdown-item d-flex align-items-center py-1">
        <input
          type="checkbox"
          class="form-check-input me-2"
          :checked="isVisible(prop.id)"
          @change="emit('toggleProperty', prop.id)"
        />
        <span class="flex-grow-1">{{ prop.name }}</span>
        <span class="badge bg-secondary bg-opacity-10 text-muted ms-2" style="font-size: 9px;">{{ prop.type }}</span>
      </label>
      <hr class="dropdown-divider">
      <button class="dropdown-item" @click="emit('addProperty')">
        <i class="bi bi-plus me-1"></i> Add property
      </button>
    </div>
  </div>
</template>
