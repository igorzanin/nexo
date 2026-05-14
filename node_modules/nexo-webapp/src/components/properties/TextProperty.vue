<script setup lang="ts">
import { ref } from "vue";

const props = defineProps<{
  modelValue: string;
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
  <div>
    <div v-if="!editing" class="small" style="cursor: pointer;" @click="startEdit">
      {{ modelValue || <span class="text-muted">Empty</span> }}
    </div>
    <input
      v-else
      v-model="editValue"
      type="text"
      class="form-control form-control-sm"
      maxlength="255"
      @blur="save"
      @keyup.enter="save"
      @keyup.escape="cancel"
      autofocus
    />
  </div>
</template>
