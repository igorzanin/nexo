<script setup lang="ts">
import { ref } from "vue";
import type { Block } from "../../types/block";
import type { IPropertyTemplate } from "../../types/board";
import { useBoardStore } from "../../stores";
import SelectProperty from "../properties/SelectProperty.vue";
import MultiSelectProperty from "../properties/MultiSelectProperty.vue";
import TextProperty from "../properties/TextProperty.vue";
import NumberProperty from "../properties/NumberProperty.vue";
import DateProperty from "../properties/DateProperty.vue";
import PersonProperty from "../properties/PersonProperty.vue";
import CheckboxProperty from "../properties/CheckboxProperty.vue";
import EmailProperty from "../properties/EmailProperty.vue";
import PhoneProperty from "../properties/PhoneProperty.vue";
import UrlProperty from "../properties/UrlProperty.vue";
import * as api from "../../api";

const props = defineProps<{
  card: Block;
  properties: IPropertyTemplate[];
  boardId: string;
}>();

const boardStore = useBoardStore();
const showAddMenu = ref(false);

const PROPERTY_TYPES = [
  { type: "text", label: "Texto", icon: "bi-fonts" },
  { type: "number", label: "Número", icon: "bi-123" },
  { type: "email", label: "Email", icon: "bi-envelope" },
  { type: "phone", label: "Telefone", icon: "bi-telephone" },
  { type: "url", label: "URL", icon: "bi-link-45deg" },
  { type: "select", label: "Selecionar", icon: "bi-menu-button-wide" },
  { type: "multiSelect", label: "Seleção múltipla", icon: "bi-ui-checks" },
  { type: "date", label: "Data", icon: "bi-calendar" },
  { type: "person", label: "Pessoa", icon: "bi-person" },
  { type: "checkbox", label: "Caixa de seleção", icon: "bi-check-square" },
  { type: "createdTime", label: "Horário de criação", icon: "bi-clock" },
  { type: "createdBy", label: "Criado por", icon: "bi-person-badge" },
  { type: "updatedAt", label: "Atualizado pela última vez em", icon: "bi-clock-history" },
  { type: "updatedBy", label: "Atualizado pela última vez por", icon: "bi-person-lines-fill" },
];

const READ_ONLY_TYPES = new Set(["createdTime", "createdBy", "updatedAt", "updatedBy"]);

function getValue(propId: string): string {
  const val = props.card.fields?.properties?.[propId];
  return val != null ? val.toString() : "";
}

function getArrayValue(propId: string): string[] {
  const val = props.card.fields?.properties?.[propId];
  if (Array.isArray(val)) return val;
  if (typeof val === "string" && val) return val.split(",");
  return [];
}

function getBoolValue(propId: string): boolean {
  const val = props.card.fields?.properties?.[propId];
  return val === true || val === "true";
}

async function saveProperty(propId: string, value: string | string[] | boolean) {
  const patch = {
    fields: {
      ...props.card.fields,
      properties: { ...props.card.fields?.properties, [propId]: value },
    },
  };
  try {
    await api.patchBlock(props.boardId, props.card.id, patch);
    if (props.card.fields?.properties) {
      (props.card.fields.properties as Record<string, unknown>)[propId] = value;
    }
  } catch {}
}

function getReadOnlyValue(prop: IPropertyTemplate): string {
  switch (prop.type) {
    case "createdTime":
      return props.card.createAt ? new Date(props.card.createAt).toLocaleString() : "";
    case "updatedAt":
      return props.card.updateAt ? new Date(props.card.updateAt).toLocaleString() : "";
    case "createdBy":
      return (props.card.fields?.createdBy as string) || "";
    case "updatedBy":
      return (props.card.fields?.modifiedBy as string) || "";
    default:
      return "";
  }
}

async function addProperty(type: string) {
  const typeInfo = PROPERTY_TYPES.find((t) => t.type === type);
  const newProp: IPropertyTemplate = {
    id: `prop_${Date.now()}`,
    name: typeInfo?.label || "Nova propriedade",
    type,
    options: [],
  };
  const board = boardStore.boards[props.boardId];
  if (!board) return;
  const updatedProps = [...(board.cardProperties || []), newProp];
  try {
    const updated = await api.patchBoard(props.boardId, { cardProperties: updatedProps } as any);
    boardStore.setBoard(updated);
  } catch {}
  showAddMenu.value = false;
}
</script>

