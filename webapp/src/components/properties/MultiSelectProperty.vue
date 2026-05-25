<script setup lang="ts">
import { computed } from "vue";
import type { IPropertyOption } from "../../types/board";

const props = defineProps<{
  modelValue: string[];
  options: IPropertyOption[];
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string[]): void;
  (e: "save"): void;
}>();

const selectedIds = computed(() => new Set(props.modelValue || []));

const selectedOptions = computed(() =>
  (props.modelValue || []).map((id) => props.options.find((o) => o.id === id)).filter(Boolean)
);

function toggle(opt: IPropertyOption) {
  const ids = new Set(props.modelValue || []);
  if (ids.has(opt.id)) {
    ids.delete(opt.id);
  } else {
    ids.add(opt.id);
  }
  emit("update:modelValue", Array.from(ids));
  emit("save");
}
</script>

<template>
  <div class="dropdown">
    <div class="small d-flex align-items-center flex-wrap gap-1" style="cursor: pointer;" data-bs-toggle="dropdown" aria-expanded="false" data-bs-auto-close="outside">
      <template v-if="selectedOptions.length > 0">
        <span v-for="opt in selectedOptions" :key="opt.id" class="badge" :style="{ backgroundColor: opt.color || '#ccc' }">
          {{ opt.value }}
        </span>
      </template>
      <span v-else class="text-muted">Empty</span>
    </div>
    <ul class="dropdown-menu">
      <li v-for="opt in options" :key="opt.id">
        <button class="dropdown-item small py-1 d-flex align-items-center gap-2" @click.prevent="toggle(opt)">
          <input type="checkbox" class="form-check-input" :checked="selectedIds.has(opt.id)" @click.stop />
          <span class="rounded-circle d-inline-block flex-shrink-0" :style="{ backgroundColor: opt.color, width: '8px', height: '8px' }"></span>
          {{ opt.value }}
        </button>
      </li>
    </ul>
  </div>
</template>
