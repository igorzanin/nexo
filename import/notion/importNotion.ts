import * as fs from "fs";
import * as path from "path";
import { parse } from "csv-parse/sync";
import { ArchiveUtils } from "../util/archive";
import { createGuid, currentTimestamp, parseArgs } from "../util/utils";

interface NotionRow {
  [columnName: string]: string;
}

function convertRowsToBoard(rows: NotionRow[], folderPath: string, csvFilename: string) {
  const boards: any[] = [];
  const blocks: any[] = [];
  const now = currentTimestamp();

  const boardId = createGuid();
  const viewId = createGuid();
  const boardName = path.basename(folderPath) || csvFilename.replace(/\.csv$/i, "");

  const columnNames = rows.length > 0 ? Object.keys(rows[0]) : [];
  const propertyTemplates: { id: string; name: string; type: string; options: { id: string; value: string; color: string }[] }[] = [];

  const selectOptions = new Map<string, Set<string>>();

  for (const col of columnNames) {
    const values = new Set<string>();
    for (const row of rows) {
      const val = row[col]?.trim();
      if (val) values.add(val);
    }

    if (values.size > 0 && values.size <= 20) {
      const propId = createGuid();
      const options: { id: string; value: string; color: string }[] = [];
      for (const v of values) {
        options.push({ id: createGuid(), value: v, color: "propColorBlue" });
      }
      propertyTemplates.push({ id: propId, name: col, type: "select", options });
      selectOptions.set(col, values);
    } else {
      const propId = createGuid();
      propertyTemplates.push({ id: propId, name: col, type: "text", options: [] });
      selectOptions.set(col, new Set());
    }
  }

  boards.push({
    id: boardId,
    teamId: "",
    channelId: "",
    type: "P",
    title: boardName,
    description: "",
    icon: "",
    showDescription: false,
    isTemplate: false,
    templateVersion: 0,
    minimumRole: "",
    cardProperties: propertyTemplates,
    createAt: now,
    updateAt: now,
    deleteAt: 0,
  });

  blocks.push({
    id: viewId,
    boardId,
    parentId: "",
    type: "view",
    title: "Table view",
    fields: { viewType: "table", cardOrder: [], visiblePropertyIds: [] },
    schema: 1,
    createAt: now,
    updateAt: now,
    deleteAt: 0,
  });

  for (const row of rows) {
    const cardId = createGuid();
    const properties: Record<string, string | string[]> = {};
    let description = "";

    for (const col of columnNames) {
      const val = row[col]?.trim();
      if (!val) continue;

      const prop = propertyTemplates.find((p) => p.name === col);
      if (!prop) continue;

      if (prop.type === "select") {
        const opt = prop.options.find((o) => o.value === val);
        if (opt) properties[prop.id] = opt.id;
      } else if (prop.type === "text") {
        if (col.toLowerCase() === "description" || col.toLowerCase() === "notes") {
          description = val;
        } else {
          properties[prop.id] = val;
        }
      }
    }

    const title = row["Name"] || row["name"] || row["Title"] || row["title"] || `Card ${cardId.slice(0, 8)}`;

    blocks.push({
      id: cardId,
      boardId,
      parentId: "",
      type: "card",
      title,
      fields: { icon: "", isTemplate: false, properties, contentOrder: [] },
      schema: 1,
      createAt: now,
      updateAt: now,
      deleteAt: 0,
    });

    if (description) {
      const textId = createGuid();
      blocks.push({
        id: textId,
        boardId,
        parentId: cardId,
        type: "text",
        title: description,
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

function main() {
  const args = parseArgs(process.argv);
  const inputPath = (args.i || args.input) as string;
  const outputFile = (args.o || args.output || "archive.boardarchive") as string;

  if (!inputPath) {
    console.error("Usage: npx ts-node importNotion.ts -i <folder> [-o output]");
    process.exit(1);
  }

  const stat = fs.statSync(inputPath);
  let csvContent: string;
  let folderPath: string;
  let csvFilename: string;

  if (stat.isDirectory()) {
    const files = fs.readdirSync(inputPath).filter((f) => f.endsWith(".csv"));
    if (files.length === 0) {
      console.error("No CSV files found in folder");
      process.exit(1);
    }
    csvContent = fs.readFileSync(path.join(inputPath, files[0]), "utf-8");
    folderPath = inputPath;
    csvFilename = files[0];
  } else {
    csvContent = fs.readFileSync(inputPath, "utf-8");
    folderPath = path.dirname(inputPath);
    csvFilename = path.basename(inputPath);
  }

  const rows = parse(csvContent, { columns: true, skip_empty_lines: true }) as NotionRow[];
  const { boards, blocks } = convertRowsToBoard(rows, folderPath, csvFilename);
  const archive = ArchiveUtils.buildBlockArchive(boards, blocks);
  fs.writeFileSync(outputFile, archive, "utf-8");
  console.log(`Written ${outputFile} (${boards.length} boards, ${blocks.length} blocks)`);
}

if (require.main === module) {
  main();
}

export { convertRowsToBoard };
