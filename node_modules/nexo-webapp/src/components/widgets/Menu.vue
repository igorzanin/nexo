<script setup lang="ts">
import { ref } from "vue";

defineProps<{
  items: { id: string; label: string; icon?: string; danger?: boolean; divider?: boolean }[];
}>();

const emit = defineEmits<{
  (e: "select", id: string): void;
}>();

const isOpen = ref(false);

function toggle() {
  isOpen.value = !isOpen.value;
}

function select(id: string) {
  emit("select", id);
  isOpen.value = false;
}
</script>

<template>
  <div class="position-relative">
    <slot name="trigger" :toggle="toggle">
      <button class="btn btn-sm btn-outline-secondary border-0" @click="toggle">
        <i class="bi bi-three-dots-vertical"></i>
      </button>
    </slot>
    <div v-if="isOpen" class="position-absolute end-0 mt-1 bg-white border rounded shadow-sm" style="z-index: 100; min-width: 160px;">
      <template v-for="item in items" :key="item.id">
        <hr v-if="item.divider" class="my-1" />
        <button
          v-else
          class="dropdown-item small py-1 px-3 d-flex align-items-center gap-2"
          :class="{ 'text-danger': item.danger }"
          @click="select(item.id)"
        >
          <i v-if="item.icon" :class="item.icon"></i>
          {{ item.label }}
        </button>
      </template>
    </div>
  </div>
</template>
