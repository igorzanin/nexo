<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { useFlashMessage } from "../../composables/useFlashMessage";

interface Flash {
  id: number;
  message: string;
  type: string;
}

const flashes = ref<Flash[]>([]);
let nextId = 0;

const { onFlash } = useFlashMessage();
let unbind: (() => void) | null = null;

onMounted(() => {
  unbind = onFlash(({ message, type, duration }) => {
    const id = nextId++;
    flashes.value.push({ id, message, type });
    setTimeout(() => {
      flashes.value = flashes.value.filter((f) => f.id !== id);
    }, duration);
  });
});

onUnmounted(() => {
  unbind?.();
});
</script>

<template>
  <div class="flash-messages position-fixed top-0 end-0 p-3" style="z-index: 1060">
    <div
      v-for="flash in flashes"
      :key="flash.id"
      class="toast show align-items-center border-0 mb-2"
      :class="`text-bg-${flash.type}`"
      role="alert"
    >
      <div class="d-flex">
        <div class="toast-body">{{ flash.message }}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" @click="flashes = flashes.filter(f => f.id !== flash.id)" />
      </div>
    </div>
  </div>
</template>
