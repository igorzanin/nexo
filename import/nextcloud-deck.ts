import { AxiosInstance } from "axios";
import { fetchBoard, convert } from "./nextcloud-deck/importDeck";
import { importToBoard } from "./client";

export interface DeckImportOptions {
  url: string;
  user: string;
  pass: string;
  deckBoard: number;
}

export async function run(
  opts: DeckImportOptions,
  boardId: string,
  client: AxiosInstance
): Promise<void> {
  console.log(`Fetching Nextcloud Deck board ${opts.deckBoard} from ${opts.url}...`);
  const board = await fetchBoard(opts.url, opts.user, opts.pass, opts.deckBoard);
  const { boards, blocks } = convert(board);
  const cardProperties = boards[0]?.cardProperties as unknown[] | undefined;
  console.log(`Converting Deck board: "${board.title}" (${blocks.length} blocks)`);
  await importToBoard(client, boardId, blocks, cardProperties);
  console.log(`✓ Imported ${blocks.length} blocks into board ${boardId}`);
}
