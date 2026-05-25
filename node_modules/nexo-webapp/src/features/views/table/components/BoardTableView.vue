<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import type { BoardMember, IPropertyTemplate } from "../../../../types/board";
import type { Block } from "../../../../types/block";
import type { BoardView } from "../../../../types/boardView";
import * as api from "../../../../api";
import BoardPermissionGate from "../../../../components/permissions/BoardPermissionGate.vue";
import AppLayout from "../../../../shared/layouts/AppLayout.vue";
import { useBoardStore, useCardStore, useUserStore } from "../../../../stores";
import { useBoardsStore } from "../../../boards/stores/boards.store";
import { useTeamsStore } from "../../../boards/stores/teams.store";
import ExportDropdown from "../../../boards/components/ExportDropdown.vue";
import CardDetailModal from "../../../content/components/CardDetailModal.vue";
import NewCardTemplateSelector from "../../../content/components/NewCardTemplateSelector.vue";
import ShareBoardModal from "../../../collaboration/components/ShareBoardModal.vue";
import GroupByDropdown from "../../components/GroupByDropdown.vue";
import FilterPanel from "../../components/FilterPanel.vue";
import PropertiesPanel from "../../components/PropertiesPanel.vue";
import SortPanel from "../../components/SortPanel.vue";
import { useViewStore } from "../../stores/views.store";

interface FilterClause {
  propertyId: string;
  operator: "is" | "is not" | "contains" | "does not contain";
  value: string;
}

interface SortClause {
  propertyId: string;
  direction: "asc" | "desc";
}

const route = useRoute();
const router = useRouter();
const boardId = route.params.boardId as string;

const boardStore = useBoardStore();
const cardStore = useCardStore();
const boardsStore = useBoardsStore();
const teamsStore = useTeamsStore();
const userStore = useUserStore();
const viewsStore = useViewStore();

const status = ref<"idle" | "loading" | "error" | "success">("loading");
const errorMessage = ref("");
const activeViewId = ref("");
const groupById = ref<string | null>(null);
const visibleIds = ref<string[]>([]);
const filterClauses = ref<FilterClause[]>([]);
const sortClauses = ref<SortClause[]>([]);
const searchQuery = ref("");
const detailCard = ref<Block | null>(null);
const showShareModal = ref(false);
const collapsedGroups = ref<string[]>([]);
const members = ref<BoardMember[]>([]);

const board = computed(() => boardStore.boards[boardId]);
const properties = computed<IPropertyTemplate[]>(() => board.value?.cardProperties ?? []);
const boardViews = computed(() => viewsStore.viewList.filter((view: BoardView) => view.boardId === boardId));
const activeView = computed(() => boardViews.value.find((view: BoardView) => view.id === activeViewId.value));
const currentViewName = computed(() => activeView.value?.title || "Table");
const groupByPropName = computed(() => properties.value.find((property) => property.id === groupById.value)?.name || "None");
const teamName = computed(() => teamsStore.current?.title || "Nexo");
const visibleProperties = computed(() => {
  const ids = visibleIds.value.length ? visibleIds.value : properties.value.map((property) => property.id);
  return properties.value.filter((property) => ids.includes(property.id));
});
const rawCards = computed(() => cardStore.cardList.filter((card) => card.boardId === boardId));
const permissionMember = computed(() => {
  const userId = userStore.me?.id || "";
  return members.value.find((member) => member.userId === userId) || { schemeAdmin: true };
});

const filteredCards = computed(() => rawCards.value.filter((card) => {
  const matchesSearch = !searchQuery.value || card.title.toLowerCase().includes(searchQuery.value.toLowerCase());
  const matchesFilters = filterClauses.value.every((clause) => {
    const displayValue = getDisplayValue(card, clause.propertyId).toLowerCase();
    const filterValue = clause.value.toLowerCase();
    switch (clause.operator) {
      case "is":
        return displayValue === filterValue;
      case "is not":
        return displayValue !== filterValue;
      case "contains":
        return displayValue.includes(filterValue);
      case "does not contain":
        return !displayValue.includes(filterValue);
      default:
        return true;
    }
  });
  return matchesSearch && matchesFilters;
}));

const sortedCards = computed(() => [...filteredCards.value].sort((left, right) => {
  for (const clause of sortClauses.value) {
    const leftValue = getDisplayValue(left, clause.propertyId).toLowerCase();
    const rightValue = getDisplayValue(right, clause.propertyId).toLowerCase();
    if (leftValue === rightValue) continue;
    const result = leftValue.localeCompare(rightValue, undefined, { numeric: true });
    return clause.direction === "asc" ? result : -result;
  }
  return 0;
}));