<template>
  <div class="octo-propertylist">
    <div v-for="prop in properties" :key="prop.id" class="octo-propertyrow">
      <div class="octo-propertyname">{{ prop.name }}</div>
      <div class="octo-propertyvalue">
        <template v-if="READ_ONLY_TYPES.has(prop.type)">
          <span class="small">{{ getReadOnlyValue(prop) || '—' }}</span>
        </template>

        <SelectProperty
          v-else-if="prop.type === 'select'"
          :model-value="getValue(prop.id)"
          :options="prop.options || []"
          @update:model-value="(v) => saveProperty(prop.id, v)"
        />

        <MultiSelectProperty
          v-else-if="prop.type === 'multiSelect'"
          :model-value="getArrayValue(prop.id)"
          :options="prop.options || []"
          @update:model-value="(v) => saveProperty(prop.id, v)"
        />

        <DateProperty
          v-else-if="prop.type === 'date'"
          :model-value="getValue(prop.id)"
          @update:model-value="(v) => saveProperty(prop.id, v)"
        />

        <PersonProperty
          v-else-if="prop.type === 'person'"
          :model-value="getValue(prop.id)"
          @update:model-value="(v) => saveProperty(prop.id, v)"
        />

        <CheckboxProperty
          v-else-if="prop.type === 'checkbox'"
          :model-value="getBoolValue(prop.id)"
          @update:model-value="(v) => saveProperty(prop.id, v)"
        />

        <NumberProperty
          v-else-if="prop.type === 'number'"
          :model-value="getValue(prop.id)"
          @update:model-value="(v) => saveProperty(prop.id, v)"
        />

        <EmailProperty
          v-else-if="prop.type === 'email'"
          :model-value="getValue(prop.id)"
          @update:model-value="(v) => saveProperty(prop.id, v)"
        />

        <PhoneProperty
          v-else-if="prop.type === 'phone'"
          :model-value="getValue(prop.id)"
          @update:model-value="(v) => saveProperty(prop.id, v)"
        />

        <UrlProperty
          v-else-if="prop.type === 'url'"
          :model-value="getValue(prop.id)"
          @update:model-value="(v) => saveProperty(prop.id, v)"
        />

        <TextProperty
          v-else
          :model-value="getValue(prop.id)"
          @update:model-value="(v) => saveProperty(prop.id, v)"
        />
      </div>
    </div>

    <div class="add-property-row">
      <div class="dropdown">
        <button
          class="btn btn-link btn-sm text-decoration-none text-muted px-0"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <i class="bi bi-plus me-1"></i>Adicionar propriedade
        </button>
        <ul class="dropdown-menu" style="max-height: 320px; overflow-y: auto;">
          <li class="dropdown-header small fw-semibold text-muted">Selecione o tipo de propriedade</li>
          <li v-for="pt in PROPERTY_TYPES" :key="pt.type">
            <button class="dropdown-item small py-2" @click="addProperty(pt.type)">
              <i :class="['bi', pt.icon, 'me-2']"></i>{{ pt.label }}
            </button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.octo-propertylist {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.octo-propertyrow {
  display: flex;
  align-items: flex-start;
  min-height: 32px;
  margin: 2px 0;
  max-width: 595px;
}

.octo-propertyname {
  width: 150px;
  flex-shrink: 0;
  font-weight: 600;
  font-size: 14px;
  padding: 4px 8px;
  color: var(--bs-body-color);
}

.octo-propertyvalue {
  flex: 1;
  font-size: 14px;
  padding: 2px 8px;
  border-radius: 4px;
  min-height: 32px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: background 100ms;
}

.octo-propertyvalue:hover {
  background-color: var(--bs-secondary-bg);
}

.add-property-row {
  margin-top: 6px;
  padding-left: 4px;
}
</style>
