<script setup lang="ts">
import type { IPropertyTemplate } from "../../../types/board";

const props = withDefaults(defineProps<{
  id?: string;
  properties: IPropertyTemplate[];
  visibleIds: string[];
}>(), {
  id: "propertiesOffcanvas",
});

const emit = defineEmits<{
  (e: "update:visibleIds", ids: string[]): void;
  (e: "close"): void;
}>();

function toggleVisibility(propertyId: string) {
  const next = props.visibleIds.includes(propertyId)
    ? props.visibleIds.filter((id) => id !== propertyId)
    : [...props.visibleIds, propertyId];
  emit("update:visibleIds", next);
}
</script>

<template>
  <div :id="id" class="offcanvas offcanvas-end" tabindex="-1" :aria-labelledby="`${id}-label`">
    <div class="offcanvas-header">
      <h5 :id="`${id}-label`" class="offcanvas-title">Properties</h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close" @click="emit('close')"></button>
    </div>
    <div class="offcanvas-body">
      <div class="list-group">
        <div v-for="property in properties" :key="property.id" class="list-group-item d-flex justify-content-between align-items-center">
          <span>{{ property.name }}</span>
          <div class="form-check form-switch mb-0">
            <input
              :id="`${id}-${property.id}`"
              class="form-check-input"
              type="checkbox"
              role="switch"
              :checked="visibleIds.includes(property.id)"
              @change="toggleVisibility(property.id)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
