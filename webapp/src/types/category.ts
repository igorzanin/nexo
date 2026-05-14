export interface Category {
  id: string;
  name: string;
  userID: string;
  teamID: string;
  type: "system" | "custom";
  collapsed: boolean;
  sortOrder: number;
  createAt: number;
  updateAt: number;
  deleteAt: number;
}

export interface CategoryBoard {
  categoryId: string;
  boardId: string;
  sortOrder: number;
  hidden: boolean;
}

export interface CategoryBoards {
  id: string;
  name: string;
  userID: string;
  teamID: string;
  createAt: number;
  updateAt: number;
  deleteAt: number;
  collapsed: boolean;
  sortOrder: number;
  type: "system" | "custom";
  isNew?: boolean;
  boardMetadata: { boardID: string; hidden: boolean }[];
}
