import { createNanoEvents } from "nanoevents";

type FlashType = "success" | "error" | "info" | "warning";

interface FlashEvent {
  message: string;
  type: FlashType;
  duration: number;
}

const emitter = createNanoEvents<{
  flash: (event: FlashEvent) => void;
}>();

export function useFlashMessage() {
  function show(message: string, type: FlashType = "info", duration: number = 3000) {
    emitter.emit("flash", { message, type, duration });
  }

  function onFlash(handler: (event: FlashEvent) => void) {
    return emitter.on("flash", handler);
  }

  return { show, onFlash };
}
