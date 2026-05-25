"""ViewRepository — persists BoardView blocks (type='view') via BlockRepository."""
from __future__ import annotations

import time

from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from nexo.models import Block
from nexo.models.enums import IViewType
from nexo.schemas.view import BoardViewCreate, BoardViewUpdate, ViewFields


class ViewRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def _view_query(self, board_id: str):
        return select(Block).where(
            Block.board_id == board_id,
            Block.type == "view",
            Block.delete_at == 0,
        )

    def get(self, view_id: str) -> Block | None:
        block = self.db.get(Block, view_id)
        if block and block.type == "view" and block.delete_at == 0:
            return block
        return None

    def list_for_board(self, board_id: str) -> list[Block]:
        stmt = self._view_query(board_id).order_by(Block.create_at)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, data: BoardViewCreate, created_by: str) -> Block:
        now = int(time.time() * 1000)
        view_fields = ViewFields(view_type=data.view_type)
        block = Block(
            board_id=data.board_id,
            created_by=created_by,
            modified_by=created_by,
            type="view",
            title=data.title,
            fields=view_fields.model_dump(by_alias=False),
            schema=1,
            create_at=now,
            update_at=now,
            delete_at=0,
        )
        self.db.add(block)
        self.db.commit()
        self.db.refresh(block)
        return block

    def update(self, view_id: str, data: BoardViewUpdate, modified_by: str) -> Block | None:
        block = self.get(view_id)
        if not block:
            return None
        now = int(time.time() * 1000)
        if data.title is not None:
            block.title = data.title
        if data.fields is not None:
            block.fields = data.fields
        block.modified_by = modified_by
        block.update_at = now
        self.db.commit()
        self.db.refresh(block)
        return block

    def soft_delete(self, view_id: str) -> bool:
        block = self.get(view_id)
        if not block:
            return False
        block.delete_at = int(time.time() * 1000)
        self.db.commit()
        return True
