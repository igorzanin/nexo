<script setup lang="ts">
import { computed, ref } from "vue";
import type { Board, IPropertyTemplate } from "../../types/board";
import type { BoardView } from "../../types/boardView";
import type { Block } from "../../types/block";
import { useMutator } from "../../composables/useMutator";
import { useFlashMessage } from "../../composables/useFlashMessage";
import { useCalculations } from "../../composables/useCalculations";
import KanbanColumn from "./KanbanColumn.vue";
import draggable from "vuedraggable";

const props = defineProps<{
  board: Board;
  view: BoardView;
  cards: Block[];
}>();

const emit = defineEmits<{
  (e: "openCard", cardId: string): void;
  (e: "addCard", columnId?: string): void;
}>();

const mutator = useMutator();
const { show } = useFlashMessage();
const collapsedColumns = ref<Set<string>>(new Set());
const dragging = ref(false);

const groupByProperty = computed(() => {
  const propId = props.view.fields.groupById;
  if (!propId) return null;
  return props.board.cardProperties?.find((p: IPropertyTemplate) => p.id === propId) || null;
});

const groupPropId = computed(() => groupByProperty.value?.id || null);

const columns = computed(() => {
  const prop = groupByProperty.value;
  if (!prop) return [{ id: "default", title: "Cards", key: "default", cards: [...props.cards] }];
  const groups = new Map<string, Block[]>();
  groups.set("", []);
  for (const opt of prop.options || []) {
    groups.set(opt.id, []);
  }
  for (const card of props.cards) {
    const val = card.fields?.properties?.[prop.id];
    if (typeof val === "string" && groups.has(val)) {
      groups.get(val)?.push(card);
    } else {
      groups.get("")?.push(card);
    }
  }
  return Array.from(groups.entries()).map(([id, cards]) => {
    const opt = prop.options?.find((o) => o.id === id);
    return {
      id,
      key: id || "__empty__",
      title: opt?.value || (id === "" ? "No status" : id),
      color: opt?.color || undefined,
      cards,
    };
  });
});

function toggleCollapse(columnId: string) {
  if (collapsedColumns.value.has(columnId)) {
    collapsedColumns.value.delete(columnId);
  } else {
    collapsedColumns.value.add(columnId);
  }
}

async function onCardMove(evt: any, targetColumnId: string) {
  const cardId = evt.item?.dataset?.cardId || evt.item?.id;
  if (!cardId || !groupPropId.value) return;
  const card = props.cards.find((c) => c.id === cardId);
  if (!card) return;
  const newValue = targetColumnId === "default" || targetColumnId === "" ? "" : targetColumnId;
  const oldValue = card.fields?.properties?.[groupPropId.value]?.toString() || "";
  if (newValue === oldValue) return;
  const patch = {
    fields: {
      ...card.fields,
      properties: {
        ...card.fields?.properties,
        [groupPropId.value]: newValue,
      },
    },
  };
  const undoPatch = {
    fields: {
      ...card.fields,
      properties: {
        ...card.fields?.properties,
        [groupPropId.value]: oldValue,
      },
    },
  };
  try {
    await mutator.patchBlock(props.board.id, cardId, patch, undoPatch);
  } catch (e: any) {
    show(e.response?.data?.detail || "Failed to move card", "error");
  }
}
</script>

<template>
  <div class="kanban d-flex gap-2 overflow-auto p-3" style="height: 100%;">
    <div v-for="col in columns" :key="col.key" class="kanban-column-wrapper d-flex flex-column" style="min-width: 260px; max-width: 300px;">
      <KanbanColumn
        :column="{ id: col.id, title: col.title, color: col.color }"
        :collapsed="collapsedColumns.has(col.id)"
        @toggle-collapse="toggleCollapse(col.id)"
        @add-card="emit('addCard', col.id)"
      >
        <template #cards>
          <div class="px-2 py-1 border-bottom bg-body small text-muted d-flex gap-2" style="font-size: 10px;">
            <span>{{ col.cards.length }} cards</span>
          </div>
          <draggable
            :list="col.cards"
            group="kanban-cards"
            item-key="id"
            ghost-class="kanban-card-ghost"
            class="p-2 flex-grow-1 overflow-auto"
            :style="{ maxHeight: collapsedColumns.has(col.id) ? '0' : 'calc(100vh - 240px)' }"
            @change="(evt: any) => onCardMove(evt, col.id)"
            @start="dragging = true"
            @end="dragging = false"
          >
            <template #item="{ element: card }">
              <div class="kanban-card card shadow-sm border-0 mb-2 cursor-pointer" @click="emit('openCard', card.id)">
                <div class="card-body p-2">
                  <div v-if="card.fields?.icon" class="fs-6 mb-1">{{ card.fields.icon }}</div>
                  <h6 class="card-title small mb-0">{{ card.title || "Untitled" }}</h6>
                </div>
              </div>
            </template>
          </draggable>
        </template>
      </KanbanColumn>
    </div>
  </div>
</template>

<style scoped>
.kanban-card-ghost {
  opacity: 0.4;
}
</style>
