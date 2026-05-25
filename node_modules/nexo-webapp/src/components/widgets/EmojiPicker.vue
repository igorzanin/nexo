<script setup lang="ts">
import { ref } from "vue";

const emit = defineEmits<{
  (e: "select", emoji: string): void;
}>();

const isOpen = ref(false);
const emojis = ["😀", "😎", "🚀", "📋", "✅", "⭐", "🎯", "💡", "🔧", "📊", "🎨", "📁", "🔗", "📌", "🧩", "⚡"];

function toggle() {
  isOpen.value = !isOpen.value;
}

function select(emoji: string) {
  emit("select", emoji);
  isOpen.value = false;
}
</script>

<template>
  <div class="position-relative">
    <slot name="trigger" :toggle="toggle">
      <button class="btn btn-sm btn-outline-secondary" @click="toggle">
        <i class="bi bi-emoji-smile"></i>
      </button>
    </slot>
    <div v-if="isOpen" class="position-absolute start-0 mt-1 bg-white border rounded shadow-sm p-2" style="z-index: 100; width: 200px;">
      <div class="d-flex flex-wrap gap-1">
        <button
          v-for="emoji in emojis"
          :key="emoji"
          class="btn btn-sm border-0 p-1"
          style="font-size: 20px; width: 36px; height: 36px;"
          @click="select(emoji)"
        >
          {{ emoji }}
        </button>
      </div>
    </div>
  </div>
</template>
