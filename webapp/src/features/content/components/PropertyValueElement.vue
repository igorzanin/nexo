<template>
  <div class="property-value-element d-flex align-items-start py-2" style="min-height: 36px;">
    <span class="text-muted small fw-semibold" style="min-width: 130px; padding-top: 2px;">{{ label }}</span>

    <!-- Select → colored badge dropdown -->
    <div v-if="type === 'select'" class="flex-grow-1">
      <div class="dropdown">
        <button
          type="button"
          class="btn btn-sm p-0 border-0 bg-transparent"
          data-bs-toggle="dropdown"
          :disabled="disabled"
        >
          <span v-if="selectedOption" class="badge rounded-pill px-2 py-1" :style="badgeStyle(selectedOption.color)">
            {{ selectedOption.value }}
          </span>
          <span v-else class="small text-muted fst-italic">Empty</span>
        </button>
        <ul class="dropdown-menu">
          <li>
            <button type="button" class="dropdown-item text-muted small" @click="emit('update:modelValue', '')">
              — Empty
            </button>
          </li>
          <li v-for="opt in options" :key="opt.id">
            <button type="button" class="dropdown-item d-flex align-items-center gap-2" @click="emit('update:modelValue', opt.id)">
              <span class="badge rounded-pill px-2" :style="badgeStyle(opt.color)">{{ opt.value }}</span>
            </button>
          </li>
        </ul>
      </div>
    </div>

    <!-- Multiselect -->
    <div v-else-if="type === 'multiselect'" class="flex-grow-1 d-flex flex-wrap align-items-center gap-1">
      <span
        v-for="val in asArray(modelValue)"
        :key="val"
        class="badge rounded-pill px-2 py-1"
        :style="badgeStyle(optionColor(val))"
        style="cursor:pointer;"
        @click="!disabled && onMultiselectRemove(val)"
      >{{ labelForOption(val) }}</span>
      <div v-if="!disabled && availableOptions.length" class="dropdown">
        <button type="button" class="btn btn-sm border-0 text-muted py-0 px-1" data-bs-toggle="dropdown">
          <i class="bi bi-plus"></i>
        </button>
        <ul class="dropdown-menu">
          <li v-for="opt in availableOptions" :key="opt.id">
            <button type="button" class="dropdown-item d-flex align-items-center gap-2" @click="onMultiselectAdd(opt.id)">
              <span class="badge rounded-pill px-2" :style="badgeStyle(opt.color)">{{ opt.value }}</span>
            </button>
          </li>
        </ul>
      </div>
      <span v-if="!asArray(modelValue).length" class="small text-muted fst-italic">Empty</span>
    </div>

    <!-- Person -->
    <span v-else-if="type === 'person'" class="small flex-grow-1">
      <span v-if="modelValue">{{ modelValue }}</span>
      <span v-else class="text-muted fst-italic">Empty</span>
    </span>

    <!-- Date -->
    <div v-else-if="type === 'date'" class="flex-grow-1">
      <input
        type="date"
        class="form-control form-control-sm"
        style="max-width: 200px;"
        :value="modelValue"
        :disabled="disabled"
        @change="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
    </div>

    <!-- Number -->
    <div v-else-if="type === 'number'" class="flex-grow-1">
      <input
        type="number"
        class="form-control form-control-sm"
        style="max-width: 120px;"
        :value="modelValue"
        :disabled="disabled"
        @change="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
    </div>

    <!-- Checkbox -->
    <div v-else-if="type === 'checkbox'" class="flex-grow-1">
      <input
        type="checkbox"
        class="form-check-input"
        :checked="!!modelValue"
        :disabled="disabled"
        @change="emit('update:modelValue', ($event.target as HTMLInputElement).checked)"
      />
    </div>

    <!-- URL -->
    <div v-else-if="type === 'url'" class="flex-grow-1 small">
      <a v-if="modelValue" :href="String(modelValue)" target="_blank" rel="noopener noreferrer" class="text-truncate d-block" style="max-width:260px;">{{ modelValue }}</a>
      <span v-else class="text-muted fst-italic">Empty</span>
    </div>

    <!-- Email -->
    <div v-else-if="type === 'email'" class="flex-grow-1 small">
      <a v-if="modelValue" :href="`mailto:${modelValue}`">{{ modelValue }}</a>
      <span v-else class="text-muted fst-italic">Empty</span>
    </div>

    <!-- Default: text -->
    <div v-else class="flex-grow-1">
      <input
        v-if="!disabled"
        type="text"
        class="form-control form-control-sm"
        :value="modelValue"
        @change="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
      <span v-else class="small">
        <span v-if="modelValue">{{ modelValue }}</span>
        <span v-else class="text-muted fst-italic">Empty</span>
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

