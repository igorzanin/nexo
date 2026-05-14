<script setup lang="ts">
import { onMounted, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useBoardStore, useViewStore, useCardStore, useTeamStore, useUserStore, useSidebarStore } from "../../stores";
import { useWebSocket } from "../../composables/useWebSocket";
import { useTitleAndIcon } from "./useTitleAndIcon";
import { useUndoRedo } from "./useUndoRedo";
import Workspace from "../../components/workspace/Workspace.vue";
import * as api from "../../api";

const route = useRoute();
const router = useRouter();
const boardStore = useBoardStore();
const viewStore = useViewStore();
const cardStore = useCardStore();
const teamStore = useTeamStore();
const userStore = useUserStore();
const sidebarStore = useSidebarStore();

const token = localStorage.getItem("access_token") || "";
const ws = useWebSocket();
useTitleAndIcon(boardStore);
const { bind: bindUndoRedo, unbind: unbindUndoRedo } = useUndoRedo();

onMounted(async () => {
  const boardId = route.params.boardId as string;

  if (!teamStore.currentId) {
    await teamStore.fetchTeams();
    if (!teamStore.currentId) {
      await api.createTeam("My Workspace");
      await teamStore.fetchTeams();
    }
  }

  if (teamStore.currentId) {
    await Promise.all([
      boardStore.fetchBoards(teamStore.currentId),
      sidebarStore.fetchCategories(teamStore.currentId),
    ]);
  }

  if (!boardId && boardStore.boardList.length > 0) {
    router.replace(`/board/${boardStore.boardList[0].id}`);
    return;
  }

  if (boardId) {
    boardStore.current = boardId;
    await Promise.all([
      boardStore.fetchBoard(boardId).catch(() => {}),
      cardStore.fetchCards(boardId).catch(() => {}),
    ]);
    const blocks = await api.getBlocks(boardId).catch(() => [] as any[]);
    viewStore.updateFromBlocks(blocks.filter((b: any) => b.type === "view") as any);
    if (viewStore.viewList.length > 0 && !viewStore.current) {
      viewStore.current = viewStore.viewList[0].id;
    } else if (viewStore.viewList.length === 0) {
      try {
        const defaultView = await api.createBlock(boardId, {
          type: "view",
          title: "Board view",
          parentId: boardId,
          boardId,
          fields: { viewType: "board", cardOrder: [], visiblePropertyIds: [], sortOptions: [], groupById: "", filter: null },
        } as any);
        viewStore.setView(defaultView as any);
        viewStore.current = defaultView.id;
      } catch {
        // silently fail
      }
    }
  }

  if (token) ws.connect(token);
  bindUndoRedo();
});

onUnmounted(() => {
  ws.disconnect();
  unbindUndoRedo();
});
</script>

<template>
  <Workspace :board-id="route.params.boardId as string" />
</template>
