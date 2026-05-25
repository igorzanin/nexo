import { watch } from "vue";
import type { BoardStore } from "../../stores/boardStore";

export function useTitleAndIcon(boardStore: any) {
  watch(
    () => boardStore.currentBoard,
    (board) => {
      if (board) {
        document.title = `${board.title} - Nexo`;
        const icon = document.querySelector("link[rel~=icon]") as HTMLLinkElement;
        // favicon remains unchanged in this version
      } else {
        document.title = "Nexo";
      }
    }
  );
}
