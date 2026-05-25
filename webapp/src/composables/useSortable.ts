import { ref } from "vue";

interface SortableOptions {
  onEnd?: (fromIndex: number, toIndex: number) => void;
}

export function useSortable(options: SortableOptions = {}) {
  const dragIndex = ref<number | null>(null);
  const dragOverIndex = ref<number | null>(null);
  const isDragging = ref(false);

  function onDragStart(index: number) {
    dragIndex.value = index;
    isDragging.value = true;
  }

  function onDragOver(index: number) {
    dragOverIndex.value = index;
  }

  function onDragEnd() {
    if (dragIndex.value !== null && dragOverIndex.value !== null && dragIndex.value !== dragOverIndex.value) {
      options.onEnd?.(dragIndex.value, dragOverIndex.value);
    }
    dragIndex.value = null;
    dragOverIndex.value = null;
    isDragging.value = false;
  }

  function getItemProps(index: number) {
    return {
      draggable: true,
      class: {
        "opacity-50": isDragging.value && dragIndex.value === index,
      },
      onDragstart: () => onDragStart(index),
      onDragover: (e: DragEvent) => {
        e.preventDefault();
        onDragOver(index);
      },
      onDragend: onDragEnd,
      onDrop: (e: DragEvent) => {
        e.preventDefault();
        onDragEnd();
      },
    };
  }

  return {
    dragIndex,
    isDragging,
    getItemProps,
  };
}
