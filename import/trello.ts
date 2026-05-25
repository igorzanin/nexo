import * as fs from "fs";
import { AxiosInstance } from "axios";
import { z } from "zod";
import { convert } from "./trello/importTrello";
import { importToBoard } from "./client";

const CheckItemSchema = z.object({
  id: z.string(),
  name: z.string(),
  state: z.string(),
});

const ChecklistSchema = z.object({
  id: z.string(),
  idCard: z.string(),
  checkItems: z.array(CheckItemSchema),
});

const ListSchema = z.object({
  id: z.string(),
  name: z.string(),
  closed: z.boolean().optional(),
  pos: z.number().optional(),
});

const CardSchema = z.object({
  id: z.string(),
  name: z.string(),
  idList: z.string(),
  closed: z.boolean().optional(),
  desc: z.string().optional(),
  due: z.string().nullable().optional(),
  pos: z.number().optional(),
  idChecklists: z.array(z.string()).optional(),
});

export const TrelloBoardSchema = z.object({
  name: z.string(),
  desc: z.string().optional(),
  lists: z.array(ListSchema).optional(),
  cards: z.array(CardSchema).optional(),
  checklists: z.array(ChecklistSchema).optional(),
});

export async function run(file: string, boardId: string, client: AxiosInstance): Promise<void> {
  const raw = JSON.parse(fs.readFileSync(file, "utf-8"));
  const data = TrelloBoardSchema.parse(raw);
  const { boards, blocks } = convert(data as any);
  const cardProperties = boards[0]?.cardProperties as unknown[] | undefined;
  console.log(`Converting Trello board: "${data.name}" (${blocks.length} blocks)`);
  await importToBoard(client, boardId, blocks, cardProperties);
  console.log(`✓ Imported ${blocks.length} blocks into board ${boardId}`);
}
