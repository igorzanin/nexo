<script setup lang="ts">
import type { IPropertyTemplate } from "../../types/board";

defineProps<{
  properties: IPropertyTemplate[];
  visiblePropertyIds: string[];
}>();
</script>

<template>
  <thead>
    <tr>
      <th class="sticky-top bg-white border-bottom px-2 py-2 small fw-semibold text-muted" style="min-width: 200px;">Title</th>
      <th
        v-for="prop in properties.filter(p => visiblePropertyIds.includes(p.id))"
        :key="prop.id"
        class="sticky-top bg-white border-bottom px-2 py-2 small fw-semibold text-muted text-truncate"
        style="min-width: 140px; max-width: 200px;"
      >
        {{ prop.name }}
        <span class="badge bg-secondary bg-opacity-10 text-muted ms-1" style="font-size: 8px;">{{ prop.type }}</span>
      </th>
    </tr>
  </thead>
</template>
