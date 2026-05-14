<script setup lang="ts">
import { ref } from "vue";
import type { IPropertyTemplate } from "../../types/board";

const props = defineProps<{
  properties: IPropertyTemplate[];
  visibleProperties: string[];
}>();

const emit = defineEmits<{
  (e: "toggleProperty", propertyId: string): void;
  (e: "addProperty"): void;
}>();

const isOpen = ref(false);

function toggle() {
  isOpen.value = !isOpen.value;
}

function isVisible(id: string) {
  return props.visibleProperties.includes(id);
}
</script>

<template>
  <div class="position-relative">
    <button class="btn btn-sm btn-outline-secondary border-0" @click="toggle">
      <i class="bi bi-list-columns"></i>
    </button>
    <div v-if="isOpen" class="position-absolute start-0 mt-1 bg-white border rounded shadow-sm" style="z-index: 100; min-width: 220px;">
      <div class="px-3 py-1 small fw-semibold text-muted">Properties</div>
      <div v-for="prop in properties" :key="prop.id" class="px-3 py-1 small d-flex align-items-center">
        <input
          type="checkbox"
          class="form-check-input me-2"
          :checked="isVisible(prop.id)"
          @change="emit('toggleProperty', prop.id)"
        />
        {{ prop.name }}
        <span class="badge bg-secondary bg-opacity-10 text-muted ms-auto" style="font-size: 9px;">{{ prop.type }}</span>
      </div>
      <hr class="my-1">
      <button class="dropdown-item small py-1 px-3" @click="emit('addProperty')">
        <i class="bi bi-plus me-1"></i> Add property
      </button>
    </div>
  </div>
</template>
