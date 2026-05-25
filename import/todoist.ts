import * as fs from "fs";
import { AxiosInstance } from "axios";
import { z } from "zod";
import { convert } from "./todoist/importTodoist";
import { importToBoard } from "./client";

const TodoistProjectSchema = z.object({
  id: z.number(),
  name: z.string(),
  color: z.string().optional(),
  indent: z.number().optional(),
});

const TodoistSectionSchema = z.object({
  id: z.number(),
  project_id: z.number(),
  name: z.string(),
  order: z.number().optional(),
});

const TodoistTaskSchema = z.object({
  id: z.number(),
  project_id: z.number(),
  section_id: z.number().optional(),
  content: z.string(),
  description: z.string().optional(),
  due: z
    .object({ date: z.string().optional(), datetime: z.string().optional() })
    .optional(),
  priority: z.number().optional(),
  labels: z.array(z.string()).optional(),
  parent_id: z.number().optional(),
  order: z.number().optional(),
});

export const TodoistExportSchema = z.object({
  projects: z.array(TodoistProjectSchema),
  sections: z.array(TodoistSectionSchema).optional(),
  items: z.array(TodoistTaskSchema),
});

export async function run(file: string, boardId: string, client: AxiosInstance): Promise<void> {
  const raw = JSON.parse(fs.readFileSync(file, "utf-8"));
  const data = TodoistExportSchema.parse(raw);
  const { boards, blocks } = convert(data as any);
  const cardProperties = boards[0]?.cardProperties as unknown[] | undefined;
  console.log(`Converting Todoist export (${blocks.length} blocks)`);
  await importToBoard(client, boardId, blocks, cardProperties);
  console.log(`✓ Imported ${blocks.length} blocks into board ${boardId}`);
}
