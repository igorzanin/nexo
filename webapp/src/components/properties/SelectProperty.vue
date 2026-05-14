<script setup lang="ts">
import { ref } from "vue";
import type { IPropertyOption } from "../../types/board";

const props = defineProps<{
  modelValue: string;
  options: IPropertyOption[];
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
  (e: "save"): void;
}>();

const isOpen = ref(false);

const selected = ref(props.options.find((o) => o.id === props.modelValue));

function select(opt: IPropertyOption) {
  selected.value = opt;
  emit("update:modelValue", opt.id);
  emit("save");
  isOpen.value = false;
}

function clear() {
  selected.value = undefined;
  emit("update:modelValue", "");
  emit("save");
  isOpen.value = false;
}
</script>

<template>
  <div class="position-relative">
    <div class="small d-flex align-items-center gap-1" style="cursor: pointer;" @click="isOpen = !isOpen">
      <span v-if="selected" class="badge" :style="{ backgroundColor: selected.color || '#ccc' }">
        {{ selected.value }}
      </span>
      <span v-else class="text-muted">Empty</span>
      <i class="bi bi-chevron-down ms-auto" style="font-size: 10px;"></i>
    </div>
    <div v-if="isOpen" class="position-absolute start-0 mt-1 bg-white border rounded shadow-sm" style="z-index: 100; min-width: 160px;">
      <button class="dropdown-item small py-1 px-3 text-muted" @click="clear">
        <i class="bi bi-x me-1"></i> Empty
      </button>
      <button
        v-for="opt in options"
        :key="opt.id"
        class="dropdown-item small py-1 px-3 d-flex align-items-center gap-2"
        @click="select(opt)"
      >
        <span class="rounded-circle d-inline-block" :style="{ backgroundColor: opt.color, width: 8, height: 8 }"></span>
        {{ opt.value }}
        <i v-if="selected?.id === opt.id" class="bi bi-check ms-auto text-primary"></i>
      </button>
    </div>
  </div>
</template>
