import * as fs from "fs";
import { ArchiveUtils } from "../util/archive";
import { createGuid, currentTimestamp, parseArgs } from "../util/utils";

interface TodoistProject {
  id: number;
  name: string;
  color?: string;
  indent?: number;
}

interface TodoistSection {
  id: number;
  project_id: number;
  name: string;
  order?: number;
}

interface TodoistTask {
  id: number;
  project_id: number;
  section_id?: number;
  content: string;
  description?: string;
  due?: { date?: string; datetime?: string };
  priority?: number;
  labels?: string[];
  parent_id?: number;
  order?: number;
}

interface TodoistExport {
  projects: TodoistProject[];
  sections?: TodoistSection[];
  items: TodoistTask[];
}

function convert(data: TodoistExport) {
  const allBoards: any[] = [];
  const allBlocks: any[] = [];
  const now = currentTimestamp();

  const projects = data.projects || [];
  const allItems = data.items || [];
  const allSections = data.sections || [];

  for (const project of projects) {
    const boardId = createGuid();
    const viewId = createGuid();

    const projectTasks = allItems.filter((t) => t.project_id === project.id);
    const projectSections = allSections.filter((s) => s.project_id === project.id);

    const propPriority = {
      id: createGuid(),
      name: "Priority",
      type: "select",
      options: [
        { id: createGuid(), value: "p1", color: "propColorRed" },
        { id: createGuid(), value: "p2", color: "propColorOrange" },
        { id: createGuid(), value: "p3", color: "propColorBlue" },
        { id: createGuid(), value: "p4", color: "propColorGray" },
      ],
    };

    const propSection = {
      id: createGuid(),
      name: "Section",
      type: "select",
      options: [] as { id: string; value: string; color: string }[],
    };

    boards.push({
      id: boardId,
      teamId: "",
      channelId: "",
      type: "P",
      title: project.name,
      description: "",
      icon: "",
      showDescription: false,
      isTemplate: false,
      templateVersion: 0,
      minimumRole: "",
      cardProperties: [propPriority, propSection],
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
      fields: { viewType: "board", cardOrder: [] },
      schema: 1,
      createAt: now,
      updateAt: now,
      deleteAt: 0,
    });

    const sectionMap = new Map<number, string>();
    for (const section of projectSections) {
      const optId = createGuid();
      propSection.options.push({ id: optId, value: section.name, color: "propColorBlue" });
      sectionMap.set(section.id, optId);
    }

    for (const task of projectTasks) {
      const cardId = createGuid();
      const properties: Record<string, string | string[]> = {};

      if (task.priority) {
        const p = `p${task.priority}`;
        const opt = propPriority.options.find((o) => o.value === p);
        if (opt) properties[propPriority.id] = opt.id;
      }

      if (task.section_id) {
        const optId = sectionMap.get(task.section_id);
        if (optId) properties[propSection.id] = optId;
      }

      blocks.push({
        id: cardId,
        boardId,
        parentId: "",
        type: "card",
        title: task.content,
        fields: {
          icon: "",
          isTemplate: false,
          properties,
          contentOrder: [],
        },
        schema: 1,
        createAt: task.due?.date ? new Date(task.due.date).getTime() : now,
        updateAt: now,
        deleteAt: 0,
      });

      if (task.description) {
        const textId = createGuid();
        blocks.push({
          id: textId,
          boardId,
          parentId: cardId,
          type: "text",
          title: task.description,
          fields: {},
          schema: 1,
          createAt: now,
          updateAt: now,
          deleteAt: 0,
        });
      }
    }
  }

  return { boards: allBoards, blocks: allBlocks };
}

function main() {
  const args = parseArgs(process.argv);
  const inputFile = (args.i || args.input) as string;
  const outputFile = (args.o || args.output || "archive.boardarchive") as string;

  if (!inputFile) {
    console.error("Usage: npx ts-node importTodoist.ts -i <input.json> [-o output]");
    process.exit(1);
  }

  const content = fs.readFileSync(inputFile, "utf-8");
  const data: TodoistExport = JSON.parse(content);

  if (!data.projects && data.items) {
    const items = data.items || [];
    const projectIds = [...new Set(items.map((t) => t.project_id))];
    data.projects = projectIds.map((pid) => ({ id: pid, name: `Project ${pid}` }));
  }

  const { boards, blocks } = convert(data);
  const archive = ArchiveUtils.buildBlockArchive(boards, blocks);
  fs.writeFileSync(outputFile, archive, "utf-8");
  console.log(`Written ${outputFile} (${boards.length} boards, ${blocks.length} blocks)`);
}

if (require.main === module) {
  main();
}

export { convert };
