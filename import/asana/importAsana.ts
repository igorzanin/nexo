import * as fs from "fs";
import { ArchiveUtils } from "../util/archive";
import { createGuid, currentTimestamp, parseArgs } from "../util/utils";

interface AsanaTask {
  id: number;
  name: string;
  notes?: string;
  completed?: boolean;
  due_on?: string;
  assignee?: { id: number; name: string };
  projects?: { id: number; name: string }[];
  tags?: { id: number; name: string }[];
}

interface AsanaSection {
  id: number;
  name: string;
}

interface AsanaProject {
  id: number;
  name: string;
  notes?: string;
}

interface AsanaExport {
  projects?: AsanaProject[];
  sections?: Record<number, AsanaSection[]>;
  tasks?: Record<number, AsanaTask[]>;
}

function convert(data: AsanaExport) {
  const boards: any[] = [];
  const blocks: any[] = [];
  const now = currentTimestamp();

  const projects = data.projects || [];
  const allTasks = data.tasks || {};
  const allSections = data.sections || {};

  for (const project of projects) {
    const boardId = createGuid();
    const viewId = createGuid();

    boards.push({
      id: boardId,
      teamId: "",
      channelId: "",
      type: "P",
      title: project.name,
      description: project.notes || "",
      icon: "",
      showDescription: false,
      isTemplate: false,
      templateVersion: 0,
      minimumRole: "",
      cardProperties: [
        { id: createGuid(), name: "Section", type: "select", options: [] },
      ],
      createAt: now,
      updateAt: now,
      deleteAt: 0,
    });

    blocks.push({
      id: viewId,
      boardId,
      parentId: "",
      createdBy: "",
      modifiedBy: "",
      type: "view",
      title: "Board view",
      fields: { viewType: "board", cardOrder: [], visiblePropertyIds: [] },
      schema: 1,
      createAt: now,
      updateAt: now,
      deleteAt: 0,
    });

    const projectSections = allSections[project.id] || [];
    const sectionOptions: { id: string; value: string; color: string }[] = [];
    const sectionMap: Record<string, string> = {};

    for (const section of projectSections) {
      const optId = createGuid();
      sectionOptions.push({ id: optId, value: section.name, color: "propColorBlue" });
      sectionMap[section.id] = optId;
    }

    if (boards.length > 0) {
      const board = boards[boards.length - 1];
      board.cardProperties[0].options = sectionOptions;
    }

    const tasks = allTasks[project.id] || [];
    for (const task of tasks) {
      const cardId = createGuid();
      const properties: Record<string, string | string[]> = {};

      const assignee = task.assignee;
      if (assignee) {
        const propId = createGuid();
        if (!board.cardProperties.find((p: any) => p.name === "Assignee")) {
          board.cardProperties.push({ id: propId, name: "Assignee", type: "person", options: [] });
        }
        properties[propId] = assignee.name;
      }

      const dueDate = task.due_on;
      if (dueDate) {
        const propId = createGuid();
        if (!board.cardProperties.find((p: any) => p.name === "Due Date")) {
          board.cardProperties.push({ id: propId, name: "Due Date", type: "date", options: [] });
        }
        properties[propId] = dueDate;
      }

      blocks.push({
        id: cardId,
        boardId,
        parentId: "",
        createdBy: "",
        modifiedBy: "",
        type: "card",
        title: task.name,
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

      if (task.notes) {
        const textId = createGuid();
        blocks.push({
          id: textId,
          boardId,
          parentId: cardId,
          createdBy: "",
          modifiedBy: "",
          type: "text",
          title: task.notes,
          fields: {},
          schema: 1,
          createAt: now,
          updateAt: now,
          deleteAt: 0,
        });
      }
    }
  }

  return { boards, blocks };
}

function main() {
  const args = parseArgs(process.argv);
  const inputFile = args.i || args.input;
  const outputFile = (args.o || args.output || "archive.boardarchive") as string;

  if (!inputFile) {
    console.error("Usage: npx ts-node importAsana.ts -i <input.json> [-o output]");
    process.exit(1);
  }

  const content = fs.readFileSync(inputFile as string, "utf-8");
  const data: AsanaExport = JSON.parse(content);
  const { boards, blocks } = convert(data);
  const archive = ArchiveUtils.buildBlockArchive(boards, blocks);
  fs.writeFileSync(outputFile as string, archive, "utf-8");
  console.log(`Written ${outputFile} (${boards.length} boards, ${blocks.length} blocks)`);
}

if (require.main === module) {
  main();
}

export { convert };
