<template>
  <button
    type="button"
    class="btn btn-sm"
    :class="subscribed ? 'btn-warning' : 'btn-outline-secondary'"
    :disabled="loading"
    @click="toggle"
    :title="subscribed ? 'Unsubscribe from notifications' : 'Subscribe to notifications'"
  >
    <span v-if="loading" class="spinner-border spinner-border-sm" />
    <template v-else>
      <i :class="subscribed ? 'bi bi-bell-fill' : 'bi bi-bell'" />
      {{ subscribed ? "Subscribed" : "Subscribe" }}
    </template>
  </button>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useSubscriptionsStore } from "../stores/subscriptions.store";
import { useUserStore } from "../../../stores/userStore";

const props = defineProps<{
  blockId: string;
}>();

const subsStore = useSubscriptionsStore();
const userStore = useUserStore();
const loading = ref(false);

const userId = computed(() => userStore.me?.id ?? "");
const subscribed = computed(() => subsStore.isSubscribed(props.blockId, userId.value));

async function toggle() {
  if (!userId.value) return;
  loading.value = true;
  try {
    if (subscribed.value) {
      await subsStore.unsubscribe(props.blockId, userId.value);
    } else {
      await subsStore.subscribe(props.blockId, userId.value);
    }
  } finally {
    loading.value = false;
  }
}

onMounted(async () => {
  if (userId.value && !subsStore.subscriptions.length) {
    await subsStore.fetchSubscriptions(userId.value);
  }
});
</script>
