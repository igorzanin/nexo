<script setup lang="ts">
import { RouterView } from "vue-router";
import FlashMessages from "./components/flash/FlashMessages.vue";
</script>

<template>
  <RouterView :key="$route.fullPath" />
  <FlashMessages />
</template>
