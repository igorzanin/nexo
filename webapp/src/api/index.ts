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

function toCamel(obj: unknown): unknown {
  if (Array.isArray(obj)) return obj.map(toCamel);
  if (obj !== null && typeof obj === "object") {
    const result: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(obj as Record<string, unknown>)) {
      const camelKey = key.replace(/_([a-z])/g, (_, c) => c.toUpperCase());
      result[camelKey] = toCamel(value);
    }
    return result;
  }
  return obj;
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
  return toCamel(res.data) as ITeam[];
}

export async function createTeam(title: string): Promise<ITeam> {
  const res = await api.post("/teams", { title, signupToken: "" });
  return toCamel(res.data) as ITeam;
}

export async function getBoards(teamId: string): Promise<Board[]> {
  const res = await api.get(`/teams/${teamId}/boards`);
  return toCamel(res.data) as Board[];
}

export async function getBoard(boardId: string): Promise<Board> {
  const res = await api.get(`/boards/${boardId}`);
  return toCamel(res.data) as Board;
}

export async function createBoard(data: Partial<Board>): Promise<Board> {
  const res = await api.post("/boards", toSnake(data as any));
  return toCamel(res.data) as Board;
}

export async function patchBoard(boardId: string, data: BoardPatch): Promise<Board> {
  const res = await api.patch(`/boards/${boardId}`, toSnake(data as any));
  return toCamel(res.data) as Board;
}

export async function deleteBoard(boardId: string): Promise<void> {
  await api.delete(`/boards/${boardId}`);
}

export async function duplicateBoard(boardId: string): Promise<Board> {
  const res = await api.post(`/boards/${boardId}/duplicate`);
  return toCamel(res.data) as Board;
}

export async function getBlocks(boardId: string): Promise<Block[]> {
  const res = await api.get(`/boards/${boardId}/blocks`);
  return toCamel(res.data) as Block[];
}

export async function createBlock(boardId: string, data: Partial<Block>): Promise<Block> {
  const res = await api.post(`/boards/${boardId}/blocks`, toSnake(data as any));
  return toCamel(res.data) as Block;
}

export async function patchBlock(boardId: string, blockId: string, data: BlockPatch): Promise<Block> {
  const res = await api.patch(`/boards/${boardId}/blocks/${blockId}`, toSnake(data as any));
  return toCamel(res.data) as Block;
}

export async function deleteBlock(boardId: string, blockId: string): Promise<void> {
  await api.delete(`/boards/${boardId}/blocks/${blockId}`);
}

export async function getCards(boardId: string): Promise<Block[]> {
  const res = await api.get(`/boards/${boardId}/cards`);
  return toCamel(res.data) as Block[];
}

export async function createCard(boardId: string, data: Partial<Block>): Promise<Block> {
  const res = await api.post(`/boards/${boardId}/cards`, toSnake(data as any));
  return toCamel(res.data) as Block;
}

export async function getMembers(boardId: string): Promise<BoardMember[]> {
  const res = await api.get(`/boards/${boardId}/members`);
  return toCamel(res.data) as BoardMember[];
}

export async function createCategory(teamId: string, name: string): Promise<Category> {
  const res = await api.post(`/teams/${teamId}/categories`, { name });
  return toCamel(res.data) as Category;
}

export async function renameCategory(categoryId: string, name: string): Promise<void> {
  await api.patch(`/categories/${categoryId}`, { name });
}

export async function deleteCategory(categoryId: string): Promise<void> {
  await api.delete(`/categories/${categoryId}`);
}

export async function getCategories(teamId: string): Promise<Category[]> {
  const res = await api.get(`/teams/${teamId}/categories`);
  return toCamel(res.data) as Category[];
}

export async function getSharing(boardId: string): Promise<ISharing> {
  const res = await api.get(`/boards/${boardId}/sharing`);
  return toCamel(res.data) as ISharing;
}

export async function postSharing(boardId: string, data: { enabled: boolean; token: string }): Promise<ISharing> {
  const res = await api.post(`/boards/${boardId}/sharing`, data);
  return toCamel(res.data) as ISharing;
}

export async function getSubscriptions(subscriberId: string): Promise<Subscription[]> {
  const res = await api.get(`/subscriptions/${subscriberId}`);
  return toCamel(res.data) as Subscription[];
}

export async function patchUserConfig(userId: string, config: Record<string, unknown>): Promise<void> {
  await api.patch(`/users/${userId}/config`, config);
}

export async function changePassword(userId: string, oldPassword: string, newPassword: string): Promise<void> {
  await api.post(`/users/${userId}/changepassword`, {
    old_password: oldPassword,
    new_password: newPassword,
  });
}

export async function uploadFile(teamId: string, boardId: string, file: File): Promise<{ url: string }> {
  const form = new FormData();
  form.append("file", file);
  const res = await api.post(`/files/${teamId}/${boardId}`, form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return toCamel(res.data) as { url: string };
}

export { api as client };
