export function useUndoRedo() {
  const stack: { undo: () => void; redo: () => void }[] = [];
  let index = -1;

  function push(undo: () => void, redo: () => void) {
    stack.length = index + 1;
    stack.push({ undo, redo });
    index++;
  }

  function undo() {
    if (index >= 0) {
      stack[index].undo();
      index--;
    }
  }

  function redo() {
    if (index < stack.length - 1) {
      index++;
      stack[index].redo();
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if ((e.ctrlKey || e.metaKey) && e.key === "z") {
      if (e.shiftKey) {
        redo();
      } else {
        undo();
      }
      e.preventDefault();
    }
  }

  function bind() {
    document.addEventListener("keydown", handleKeydown);
  }

  function unbind() {
    document.removeEventListener("keydown", handleKeydown);
  }

  return { push, undo, redo, bind, unbind };
}
