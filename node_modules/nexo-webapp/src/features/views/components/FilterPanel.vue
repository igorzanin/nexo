<script setup lang="ts">
import { ref } from "vue";
import type { IPropertyTemplate } from "../../../types/board";

interface FilterPanelClause {
  propertyId: string;
  operator: "is" | "is not" | "contains" | "does not contain";
  value: string;
}

const props = withDefaults(defineProps<{
  id?: string;
  properties: IPropertyTemplate[];
  clauses: FilterPanelClause[];
}>(), {
  id: "filterOffcanvas",
});

const emit = defineEmits<{
  (e: "update:clauses", clauses: FilterPanelClause[]): void;
  (e: "close"): void;
}>();

const operators: FilterPanelClause["operator"][] = ["is", "is not", "contains", "does not contain"];
const draftProperty = ref("");
const draftOperator = ref<FilterPanelClause["operator"]>("is");
const draftValue = ref("");

function removeClause(index: number) {
  emit("update:clauses", props.clauses.filter((_, clauseIndex) => clauseIndex !== index));
}

function clearFilters() {
  emit("update:clauses", []);
}

function applyFilter() {
  if (!draftProperty.value) return;
  emit("update:clauses", [
    ...props.clauses,
    {
      propertyId: draftProperty.value,
      operator: draftOperator.value,
      value: draftValue.value,
    },
  ]);
  draftValue.value = "";
}
</script>

<template>
  <div :id="id" class="offcanvas offcanvas-end" tabindex="-1" :aria-labelledby="`${id}-label`">
    <div class="offcanvas-header">
      <h5 :id="`${id}-label`" class="offcanvas-title">Filter</h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close" @click="emit('close')"></button>
    </div>
    <div class="offcanvas-body">
      <div class="list-group mb-3">
        <div v-for="(clause, index) in clauses" :key="`${clause.propertyId}-${index}`" class="list-group-item d-flex justify-content-between align-items-center gap-2">
          <span>{{ properties.find((property) => property.id === clause.propertyId)?.name || clause.propertyId }} {{ clause.operator }} {{ clause.value }}</span>
          <button type="button" class="btn btn-sm btn-outline-danger" @click="removeClause(index)">×</button>
        </div>
      </div>

      <div class="vstack gap-3">
        <h6 class="mb-0">Add filter</h6>
        <div>
          <label class="form-label">Property</label>
          <select v-model="draftProperty" class="form-select">
            <option value="">Select property</option>
            <option v-for="property in properties" :key="property.id" :value="property.id">{{ property.name }}</option>
          </select>
        </div>
        <div>
          <label class="form-label">Operator</label>
          <select v-model="draftOperator" class="form-select">
            <option v-for="operator in operators" :key="operator" :value="operator">{{ operator }}</option>
          </select>
        </div>
        <div>
          <label class="form-label">Value</label>
          <input v-model="draftValue" type="text" class="form-control" />
        </div>
        <div class="btn-group">
          <button type="button" class="btn btn-outline-secondary" @click="clearFilters">Clear filters</button>
          <button type="button" class="btn btn-primary" @click="applyFilter">Apply</button>
        </div>
      </div>
    </div>
  </div>
</template>
