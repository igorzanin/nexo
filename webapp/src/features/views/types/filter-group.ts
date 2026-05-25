// Re-exports filter types under feature-scoped path (ADR-002).
export type { FilterGroup } from "../../../types/filterGroup";
export type { FilterClause, FilterCondition } from "../../../types/filterClause";
export { createFilterGroup } from "../../../types/filterGroup";
export { createFilterClause, ALL_FILTER_CONDITIONS } from "../../../types/filterClause";
