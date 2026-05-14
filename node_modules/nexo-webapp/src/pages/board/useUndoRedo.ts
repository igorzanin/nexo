import { useMutator } from "../../composables/useMutator";

export function useUndoRedo() {
  const mutator = useMutator();

  function handleKeydown(e: KeyboardEvent) {
    if ((e.ctrlKey || e.metaKey) && e.key === "z" && !e.shiftKey) {
      mutator.undo();
      e.preventDefault();
    }
  }

  function bind() {
    document.addEventListener("keydown", handleKeydown);
  }

  function unbind() {
    document.removeEventListener("keydown", handleKeydown);
  }

  return { bind, unbind };
}
