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
        now = int(time.time() * 1000)

        self.db.add(
            BoardMember(
                board_id=board.id,
                user_id=user_id,
                roles=Role.ADMIN.value,
                scheme_admin=True,
                scheme_editor=False,
                scheme_commenter=False,
                scheme_viewer=False,
                create_at=now,
                update_at=now,
                delete_at=0,
            )
        )

        categories = self.category_repo.get_by_user(user_id)
        default = next((c for c in categories if c.type == "system"), None)
        if default and not data.is_template:
            from nexo.models import CategoryBoard

            self.db.add(
                CategoryBoard(
                    user_id=user_id,
                    team_id=board.team_id,
                    category_id=default.id,
                    board_id=board.id,
                    sort_order=0,
                    hide=False,
                    create_at=now,
                    update_at=now,
                    delete_at=0,
                )
            )

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
            team_id=original.team_id,
            type=original.type,
            title=f"{original.title} (copy)",
            description=original.description,
            icon=original.icon,
            show_description=original.show_description,
            is_template=False,
            template_version=0,
            minimum_role=original.minimum_role,
            create_at=now,
            update_at=now,
            delete_at=0,
        )
        self.db.add(dup)
        self.db.commit()
        self.db.refresh(dup)
        return dup
