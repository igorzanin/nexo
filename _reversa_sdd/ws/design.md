# WebSocket, Design Técnico

## Estrutura

```
nexo/ws/
├── __init__.py
├── server.py         # WebSocket connection manager
├── models.py         # Message schemas (Pydantic)
└── dependencies.py   # Auth dependency for WS
```

## Connection Manager

```python
class WSConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.listeners_by_team: dict[str, set[str]] = defaultdict(set)
        self.listeners_by_block: dict[str, set[str]] = defaultdict(set)
        self.user_connections: dict[str, set[str]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, user_id: str = ""):
        await websocket.accept()
        conn_id = str(uuid4())
        async with self._lock:
            self.active_connections[conn_id] = websocket
            if user_id:
                self.user_connections[user_id].add(conn_id)
        return conn_id

    async def disconnect(self, conn_id: str):
        async with self._lock:
            ws = self.active_connections.pop(conn_id, None)
            for team, conns in self.listeners_by_team.items():
                self.listeners_by_team[team] = [c for c in conns if c != conn_id]
            for block, conns in self.listeners_by_block.items():
                self.listeners_by_block[block] = [c for c in conns if c != conn_id]

    async def broadcast_to_team(self, team_id: str, message: dict):
        async with self._lock:
            for conn_id in self.listeners_by_team.get(team_id, []):
                ws = self.active_connections.get(conn_id)
                if ws:
                    await ws.send_json(message)
```

## FastAPI WebSocket Endpoint

```python
@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
    read_token: Optional[str] = Query(None),
):
    user = None
    if token:
        try:
            payload = decode_token(token)
            user = await user_repo.get(payload["sub"])
        except:
            pass

    conn_id = await manager.connect(websocket, user.id if user else "")

    try:
        while True:
            data = await websocket.receive_json()
            command = WSCommand(**data)

            if command.action == "AUTH":
                user = await handle_auth(websocket, command.token)
            elif command.action == "SUBSCRIBE_TEAM" and user:
                await manager.subscribe_to_team(conn_id, command.team_id)
            elif command.action == "SUBSCRIBE_BLOCKS" and read_token:
                # validar read_token e inscrever
                ...
    except WebSocketDisconnect:
        await manager.disconnect(conn_id)
```

## Dependências
- FastAPI WebSocket (nativo)
