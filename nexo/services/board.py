import time

from sqlalchemy.orm import Session as DBSession

from nexo.auth.roles import Permission, Role
from nexo.models import Board, BoardMember
from nexo.repositories.board import BoardRepository
from nexo.repositories.category import CategoryRepository
from nexo.schemas.board import BoardCreate, BoardUpdate
from nexo.services.permissions import PermissionsService


class BoardService:
    def __init__(self, db: DBSession):
        self.db = db
        self.board_repo = BoardRepository(db)
        self.category_repo = CategoryRepository(db)
        self.permission_svc = PermissionsService(db)

    def create(self, data: BoardCreate, user_id: str) -> Board:
        board = self.board_repo.create(data)
        team_id = data.team_id

        self.db.add(BoardMember(
            boardId=board.id,
            userId=user_id,
            minimumRole=Role.ADMIN.value,
            schemeAdmin=True,
            schemeEditor=False,
            schemeCommenter=False,
            schemeViewer=False,
        ))

        categories = self.category_repo.get_by_user(user_id)
        default = next((c for c in categories if c.type == "system"), None)
        if default and not data.is_template:
            from nexo.models import CategoryBoard
            self.db.add(CategoryBoard(
                categoryId=default.id,
                boardId=board.id,
                sortOrder=0,
                hidden=False,
            ))

        self.db.commit()
        self.db.refresh(board)
        return board

    def get(self, board_id: str) -> Board | None:
        return self.board_repo.get(board_id)

    def get_by_team(self, team_id: str) -> list[Board]:
        return self.board_repo.get_by_team(team_id)

    def update(self, board_id: str, data: BoardUpdate, user_id: str) -> Board:
        board = self.board_repo.get(board_id)
        if not board:
            raise ValueError("Board not found")

        if "type" in data.model_dump(exclude_unset=True):
            if not self.permission_svc.has_permission_to_board(
                user_id, board_id, Permission.MANAGE_BOARD_TYPE
            ):
                raise PermissionError("Cannot change board type")

        if not self.permission_svc.has_permission_to_board(
            user_id, board_id, Permission.MANAGE_BOARD_CARDS
        ):
            raise PermissionError("Cannot modify board")

        updated = self.board_repo.update(board_id, data)
        if updated is None:
            raise ValueError("Board not found")
        return updated

    def delete(self, board_id: str, user_id: str) -> bool:
        if not self.permission_svc.has_permission_to_board(
            user_id, board_id, Permission.DELETE_BOARD
        ):
            raise PermissionError("Cannot delete board")
        return self.board_repo.soft_delete(board_id)

    def duplicate(self, board_id: str, user_id: str) -> Board:
        original = self.board_repo.get(board_id)
        if not original:
            raise ValueError("Board not found")

        now = int(time.time() * 1000)
        dup = Board(
            teamId=original.teamId,
            channelId="",
            type=original.type,
            title=f"{original.title} (copy)",
            description=original.description,
            icon=original.icon,
            showDescription=original.showDescription,
            isTemplate=False,
            templateVersion=0,
            minimumRole=original.minimumRole,
            createAt=now,
            updateAt=now,
            deleteAt=0,
        )
        self.db.add(dup)
        self.db.commit()
        self.db.refresh(dup)
        return dup
