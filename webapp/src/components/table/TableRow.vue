<script setup lang="ts">
import { ref } from "vue";
import type { Block } from "../../types/block";
import type { IPropertyTemplate } from "../../types/board";

const props = defineProps<{
  card: Block;
  properties: IPropertyTemplate[];
  visiblePropertyIds: string[];
}>();

const emit = defineEmits<{
  (e: "openCard", cardId: string): void;
  (e: "updateProperty", propertyId: string, value: string): void;
}>();

const editingProperty = ref<string | null>(null);
const editValue = ref("");

function startEdit(propertyId: string, currentValue: string) {
  editingProperty.value = propertyId;
  editValue.value = currentValue || "";
}

function saveEdit() {
  if (editingProperty.value !== null) {
    emit("updateProperty", editingProperty.value, editValue.value);
    editingProperty.value = null;
  }
}

function cancelEdit() {
  editingProperty.value = null;
}

function getPropertyValue(propertyId: string): string {
  return props.card.fields?.properties?.[propertyId]?.toString() || "";
}
</script>

<template>
  <tr class="table-row" @dblclick="emit('openCard', card.id)" style="cursor: pointer;">
    <td class="border-bottom px-2 py-2">
      <div class="d-flex align-items-center gap-2">
        <span v-if="card.fields?.icon">{{ card.fields.icon }}</span>
        <span class="small fw-semibold text-truncate">{{ card.title || "Untitled" }}</span>
      </div>
    </td>
    <td
      v-for="prop in properties.filter(p => visiblePropertyIds.includes(p.id))"
      :key="prop.id"
      class="border-bottom px-2 py-1"
      @click.stop="startEdit(prop.id, getPropertyValue(prop.id))"
    >
      <div v-if="editingProperty !== prop.id" class="small text-muted text-truncate">
        {{ getPropertyValue(prop.id) || "—" }}
      </div>
      <input
        v-else
        v-model="editValue"
        class="form-control form-control-sm"
        style="height: 24px; font-size: 12px;"
        @blur="saveEdit"
        @keyup.enter="saveEdit"
        @keyup.escape="cancelEdit"
        autofocus
      />
    </td>
  </tr>
</template>

<style scoped>
.table-row:hover {
  background-color: rgba(0, 0, 0, 0.02);
}
</style>
