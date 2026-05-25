<template>
  <div class="content-registry">
    <template v-for="block in sortedBlocks" :key="block.id">
      <!-- text / h1 / h2 / h3 / quote / list-item -->
      <div
        v-if="isTextType(block.type)"
        :class="blockClass(block.type)"
        :contenteditable="editable"
        @blur="onTextBlur(block, $event)"
        v-html="block.title"
      />

      <!-- divider -->
      <hr v-else-if="block.type === 'divider'" class="my-2" />

      <!-- checkbox -->
      <div v-else-if="block.type === 'checkbox'" class="form-check my-1">
        <input
          type="checkbox"
          class="form-check-input"
          :checked="!!block.fields?.checked"
          :disabled="!editable"
          @change="onCheckboxChange(block, ($event.target as HTMLInputElement).checked)"
        />
        <label class="form-check-label">{{ block.title }}</label>
      </div>

      <!-- image -->
      <div v-else-if="block.type === 'image'" class="my-2">
        <img
          v-if="block.fields?.url"
          :src="String(block.fields.url)"
          class="img-fluid rounded"
          :alt="block.title || 'image'"
        />
      </div>

      <!-- video -->
      <div v-else-if="block.type === 'video'" class="ratio ratio-16x9 my-2">
        <iframe
          v-if="block.fields?.url"
          :src="String(block.fields.url)"
          allowfullscreen
        />
      </div>

      <!-- attachment (rendered separately in FileAttachmentsPanel) -->
      <div v-else-if="block.type !== 'attachment'" class="text-muted small fst-italic my-1">
        [{{ block.type }}] {{ block.title }}
      </div>
    </template>

    <!-- Add block controls (edit mode only) -->
    <div v-if="editable" class="mt-2 d-flex gap-2 flex-wrap">
      <button
        v-for="type in addableTypes"
        :key="type"
        class="btn btn-sm btn-outline-secondary"
        type="button"
        @click="emit('add-block', type)"
      >
        + {{ type }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { Block } from "../../../types/block";
import type { ContentBlockType } from "../../../types/contentBlock";

const props = withDefaults(defineProps<{
  content: Block[];
  editable?: boolean;
}>(), { editable: false });

const emit = defineEmits<{
  (e: "add-block", type: ContentBlockType): void;
  (e: "update-block", block: Block, title: string): void;
  (e: "toggle-checkbox", block: Block, checked: boolean): void;
}>();

const TEXT_TYPES = ["text", "h1", "h2", "h3", "quote", "list-item"] as const;

const addableTypes: ContentBlockType[] = ["text", "h1", "h2", "h3", "divider", "checkbox", "list-item"];

const sortedBlocks = computed(() =>
  [...props.content].sort((a, b) => {
    const ao = (a.fields?.order as number) ?? a.createAt;
    const bo = (b.fields?.order as number) ?? b.createAt;
    return ao - bo;
  })
);

function isTextType(type: string): type is typeof TEXT_TYPES[number] {
  return (TEXT_TYPES as readonly string[]).includes(type);
}

function blockClass(type: string): string {
  const map: Record<string, string> = {
    h1: "h3 fw-bold my-2",
    h2: "h4 fw-bold my-1",
    h3: "h5 fw-semibold my-1",
    quote: "blockquote border-start border-3 ps-3 text-muted my-2",
    "list-item": "my-1 ms-3",
    text: "my-1",
  };
  return map[type] ?? "my-1";
}

function onTextBlur(block: Block, event: FocusEvent) {
  const el = event.target as HTMLElement;
  emit("update-block", block, el.innerText);
}

function onCheckboxChange(block: Block, checked: boolean) {
  emit("toggle-checkbox", block, checked);
}
</script>
