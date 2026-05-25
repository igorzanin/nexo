<script setup lang="ts">
const emit = defineEmits<{
  (e: "select", emoji: string): void;
}>();

const emojis = ["😀", "😎", "🚀", "📋", "✅", "⭐", "🎯", "💡", "🔧", "📊", "🎨", "📁", "🔗", "📌", "🧩", "⚡"];
</script>

<template>
  <div class="dropdown">
    <slot name="trigger">
      <button class="btn btn-sm btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
        <i class="bi bi-emoji-smile"></i>
      </button>
    </slot>
    <div class="dropdown-menu p-2" style="width: 200px;">
      <div class="d-flex flex-wrap gap-1">
        <button
          v-for="emoji in emojis"
          :key="emoji"
          class="btn btn-sm border-0 p-1"
          style="font-size: 20px; width: 36px; height: 36px;"
          @click="emit('select', emoji)"
        >
          {{ emoji }}
        </button>
      </div>
    </div>
  </div>
</template>
