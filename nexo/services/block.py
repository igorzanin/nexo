from sqlalchemy.orm import Session as DBSession

from nexo.models import Block
from nexo.models.block import BlockHistory
from nexo.repositories.block import BlockRepository
from nexo.schemas.block import BlockCreate, BlockUpdate


class BlockService:
    def __init__(self, db: DBSession):
        self.db = db
        self.block_repo = BlockRepository(db)

    def create(self, data: BlockCreate, user_id: str) -> Block:
        return self.block_repo.create(data, user_id)

    def get_blocks_for_board(self, board_id: str) -> list[Block]:
        return self.block_repo.get_blocks_for_board(board_id)

    def update(self, block_id: str, data: BlockUpdate, user_id: str) -> Block:
        block = self.block_repo.update(block_id, data, user_id)
        if block is None:
            raise ValueError("Block not found")
        return block

    def delete(self, block_id: str) -> bool:
        """Soft-delete block and archive snapshot to blocks_history."""
        return self.block_repo.soft_delete(block_id)

    def undelete(self, block_id: str) -> bool:
        """Restore a soft-deleted block (re-activate from blocks_history)."""
        return self.block_repo.undelete(block_id)

    def get_history(self, block_id: str) -> list[BlockHistory]:
        return self.block_repo.get_history(block_id)

    def batch_create(self, items: list[BlockCreate], user_id: str) -> list[Block]:
        if not items:
            return []
        board_ids = {item.board_id for item in items}
        if len(board_ids) > 1:
            raise ValueError("All blocks in batch must belong to the same board")
        import time
        now = int(time.time() * 1000)
        blocks = [
            Block(
                board_id=item.board_id,
                parent_id=item.parent_id or None,
                created_by=user_id,
                modified_by=user_id,
                type=item.type.value if hasattr(item.type, "value") else item.type,
                title=item.title,
                fields=item.fields,
                schema=item.schema,
                create_at=now,
                update_at=now,
                delete_at=0,
            )
            for item in items
        ]
        return self.block_repo.batch_create(blocks)
