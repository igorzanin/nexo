/**
 * useCollaboration — connects to WS for a given boardId and dispatches
 * real-time block updates to the card/view stores.
 */
import { onMounted, onUnmounted } from "vue";
import { useWebSocket } from "../../../shared/ws/useWebSocket";
import { useCardStore } from "../../../stores/cardStore";
import { useViewStore } from "../../../stores/viewStore";
import type { Block } from "../../../types/block";
import type { BoardView } from "../../../types/boardView";

export function useCollaboration(boardId: string) {
  const { connected, connect, disconnect, onMessage } = useWebSocket();
  const cardStore = useCardStore();
  const viewStore = useViewStore();

  let unsubWs: (() => void) | null = null;

  function handleMessage(data: unknown) {
    const msg = data as {
      action?: string;
      block?: Block;
      boardId?: string;
    };

    if (!msg.block) return;
    if (msg.boardId && msg.boardId !== boardId) return;

    const block = msg.block;

    switch (msg.action) {
      case "UPDATE_BLOCK":
        if (block.type === "card") cardStore.setCard(block);
        else if (block.type === "view") viewStore.setView(block as BoardView);
        break;
      case "DELETE_BLOCK":
        if (block.type === "card") cardStore.removeCard(block.id);
        else if (block.type === "view") viewStore.removeView(block.id);
        break;
    }
  }

  onMounted(() => {
    const token = localStorage.getItem("token") ?? "";
    if (token) connect(token);
    unsubWs = onMessage(handleMessage);
  });

  onUnmounted(() => {
    unsubWs?.();
    disconnect();
  });

  return { connected };
}
