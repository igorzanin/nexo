<script setup lang="ts">
import { RouterView } from "vue-router";
import FlashMessages from "./components/flash/FlashMessages.vue";
</script>

<template>
  <RouterView />
  <FlashMessages />
</template>
