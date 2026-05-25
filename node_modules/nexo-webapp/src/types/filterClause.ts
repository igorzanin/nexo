export type FilterCondition =
  | "includes"
  | "notIncludes"
  | "isEmpty"
  | "isNotEmpty"
  | "isSet"
  | "isNotSet"
  | "is"
  | "contains"
  | "notContains"
  | "startsWith"
  | "notStartsWith"
  | "endsWith"
  | "notEndsWith"
  | "isBefore"
  | "isAfter";

export const ALL_FILTER_CONDITIONS: FilterCondition[] = [
  "includes",
  "notIncludes",
  "isEmpty",
  "isNotEmpty",
  "isSet",
  "isNotSet",
  "is",
  "contains",
  "notContains",
  "startsWith",
  "notStartsWith",
  "endsWith",
  "notEndsWith",
  "isBefore",
  "isAfter",
];

export interface FilterClause {
  propertyId: string;
  condition: FilterCondition;
  values: string[];
}

export function createFilterClause(partial?: Partial<FilterClause>): FilterClause {
  return {
    propertyId: partial?.propertyId ?? "",
    condition: partial?.condition ?? "includes",
    values: partial?.values ?? [],
  };
}
