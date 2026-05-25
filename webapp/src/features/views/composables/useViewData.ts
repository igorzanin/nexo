/**
 * useViewData — loads board + cards + views for a given boardId and
 * provides derived data for all view types.
 */
import { ref, computed, onMounted } from "vue";
import type { Board, IPropertyTemplate } from "../../../types/board";
import type { Block } from "../../../types/block";
import type { BoardView } from "../../../types/boardView";
import type { FilterClause } from "../../../types/filterClause";
import { useViewStore } from "../../../stores/viewStore";
import { useBoardStore } from "../../../stores/boardStore";
import { useCardStore } from "../../../stores/cardStore";
import * as api from "../../../api";

export function useViewData(boardId: string) {
  const viewStore = useViewStore();
  const boardStore = useBoardStore();
  const cardStore = useCardStore();

  const status = ref<"idle" | "loading" | "error">("loading");
  const errorMessage = ref("");
  const activeViewId = ref("");
  const searchQuery = ref("");
  const showProperties = ref(false);
  const showFilter = ref(false);
  const showSort = ref(false);
  const filterClauses = ref<FilterClause[]>([]);

  const board = computed<Board | undefined>(() => boardStore.boards[boardId]);
  const properties = computed<IPropertyTemplate[]>(() => board.value?.cardProperties ?? []);

  const activeView = computed<BoardView | undefined>(() =>
    activeViewId.value ? (viewStore.views[activeViewId.value] as BoardView | undefined) : undefined
  );

  const groupById = computed<string | null>(() =>
    activeView.value?.fields?.groupById ?? null
  );

  const visiblePropertyIds = computed<string[]>(() =>
    activeView.value?.fields?.visiblePropertyIds ?? properties.value.map((p) => p.id)
  );

  const visibleProperties = computed<IPropertyTemplate[]>(() =>
    properties.value.filter((p) => visiblePropertyIds.value.includes(p.id))
  );

  const allCards = computed<Block[]>(() => cardStore.cardList.filter((c) => c.boardId === boardId));

  const filteredCards = computed<Block[]>(() => {
    let cards = allCards.value;

    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase();
      cards = cards.filter((c) => c.title.toLowerCase().includes(q));
    }

    if (filterClauses.value.length) {
      cards = cards.filter((card) =>
        filterClauses.value.every((clause) => {
          const cardProps = (card.fields?.properties as Record<string, unknown>) ?? {};
          const val = String(cardProps[clause.propertyId] ?? "").toLowerCase();
          const clauseVal = (clause.values[0] ?? "").toLowerCase();
          switch (clause.condition) {
            case "contains":
            case "includes": return val.includes(clauseVal);
            case "notContains":
            case "notIncludes": return !val.includes(clauseVal);
            case "is": return val === clauseVal;
            case "isEmpty":
            case "isNotSet": return !val;
            case "isNotEmpty":
            case "isSet": return !!val;
            default: return true;
          }
        })
      );
    }

    return cards;
  });

  function groupedCards(propId: string | null): Array<{ label: string; optionId: string; cards: Block[] }> {
    if (!propId) return [{ label: "All cards", optionId: "", cards: filteredCards.value }];
    const prop = properties.value.find((p) => p.id === propId);
    if (!prop?.options?.length) return [{ label: "All cards", optionId: "", cards: filteredCards.value }];

    const groups = prop.options.map((opt) => ({
      label: opt.value,
      optionId: opt.id,
      cards: filteredCards.value.filter((c) => {
        const cardProps = (c.fields?.properties as Record<string, unknown>) ?? {};
        return cardProps[propId] === opt.id;
      }),
    }));

    const ungrouped = filteredCards.value.filter((c) => {
      const cardProps = (c.fields?.properties as Record<string, unknown>) ?? {};
      return !prop.options.some((opt) => opt.id === cardProps[propId]);
    });

    if (ungrouped.length) groups.push({ label: "No value", optionId: "", cards: ungrouped });
    return groups;
  }

  async function load() {
    status.value = "loading";
    errorMessage.value = "";
    try {
      const [boardData, blocks] = await Promise.all([
        api.getBoard(boardId),
        api.getBlocks(boardId),
      ]);
      boardStore.setBoard(boardData);

      const views = blocks.filter((b) => b.type === "view") as BoardView[];
      for (const v of views) viewStore.setView(v);
      if (views.length && !activeViewId.value) activeViewId.value = views[0].id;

      const cards = blocks.filter((b) => b.type === "card");
      for (const c of cards) cardStore.setCard(c);

      status.value = "idle";
    } catch (e: unknown) {
      errorMessage.value = e instanceof Error ? e.message : "Failed to load board";
      status.value = "error";
    }
  }

  onMounted(load);

  return {
    status, errorMessage, board, properties,
    activeViewId, activeView, groupById, visibleProperties, visiblePropertyIds,
    allCards, filteredCards, groupedCards,
    searchQuery, showProperties, showFilter, showSort, filterClauses,
  };
}
