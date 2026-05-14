import asyncio
import uuid
from collections import defaultdict

from fastapi import WebSocket


class WSConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.conn_user: dict[str, str] = {}
        self.listeners_by_team: dict[str, set[str]] = defaultdict(set)
        self.listeners_by_block: dict[str, set[str]] = defaultdict(set)
        self.user_connections: dict[str, set[str]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, user_id: str = "") -> str:
        await websocket.accept()
        conn_id = str(uuid.uuid4())
        async with self._lock:
            self.active_connections[conn_id] = websocket
            self.conn_user[conn_id] = user_id
            if user_id:
                self.user_connections[user_id].add(conn_id)
        return conn_id

    async def disconnect(self, conn_id: str):
        async with self._lock:
            ws = self.active_connections.pop(conn_id, None)
            user_id = self.conn_user.pop(conn_id, "")
            for team_id in list(self.listeners_by_team.keys()):
                self.listeners_by_team[team_id].discard(conn_id)
                if not self.listeners_by_team[team_id]:
                    del self.listeners_by_team[team_id]
            for block_id in list(self.listeners_by_block.keys()):
                self.listeners_by_block[block_id].discard(conn_id)
                if not self.listeners_by_block[block_id]:
                    del self.listeners_by_block[block_id]
            if user_id and conn_id in self.user_connections.get(user_id, set()):
                self.user_connections[user_id].discard(conn_id)
                if not self.user_connections[user_id]:
                    del self.user_connections[user_id]
            return ws

    async def subscribe_team(self, conn_id: str, team_id: str):
        async with self._lock:
            self.listeners_by_team[team_id].add(conn_id)

    async def unsubscribe_team(self, conn_id: str, team_id: str):
        async with self._lock:
            self.listeners_by_team[team_id].discard(conn_id)
            if not self.listeners_by_team[team_id]:
                del self.listeners_by_team[team_id]

    async def subscribe_blocks(self, conn_id: str, block_ids: list[str]):
        async with self._lock:
            for bid in block_ids:
                self.listeners_by_block[bid].add(conn_id)

    async def unsubscribe_blocks(self, conn_id: str, block_ids: list[str]):
        async with self._lock:
            for bid in block_ids:
                self.listeners_by_block[bid].discard(conn_id)
                if not self.listeners_by_block[bid]:
                    del self.listeners_by_block[bid]

    async def send_to(self, conn_id: str, message: dict):
        ws = self.active_connections.get(conn_id)
        if ws:
            try:
                await ws.send_json(message)
            except Exception:
                await self.disconnect(conn_id)

    async def broadcast_to_team(self, team_id: str, message: dict):
        async with self._lock:
            conns = list(self.listeners_by_team.get(team_id, []))
        tasks = [self.send_to(cid, message) for cid in conns]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_to_block(self, block_id: str, message: dict):
        async with self._lock:
            conns = list(self.listeners_by_block.get(block_id, []))
        tasks = [self.send_to(cid, message) for cid in conns]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_to_board_members(self, board_id: str, message: dict):
        from nexo.db.session import SessionLocal
        from nexo.repositories.board import BoardRepository

        db = SessionLocal()
        try:
            board = BoardRepository(db).get(board_id)
            if board:
                await self.broadcast_to_team(board.teamId, message)
        finally:
            db.close()

    async def broadcast_to_user(self, user_id: str, message: dict):
        async with self._lock:
            conns = list(self.user_connections.get(user_id, []))
        tasks = [self.send_to(cid, message) for cid in conns]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_all(self, message: dict):
        async with self._lock:
            conns = dict(self.active_connections)
        tasks = []
        for cid, ws in conns.items():
            tasks.append(self.send_to(cid, message))
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
