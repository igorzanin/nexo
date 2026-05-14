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
      <a v-if="modelValue" :href="modelValue" target="_blank" class="text-decoration-none" rel="noopener">{{ modelValue }}</a>
      <span v-else class="text-muted">Empty</span>
    </div>
    <input
      v-else
      v-model="editValue"
      type="url"
      class="form-control form-control-sm"
      @blur="save"
      @keyup.enter="save"
      @keyup.escape="cancel"
      autofocus
    />
  </div>
</template>
