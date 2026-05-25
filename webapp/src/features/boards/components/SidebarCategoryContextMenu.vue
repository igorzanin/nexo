<script setup lang="ts">
const props = defineProps<{
  show: boolean;
  x: number;
  y: number;
}>();

const emit = defineEmits<{
  (e: "rename"): void;
  (e: "moveTo"): void;
  (e: "delete"): void;
  (e: "close"): void;
}>();
</script>

<template>
  <div v-if="show" class="dropdown position-fixed" :style="{ left: `${x}px`, top: `${y}px`, zIndex: '1000' }">
    <ul class="dropdown-menu show">
      <li><button type="button" class="dropdown-item" @click="emit('rename')">Rename</button></li>
      <li><button type="button" class="dropdown-item" @click="emit('moveTo')">Move to</button></li>
      <li><hr class="dropdown-divider" /></li>
      <li><button type="button" class="dropdown-item text-danger" @click="emit('delete')">Delete</button></li>
    </ul>
  </div>
</template>
