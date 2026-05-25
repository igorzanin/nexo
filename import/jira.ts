import * as fs from "fs";
import { AxiosInstance } from "axios";
import { parseStringPromise } from "xml2js";
import { convert } from "./jira/jiraImporter";
import { importToBoard } from "./client";

export async function run(file: string, boardId: string, client: AxiosInstance): Promise<void> {
  const content = fs.readFileSync(file, "utf-8");
  const parsed = await parseStringPromise(content);

  const rss = parsed.rss?.channel?.[0]?.item;
  const issues = (rss || []).map((item: any) => ({
    key: item.key,
    summary: item.summary,
    description: item.description,
    status: item.status ? [item.status[0]._] : undefined,
    priority: item.priority ? [item.priority[0]._] : undefined,
    assignee: item.assignee ? [item.assignee[0]._] : undefined,
    duedate: item.duedate,
    resolution: item.resolution ? [item.resolution[0]._] : undefined,
    labels: item.labels,
  }));

  const projectName = parsed.rss?.channel?.[0]?.title?.[0] || "Jira Import";
  const project = { id: ["1"], name: [projectName], issues };

  const { blocks } = convert(project as any);
  console.log(`Converting Jira project: "${projectName}" (${blocks.length} blocks)`);
  await importToBoard(client, boardId, blocks);
  console.log(`✓ Imported ${blocks.length} blocks into board ${boardId}`);
}
