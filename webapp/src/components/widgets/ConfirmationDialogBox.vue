<script setup lang="ts">
defineProps<{
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  variant?: "danger" | "warning" | "primary";
}>();

const emit = defineEmits<{
  (e: "confirm"): void;
  (e: "cancel"): void;
}>();
</script>

<template>
  <Teleport to="#app-modal">
    <div class="modal-backdrop fade show" @click="emit('cancel')" />
    <div class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered modal-sm">
        <div class="modal-content">
          <div class="modal-header">
            <h6 class="modal-title">{{ title }}</h6>
            <button type="button" class="btn-close" @click="emit('cancel')" />
          </div>
          <div class="modal-body small">
            {{ message }}
          </div>
          <div class="modal-footer">
            <button class="btn btn-sm btn-outline-secondary" @click="emit('cancel')">{{ cancelText || "Cancel" }}</button>
            <button class="btn btn-sm" :class="`btn-${variant || 'danger'}`" @click="emit('confirm')">
              {{ confirmText || "Confirm" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>
