import time

from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from nexo.models import Block
from nexo.models.block import BlockHistory
from nexo.schemas.block import BlockCreate, BlockUpdate


class BlockRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def get(self, block_id: str) -> Block | None:
        return self.db.get(Block, block_id)

    def get_blocks_for_board(self, board_id: str) -> list[Block]:
        stmt = select(Block).where(Block.board_id == board_id, Block.delete_at == 0)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, data: BlockCreate, created_by: str) -> Block:
        now = int(time.time() * 1000)
        block = Block(
            board_id=data.board_id,
            parent_id=data.parent_id or None,
            created_by=created_by,
            modified_by=created_by,
            type=data.type.value if hasattr(data.type, "value") else data.type,
            title=data.title,
            fields=data.fields,
            schema=data.schema,
            create_at=now,
            update_at=now,
            delete_at=0,
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
        if patch.get("parent_id") == "":
            patch["parent_id"] = None
        for key, value in patch.items():
            setattr(block, key, value)
        block.modified_by = modified_by
        block.update_at = now
        self.db.commit()
        self.db.refresh(block)
        return block

    def archive_to_history(self, block: Block) -> BlockHistory:
        """Copy block snapshot to blocks_history before soft-delete."""
        now = int(time.time() * 1000)
        history = BlockHistory(
            id=block.id,
            parent_id=block.parent_id,
            root_id=block.root_id,
            created_by=block.created_by,
            modified_by=block.modified_by,
            schema=block.schema,
            type=block.type,
            title=block.title,
            fields=block.fields,
            create_at=block.create_at,
            update_at=block.update_at,
            delete_at=now,
            board_id=block.board_id,
            insert_at=now,
        )
        self.db.add(history)
        return history

    def soft_delete(self, block_id: str) -> bool:
        block = self.get(block_id)
        if not block or block.delete_at != 0:
            return True
        now = int(time.time() * 1000)
        self.archive_to_history(block)
        block.delete_at = now
        self.db.commit()
        return True

    def undelete(self, block_id: str) -> bool:
        block = self.get(block_id)
        if not block or block.delete_at == 0:
            return False
        block.delete_at = 0
        self.db.commit()
        return True

    def get_history(self, block_id: str) -> list[BlockHistory]:
        stmt = (
            select(BlockHistory)
            .where(BlockHistory.id == block_id)
            .order_by(BlockHistory.insert_at.desc())
        )
        return list(self.db.execute(stmt).scalars().all())
