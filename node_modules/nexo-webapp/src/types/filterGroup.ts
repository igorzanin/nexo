import { FilterClause, createFilterClause } from "./filterClause";

export interface FilterGroup {
  operation: "and" | "or";
  filters: Array<FilterClause | FilterGroup>;
}

export function createFilterGroup(partial?: Partial<FilterGroup>): FilterGroup {
  return {
    operation: partial?.operation ?? "and",
    filters: partial?.filters ?? [],
  };
}
