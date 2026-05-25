import { defineStore } from "pinia";
import { ref } from "vue";
import type { Subscription } from "../../../types/subscription";
import * as api from "../../../api";

export const useSubscriptionsStore = defineStore("subscriptions", () => {
  const subscriptions = ref<Subscription[]>([]);

  function isSubscribed(blockId: string, subscriberId: string): boolean {
    return subscriptions.value.some(
      (s) => s.blockId === blockId && s.subscriberId === subscriberId
    );
  }

  async function fetchSubscriptions(subscriberId: string): Promise<void> {
    subscriptions.value = await api.getSubscriptions(subscriberId);
  }

  async function subscribe(blockId: string, subscriberId: string): Promise<void> {
    const data = await api.subscribeBlock(blockId, subscriberId);
    subscriptions.value.push(data);
  }

  async function unsubscribe(blockId: string, subscriberId: string): Promise<void> {
    await api.unsubscribeBlock(blockId, subscriberId);
    subscriptions.value = subscriptions.value.filter(
      (s) => !(s.blockId === blockId && s.subscriberId === subscriberId)
    );
  }

  return { subscriptions, isSubscribed, fetchSubscriptions, subscribe, unsubscribe };
});
