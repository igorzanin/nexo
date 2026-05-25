<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";

defineProps<{
  title: string;
  size?: "sm" | "md" | "lg" | "xl";
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

const el = ref<HTMLElement | null>(null);

function onKeydown(e: KeyboardEvent) {
  if (e.key === "Escape") emit("close");
}

onMounted(() => {
  document.addEventListener("keydown", onKeydown);
  document.body.classList.add("modal-open");
});

onUnmounted(() => {
  document.removeEventListener("keydown", onKeydown);
  document.body.classList.remove("modal-open");
});
</script>

<template>
  <Teleport to="#app-modal">
    <div class="modal-backdrop fade show" @click="emit('close')" />
    <div ref="el" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable" :class="{
        'modal-sm': size === 'sm',
        'modal-lg': size === 'lg',
        'modal-xl': size === 'xl',
      }">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ title }}</h5>
            <button type="button" class="btn-close" @click="emit('close')" />
          </div>
          <div class="modal-body">
            <slot name="body" />
          </div>
          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>
