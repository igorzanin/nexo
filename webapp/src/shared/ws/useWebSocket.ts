/**
 * shared/ws/useWebSocket.ts
 * Composable Vue 3 para conexão WebSocket com reconexão automática.
 * Expõe `connected`, `connect`, `disconnect`, `send`, `onMessage`.
 */
import { ref, onUnmounted } from "vue";
import { WsClient } from "./client";

export function useWebSocket() {
  const wsClient = new WsClient();
  const connected = ref(false);

  function connect(token: string): void {
    wsClient.connect(token);
    const checkInterval = setInterval(() => {
      connected.value = wsClient.connected;
    }, 300);
    onUnmounted(() => clearInterval(checkInterval));
  }

  function disconnect(): void {
    wsClient.disconnect();
    connected.value = false;
  }

  function send(data: Record<string, unknown>): void {
    wsClient.send(data);
  }

  function onMessage(handler: (data: unknown) => void): () => void {
    return wsClient.onMessage(handler);
  }

  onUnmounted(disconnect);

  return { connected, connect, disconnect, send, onMessage };
}
