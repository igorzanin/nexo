<script setup lang="ts">
import { ref, computed } from "vue";
import type { IPropertyOption } from "../../types/board";

const props = defineProps<{
  modelValue: string[];
  options: IPropertyOption[];
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string[]): void;
  (e: "save"): void;
}>();

const isOpen = ref(false);

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
  <div class="position-relative">
    <div class="small d-flex align-items-center flex-wrap gap-1" style="cursor: pointer;" @click="isOpen = !isOpen">
      <template v-if="selectedOptions.length > 0">
        <span v-for="opt in selectedOptions" :key="opt.id" class="badge" :style="{ backgroundColor: opt.color || '#ccc' }">
          {{ opt.value }}
        </span>
      </template>
      <span v-else class="text-muted">Empty</span>
    </div>
    <div v-if="isOpen" class="position-absolute start-0 mt-1 bg-white border rounded shadow-sm" style="z-index: 100; min-width: 200px;">
      <button
        v-for="opt in options"
        :key="opt.id"
        class="dropdown-item small py-1 px-3 d-flex align-items-center gap-2"
        @click="toggle(opt)"
      >
        <input type="checkbox" class="form-check-input" :checked="selectedIds.has(opt.id)" @click.stop />
        <span class="rounded-circle d-inline-block" :style="{ backgroundColor: opt.color, width: 8, height: 8 }"></span>
        {{ opt.value }}
      </button>
    </div>
  </div>
</template>
