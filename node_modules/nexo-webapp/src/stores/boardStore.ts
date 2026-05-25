import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { Board, BoardMember } from "../types/board";
import * as api from "../api";

export const useBoardStore = defineStore("boards", () => {
  const boards = ref<Record<string, Board>>({});
  const current = ref("");
  const templates = ref<Record<string, Board>>({});
  const membersInBoards = ref<Record<string, Record<string, BoardMember>>>({});
  const myBoardMemberships = ref<Record<string, BoardMember>>({});

  const currentBoard = computed(() => boards.value[current.value]);
  const boardList = computed(() => Object.values(boards.value));
  const templateList = computed(() => Object.values(templates.value));

  function setBoard(board: Board) {
    if (board.isTemplate) {
      templates.value[board.id] = board;
    } else {
      boards.value[board.id] = board;
    }
  }

  function removeBoard(boardId: string) {
    delete boards.value[boardId];
  }

  function setMembers(boardId: string, members: BoardMember[]) {
    membersInBoards.value[boardId] = {};
    for (const m of members) {
      membersInBoards.value[boardId][m.userId] = m;
    }
  }

  async function fetchBoards(teamId: string) {
    const data = await api.getBoards(teamId);
    for (const board of data) {
      setBoard(board);
    }
  }

  async function fetchBoard(boardId: string) {
    const data = await api.getBoard(boardId);
    setBoard(data);
  }

  async function createBoard(data: Partial<Board>) {
    const board = await api.createBoard(data);
    setBoard(board);
    return board;
  }

  async function patchBoard(boardId: string, data: Partial<Board>) {
    const board = await api.patchBoard(boardId, data);
    setBoard(board);
    return board;
  }

  async function deleteBoard(boardId: string) {
    await api.deleteBoard(boardId);
    removeBoard(boardId);
  }

  return {
    boards, current, templates, membersInBoards, myBoardMemberships,
    currentBoard, boardList, templateList,
    setBoard, removeBoard, setMembers,
    fetchBoards, fetchBoard, createBoard, patchBoard, deleteBoard,
  };
});
