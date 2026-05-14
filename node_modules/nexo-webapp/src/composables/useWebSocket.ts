import { ref, onUnmounted } from "vue";

export function useWebSocket() {
  const ws = ref<WebSocket | null>(null);
  const connected = ref(false);
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null;

  function connect(token: string) {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const url = `${protocol}//${window.location.host}/ws?token=${token}`;
    ws.value = new WebSocket(url);

    ws.value.onopen = () => {
      connected.value = true;
    };

    ws.value.onclose = () => {
      connected.value = false;
      reconnectTimer = setTimeout(() => connect(token), 5000);
    };

    ws.value.onerror = () => {
      ws.value?.close();
    };
  }

  function disconnect() {
    if (reconnectTimer) clearTimeout(reconnectTimer);
    ws.value?.close();
    ws.value = null;
    connected.value = false;
  }

  function send(data: Record<string, unknown>) {
    if (ws.value?.readyState === WebSocket.OPEN) {
      ws.value.send(JSON.stringify(data));
    }
  }

  function onMessage(handler: (data: unknown) => void) {
    if (ws.value) {
      ws.value.onmessage = (event) => {
        handler(JSON.parse(event.data));
      };
    }
  }

  onUnmounted(disconnect);

  return { ws, connected, connect, disconnect, send, onMessage };
}
