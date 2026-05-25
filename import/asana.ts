import * as fs from "fs";
import { AxiosInstance } from "axios";
import { z } from "zod";
import { convert } from "./asana/importAsana";
import { importToBoard } from "./client";

const AsanaProjectSchema = z.object({
  id: z.number(),
  name: z.string(),
  notes: z.string().optional(),
});

const AsanaSectionSchema = z.object({
  id: z.number(),
  name: z.string(),
});

const AsanaTaskSchema = z.object({
  id: z.number(),
  name: z.string(),
  notes: z.string().optional(),
  completed: z.boolean().optional(),
  due_on: z.string().optional(),
  assignee: z.object({ id: z.number(), name: z.string() }).optional(),
  projects: z.array(z.object({ id: z.number(), name: z.string() })).optional(),
  tags: z.array(z.object({ id: z.number(), name: z.string() })).optional(),
  parent_id: z.number().optional(),
});

export const AsanaExportSchema = z.object({
  projects: z.array(AsanaProjectSchema).optional(),
  sections: z.record(z.array(AsanaSectionSchema)).optional(),
  items: z.array(AsanaTaskSchema),
});

export async function run(file: string, boardId: string, client: AxiosInstance): Promise<void> {
  const raw = JSON.parse(fs.readFileSync(file, "utf-8"));
  const data = AsanaExportSchema.parse(raw);
  const { boards, blocks } = convert(data as any);
  const cardProperties = boards[0]?.cardProperties as unknown[] | undefined;
  console.log(`Converting Asana export (${blocks.length} blocks)`);
  await importToBoard(client, boardId, blocks, cardProperties);
  console.log(`✓ Imported ${blocks.length} blocks into board ${boardId}`);
}
