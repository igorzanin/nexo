from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from sqlalchemy.orm import Session as DBSession

from nexo.auth.jwt import decode_token
from nexo.db.session import get_db
from nexo.models import Sharing
from nexo.ws import manager
from nexo.ws.models import WSCommand
from nexo.config import get_settings

router = APIRouter(tags=["ws"])
settings = get_settings()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(default=""),
    read_token: str = Query(default=""),
):
    user_id = ""
    if token:
        payload = decode_token(token)
        if payload and payload.get("type") == "access":
            user_id = payload.get("sub", "")

    conn_id = await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_json()
            command = WSCommand(**data)

            if command.action == "AUTH":
                payload = decode_token(command.token)
                if payload and payload.get("type") == "access":
                    uid = payload.get("sub", "")
                    if uid:
                        user_id = uid
                        async with manager._lock:
                            manager.conn_user[conn_id] = user_id
                            manager.user_connections[user_id].add(conn_id)
                        await manager.send_to(conn_id, {"action": "AUTH", "userId": user_id})
                    else:
                        await manager.send_to(conn_id, {"action": "AUTH", "error": "Invalid token"})
                else:
                    await manager.send_to(conn_id, {"action": "AUTH", "error": "Invalid token"})

            elif command.action == "SUBSCRIBE_TEAM" and user_id:
                await manager.subscribe_team(conn_id, command.teamId)
                await manager.send_to(conn_id, {"action": "SUBSCRIBE_TEAM", "teamId": command.teamId})

            elif command.action == "UNSUBSCRIBE_TEAM" and user_id:
                await manager.unsubscribe_team(conn_id, command.teamId)
                await manager.send_to(conn_id, {"action": "UNSUBSCRIBE_TEAM", "teamId": command.teamId})

            elif command.action == "SUBSCRIBE_BLOCKS":
                if command.blockIds:
                    await manager.subscribe_blocks(conn_id, command.blockIds)
                    await manager.send_to(conn_id, {"action": "SUBSCRIBE_BLOCKS", "blockIds": command.blockIds})

            elif command.action == "UNSUBSCRIBE_BLOCKS":
                if command.blockIds:
                    await manager.unsubscribe_blocks(conn_id, command.blockIds)
                    await manager.send_to(conn_id, {"action": "UNSUBSCRIBE_BLOCKS", "blockIds": command.blockIds})

    except WebSocketDisconnect:
        await manager.disconnect(conn_id)
