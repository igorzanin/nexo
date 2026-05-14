import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { BoardView } from "../types/boardView";
import { smartViewUpdate } from "../types/boardView";
import * as api from "../api";

export const useViewStore = defineStore("views", () => {
  const current = ref("");
  const views = ref<Record<string, BoardView>>({});

  const currentView = computed(() => views.value[current.value]);
  const viewList = computed(() => Object.values(views.value));

  function setView(view: BoardView) {
    views.value[view.id] = view;
  }

  function removeView(viewId: string) {
    delete views.value[viewId];
  }

  function updateFromBlocks(blocks: BoardView[]) {
    for (const block of blocks) {
      if (block.type === "view") {
        const existing = views.value[block.id];
        if (existing) {
          views.value[block.id] = smartViewUpdate(existing, block);
        } else {
          views.value[block.id] = block;
        }
      }
    }
  }

  return {
    current, views, currentView, viewList,
    setView, removeView, updateFromBlocks,
  };
});
