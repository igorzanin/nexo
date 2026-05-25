import * as fs from "fs";
import * as http from "http";
import { createGuid, currentTimestamp, parseArgs } from "../util/utils";
import { ArchiveUtils } from "../util/archive";

interface DeckBoard {
  id: number;
  title: string;
  description?: string;
  stacks?: DeckStack[];
}

interface DeckStack {
  id: number;
  title: string;
  cards?: DeckCard[];
}

interface DeckCard {
  id: number;
  title: string;
  description?: string;
  duedate?: string;
  labels?: DeckLabel[];
  comments?: DeckComment[];
}

interface DeckLabel {
  id: number;
  title: string;
  color?: string;
}

interface DeckComment {
  id: number;
  message: string;
  actorId?: string;
  creationDate?: string;
}

function apiRequest(url: string, username: string, password: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const options: http.RequestOptions = {
      hostname: parsed.hostname,
      port: parsed.port,
      path: parsed.pathname,
      method: "GET",
      headers: {
        Authorization: "Basic " + Buffer.from(`${username}:${password}`).toString("base64"),
        Accept: "application/json",
      },
    };

    const req = http.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => resolve(data));
    });
    req.on("error", reject);
    req.end();
  });
}

async function fetchBoard(baseUrl: string, username: string, password: string, boardId: number): Promise<DeckBoard> {
  const base = baseUrl.replace(/\/$/, "");
  const boardData = JSON.parse(await apiRequest(`${base}/index.php/apps/deck/api/v1.0/boards/${boardId}`, username, password));
  return boardData as DeckBoard;
}

function convert(board: DeckBoard) {
  const boards: any[] = [];
  const blocks: any[] = [];
  const now = currentTimestamp();

  const boardId = createGuid();
  const viewId = createGuid();

  const propStack = {
    id: createGuid(),
    name: "Stack",
    type: "select",
    options: [] as { id: string; value: string; color: string }[],
  };
  const propLabel = {
    id: createGuid(),
    name: "Labels",
    type: "multiSelect",
    options: [] as { id: string; value: string; color: string }[],
  };
  const propDueDate = { id: createGuid(), name: "Due Date", type: "date", options: [] };

  boards.push({
    id: boardId,
    teamId: "",
    channelId: "",
    type: "P",
    title: board.title,
    description: board.description || "",
    icon: "",
    showDescription: false,
    isTemplate: false,
    templateVersion: 0,
    minimumRole: "",
    cardProperties: [propStack, propLabel, propDueDate],
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

  const allLabels = new Map<number, DeckLabel>();

  for (const stack of board.stacks || []) {
    const stackOptId = createGuid();
    propStack.options.push({ id: stackOptId, value: stack.title, color: "propColorBlue" });

    for (const card of stack.cards || []) {
      for (const label of card.labels || []) {
        if (!allLabels.has(label.id)) {
          allLabels.set(label.id, label);
          propLabel.options.push({
            id: createGuid(),
            value: label.title,
            color: label.color ? `propColor${label.color.charAt(0).toUpperCase() + label.color.slice(1)}` : "propColorGreen",
          });
        }
      }
    }
  }

  for (const stack of board.stacks || []) {
    const stackOpt = propStack.options.find((o) => o.value === stack.title);

    for (const card of stack.cards || []) {
      const cardId = createGuid();
      const properties: Record<string, string | string[]> = {};

      if (stackOpt) properties[propStack.id] = stackOpt.id;

      if (card.duedate) {
        properties[propDueDate.id] = card.duedate;
      }

      if (card.labels && card.labels.length > 0) {
        const labelIds = card.labels
          .map((l) => propLabel.options.find((o) => o.value === l.title))
          .filter(Boolean)
          .map((o) => o!.id);
        if (labelIds.length > 0) {
          properties[propLabel.id] = labelIds;
        }
      }

      blocks.push({
        id: cardId,
        boardId,
        parentId: "",
        type: "card",
        title: card.title,
        fields: { icon: "", isTemplate: false, properties, contentOrder: [] },
        schema: 1,
        createAt: now,
        updateAt: now,
        deleteAt: 0,
      });

      if (card.description) {
        const textId = createGuid();
        blocks.push({
          id: textId,
          boardId,
          parentId: cardId,
          type: "text",
          title: card.description,
          fields: {},
          schema: 1,
          createAt: now,
          updateAt: now,
          deleteAt: 0,
        });
      }

      for (const comment of card.comments || []) {
        const commentId = createGuid();
        blocks.push({
          id: commentId,
          boardId,
          parentId: cardId,
          type: "comment",
          title: comment.message,
          fields: {},
          schema: 1,
          createAt: comment.creationDate ? new Date(comment.creationDate).getTime() : now,
          updateAt: now,
          deleteAt: 0,
        });
      }
    }
  }

  return { boards, blocks };
}

async function main() {
  const args = parseArgs(process.argv);
  const baseUrl = (args.url || args.baseUrl) as string;
  const username = (args.u || args.user) as string;
  const password = (args.p || args.pass || args.password) as string;
  const boardId = parseInt((args.b || args.boardId) as string, 10);
  const outputFile = (args.o || args.output || "archive.boardarchive") as string;

  if (!baseUrl || !username || !password || !boardId) {
    console.error("Usage: npx ts-node importDeck.ts --url <url> -u <user> -p <pass> -b <boardId> [-o output]");
    process.exit(1);
  }

  const board = await fetchBoard(baseUrl, username, password, boardId);
  const { boards, blocks } = convert(board);
  const archive = ArchiveUtils.buildBlockArchive(boards, blocks);
  fs.writeFileSync(outputFile, archive, "utf-8");
  console.log(`Written ${outputFile} (${boards.length} boards, ${blocks.length} blocks)`);
}

if (require.main === module) {
  main();
}

export { convert, fetchBoard };
