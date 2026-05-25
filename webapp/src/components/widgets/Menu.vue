<script setup lang="ts">
defineProps<{
  items: { id: string; label: string; icon?: string; danger?: boolean; divider?: boolean }[];
}>();

const emit = defineEmits<{
  (e: "select", id: string): void;
}>();
</script>

<template>
  <div class="dropdown">
    <slot name="trigger">
      <button class="btn btn-sm btn-outline-secondary border-0 dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
        <i class="bi bi-three-dots-vertical"></i>
      </button>
    </slot>
    <ul class="dropdown-menu dropdown-menu-end">
      <template v-for="item in items" :key="item.id">
        <li v-if="item.divider"><hr class="dropdown-divider" /></li>
        <li v-else>
          <button
            class="dropdown-item"
            :class="{ 'text-danger': item.danger }"
            @click="emit('select', item.id)"
          >
            <i v-if="item.icon" :class="[item.icon, 'me-2']"></i>
            {{ item.label }}
          </button>
        </li>
      </template>
    </ul>
  </div>
</template>
