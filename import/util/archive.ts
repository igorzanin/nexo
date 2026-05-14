interface BoardData {
  id: string;
  teamId: string;
  title: string;
  type: string;
  description?: string;
  icon?: string;
  cardProperties?: unknown[];
}

interface BlockData {
  id: string;
  boardId: string;
  parentId: string;
  type: string;
  title: string;
  fields: Record<string, unknown>;
  schema?: number;
  createAt: number;
  updateAt: number;
}

interface ArchiveHeader {
  version: number;
  date: number;
}

export class ArchiveUtils {
  static buildBlockArchive(boards: BoardData[], blocks: BlockData[]): string {
    const header: ArchiveHeader = {
      version: 1,
      date: Date.now(),
    };

    const lines: string[] = [JSON.stringify(header)];

    for (const board of boards) {
      lines.push(JSON.stringify({ type: "board", data: board }));
    }

    for (const block of blocks) {
      lines.push(JSON.stringify({ type: "block", data: block }));
    }

    return lines.join("\n") + "\n";
  }

  static parseBlockArchive(contents: string): { boards: BoardData[]; blocks: BlockData[] } {
    const lines = contents.trim().split("\n").filter((l) => l.trim());
    if (lines.length === 0) {
      throw new Error("Empty archive");
    }

    const header: ArchiveHeader = JSON.parse(lines[0]);
    if (!header.version || !header.date) {
      throw new Error("Invalid archive header");
    }

    const boards: BoardData[] = [];
    const blocks: BlockData[] = [];

    for (let i = 1; i < lines.length; i++) {
      const item = JSON.parse(lines[i]);
      switch (item.type) {
        case "board":
          boards.push(item.data);
          break;
        case "block":
          blocks.push(item.data);
          break;
        default:
          console.warn(`Unknown archive entry type: ${item.type}`);
      }
    }

    return { boards, blocks };
  }
}
