import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { Block } from "../types/block";
import type { BoardView } from "../types/boardView";
import * as api from "../api";

export const useCardStore = defineStore("cards", () => {
  const cards = ref<Record<string, Block>>({});
  const templates = ref<Record<string, Block>>({});

  const cardList = computed(() => Object.values(cards.value));

  function setCard(card: Block) {
    if (card.fields?.isTemplate) {
      templates.value[card.id] = card;
    } else {
      cards.value[card.id] = card;
    }
  }

  function removeCard(cardId: string) {
    delete cards.value[cardId];
  }

  async function fetchCards(boardId: string) {
    const data = await api.getCards(boardId);
    cards.value = {};
    for (const card of data) {
      setCard(card);
    }
  }

  async function createCard(boardId: string, data: Partial<Block>) {
    const card = await api.createCard(boardId, data);
    setCard(card);
    return card;
  }

  function getCardsForView(boardId: string, view: BoardView): Block[] {
    let filtered = Object.values(cards.value).filter((c) => c.boardId === boardId);
    if (view.fields.cardOrder.length > 0) {
      const orderMap = new Map(view.fields.cardOrder.map((id, i) => [id, i]));
      filtered.sort((a, b) => (orderMap.get(a.id) ?? Infinity) - (orderMap.get(b.id) ?? Infinity));
    }
    return filtered;
  }

  return {
    cards, templates, cardList,
    setCard, removeCard, fetchCards, createCard, getCardsForView,
  };
});
