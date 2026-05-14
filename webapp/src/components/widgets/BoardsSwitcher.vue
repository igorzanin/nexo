<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useBoardStore } from "../../stores";

const emit = defineEmits<{
  (e: "close"): void;
}>();

const router = useRouter();
const boardStore = useBoardStore();
const query = ref("");

const filtered = ref(boardStore.boardList);

function search(val: string) {
  query.value = val;
  if (!val.trim()) {
    filtered.value = boardStore.boardList;
  } else {
    const q = val.toLowerCase();
    filtered.value = boardStore.boardList.filter((b) => b.title.toLowerCase().includes(q));
  }
}

function select(boardId: string) {
  router.push(`/board/${boardId}`);
  emit("close");
}
</script>

<template>
  <Teleport to="#app-modal">
    <div class="modal-backdrop fade show" @click="emit('close')" />
    <div class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-body p-0">
            <div class="p-3 border-bottom">
              <input
                v-model="query"
                type="text"
                class="form-control"
                placeholder="Search boards..."
                @input="search(query)"
                autofocus
              />
            </div>
            <div class="p-2" style="max-height: 300px; overflow-y: auto;">
              <div
                v-for="board in filtered"
                :key="board.id"
                class="d-flex align-items-center px-3 py-2 small rounded cursor-pointer"
                @click="select(board.id)"
              >
                <span class="me-2">{{ board.icon || "📋" }}</span>
                <span class="text-truncate">{{ board.title }}</span>
              </div>
              <div v-if="filtered.length === 0" class="text-center text-muted small py-4">
                No boards found
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>
