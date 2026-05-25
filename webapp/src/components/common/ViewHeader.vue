<script setup lang="ts">
import { ref, computed } from "vue";
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
const showViewMenu = ref(false);
const showViewTypeMenu = ref(false);

const viewTypes = ["board", "table", "calendar", "gallery"];

function startEditBoardTitle() {
  editBoardTitle.value = props.board.title || "";
  editingBoardTitle.value = true;
}

function startEditViewTitle() {
  editViewTitle.value = props.view.title || "";
  editingViewTitle.value = true;
}

function selectView(viewId: string) {
  showViewMenu.value = false;
  emit("switchView", viewId);
}

function selectViewType(viewType: string) {
  showViewTypeMenu.value = false;
  emit("switchViewType", viewType);
}
</script>

<template>
  <div class="view-header px-3 py-1 border-bottom bg-white">
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

        <div class="position-relative">
          <div class="d-flex align-items-center gap-1 cursor-pointer" @click="showViewMenu = !showViewMenu">
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
          <div v-if="showViewMenu" class="position-absolute start-0 mt-1 bg-white border rounded shadow-sm" style="z-index: 100; min-width: 180px;">
            <div class="px-3 py-1 small fw-semibold text-muted border-bottom">Views</div>
            <div v-for="v in views" :key="v.id">
              <button
                class="dropdown-item small py-1 px-3 d-flex align-items-center justify-content-between"
                :class="{ 'bg-primary bg-opacity-10': v.id === view.id }"
                @click="selectView(v.id)"
              >
                {{ v.title }}
                <i v-if="v.id === view.id" class="bi bi-check text-primary"></i>
              </button>
            </div>
            <hr class="my-1">
            <button class="dropdown-item small py-1 px-3" @click="emit('addView'); showViewMenu = false">
              <i class="bi bi-plus me-1"></i> Add view
            </button>
            <button v-if="views && views.length > 1" class="dropdown-item small py-1 px-3 text-danger" @click="emit('deleteView', view.id); showViewMenu = false">
              <i class="bi bi-trash me-1"></i> Delete view
            </button>
          </div>
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

        <div class="position-relative">
          <button class="btn btn-sm btn-outline-secondary border-0" @click="showViewTypeMenu = !showViewTypeMenu">
            <i class="bi" :class="{
              'bi-kanban': view.fields.viewType === 'board' || view.fields.viewType === 'kanban',
              'bi-table': view.fields.viewType === 'table',
              'bi-calendar3': view.fields.viewType === 'calendar',
              'bi-images': view.fields.viewType === 'gallery',
            }"></i>
            <span class="ms-1 small">{{ view.fields.viewType }}</span>
            <i class="bi bi-chevron-down ms-1" style="font-size: 9px;"></i>
          </button>
          <div v-if="showViewTypeMenu" class="position-absolute end-0 mt-1 bg-white border rounded shadow-sm" style="z-index: 100; min-width: 140px;">
            <button
              v-for="vt in viewTypes"
              :key="vt"
              class="dropdown-item small py-1 px-3 d-flex align-items-center gap-2"
              :class="{ 'bg-primary bg-opacity-10': view.fields.viewType === vt }"
              @click="selectViewType(vt)"
            >
              <i class="bi" :class="{
                'bi-kanban': vt === 'board' || vt === 'kanban',
                'bi-table': vt === 'table',
                'bi-calendar3': vt === 'calendar',
                'bi-images': vt === 'gallery',
              }"></i>
              {{ vt.charAt(0).toUpperCase() + vt.slice(1) }}
            </button>
          </div>
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
