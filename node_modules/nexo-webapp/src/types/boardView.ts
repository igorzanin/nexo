import { Block, createBlock } from "./block";
import { FilterGroup, createFilterGroup } from "./filterGroup";

export type IViewType = "board" | "table" | "gallery" | "calendar";

export interface ISortOption {
  propertyId: string;
  reversed: boolean;
}

export interface BoardViewFields {
  viewType: IViewType;
  groupById?: string;
  dateDisplayPropertyId?: string;
  sortOptions: ISortOption[];
  filter: FilterGroup;
  cardOrder: string[];
  visiblePropertyIds: string[];
  columnWidths: Record<string, number>;
  columnCalculations: Record<string, string>;
  kanbanCalculations: Record<string, { calculation: string; propertyId: string }>;
  defaultTemplateId?: string;
}

export type BoardView = Block & { fields: BoardViewFields };

export function createBoardView(partial?: Partial<BoardView>): BoardView {
  return {
    ...createBlock({ type: "view", ...partial }),
    fields: {
      viewType: partial?.fields?.viewType ?? "board",
      sortOptions: partial?.fields?.sortOptions ?? [],
      filter: partial?.fields?.filter ?? createFilterGroup(),
      cardOrder: partial?.fields?.cardOrder ?? [],
      visiblePropertyIds: partial?.fields?.visiblePropertyIds ?? [],
      columnWidths: partial?.fields?.columnWidths ?? {},
      columnCalculations: partial?.fields?.columnCalculations ?? {},
      kanbanCalculations: partial?.fields?.kanbanCalculations ?? {},
    },
  };
}

export function smartViewUpdate(oldView: BoardView, newView: BoardView): BoardView {
  const result = { ...newView };
  if (JSON.stringify(oldView.fields.cardOrder) === JSON.stringify(newView.fields.cardOrder)) {
    result.fields = { ...result.fields, cardOrder: oldView.fields.cardOrder };
  }
  return result;
}
