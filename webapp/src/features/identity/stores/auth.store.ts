/**
 * features/identity/stores/auth.store.ts
 * Pinia store para autenticação: login, register, logout, changePassword.
 * Única fonte de verdade para token e usuário logado.
 */
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import * as api from "../../../api";
import { useUserStore } from "../../../stores/userStore";

export const useAuthStore = defineStore("auth", () => {
  const userStore = useUserStore();
  const loading = ref(false);
  const error = ref("");

  const isAuthenticated = computed(() => !!localStorage.getItem("access_token"));

  function clearError() {
    error.value = "";
  }

  async function login(username: string, password: string): Promise<void> {
    error.value = "";
    loading.value = true;
    try {
      const res = await api.login(username, password);
      localStorage.setItem("access_token", res.access_token);
      localStorage.setItem("refresh_token", res.refresh_token);
      userStore.setMe({ id: "", username, email: "", createAt: 0, updateAt: 0, deleteAt: 0 });
    } catch (e: any) {
      error.value = e.response?.data?.detail || "Invalid credentials";
      throw e;
    } finally {
      loading.value = false;
    }
  }

  async function register(username: string, email: string, password: string): Promise<void> {
    error.value = "";
    loading.value = true;
    try {
      const res = await api.register(username, email, password);
      localStorage.setItem("access_token", res.access_token);
      localStorage.setItem("refresh_token", res.refresh_token);
      userStore.setMe({ id: "", username, email, createAt: 0, updateAt: 0, deleteAt: 0 });
    } catch (e: any) {
      error.value = e.response?.data?.detail || "Registration failed";
      throw e;
    } finally {
      loading.value = false;
    }
  }

  function logout(): void {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    userStore.clearMe();
  }

  async function changePassword(oldPassword: string, newPassword: string): Promise<void> {
    error.value = "";
    loading.value = true;
    try {
      const token = localStorage.getItem("access_token") || "";
      const payload = JSON.parse(atob(token.split(".")[1]));
      const userId: string = payload?.sub || "me";
      await api.changePassword(userId, oldPassword, newPassword);
    } catch (e: any) {
      error.value = e.response?.data?.detail || "Failed to change password";
      throw e;
    } finally {
      loading.value = false;
    }
  }

  return { loading, error, isAuthenticated, clearError, login, register, logout, changePassword };
});
