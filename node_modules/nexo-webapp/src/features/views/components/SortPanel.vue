<script setup lang="ts">
import { ref } from "vue";
import type { IPropertyTemplate } from "../../../types/board";

interface SortPanelClause {
  propertyId: string;
  direction: "asc" | "desc";
}

const props = withDefaults(defineProps<{
  id?: string;
  properties: IPropertyTemplate[];
  clauses: SortPanelClause[];
}>(), {
  id: "sortOffcanvas",
});

const emit = defineEmits<{
  (e: "update:clauses", clauses: SortPanelClause[]): void;
  (e: "close"): void;
}>();

const draftProperty = ref("");
const draftDirection = ref<SortPanelClause["direction"]>("asc");

function removeClause(index: number) {
  emit("update:clauses", props.clauses.filter((_, clauseIndex) => clauseIndex !== index));
}

function clearSort() {
  emit("update:clauses", []);
}

function applySort() {
  if (!draftProperty.value) return;
  emit("update:clauses", [...props.clauses, { propertyId: draftProperty.value, direction: draftDirection.value }]);
}
</script>

<template>
  <div :id="id" class="offcanvas offcanvas-end" tabindex="-1" :aria-labelledby="`${id}-label`">
    <div class="offcanvas-header">
      <h5 :id="`${id}-label`" class="offcanvas-title">Sort</h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close" @click="emit('close')"></button>
    </div>
    <div class="offcanvas-body">
      <div class="list-group mb-3">
        <div v-for="(clause, index) in clauses" :key="`${clause.propertyId}-${index}`" class="list-group-item d-flex justify-content-between align-items-center gap-2">
          <span>{{ properties.find((property) => property.id === clause.propertyId)?.name || clause.propertyId }} {{ clause.direction }}</span>
          <button type="button" class="btn btn-sm btn-outline-danger" @click="removeClause(index)">×</button>
        </div>
      </div>

      <div class="vstack gap-3">
        <h6 class="mb-0">Add sort</h6>
        <div>
          <label class="form-label">Property</label>
          <select v-model="draftProperty" class="form-select">
            <option value="">Select property</option>
            <option v-for="property in properties" :key="property.id" :value="property.id">{{ property.name }}</option>
          </select>
        </div>
        <div>
          <label class="form-label">Direction</label>
          <div class="btn-group w-100">
            <button type="button" class="btn btn-outline-secondary" :class="{ active: draftDirection === 'asc' }" @click="draftDirection = 'asc'">Ascending</button>
            <button type="button" class="btn btn-outline-secondary" :class="{ active: draftDirection === 'desc' }" @click="draftDirection = 'desc'">Descending</button>
          </div>
        </div>
        <div class="btn-group">
          <button type="button" class="btn btn-outline-secondary" @click="clearSort">Clear sort</button>
          <button type="button" class="btn btn-primary" @click="applySort">Apply</button>
        </div>
      </div>
    </div>
  </div>
</template>
