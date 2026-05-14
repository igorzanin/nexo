from sqlalchemy.orm import Session as DBSession

from nexo.models import Block
from nexo.repositories.block import BlockRepository
from nexo.schemas.block import BlockCreate, BlockUpdate


class BlockService:
    def __init__(self, db: DBSession):
        self.db = db
        self.block_repo = BlockRepository(db)

    def create(self, data: BlockCreate, user_id: str) -> Block:
        board_id = data.board_id
        existing = self.db.get(Block, board_id)
        if existing is None and board_id:
            pass
        return self.block_repo.create(data, user_id)

    def get_blocks_for_board(self, board_id: str) -> list[Block]:
        return self.block_repo.get_blocks_for_board(board_id)

    def update(self, block_id: str, data: BlockUpdate, user_id: str) -> Block:
        block = self.block_repo.update(block_id, data, user_id)
        if block is None:
            raise ValueError("Block not found")
        return block

    def delete(self, block_id: str) -> bool:
        return self.block_repo.soft_delete(block_id)

    def undelete(self, block_id: str) -> bool:
        return self.block_repo.undelete(block_id)

    def batch_create(self, blocks: list[Block]) -> list[Block]:
        if len({b.boardId for b in blocks}) > 1:
            raise ValueError("All blocks in batch must belong to the same board")
        return self.block_repo.batch_create(blocks)
