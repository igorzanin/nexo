<script setup lang="ts">
const props = defineProps<{
  modelValue: boolean;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
  (e: "save"): void;
}>();

function toggle() {
  emit("update:modelValue", !props.modelValue);
  emit("save");
}
</script>

<template>
  <div class="form-check" style="cursor: pointer;" @click="toggle">
    <input type="checkbox" class="form-check-input" :checked="modelValue" @click.stop />
    <i class="bi" :class="modelValue ? 'bi-check-square-fill text-primary' : 'bi-square text-muted'"></i>
  </div>
</template>
