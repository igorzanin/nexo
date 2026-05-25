<script setup lang="ts">
import { computed } from "vue";
import type { IPropertyTemplate } from "../../../types/board";

const props = defineProps<{
  properties: IPropertyTemplate[];
  modelValue: string | null;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string | null): void;
}>();

const selectedPropName = computed(() => props.properties.find((property) => property.id === props.modelValue)?.name || "None");
</script>

<template>
  <div class="dropdown">
    <button type="button" class="btn btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">
      Group by: {{ selectedPropName }}
    </button>
    <ul class="dropdown-menu">
      <li>
        <button type="button" class="dropdown-item d-flex justify-content-between" :class="{ active: modelValue === null }" @click="emit('update:modelValue', null)">
          <span>No grouping</span>
          <i v-if="modelValue === null" class="bi bi-check"></i>
        </button>
      </li>
      <li v-for="property in properties" :key="property.id">
        <button
          type="button"
          class="dropdown-item d-flex justify-content-between"
          :class="{ active: property.id === modelValue }"
          @click="emit('update:modelValue', property.id)"
        >
          <span>{{ property.name }}</span>
          <i v-if="property.id === modelValue" class="bi bi-check"></i>
        </button>
      </li>
    </ul>
  </div>
</template>