const groups = computed(() => {
  if (!groupById.value) {
    return [{ key: "all", label: "All cards", cards: sortedCards.value }];
  }

  const property = properties.value.find((item) => item.id === groupById.value);
  if (property?.options?.length) {
    const grouped = property.options.map((option) => ({
      key: option.id,
      label: option.value,
      cards: sortedCards.value.filter((card) => getRawValue(card, property.id) === option.id),
    }));
    const noValueCards = sortedCards.value.filter((card) => !getRawValue(card, property.id));
    if (noValueCards.length) {
      grouped.push({ key: "no-value", label: "No value", cards: noValueCards });
    }
    return grouped;
  }

  const grouped = new Map<string, Block[]>();
  sortedCards.value.forEach((card) => {
    const label = getDisplayValue(card, groupById.value as string) || "No value";
    const existing = grouped.get(label) || [];
    existing.push(card);
    grouped.set(label, existing);
  });

  return Array.from(grouped.entries()).map(([label, groupedCards]) => ({ key: label, label, cards: groupedCards }));
});

function getRawValue(card: Block, propertyId: string) {
  return ((card.fields?.properties as Record<string, unknown>) ?? {})[propertyId];
}

function getDisplayValue(card: Block, propertyId: string) {
  const property = properties.value.find((item) => item.id === propertyId);
  const rawValue = getRawValue(card, propertyId);
  if (rawValue === undefined || rawValue === null || rawValue === "") {
    return "";
  }
  if (property?.options?.length) {
    const values = Array.isArray(rawValue) ? rawValue : [rawValue];
    return values.map((value) => property.options.find((option) => option.id === value)?.value || String(value)).join(", ");
  }
  return String(rawValue);
}

function syncViewState(view: BoardView | undefined) {
  if (!view) return;
  groupById.value = view.fields.groupById || null;
  visibleIds.value = view.fields.visiblePropertyIds?.length ? [...view.fields.visiblePropertyIds] : properties.value.map((property) => property.id);
  filterClauses.value = (((view.fields.filter?.filters as unknown) as Array<Record<string, unknown>> | undefined) ?? [])
    .filter((item) => typeof item.propertyId === "string")
    .map((item) => ({
      propertyId: String(item.propertyId),
      operator: item.condition === "notContains" || item.condition === "notIncludes" ? "does not contain" : item.condition === "is" ? "is" : "contains",
      value: String((item.values as string[] | undefined)?.[0] ?? ""),
    }));
  sortClauses.value = (view.fields.sortOptions ?? []).map((item) => ({ propertyId: item.propertyId, direction: item.reversed ? "desc" : "asc" }));
}

async function persistViewState() {
  if (!activeView.value) return;
  const updated = await api.patchBlock(boardId, activeView.value.id, {
    fields: {
      ...activeView.value.fields,
      groupById: groupById.value ?? undefined,
      visiblePropertyIds: visibleIds.value,
      sortOptions: sortClauses.value.map((clause) => ({ propertyId: clause.propertyId, reversed: clause.direction === "desc" })),
      filter: {
        operation: "and",
        filters: filterClauses.value.map((clause) => ({
          propertyId: clause.propertyId,
          condition: clause.operator === "is" ? "is" : clause.operator === "does not contain" ? "notContains" : clause.operator === "is not" ? "notIncludes" : "contains",
          values: [clause.value],
        })),
      },
    },
  });
  viewsStore.setView(updated as BoardView);
}

function toggleGroup(groupKey: string) {
  collapsedGroups.value = collapsedGroups.value.includes(groupKey)
    ? collapsedGroups.value.filter((key) => key !== groupKey)
    : [...collapsedGroups.value, groupKey];
}

function isCollapsed(groupKey: string) {
  return collapsedGroups.value.includes(groupKey);
}

async function loadBoard() {
  status.value = "loading";
  errorMessage.value = "";
  try {
    const [boardData, blocks, boardMembers] = await Promise.all([
      api.getBoard(boardId),
      api.getBlocks(boardId),
      api.getMembers(boardId),
    ]);

    boardStore.setBoard(boardData);
    boardsStore.current = boardId;
    members.value = boardMembers;

    if (!teamsStore.allTeams.length) {
      await teamsStore.fetchTeams();
    }
    if (boardData.teamId) {
      teamsStore.setCurrent(boardData.teamId);
      await boardsStore.fetchBoards(boardData.teamId);
    }

    viewsStore.views = {};
    cardStore.cards = {};
    cardStore.templates = {};
    blocks.filter((block) => block.type === "view").forEach((block) => viewsStore.setView(block as BoardView));
    blocks.filter((block) => block.type === "card").forEach((block) => cardStore.setCard(block));

    const tableView = blocks.find((block) => block.type === "view" && (block as BoardView).fields.viewType === "table") as BoardView | undefined;
    activeViewId.value = tableView?.id || (boardViews.value[0]?.id ?? "");
    syncViewState(tableView || boardViews.value[0]);
    status.value = "success";
  } catch (error: unknown) {
    errorMessage.value = error instanceof Error ? error.message : "Failed to load board";
    status.value = "error";
  }
}

function openCard(card: Block) {
  detailCard.value = card;
}

function switchView(view: BoardView) {
  const path = view.fields.viewType === "table" ? `/boards/${boardId}/table` : view.fields.viewType === "board" ? `/boards/${boardId}/kanban` : "";
  if (path) {
    router.push(path);
  }
}

