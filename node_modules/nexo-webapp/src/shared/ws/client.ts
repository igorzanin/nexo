/**
 * shared/ws/client.ts
 * Conexão WebSocket bruta com reconexão automática (BR-MIGRAR-022).
 * useWebSocket.ts consome este módulo; componentes não usam diretamente.
 */
export type WsEventHandler = (data: unknown) => void;

export class WsClient {
  private ws: WebSocket | null = null;
  private token: string = "";
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private handlers: WsEventHandler[] = [];

  get connected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }

  connect(token: string): void {
    this.token = token;
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const url = `${protocol}//${window.location.host}/ws?token=${token}`;
    this.ws = new WebSocket(url);

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handlers.forEach((h) => h(data));
    };

    this.ws.onclose = () => {
      this.reconnectTimer = setTimeout(() => this.connect(this.token), 5000);
    };

    this.ws.onerror = () => {
      this.ws?.close();
    };
  }

  disconnect(): void {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    this.ws?.close();
    this.ws = null;
  }

  send(data: Record<string, unknown>): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  onMessage(handler: WsEventHandler): () => void {
    this.handlers.push(handler);
    return () => {
      this.handlers = this.handlers.filter((h) => h !== handler);
    };
  }
}
