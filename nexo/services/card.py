from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from nexo.models import Block
from nexo.repositories.block import BlockRepository
from nexo.schemas.block import BlockCreate, BlockUpdate


class CardService:
    def __init__(self, db: DBSession):
        self.db = db
        self.block_repo = BlockRepository(db)

    def create(self, data: BlockCreate, user_id: str) -> Block:
        card_data = data.model_copy(update={"type": "card"})
        return self.block_repo.create(card_data, user_id)

    def get(self, card_id: str) -> Block | None:
        block = self.block_repo.get(card_id)
        if block and block.type == "card":
            return block
        return None

    def get_by_board(self, board_id: str) -> list[Block]:
        stmt = select(Block).where(
            Block.board_id == board_id,
            Block.type == "card",
            Block.delete_at == 0,
        )
        return list(self.db.execute(stmt).scalars().all())

    def update(self, card_id: str, data: BlockUpdate, user_id: str) -> Block:
        block = self.block_repo.update(card_id, data, user_id)
        if block is None:
            raise ValueError("Card not found")
        return block

    def delete(self, card_id: str) -> bool:
        return self.block_repo.soft_delete(card_id)

    def get_content_blocks(self, card_id: str) -> list[Block]:
        stmt = select(Block).where(
            Block.parent_id == card_id,
            Block.delete_at == 0,
        )
        return list(self.db.execute(stmt).scalars().all())
