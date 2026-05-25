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

const selected = ref(props.options.find((o) => o.id === props.modelValue));

function select(opt: IPropertyOption) {
  selected.value = opt;
  emit("update:modelValue", opt.id);
  emit("save");
}

function clear() {
  selected.value = undefined;
  emit("update:modelValue", "");
  emit("save");
}
</script>

<template>
  <div class="dropdown">
    <div class="small d-flex align-items-center gap-1" style="cursor: pointer;" data-bs-toggle="dropdown" aria-expanded="false">
      <span v-if="selected" class="badge" :style="{ backgroundColor: selected.color || '#ccc' }">
        {{ selected.value }}
      </span>
      <span v-else class="text-muted">Empty</span>
      <i class="bi bi-chevron-down ms-auto" style="font-size: 10px;"></i>
    </div>
    <ul class="dropdown-menu">
      <li>
        <button class="dropdown-item small py-1 text-muted" @click="clear">
          <i class="bi bi-x me-1"></i> Empty
        </button>
      </li>
      <li v-for="opt in options" :key="opt.id">
        <button class="dropdown-item small py-1 d-flex align-items-center gap-2" @click="select(opt)">
          <span class="rounded-circle d-inline-block flex-shrink-0" :style="{ backgroundColor: opt.color, width: '8px', height: '8px' }"></span>
          {{ opt.value }}
          <i v-if="selected?.id === opt.id" class="bi bi-check ms-auto text-primary"></i>
        </button>
      </li>
    </ul>
  </div>
</template>
