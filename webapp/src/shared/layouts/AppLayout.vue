<script setup lang="ts">
import type { Board } from "../../types/board";
import Sidebar from "../components/Sidebar.vue";

withDefaults(defineProps<{
  brandText?: string;
  teamName?: string;
  boards?: Board[];
  activeBoard?: string;
  footerSettingsLabel?: string;
}>(), {
  brandText: "Nexo",
  teamName: "",
  boards: () => [],
  activeBoard: "",
  footerSettingsLabel: "Settings",
});

const emit = defineEmits<{
  (e: "createBoard"): void;
}>();
</script>

<template>
  <div class="d-flex" style="height: 100vh; overflow: hidden;">
    <Sidebar
      :brand-text="brandText"
      :team-name="teamName"
      :boards="boards"
      :active-board="activeBoard"
      :footer-settings-label="footerSettingsLabel"
      @create-board="emit('createBoard')"
    />
    <main class="flex-grow-1 d-flex flex-column overflow-hidden bg-body-secondary">
      <slot />
    </main>
  </div>
</template>
