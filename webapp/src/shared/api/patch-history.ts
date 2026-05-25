/**
 * shared/api/patch-history.ts
 * Pilha de undo/redo para patches de bloco (ADR-008 / BR-MIGRAR-012).
 * Cada entrada armazena o patch direto e o reverso para desfazer a mutação.
 */

export interface PatchEntry<T> {
  do: T;
  undo: T;
  description?: string;
}

export function usePatchHistory<T>() {
  const undoStack: PatchEntry<T>[] = [];
  const redoStack: PatchEntry<T>[] = [];

  function push(entry: PatchEntry<T>): void {
    undoStack.push(entry);
    redoStack.splice(0);
  }

  function popUndo(): PatchEntry<T> | undefined {
    const entry = undoStack.pop();
    if (entry) redoStack.push(entry);
    return entry;
  }

  function popRedo(): PatchEntry<T> | undefined {
    const entry = redoStack.pop();
    if (entry) undoStack.push(entry);
    return entry;
  }

  function clear(): void {
    undoStack.splice(0);
    redoStack.splice(0);
  }

  const canUndo = (): boolean => undoStack.length > 0;
  const canRedo = (): boolean => redoStack.length > 0;

  return { push, popUndo, popRedo, clear, canUndo, canRedo };
}

