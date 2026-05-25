<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useLanguageStore } from "../../../stores/languageStore";
import SetLanguageSubmenu from "./SetLanguageSubmenu.vue";
import SetThemeSubmenu from "./SetThemeSubmenu.vue";

withDefaults(defineProps<{
  label?: string;
}>(), {
  label: "Settings",
});

const router = useRouter();
const languageStore = useLanguageStore();

const activePanel = ref<"settings" | "theme" | "language">("settings");
const currentTheme = ref<"default" | "dark" | "light">(
  (localStorage.getItem("nexo-theme") as "dark" | "light" | null) ?? "default"
);
const currentLanguage = computed<"en" | "pt-BR" | "es">(() =>
  (languageStore.value === "pt-BR" ? "pt-BR" : languageStore.value === "es" ? "es" : "en")
);
const appVersion = import.meta.env.VITE_APP_VERSION || "dev";

function selectTheme(theme: "default" | "dark" | "light") {
  currentTheme.value = theme;
  if (theme === "default") {
    document.documentElement.removeAttribute("data-bs-theme");
    localStorage.removeItem("nexo-theme");
  } else {
    document.documentElement.setAttribute("data-bs-theme", theme);
    localStorage.setItem("nexo-theme", theme);
  }
  activePanel.value = "settings";
}

function selectLanguage(language: "en" | "pt-BR" | "es") {
  languageStore.setLanguage(language);
  activePanel.value = "settings";
}
</script>

<template>
  <div class="dropup">
    <button
      type="button"
      class="btn btn-outline-secondary w-100 text-start dropdown-toggle"
      data-bs-toggle="dropdown"
      data-bs-auto-close="outside"
      aria-expanded="false"
      @click="activePanel = 'settings'"
    >
      {{ label }}
    </button>

    <ul class="dropdown-menu w-100">
      <!-- Settings panel -->
      <template v-if="activePanel === 'settings'">
        <li>
          <button type="button" class="dropdown-item" @click="router.push('/settings')">
            Settings
          </button>
        </li>
        <li>
          <button type="button" class="dropdown-item" @click.stop="activePanel = 'theme'">
            Set theme ▶
          </button>
        </li>
        <li>
          <button type="button" class="dropdown-item" @click.stop="activePanel = 'language'">
            Set language ▶
          </button>
        </li>
        <li><hr class="dropdown-divider" /></li>
        <li><span class="dropdown-item-text text-muted small">{{ appVersion }}</span></li>
      </template>

      <!-- Theme submenu inline -->
      <template v-else-if="activePanel === 'theme'">
        <SetThemeSubmenu
          :current-theme="currentTheme"
          @back="activePanel = 'settings'"
          @select-theme="selectTheme"
        />
      </template>

      <!-- Language submenu inline -->
      <template v-else-if="activePanel === 'language'">
        <SetLanguageSubmenu
          :current-language="currentLanguage"
          @back="activePanel = 'settings'"
          @select-language="selectLanguage"
        />
      </template>
    </ul>
  </div>
</template>
