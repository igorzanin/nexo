import time

from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from nexo.models import Board
from nexo.schemas.board import BoardCreate, BoardUpdate


class BoardRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def get(self, board_id: str) -> Board | None:
        return self.db.get(Board, board_id)

    def get_by_team(self, team_id: str) -> list[Board]:
        stmt = select(Board).where(Board.team_id == team_id, Board.delete_at == 0)
        return list(self.db.execute(stmt).scalars().all())

    def get_board_count(self, team_id: str) -> int:
        stmt = select(Board).where(Board.team_id == team_id, Board.delete_at == 0)
        return len(list(self.db.execute(stmt).scalars().all()))

    def create(self, data: BoardCreate) -> Board:
        now = int(time.time() * 1000)
        board = Board(
            team_id=data.team_id,
            type=data.type.value if hasattr(data.type, "value") else data.type,
            title=data.title,
            description=data.description,
            icon=data.icon,
            show_description=data.show_description,
            is_template=data.is_template,
            template_version=data.template_version,
            minimum_role=data.minimum_role.value if hasattr(data.minimum_role, "value") else data.minimum_role,
            create_at=now,
            update_at=now,
            delete_at=0,
        )
        self.db.add(board)
        self.db.commit()
        self.db.refresh(board)
        return board

    def update(self, board_id: str, data: BoardUpdate) -> Board | None:
        board = self.get(board_id)
        if not board:
            return None
        now = int(time.time() * 1000)
        patch = data.model_dump(exclude_unset=True)
        patch.pop("channel_id", None)
        for key, value in patch.items():
            setattr(board, key, value)
        board.update_at = now
        self.db.commit()
        self.db.refresh(board)
        return board

    def soft_delete(self, board_id: str) -> bool:
        board = self.get(board_id)
        if not board:
            return False
        board.delete_at = int(time.time() * 1000)
        self.db.commit()
        return True

    def undelete(self, board_id: str) -> bool:
        board = self.get(board_id)
        if not board or board.delete_at == 0:
            return False
        board.delete_at = 0
        self.db.commit()
        return True
