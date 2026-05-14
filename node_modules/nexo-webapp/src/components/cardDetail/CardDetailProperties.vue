<script setup lang="ts">
import { ref } from "vue";
import type { Block } from "../../types/block";
import type { IPropertyTemplate } from "../../types/board";
import { useMutator } from "../../composables/useMutator";

const props = defineProps<{
  card: Block;
  properties: IPropertyTemplate[];
  boardId: string;
}>();

const mutator = useMutator();
const editingProp = ref<string | null>(null);
const editValue = ref("");

function getValue(propId: string): string {
  return props.card.fields?.properties?.[propId]?.toString() || "";
}

function startEdit(propId: string) {
  editingProp.value = propId;
  editValue.value = getValue(propId);
}

async function saveEdit() {
  if (!editingProp.value) return;
  const propId = editingProp.value;
  const patch = {
    fields: {
      ...props.card.fields,
      properties: {
        ...props.card.fields?.properties,
        [propId]: editValue.value,
      },
    },
  };
  try {
    await mutator.patchBlock({ id: props.boardId } as any, props.card, patch);
    if (props.card.fields?.properties) {
      props.card.fields.properties[propId] = editValue.value;
    }
  } catch {
    // silently fail
  }
  editingProp.value = null;
}

function cancelEdit() {
  editingProp.value = null;
}

function displayValue(prop: IPropertyTemplate): string {
  const val = getValue(prop.id);
  if (!val) return "";
  if (prop.type === "select" || prop.type === "multiSelect") {
    const ids = val.split(",");
    return ids.map((id) => prop.options?.find((o) => o.id === id)?.value || id).join(", ");
  }
  if (prop.type === "date") {
    try { return new Date(val).toLocaleDateString(); } catch { return val; }
  }
  return val;
}
</script>

<template>
  <div class="octo-propertylist d-flex flex-column w-100">
    <div
      v-for="prop in properties"
      :key="prop.id"
      class="octo-propertyrow d-flex align-items-start"
      style="min-height: 32px; margin: 6px 0; max-width: 595px;"
    >
      <div class="octo-propertyname flex-shrink-0 text-muted small" style="width: 150px; margin-right: 5px; padding: 4px 8px;">
        {{ prop.name }}
      </div>
      <div
        class="octo-propertyvalue flex-grow-1"
        :class="{ 'octo-propertyvalue--readonly': false }"
        style="font-size: 14px; padding: 4px 8px; min-height: 32px; cursor: pointer; border-radius: 4px; transition: background 100ms;"
        @click="startEdit(prop.id)"
        @mouseenter="$event.target.classList.add('hover-bg')"
        @mouseleave="$event.target.classList.remove('hover-bg')"
      >
        <input
          v-if="editingProp === prop.id"
          v-model="editValue"
          class="form-control form-control-sm border-0 p-0"
          style="font-size: 14px; height: 22px;"
          @blur="saveEdit"
          @keyup.enter="saveEdit"
          @keyup.escape="cancelEdit"
          autofocus
        />
        <span v-else-if="displayValue(prop)">{{ displayValue(prop) }}</span>
        <span v-else class="text-muted">Empty</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.octo-propertyvalue.hover-bg {
  background-color: rgba(63, 67, 80, 0.08);
}
</style>
