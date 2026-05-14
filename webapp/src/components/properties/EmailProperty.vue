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
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function startEdit() {
  editValue.value = props.modelValue || "";
  editing.value = true;
}

function save() {
  if (editValue.value && !emailRegex.test(editValue.value)) return;
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
      <a v-if="modelValue" :href="`mailto:${modelValue}`" class="text-decoration-none">{{ modelValue }}</a>
      <span v-else class="text-muted">Empty</span>
    </div>
    <div v-else>
      <input
        v-model="editValue"
        type="email"
        class="form-control form-control-sm"
        :class="{ 'is-invalid': editValue && !emailRegex.test(editValue) }"
        @blur="save"
        @keyup.enter="save"
        @keyup.escape="cancel"
        autofocus
      />
      <div v-if="editValue && !emailRegex.test(editValue)" class="invalid-feedback">Invalid email</div>
    </div>
  </div>
</template>
