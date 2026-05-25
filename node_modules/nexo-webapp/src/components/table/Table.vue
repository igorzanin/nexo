<script setup lang="ts">
import { computed } from "vue";
import type { Board, IPropertyTemplate } from "../../types/board";
import type { BoardView } from "../../types/boardView";
import type { Block } from "../../types/block";
import { useMutator } from "../../composables/useMutator";
import TableHeader from "./TableHeader.vue";
import TableRow from "./TableRow.vue";

const props = defineProps<{
  board: Board;
  view: BoardView;
  cards: Block[];
}>();

const emit = defineEmits<{
  (e: "openCard", cardId: string): void;
}>();

const mutator = useMutator();

const visiblePropertyIds = computed(() => {
  const visible = props.view.fields.visiblePropertyIds;
  if (visible && visible.length > 0) return visible;
  return props.board.cardProperties?.map((p: IPropertyTemplate) => p.id) || [];
});

const properties = computed(() => props.board.cardProperties || []);

async function updateProperty(cardId: string, propertyId: string, value: string) {
  const card = props.cards.find((c) => c.id === cardId);
  if (!card) return;
  const patch = {
    fields: {
      ...card.fields,
      properties: {
        ...card.fields?.properties,
        [propertyId]: value,
      },
    },
  };
  try {
    await mutator.patchBlock(props.board, card, patch);
  } catch {
    // silently fail
  }
}
</script>

<template>
  <div class="table-view overflow-auto flex-grow-1">
    <table class="table table-hover table-sm mb-0">
      <TableHeader :properties="properties" :visible-property-ids="visiblePropertyIds" />
      <tbody>
        <TableRow
          v-for="card in cards"
          :key="card.id"
          :card="card"
          :properties="properties"
          :visible-property-ids="visiblePropertyIds"
          @open-card="emit('openCard', $event)"
          @update-property="updateProperty(card.id, $event.propertyId, $event.value)"
        />
        <tr v-if="cards.length === 0">
          <td :colspan="visiblePropertyIds.length + 1" class="text-center text-muted small py-4">
            No cards yet. Add a card to get started.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
