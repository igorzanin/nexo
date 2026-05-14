from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from nexo.auth.roles import Role, Permission
from nexo.models import BoardMember
from nexo.schemas.board_member import BoardMemberCreate
from nexo.services.permissions import PermissionsService


class MemberService:
    def __init__(self, db: DBSession):
        self.db = db
        self.permission_svc = PermissionsService(db)

    def get_members(self, board_id: str) -> list[BoardMember]:
        stmt = select(BoardMember).where(BoardMember.boardId == board_id)
        return list(self.db.execute(stmt).scalars().all())

    def add_member(self, board_id: str, data: BoardMemberCreate, actor_id: str) -> BoardMember:
        if not self.permission_svc.has_permission_to_board(
            actor_id, board_id, Permission.MANAGE_BOARD_ROLES
        ):
            raise PermissionError("Cannot manage board roles")

        member = BoardMember(
            boardId=board_id,
            userId=data.userId,
            minimumRole=data.minimumRole,
            schemeAdmin=data.schemeAdmin,
            schemeEditor=data.schemeEditor,
            schemeCommenter=data.schemeCommenter,
            schemeViewer=data.schemeViewer,
        )
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def update_member(self, board_id: str, user_id: str, data: BoardMemberCreate, actor_id: str) -> BoardMember:
        if not self.permission_svc.has_permission_to_board(
            actor_id, board_id, Permission.MANAGE_BOARD_ROLES
        ):
            raise PermissionError("Cannot manage board roles")

        if self.permission_svc.is_last_admin(board_id, user_id):
            raise ValueError("Cannot modify the last admin")

        stmt = select(BoardMember).where(
            BoardMember.boardId == board_id,
            BoardMember.userId == user_id,
        )
        member = self.db.execute(stmt).scalar_one_or_none()
        if not member:
            raise ValueError("Member not found")

        member.minimumRole = data.minimumRole
        member.schemeAdmin = data.schemeAdmin
        member.schemeEditor = data.schemeEditor
        member.schemeCommenter = data.schemeCommenter
        member.schemeViewer = data.schemeViewer
        self.db.commit()
        self.db.refresh(member)
        return member

    def remove_member(self, board_id: str, user_id: str, actor_id: str) -> bool:
        if self.permission_svc.is_last_admin(board_id, user_id):
            raise ValueError("Cannot remove the last admin")

        if not self.permission_svc.has_permission_to_board(
            actor_id, board_id, Permission.MANAGE_BOARD_ROLES
        ):
            raise PermissionError("Cannot manage board roles")

        stmt = select(BoardMember).where(
            BoardMember.boardId == board_id,
            BoardMember.userId == user_id,
        )
        member = self.db.execute(stmt).scalar_one_or_none()
        if not member:
            return False
        self.db.delete(member)
        self.db.commit()
        return True
