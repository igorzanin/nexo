import * as fs from "fs";
import { ArchiveUtils } from "../util/archive";
import { createGuid, currentTimestamp, parseArgs } from "../util/utils";

interface TrelloList {
  id: string;
  name: string;
  closed?: boolean;
  pos?: number;
}

interface TrelloChecklist {
  id: string;
  name: string;
  checkItems: { id: string; name: string; state: "complete" | "incomplete" }[];
}

interface TrelloLabel {
  id: string;
  name: string;
  color?: string;
}

interface TrelloCard {
  id: string;
  name: string;
  desc?: string;
  due?: string;
  idList: string;
  labels?: TrelloLabel[];
  idChecklists?: string[];
  closed?: boolean;
  pos?: number;
}

interface TrelloBoard {
  id: string;
  name: string;
  desc?: string;
  lists?: TrelloList[];
  cards?: TrelloCard[];
  checklists?: TrelloChecklist[];
  labels?: TrelloLabel[];
}

function convert(data: TrelloBoard) {
  const boards: any[] = [];
  const blocks: any[] = [];
  const now = currentTimestamp();

  const boardId = createGuid();
  const viewId = createGuid();

  const propList = {
    id: createGuid(),
    name: "List",
    type: "select",
    options: [] as { id: string; value: string; color: string }[],
  };

  const propDueDate = { id: createGuid(), name: "Due Date", type: "date", options: [] };

  boards.push({
    id: boardId,
    teamId: "",
    channelId: "",
    type: "P",
    title: data.name,
    description: data.desc || "",
    icon: "",
    showDescription: false,
    isTemplate: false,
    templateVersion: 0,
    minimumRole: "",
    cardProperties: [propList, propDueDate],
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

  const lists = (data.lists || []).filter((l) => !l.closed).sort((a, b) => (a.pos || 0) - (b.pos || 0));
  const listOptions = new Map<string, string>();

  for (const list of lists) {
    const optId = createGuid();
    propList.options.push({ id: optId, value: list.name, color: "propColorBlue" });
    listOptions.set(list.id, optId);
  }

  const cards = (data.cards || []).filter((c) => !c.closed).sort((a, b) => (a.pos || 0) - (b.pos || 0));
  const checklists = data.checklists || [];

  for (const card of cards) {
    const cardId = createGuid();
    const properties: Record<string, string | string[]> = {};

    const listOpt = listOptions.get(card.idList);
    if (listOpt) properties[propList.id] = listOpt;

    if (card.due) {
      properties[propDueDate.id] = card.due;
    }

    blocks.push({
      id: cardId,
      boardId,
      parentId: "",
      type: "card",
      title: card.name,
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

    if (card.desc) {
      const textId = createGuid();
      blocks.push({
        id: textId,
        boardId,
        parentId: cardId,
        type: "text",
        title: card.desc,
        fields: {},
        schema: 1,
        createAt: now,
        updateAt: now,
        deleteAt: 0,
      });
    }

    const cardChecklists = checklists.filter((cl) => card.idChecklists?.includes(cl.id));
    for (const cl of cardChecklists) {
      for (const item of cl.checkItems) {
        const checkboxId = createGuid();
        blocks.push({
          id: checkboxId,
          boardId,
          parentId: cardId,
          type: "checkbox",
          title: item.name,
          fields: { checked: item.state === "complete" },
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
  const inputFile = (args.i || args.input) as string;
  const outputFile = (args.o || args.output || "archive.boardarchive") as string;

  if (!inputFile) {
    console.error("Usage: npx ts-node importTrello.ts -i <input.json> [-o output]");
    process.exit(1);
  }

  const content = fs.readFileSync(inputFile, "utf-8");
  const data: TrelloBoard = JSON.parse(content);
  const { boards, blocks } = convert(data);
  const archive = ArchiveUtils.buildBlockArchive(boards, blocks);
  fs.writeFileSync(outputFile, archive, "utf-8");
  console.log(`Written ${outputFile} (${boards.length} boards, ${blocks.length} blocks)`);
}

if (require.main === module) {
  main();
}

export { convert };