interface PropertyOption {
  id: string;
  value: string;
  color?: string;
}

type PropertyType = "text" | "number" | "select" | "multiselect" | "person" | "date" | "checkbox" | "url" | "email";

const PROP_COLOR_MAP: Record<string, { bg: string; color: string }> = {
  propColorYellow: { bg: "#f3c916", color: "#000" },
  propColorOrange: { bg: "#fba510", color: "#000" },
  propColorRed:    { bg: "#f87171", color: "#fff" },
  propColorPink:   { bg: "#f892d4", color: "#000" },
  propColorPurple: { bg: "#b5a1f8", color: "#000" },
  propColorBlue:   { bg: "#5f8fc9", color: "#fff" },
  propColorSky:    { bg: "#7ed9f5", color: "#000" },
  propColorTeal:   { bg: "#5aa9b5", color: "#fff" },
  propColorGreen:  { bg: "#45d483", color: "#000" },
  propColorGray:   { bg: "#aba8a3", color: "#fff" },
  propColorBrown:  { bg: "#c0956f", color: "#fff" },
};

const FALLBACK_COLORS = [
  { bg: "#e0e7ff", color: "#3730a3" },
  { bg: "#dcfce7", color: "#166534" },
  { bg: "#fef9c3", color: "#713f12" },
  { bg: "#ffe4e6", color: "#9f1239" },
  { bg: "#f3e8ff", color: "#6b21a8" },
  { bg: "#cffafe", color: "#164e63" },
];

const props = withDefaults(defineProps<{
  label: string;
  type?: PropertyType;
  modelValue?: unknown;
  options?: PropertyOption[];
  disabled?: boolean;
}>(), {
  type: "text",
  options: () => [],
  disabled: false,
});

const emit = defineEmits<{
  (e: "update:modelValue", value: unknown): void;
}>();

const selectedOption = computed(() =>
  props.type === "select"
    ? (props.options ?? []).find((o) => o.id === props.modelValue) ?? null
    : null
);

function badgeStyle(colorName?: string): string {
  if (colorName && PROP_COLOR_MAP[colorName]) {
    const c = PROP_COLOR_MAP[colorName];
    return `background-color:${c.bg};color:${c.color};font-weight:600;font-size:0.75rem;`;
  }
  const idx = colorName ? (colorName.charCodeAt(0) % FALLBACK_COLORS.length) : 0;
  const c = FALLBACK_COLORS[idx];
  return `background-color:${c.bg};color:${c.color};font-weight:600;font-size:0.75rem;`;
}

function optionColor(id: string): string | undefined {
  return props.options?.find((o) => o.id === id)?.color;
}

function asArray(val: unknown): string[] {
  if (Array.isArray(val)) return val as string[];
  if (val) return [String(val)];
  return [];
}

const availableOptions = computed(() =>
  (props.options ?? []).filter((o) => !asArray(props.modelValue).includes(o.id))
);

function labelForOption(id: string): string {
  return props.options?.find((o) => o.id === id)?.value ?? id;
}

function onMultiselectAdd(id: string) {
  if (!id) return;
  const current = asArray(props.modelValue);
  if (!current.includes(id)) emit("update:modelValue", [...current, id]);
}

function onMultiselectRemove(id: string) {
  emit("update:modelValue", asArray(props.modelValue).filter((v) => v !== id));
}
</script>