async function updateGroupBy(value: string | null) {
  groupById.value = value;
  await persistViewState();
}

async function updateVisibleIds(value: string[]) {
  visibleIds.value = value;
  await persistViewState();
}

async function updateFilterClauses(value: FilterClause[]) {
  filterClauses.value = value;
  await persistViewState();
}

async function updateSortClauses(value: SortClause[]) {
  sortClauses.value = value;
  await persistViewState();
}

async function createCard(templateId: string | null) {
  const template = templateId ? cardStore.templates[templateId] : null;
  const created = await api.createCard(boardId, {
    boardId,
    type: "card",
    title: template?.title || "Untitled",
    fields: template ? { ...template.fields, isTemplate: false } : { properties: {} },
  });
  cardStore.setCard(created);
  detailCard.value = created;
}

onMounted(loadBoard);
</script>

<template>
  <AppLayout :active-board="board?.title || ''" :team-name="teamName" :boards="boardsStore.boardList">
    <BoardPermissionGate :permissions="['view_board']" :board="board" :member="permissionMember">
      <div class="container-fluid p-3">
        <div class="vstack gap-3">
          <div class="d-flex gap-2 flex-wrap align-items-center">
            <div class="dropdown">
              <button type="button" class="btn btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">{{ currentViewName }}</button>
              <ul class="dropdown-menu">
                <li v-for="view in boardViews" :key="view.id"><button type="button" class="dropdown-item" @click="switchView(view)">{{ view.title || view.fields.viewType }}</button></li>
              </ul>
            </div>
            <button type="button" class="btn btn-outline-secondary" data-bs-toggle="offcanvas" data-bs-target="#table-properties-panel">Properties</button>
            <GroupByDropdown :properties="properties" :model-value="groupById" @update:model-value="updateGroupBy" />
            <button type="button" class="btn btn-outline-secondary" data-bs-toggle="offcanvas" data-bs-target="#table-filter-panel">
              Filter
              <span v-if="filterClauses.length" class="badge text-bg-secondary ms-1">{{ filterClauses.length }}</span>
            </button>
            <button type="button" class="btn btn-outline-secondary" data-bs-toggle="offcanvas" data-bs-target="#table-sort-panel">Sort</button>
            <input v-model="searchQuery" type="search" class="form-control" placeholder="Search cards" style="max-width: 220px;" />
            <ExportDropdown :board-id="boardId" />
            <NewCardTemplateSelector :board-id="boardId" @select="createCard" />
            <button type="button" class="btn btn-primary" @click="showShareModal = true">Share</button>
          </div>

          <div v-if="status === 'loading'" class="d-flex align-items-center gap-2 text-muted">
            <div class="spinner-border spinner-border-sm" role="status"></div>
            <span>Loading board...</span>
          </div>
          <div v-else-if="status === 'error'" class="alert alert-danger mb-0">{{ errorMessage }}</div>
          <template v-else>
            <div class="visually-hidden" aria-live="polite">Board loaded.</div>
            <div class="card">
              <div class="table-responsive">
                <table class="table table-hover mb-0">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th v-for="property in visibleProperties" :key="property.id">{{ property.name }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <template v-for="group in groups" :key="group.key">
                      <tr v-if="groupById" class="table-light">
                        <td :colspan="visibleProperties.length + 1">
                          <button type="button" class="btn btn-link p-0 text-decoration-none" @click="toggleGroup(group.key)">
                            {{ isCollapsed(group.key) ? '▶' : '▼' }} {{ group.label }} ({{ group.cards.length }})
                          </button>
                        </td>
                      </tr>
                      <tr v-for="card in isCollapsed(group.key) ? [] : group.cards" :key="card.id" @click="openCard(card)" style="cursor: pointer;">
                        <td class="fw-semibold">{{ card.title }}</td>
                        <td v-for="property in visibleProperties" :key="property.id">{{ getDisplayValue(card, property.id) }}</td>
                      </tr>
                    </template>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="text-muted">COUNT {{ sortedCards.length }}</div>
          </template>
        </div>
      </div>

      <template #fallback>
        <div class="container-fluid p-3"><div class="alert alert-danger mb-0">Access denied.</div></div>
      </template>
    </BoardPermissionGate>

    <PropertiesPanel id="table-properties-panel" :properties="properties" :visible-ids="visibleIds" @update:visible-ids="updateVisibleIds" />
    <FilterPanel id="table-filter-panel" :properties="properties" :clauses="filterClauses" @update:clauses="updateFilterClauses" />
    <SortPanel id="table-sort-panel" :properties="properties" :clauses="sortClauses" @update:clauses="updateSortClauses" />
    <ShareBoardModal v-if="showShareModal" :board-id="boardId" @close="showShareModal = false" />
    <CardDetailModal v-if="detailCard" :board-id="boardId" :card-id="detailCard.id" @close="detailCard = null" />
  </AppLayout>
</template>
