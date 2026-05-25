<script setup lang="ts">
import { ref } from "vue";
import type { Board, IPropertyTemplate } from "../../types/board";
import type { BoardView } from "../../types/boardView";
import ViewHeaderActionsMenu from "./ViewHeaderActionsMenu.vue";
import ViewHeaderSortMenu from "./ViewHeaderSortMenu.vue";
import ViewHeaderGroupByMenu from "./ViewHeaderGroupByMenu.vue";
import ViewHeaderPropertiesMenu from "./ViewHeaderPropertiesMenu.vue";
import ViewHeaderSearch from "./ViewHeaderSearch.vue";

const props = defineProps<{
  board: Board;
  view: BoardView;
  views?: BoardView[];
  properties: IPropertyTemplate[];
  visiblePropertyIds: string[];
  currentSort?: { propertyId: string; direction: "asc" | "desc" } | null;
  currentGroupBy?: string | null;
}>();

const emit = defineEmits<{
  (e: "addCard"): void;
  (e: "addView"): void;
  (e: "sort", propertyId: string, direction: "asc" | "desc"): void;
  (e: "clearSort"): void;
  (e: "groupBy", propertyId: string | null): void;
  (e: "toggleProperty", propertyId: string): void;
  (e: "addProperty"): void;
  (e: "search", query: string): void;
  (e: "exportBoard"): void;
  (e: "duplicateBoard"): void;
  (e: "deleteBoard"): void;
  (e: "renameView", name: string): void;
  (e: "deleteView", viewId: string): void;
  (e: "switchView", viewId: string): void;
  (e: "switchViewType", viewType: string): void;
}>();

const editingBoardTitle = ref(false);
const editingViewTitle = ref(false);
const editBoardTitle = ref("");
const editViewTitle = ref("");

const viewTypes = ["board", "table", "calendar", "gallery"];

function startEditBoardTitle() {
  editBoardTitle.value = props.board.title || "";
  editingBoardTitle.value = true;
}

function startEditViewTitle() {
  editViewTitle.value = props.view.title || "";
  editingViewTitle.value = true;
}
</script>

<template>
  <div class="view-header px-3 py-1 border-bottom bg-body">
    <div class="d-flex align-items-center justify-content-between">
      <div class="d-flex align-items-center gap-3">
        <div class="d-flex align-items-center gap-2" style="min-width: 0;">
          <span class="fs-5">{{ board.icon }}</span>
          <div>
            <input
              v-if="editingBoardTitle"
              v-model="editBoardTitle"
              class="form-control form-control-sm fw-semibold"
              style="height: 24px; font-size: 14px; width: 200px;"
              @blur="editingBoardTitle = false"
              @keyup.escape="editingBoardTitle = false"
              autofocus
            />
            <h6 v-else class="mb-0 text-truncate fw-semibold" style="cursor: pointer; max-width: 200px;" @click="startEditBoardTitle">
              {{ board.title }}
            </h6>
          </div>
        </div>

        <div class="vr"></div>

        <div class="dropdown">
          <div class="d-flex align-items-center gap-1 cursor-pointer" data-bs-toggle="dropdown" aria-expanded="false">
            <input
              v-if="editingViewTitle"
              v-model="editViewTitle"
              class="form-control form-control-sm"
              style="height: 22px; font-size: 12px; width: 150px;"
              @blur="editingViewTitle = false; if(editViewTitle.trim()) emit('renameView', editViewTitle.trim())"
              @keyup.enter="editingViewTitle = false; if(editViewTitle.trim()) emit('renameView', editViewTitle.trim())"
              @keyup.escape="editingViewTitle = false"
              @click.stop
              autofocus
            />
            <span v-else class="small fw-semibold text-muted" @click.stop="startEditViewTitle">
              {{ view.title || "Untitled view" }}
              <i class="bi bi-chevron-down ms-1" style="font-size: 10px;"></i>
            </span>
          </div>
          <ul class="dropdown-menu">
            <li><h6 class="dropdown-header">Views</h6></li>
            <li v-for="v in views" :key="v.id">
              <button
                class="dropdown-item d-flex align-items-center justify-content-between"
                :class="{ 'active': v.id === view.id }"
                @click="emit('switchView', v.id)"
              >
                {{ v.title }}
                <i v-if="v.id === view.id" class="bi bi-check"></i>
              </button>
            </li>
            <li><hr class="dropdown-divider"></li>
            <li><button class="dropdown-item" @click="emit('addView')"><i class="bi bi-plus me-1"></i> Add view</button></li>
            <li v-if="views && views.length > 1"><button class="dropdown-item text-danger" @click="emit('deleteView', view.id)"><i class="bi bi-trash me-1"></i> Delete view</button></li>
          </ul>
        </div>
      </div>

      <div class="d-flex align-items-center gap-1">
        <ViewHeaderSearch @search="emit('search', $event)" />

        <div class="vr mx-1"></div>

        <ViewHeaderPropertiesMenu
          :properties="properties"
          :visible-properties="visiblePropertyIds"
          @toggle-property="emit('toggleProperty', $event)"
          @add-property="emit('addProperty')"
        />
        <ViewHeaderGroupByMenu
          :properties="properties"
          :current-group-by="currentGroupBy"
          @group-by="emit('groupBy', $event)"
        />
        <ViewHeaderSortMenu
          :properties="properties"
          :current-sort="currentSort"
          @sort="emit('sort', $event.propertyId, $event.direction)"
          @clear-sort="emit('clearSort')"
        />

        <div class="vr mx-1"></div>

        <div class="dropdown">
          <button class="btn btn-sm btn-outline-secondary border-0 dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
            <i class="bi" :class="{
              'bi-kanban': view.fields.viewType === 'board',
              'bi-table': view.fields.viewType === 'table',
              'bi-calendar3': view.fields.viewType === 'calendar',
              'bi-images': view.fields.viewType === 'gallery',
            }"></i>
            <span class="ms-1 small">{{ view.fields.viewType }}</span>
          </button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li v-for="vt in viewTypes" :key="vt">
              <button
                class="dropdown-item d-flex align-items-center gap-2"
                :class="{ 'active': view.fields.viewType === vt }"
                @click="emit('switchViewType', vt)"
              >
                <i class="bi" :class="{
                  'bi-kanban': vt === 'board',
                  'bi-table': vt === 'table',
                  'bi-calendar3': vt === 'calendar',
                  'bi-images': vt === 'gallery',
                }"></i>
                {{ vt.charAt(0).toUpperCase() + vt.slice(1) }}
              </button>
            </li>
          </ul>
        </div>

        <button class="btn btn-sm btn-primary" @click="emit('addCard')">
          <i class="bi bi-plus"></i> Add card
        </button>
        <ViewHeaderActionsMenu
          @export-board="emit('exportBoard')"
          @duplicate-board="emit('duplicateBoard')"
          @delete-board="emit('deleteBoard')"
        />
      </div>
    </div>
  </div>
</template>
