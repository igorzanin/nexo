<script setup lang="ts">
import { ref } from "vue";

const props = defineProps<{
  modelValue: string;
  placeholder?: string;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
  (e: "save"): void;
}>();

const editing = ref(false);
const editValue = ref("");

function startEdit() {
  editValue.value = props.modelValue || "";
  editing.value = true;
}

function save() {
  emit("update:modelValue", editValue.value);
  emit("save");
  editing.value = false;
}

function cancel() {
  editing.value = false;
}
</script>

<template>
  <span>
    <span v-if="!editing" style="cursor: pointer;" @click="startEdit">
      <slot name="display" :value="modelValue">
        {{ modelValue || <span class="text-muted">{{ placeholder || "Click to edit" }}</span> }}
      </slot>
    </span>
    <input
      v-else
      v-model="editValue"
      type="text"
      class="form-control form-control-sm d-inline-block"
      style="width: auto; min-width: 100px;"
      :placeholder="placeholder"
      @blur="save"
      @keyup.enter="save"
      @keyup.escape="cancel"
      autofocus
    />
  </span>
</template>
