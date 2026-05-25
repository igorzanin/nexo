<script setup lang="ts">
// BaseModal — wraps Bootstrap modal (static backdrop, accessible)
defineProps<{
  title: string;
  show: boolean;
  size?: "sm" | "lg" | "xl";
}>();
defineEmits<{ (e: "close"): void }>();
</script>

<template>
  <Teleport to="body">
    <div v-if="show" class="modal d-block" tabindex="-1" style="background: rgba(0,0,0,.4);" @click.self="$emit('close')">
      <div :class="['modal-dialog modal-dialog-centered', size ? `modal-${size}` : '']">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ title }}</h5>
            <button type="button" class="btn-close" @click="$emit('close')" />
          </div>
          <div class="modal-body">
            <slot />
          </div>
          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>
