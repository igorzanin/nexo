import axios, { AxiosInstance } from "axios";

export interface LegacyBlock {
  id: string;
  boardId: string;
  parentId: string;
  type: string;
  title: string;
  fields: Record<string, unknown>;
  schema?: number;
}

export function createClient(baseUrl: string, token: string): AxiosInstance {
  return axios.create({
    baseURL: baseUrl.replace(/\/$/, ""),
    headers: { Authorization: `Bearer ${token}` },
  });
}

/**
 * Imports legacy blocks into a nexo board via the API.
 * Handles two-pass import so child blocks reference correct parent IDs.
 */
export async function importToBoard(
  client: AxiosInstance,
  boardId: string,
  legacyBlocks: LegacyBlock[],
  cardProperties?: unknown[]
): Promise<void> {
  if (cardProperties && cardProperties.length > 0) {
    await client.patch(`/api/v1/boards/${boardId}`, { card_properties: cardProperties });
  }

  const topLevel = legacyBlocks.filter((b) => !b.parentId || b.parentId === "");
  const children = legacyBlocks.filter((b) => b.parentId && b.parentId !== "");

  // old ID → new API-assigned ID
  const idMap = new Map<string, string>();
  const BATCH = 50;

  for (let i = 0; i < topLevel.length; i += BATCH) {
    const chunk = topLevel.slice(i, i + BATCH);
    const payload = chunk.map((b) => ({
      board_id: boardId,
      parent_id: "",
      type: b.type,
      title: b.title || "",
      fields: b.fields || {},
      schema: b.schema ?? 1,
    }));
    const resp = await client.post(`/api/v1/boards/${boardId}/blocks/batch`, payload);
    const created: { id: string }[] = resp.data;
    for (let j = 0; j < chunk.length; j++) {
      idMap.set(chunk[j].id, created[j].id);
    }
  }

  for (let i = 0; i < children.length; i += BATCH) {
    const chunk = children.slice(i, i + BATCH);
    const payload = chunk.map((b) => ({
      board_id: boardId,
      parent_id: idMap.get(b.parentId) ?? b.parentId,
      type: b.type,
      title: b.title || "",
      fields: b.fields || {},
      schema: b.schema ?? 1,
    }));
    await client.post(`/api/v1/boards/${boardId}/blocks/batch`, payload);
  }
}
