from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from nexo.auth.roles import (
    Role,
    Permission,
    resolve_effective_role,
    has_permission,
    ROLE_HIERARCHY,
)
from nexo.models import Board, BoardMember


class PermissionsService:
    def __init__(self, db: DBSession):
        self.db = db

    def _get_board(self, board_id: str) -> Board | None:
        return self.db.get(Board, board_id)

    def _get_member(self, user_id: str, board_id: str) -> BoardMember | None:
        stmt = select(BoardMember).where(
            BoardMember.userId == user_id,
            BoardMember.boardId == board_id,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def has_permission_to_board(self, user_id: str, board_id: str, permission: Permission) -> bool:
        board = self._get_board(board_id)
        if not board:
            return False

        member = self._get_member(user_id, board_id)
        board_min_role = Role(board.minimumRole) if board.minimumRole else Role.NONE

        if member:
            member_role = self._flags_to_role(member)
            effective = resolve_effective_role(member_role, board_min_role)
        elif board.type == "O":
            effective = resolve_effective_role(Role.VIEWER, board_min_role)
        else:
            return False

        return has_permission(effective, permission)

    def _flags_to_role(self, member: BoardMember) -> Role:
        if member.schemeAdmin:
            return Role.ADMIN
        if member.schemeEditor:
            return Role.EDITOR
        if member.schemeCommenter:
            return Role.COMMENTEUR
        if member.schemeViewer:
            return Role.VIEWER
        if member.minimumRole:
            return Role(member.minimumRole) if member.minimumRole else Role.NONE
        return Role.NONE

    def get_user_role(self, user_id: str, board_id: str) -> Role:
        board = self._get_board(board_id)
        if not board:
            return Role.NONE

        member = self._get_member(user_id, board_id)
        board_min_role = Role(board.minimumRole) if board.minimumRole else Role.NONE

        if member:
            member_role = self._flags_to_role(member)
            return resolve_effective_role(member_role, board_min_role)
        elif board.type == "O":
            return resolve_effective_role(Role.VIEWER, board_min_role)
        return Role.NONE

    def is_last_admin(self, board_id: str, user_id: str) -> bool:
        stmt = select(BoardMember).where(
            BoardMember.boardId == board_id,
            BoardMember.schemeAdmin == True,
        )
        admins = list(self.db.execute(stmt).scalars().all())
        return len(admins) == 1 and admins[0].userId == user_id

    def can_remove_member(self, board_id: str, user_id: str, target_user_id: str) -> bool:
        if self.is_last_admin(board_id, target_user_id):
            return False
        return self.has_permission_to_board(user_id, board_id, Permission.MANAGE_BOARD_ROLES)
