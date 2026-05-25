import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { IUser } from "../types/user";
import type { Subscription } from "../types/subscription";
import * as api from "../api";

export interface UserPreference {
  [key: string]: unknown;
}

export const useUserStore = defineStore("users", () => {
  const me = ref<IUser | null>(null);
  const boardUsers = ref<Record<string, IUser>>({});
  const loggedIn = ref<boolean | null>(null);
  const blockSubscriptions = ref<Subscription[]>([]);
  const myConfig = ref<Record<string, unknown>>({});

  const isLoggedIn = computed(() => loggedIn.value === true);
  const hasBoardUsers = computed(() => Object.keys(boardUsers.value).length > 0);

  function setMe(user: IUser) {
    me.value = user;
    loggedIn.value = true;
  }

  function clearMe() {
    me.value = null;
    loggedIn.value = false;
  }

  function addBoardUser(user: IUser) {
    boardUsers.value[user.id] = user;
  }

  async function updateMyConfig(config: Record<string, unknown>) {
    myConfig.value = { ...myConfig.value, ...config };
    if (me.value?.id) {
      await api.patchUserConfig(me.value.id, config).catch(() => {});
    }
  }

  async function fetchSubscriptions(subscriberId: string) {
    const data = await api.getSubscriptions(subscriberId);
    blockSubscriptions.value = data;
  }

  return {
    me, boardUsers, loggedIn, blockSubscriptions, myConfig,
    isLoggedIn, hasBoardUsers,
    setMe, clearMe, addBoardUser, updateMyConfig, fetchSubscriptions,
  };
});
