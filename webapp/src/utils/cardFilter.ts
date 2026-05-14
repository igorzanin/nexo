import type { FilterGroup, FilterClause } from "../types/filterGroup";

export function evaluateFilterGroup(group: FilterGroup | null, card: Record<string, unknown>): boolean {
  if (!group) return true;

  const { operation, filters } = group;
  if (!filters || filters.length === 0) return true;

  if (operation === "and") {
    return filters.every((f) => {
      if ("operation" in f) return evaluateFilterGroup(f as FilterGroup, card);
      return evaluateFilterClause(f as FilterClause, card);
    });
  }

  if (operation === "or") {
    return filters.some((f) => {
      if ("operation" in f) return evaluateFilterGroup(f as FilterGroup, card);
      return evaluateFilterClause(f as FilterClause, card);
    });
  }

  return true;
}

function evaluateFilterClause(clause: FilterClause, card: Record<string, unknown>): boolean {
  const { propertyId, condition, values } = clause;
  const value = card[propertyId];

  switch (condition) {
    case "includes":
      return values?.some((v) => String(value) === v) ?? false;
    case "notIncludes":
      return !values?.some((v) => String(value) === v);
    case "isEmpty":
      return !value || value === "";
    case "isNotEmpty":
      return !!value;
    case "is":
      return values?.some((v) => String(value) === v) ?? false;
    case "isNot":
      return !values?.some((v) => String(value) === v);
    default:
      return true;
  }
}
