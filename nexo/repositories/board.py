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
        stmt = select(Board).where(Board.teamId == team_id, Board.deleteAt == 0)
        return list(self.db.execute(stmt).scalars().all())

    def get_board_count(self, team_id: str) -> int:
        stmt = select(Board).where(Board.teamId == team_id, Board.deleteAt == 0)
        return len(list(self.db.execute(stmt).scalars().all()))

    def create(self, data: BoardCreate) -> Board:
        now = int(time.time() * 1000)
        board = Board(
            teamId=data.team_id,
            channelId="",
            type=data.type.value if hasattr(data.type, "value") else data.type,
            title=data.title,
            description=data.description,
            icon=data.icon,
            showDescription=data.show_description,
            isTemplate=data.is_template,
            templateVersion=data.template_version,
            minimumRole=data.minimum_role.value if hasattr(data.minimum_role, "value") else data.minimum_role,
            createAt=now,
            updateAt=now,
            deleteAt=0,
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
        for key, value in patch.items():
            setattr(board, key, value)
        board.updateAt = now
        self.db.commit()
        self.db.refresh(board)
        return board

    def soft_delete(self, board_id: str) -> bool:
        board = self.get(board_id)
        if not board:
            return False
        board.deleteAt = int(time.time() * 1000)
        self.db.commit()
        return True

    def undelete(self, board_id: str) -> bool:
        board = self.get(board_id)
        if not board or board.deleteAt == 0:
            return False
        board.deleteAt = 0
        self.db.commit()
        return True
