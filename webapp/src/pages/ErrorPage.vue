<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const errors: Record<string, { title: string; message: string; action: string; link: string }> = {
  "not-logged-in": {
    title: "Session Expired",
    message: "Your session has expired. Please sign in again.",
    action: "Sign in",
    link: "/login",
  },
  "board-not-found": {
    title: "Board Not Found",
    message: "The board you're looking for doesn't exist or has been deleted.",
    action: "Go to Home",
    link: "/board",
  },
  "invalid-read-only-board": {
    title: "Access Denied",
    message: "You don't have permission to view this board.",
    action: "Sign in",
    link: "/login",
  },
};

const errorId = computed(() => (route.query.id as string) || "unknown");
const errorInfo = computed(() => errors[errorId.value] || {
  title: "Error",
  message: "An unexpected error occurred.",
  action: "Go to Home",
  link: "/board",
});
</script>

<template>
  <div class="d-flex align-items-center justify-content-center vh-100 bg-body-secondary">
    <div class="text-center">
      <h2 class="mb-3">{{ errorInfo.title }}</h2>
      <p class="text-muted mb-4">{{ errorInfo.message }}</p>
      <router-link :to="errorInfo.link" class="btn btn-primary">
        {{ errorInfo.action }}
      </router-link>
    </div>
  </div>
</template>
