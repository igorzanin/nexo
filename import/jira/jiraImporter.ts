import * as fs from "fs";
import { parseStringPromise } from "xml2js";
import { ArchiveUtils } from "../util/archive";
import { createGuid, currentTimestamp, parseArgs } from "../util/utils";

interface JiraIssue {
  key: string[];
  summary: string[];
  description?: string[];
  status?: string[];
  priority?: string[];
  assignee?: string[];
  duedate?: string[];
  resolution?: string[];
  labels?: { label: string[] }[];
}

interface JiraProject {
  id: string[];
  name: string[];
  description?: string[];
  issues?: JiraIssue[];
}

function htmlToMarkdown(html: string): string {
  return html
    .replace(/<h1>([\s\S]*?)<\/h1>/gi, "# $1\n\n")
    .replace(/<h2>([\s\S]*?)<\/h2>/gi, "## $1\n\n")
    .replace(/<h3>([\s\S]*?)<\/h3>/gi, "### $1\n\n")
    .replace(/<b>([\s\S]*?)<\/b>/gi, "**$1**")
    .replace(/<i>([\s\S]*?)<\/i>/gi, "*$1*")
    .replace(/<a href="([^"]+)">([\s\S]*?)<\/a>/gi, "[$2]($1)")
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<li>([\s\S]*?)<\/li>/gi, "- $1\n")
    .replace(/<ul>([\s\S]*?)<\/ul>/gi, "$1")
    .replace(/<p>([\s\S]*?)<\/p>/gi, "$1\n\n")
    .replace(/<[^>]+>/g, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function convert(project: JiraProject) {
  const boards: any[] = [];
  const blocks: any[] = [];
  const now = currentTimestamp();

  const boardId = createGuid();
  const viewId = createGuid();

  const propStatus = { id: createGuid(), name: "Status", type: "select", options: [] as { id: string; value: string; color: string }[] };
  const propPriority = { id: createGuid(), name: "Priority", type: "select", options: [] as { id: string; value: string; color: string }[] };
  const propAssignee = { id: createGuid(), name: "Assignee", type: "person", options: [] };
  const propDueDate = { id: createGuid(), name: "Due Date", type: "date", options: [] };
  const propResolution = { id: createGuid(), name: "Resolution", type: "select", options: [] as { id: string; value: string; color: string }[] };
  const propLabels = { id: createGuid(), name: "Labels", type: "multiSelect", options: [] as { id: string; value: string; color: string }[] };

  boards.push({
    id: boardId,
    teamId: "",
    channelId: "",
    type: "P",
    title: project.name[0],
    description: project.description?.[0] || "",
    icon: "",
    showDescription: false,
    isTemplate: false,
    templateVersion: 0,
    minimumRole: "",
    cardProperties: [propStatus, propPriority, propAssignee, propDueDate, propResolution, propLabels],
    createAt: now,
    updateAt: now,
    deleteAt: 0,
  });

  blocks.push({
    id: viewId,
    boardId,
    parentId: "",
    type: "view",
    title: "Board view",
    fields: { viewType: "board", cardOrder: [], visiblePropertyIds: [] },
    schema: 1,
    createAt: now,
    updateAt: now,
    deleteAt: 0,
  });

  const seenStatuses = new Set<string>();
  const seenPriorities = new Set<string>();
  const seenResolutions = new Set<string>();
  const seenLabels = new Set<string>();

  const issues = project.issues || [];
  for (const issue of issues) {
    const cardId = createGuid();
    const properties: Record<string, string | string[]> = {};

    if (issue.status?.[0] && !seenStatuses.has(issue.status[0])) {
      seenStatuses.add(issue.status[0]);
      propStatus.options.push({ id: createGuid(), value: issue.status[0], color: "propColorBlue" });
    }
    if (issue.status?.[0]) {
      const opt = propStatus.options.find((o) => o.value === issue.status[0]);
      if (opt) properties[propStatus.id] = opt.id;
    }

    if (issue.priority?.[0] && !seenPriorities.has(issue.priority[0])) {
      seenPriorities.add(issue.priority[0]);
      propPriority.options.push({ id: createGuid(), value: issue.priority[0], color: "propColorYellow" });
    }
    if (issue.priority?.[0]) {
      const opt = propPriority.options.find((o) => o.value === issue.priority[0]);
      if (opt) properties[propPriority.id] = opt.id;
    }

    if (issue.resolution?.[0] && !seenResolutions.has(issue.resolution[0])) {
      seenResolutions.add(issue.resolution[0]);
      propResolution.options.push({ id: createGuid(), value: issue.resolution[0], color: "propColorGray" });
    }
    if (issue.resolution?.[0]) {
      const opt = propResolution.options.find((o) => o.value === issue.resolution[0]);
      if (opt) properties[propResolution.id] = opt.id;
    }

    if (issue.assignee?.[0]) {
      properties[propAssignee.id] = issue.assignee[0];
    }
    if (issue.duedate?.[0]) {
      properties[propDueDate.id] = issue.duedate[0];
    }

    const labels = issue.labels?.[0]?.label || [];
    const labelValues: string[] = [];
    for (const label of labels) {
      if (!seenLabels.has(label)) {
        seenLabels.add(label);
        propLabels.options.push({ id: createGuid(), value: label, color: "propColorGreen" });
      }
      const opt = propLabels.options.find((o) => o.value === label);
      if (opt) labelValues.push(opt.id);
    }
    if (labelValues.length > 0) {
      properties[propLabels.id] = labelValues;
    }

    const descHtml = issue.description?.[0] || "";
    const descMarkdown = descHtml ? htmlToMarkdown(descHtml) : "";

    blocks.push({
      id: cardId,
      boardId,
      parentId: "",
      type: "card",
      title: issue.summary?.[0] || issue.key?.[0] || "",
      fields: {
        icon: "",
        isTemplate: false,
        properties,
        contentOrder: [],
      },
      schema: 1,
      createAt: now,
      updateAt: now,
      deleteAt: 0,
    });

    if (descMarkdown) {
      const textId = createGuid();
      blocks.push({
        id: textId,
        boardId,
        parentId: cardId,
        type: "text",
        title: descMarkdown,
        fields: {},
        schema: 1,
        createAt: now,
        updateAt: now,
        deleteAt: 0,
      });
    }
  }

  return { boards, blocks };
}

async function main() {
  const args = parseArgs(process.argv);
  const inputFile = args.i || args.input;
  const outputFile = (args.o || args.output || "archive.boardarchive") as string;

  if (!inputFile) {
    console.error("Usage: npx ts-node jiraImporter.ts -i <input.xml> [-o output]");
    process.exit(1);
  }

  const content = fs.readFileSync(inputFile as string, "utf-8");
  const parsed = await parseStringPromise(content);

  const rss = parsed.rss?.channel?.[0]?.item;
  const issues: JiraIssue[] = (rss || []).map((item: any) => ({
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
  const project: JiraProject = { id: ["1"], name: [projectName], issues };

  const { boards, blocks } = convert(project);
  const archive = ArchiveUtils.buildBlockArchive(boards, blocks);
  fs.writeFileSync(outputFile as string, archive, "utf-8");
  console.log(`Written ${outputFile} (${boards.length} boards, ${blocks.length} blocks)`);
}

if (require.main === module) {
  main();
}

export { convert, htmlToMarkdown };
