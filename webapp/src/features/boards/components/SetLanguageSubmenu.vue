<script setup lang="ts">
defineProps<{
  currentLanguage: string;
}>();

const emit = defineEmits<{
  (e: "back"): void;
  (e: "select-language", language: "en" | "pt-BR" | "es"): void;
}>();
</script>

<template>
  <li>
    <button type="button" class="dropdown-item" @click.stop="emit('back')">← Back</button>
  </li>
  <li>
    <button type="button" class="dropdown-item d-flex justify-content-between" @click.stop="emit('select-language', 'en')">
      <span>English</span><i v-if="currentLanguage === 'en'" class="bi bi-check"></i>
    </button>
  </li>
  <li>
    <button type="button" class="dropdown-item d-flex justify-content-between" @click.stop="emit('select-language', 'pt-BR')">
      <span>Português</span><i v-if="currentLanguage === 'pt-BR'" class="bi bi-check"></i>
    </button>
  </li>
  <li>
    <button type="button" class="dropdown-item d-flex justify-content-between" @click.stop="emit('select-language', 'es')">
      <span>Español</span><i v-if="currentLanguage === 'es'" class="bi bi-check"></i>
    </button>
  </li>
</template>