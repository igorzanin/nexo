import time

from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from nexo.models import Block
from nexo.schemas.block import BlockCreate, BlockUpdate


class BlockRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def get(self, block_id: str) -> Block | None:
        return self.db.get(Block, block_id)

    def get_blocks_for_board(self, board_id: str) -> list[Block]:
        stmt = select(Block).where(Block.boardId == board_id, Block.deleteAt == 0)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, data: BlockCreate, created_by: str) -> Block:
        now = int(time.time() * 1000)
        block = Block(
            boardId=data.board_id,
            parentId=data.parent_id or "",
            createdBy=created_by,
            modifiedBy=created_by,
            type=data.type.value if hasattr(data.type, "value") else data.type,
            title=data.title,
            fields=data.fields,
            schema=data.schema,
            createAt=now,
            updateAt=now,
            deleteAt=0,
        )
        self.db.add(block)
        self.db.commit()
        self.db.refresh(block)
        return block

    def batch_create(self, blocks: list[Block]) -> list[Block]:
        self.db.add_all(blocks)
        self.db.commit()
        for b in blocks:
            self.db.refresh(b)
        return blocks

    def update(self, block_id: str, data: BlockUpdate, modified_by: str) -> Block | None:
        block = self.get(block_id)
        if not block:
            return None
        now = int(time.time() * 1000)
        patch = data.model_dump(exclude_unset=True)
        for key, value in patch.items():
            setattr(block, key, value)
        block.modifiedBy = modified_by
        block.updateAt = now
        self.db.commit()
        self.db.refresh(block)
        return block

    def soft_delete(self, block_id: str) -> bool:
        block = self.get(block_id)
        if not block:
            return True
        now = int(time.time() * 1000)
        block.deleteAt = now
        self.db.commit()
        return True

    def undelete(self, block_id: str) -> bool:
        block = self.get(block_id)
        if not block or block.deleteAt == 0:
            return False
        block.deleteAt = 0
        self.db.commit()
        return True
