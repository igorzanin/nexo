<script setup lang="ts">
defineProps<{
  label: string;
  value: string;
}>();
</script>

<template>
  <div class="small">
    <span class="text-muted" style="font-size: 10px;">{{ label }}:</span>
    <span class="ms-1">{{ value || <span class="text-muted">—</span> }}</span>
  </div>
</template>
