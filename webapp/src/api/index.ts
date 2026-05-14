import api from "./client";
import type { Board, BoardPatch } from "../types/board";
import type { Block, BlockPatch } from "../types/block";
import type { BoardMember } from "../types/board";
import type { Category } from "../types/category";

function toSnake(obj: Record<string, unknown>): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(obj)) {
    const snake = key.replace(/[A-Z]/g, (c) => `_${c.toLowerCase()}`);
    result[snake] = value;
  }
  return result;
}
import type { IUser } from "../types/user";
import type { ITeam } from "../types/team";
import type { ISharing } from "../types/sharing";
import type { Subscription } from "../types/subscription";

export async function login(username: string, password: string) {
  const res = await api.post("/login", { username, password });
  return res.data;
}

export async function register(username: string, email: string, password: string) {
  const res = await api.post("/register", { username, email, password });
  return res.data;
}

export async function getTeams(): Promise<ITeam[]> {
  const res = await api.get("/teams");
  return res.data;
}

export async function createTeam(title: string): Promise<ITeam> {
  const res = await api.post("/teams", { title, signupToken: "" });
  return res.data;
}

export async function getBoards(teamId: string): Promise<Board[]> {
  const res = await api.get(`/teams/${teamId}/boards`);
  return res.data;
}

export async function getBoard(boardId: string): Promise<Board> {
  const res = await api.get(`/boards/${boardId}`);
  return res.data;
}

export async function createBoard(data: Partial<Board>): Promise<Board> {
  const res = await api.post("/boards", toSnake(data as any));
  return res.data;
}

export async function patchBoard(boardId: string, data: BoardPatch): Promise<Board> {
  const res = await api.patch(`/boards/${boardId}`, toSnake(data as any));
  return res.data;
}

export async function deleteBoard(boardId: string): Promise<void> {
  await api.delete(`/boards/${boardId}`);
}

export async function duplicateBoard(boardId: string): Promise<Board> {
  const res = await api.post(`/boards/${boardId}/duplicate`);
  return res.data;
}

export async function getBlocks(boardId: string): Promise<Block[]> {
  const res = await api.get(`/boards/${boardId}/blocks`);
  return res.data;
}

export async function createBlock(boardId: string, data: Partial<Block>): Promise<Block> {
  const res = await api.post(`/boards/${boardId}/blocks`, toSnake(data as any));
  return res.data;
}

export async function patchBlock(boardId: string, blockId: string, data: BlockPatch): Promise<Block> {
  const res = await api.patch(`/boards/${boardId}/blocks/${blockId}`, toSnake(data as any));
  return res.data;
}

export async function deleteBlock(boardId: string, blockId: string): Promise<void> {
  await api.delete(`/boards/${boardId}/blocks/${blockId}`);
}

export async function getCards(boardId: string): Promise<Block[]> {
  const res = await api.get(`/boards/${boardId}/cards`);
  return res.data;
}

export async function createCard(boardId: string, data: Partial<Block>): Promise<Block> {
  const res = await api.post(`/boards/${boardId}/cards`, toSnake(data as any));
  return res.data;
}

export async function getMembers(boardId: string): Promise<BoardMember[]> {
  const res = await api.get(`/boards/${boardId}/members`);
  return res.data;
}

export async function getCategories(teamId: string): Promise<Category[]> {
  const res = await api.get(`/teams/${teamId}/categories`);
  return res.data;
}

export async function getSharing(boardId: string): Promise<ISharing> {
  const res = await api.get(`/boards/${boardId}/sharing`);
  return res.data;
}

export async function postSharing(boardId: string, data: { enabled: boolean; token: string }): Promise<ISharing> {
  const res = await api.post(`/boards/${boardId}/sharing`, data);
  return res.data;
}

export async function getSubscriptions(subscriberId: string): Promise<Subscription[]> {
  const res = await api.get(`/subscriptions/${subscriberId}`);
  return res.data;
}

export async function changePassword(userId: string, oldPassword: string, newPassword: string): Promise<void> {
  await api.post(`/users/${userId}/changepassword`, {
    old_password: oldPassword,
    new_password: newPassword,
  });
}

export { api as client };
