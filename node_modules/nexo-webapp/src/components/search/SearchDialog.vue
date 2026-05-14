<script setup lang="ts">
import { ref, watch } from "vue";

const emit = defineEmits<{
  (e: "close"): void;
  (e: "select", cardId: string): void;
}>();

const query = ref("");
const results = ref<{ id: string; title: string }[]>([]);
const searching = ref(false);

let debounceTimer: ReturnType<typeof setTimeout>;

watch(query, (val) => {
  clearTimeout(debounceTimer);
  if (!val.trim()) {
    results.value = [];
    return;
  }
  searching.value = true;
  debounceTimer = setTimeout(async () => {
    searching.value = false;
  }, 300);
});
</script>

<template>
  <Teleport to="#app-modal">
    <div class="modal-backdrop fade show" @click="emit('close')" />
    <div class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <input
              v-model="query"
              type="text"
              class="form-control"
              placeholder="Search cards..."
              autofocus
            />
            <button type="button" class="btn-close" @click="emit('close')" />
          </div>
          <div class="modal-body">
            <div v-if="searching" class="text-center text-muted py-3">Searching...</div>
            <div v-else-if="results.length === 0 && query" class="text-center text-muted py-3">No results</div>
            <div v-else>
              <div
                v-for="r in results"
                :key="r.id"
                class="p-2 rounded cursor-pointer hover-bg"
                @click="emit('select', r.id)"
              >
                {{ r.title || "Untitled card" }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>
