// Re-exports global attachment store under feature-scoped name (ADR-002).
// Extends with file upload via shared API client.
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { Block } from "../../../types/block";
import client from "../../../api/client";

export const useFilesStore = defineStore("files", () => {
  const files = ref<Record<string, Block>>({});
  const uploading = ref(false);
  const error = ref<string | null>(null);

  const fileList = computed(() => Object.values(files.value));

  const filesByCard = computed(() => {
    const map: Record<string, Block[]> = {};
    for (const f of fileList.value) {
      if (!map[f.parentId]) map[f.parentId] = [];
      map[f.parentId].push(f);
    }
    return map;
  });

  function setFile(file: Block) {
    files.value[file.id] = file;
  }

  function removeFile(fileId: string) {
    delete files.value[fileId];
  }

  function setFilesFromBlocks(blocks: Block[]) {
    for (const block of blocks) {
      if (block.type === "attachment") setFile(block);
    }
  }

  async function uploadFile(boardId: string, cardId: string, file: File): Promise<Block> {
    uploading.value = true;
    error.value = null;
    try {
      const form = new FormData();
      form.append("file", file);
      form.append("parent_id", cardId);
      const res = await client.post(`/boards/${boardId}/files`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      const block: Block = res.data;
      setFile(block);
      return block;
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : "Upload failed";
      throw e;
    } finally {
      uploading.value = false;
    }
  }

  async function deleteFile(boardId: string, fileId: string): Promise<void> {
    await client.delete(`/boards/${boardId}/files/${fileId}`);
    removeFile(fileId);
  }

  return {
    files, fileList, filesByCard, uploading, error,
    setFile, removeFile, setFilesFromBlocks, uploadFile, deleteFile,
  };
});
