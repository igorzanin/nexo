import * as fs from "fs";
import * as path from "path";
import { AxiosInstance } from "axios";
import { parse } from "csv-parse/sync";
import { convertRowsToBoard } from "./notion/importNotion";
import { importToBoard } from "./client";

export async function run(filePath: string, boardId: string, client: AxiosInstance): Promise<void> {
  const stat = fs.statSync(filePath);
  let csvContent: string;
  let folderPath: string;
  let csvFilename: string;

  if (stat.isDirectory()) {
    const files = fs.readdirSync(filePath).filter((f) => f.endsWith(".csv"));
    if (files.length === 0) throw new Error("No CSV files found in directory");
    csvContent = fs.readFileSync(path.join(filePath, files[0]), "utf-8");
    folderPath = filePath;
    csvFilename = files[0];
  } else {
    csvContent = fs.readFileSync(filePath, "utf-8");
    folderPath = path.dirname(filePath);
    csvFilename = path.basename(filePath);
  }

  const rows = parse(csvContent, { columns: true, skip_empty_lines: true });
  const { boards, blocks } = convertRowsToBoard(rows as any[], folderPath, csvFilename);
  const cardProperties = boards[0]?.cardProperties as unknown[] | undefined;
  console.log(`Converting Notion export (${blocks.length} blocks)`);
  await importToBoard(client, boardId, blocks, cardProperties);
  console.log(`✓ Imported ${blocks.length} blocks into board ${boardId}`);
}
