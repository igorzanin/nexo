import time

from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from nexo.auth.roles import Permission
from nexo.models import BoardMember
from nexo.schemas.board_member import BoardMemberCreate
from nexo.services.permissions import PermissionsService


class MemberService:
    def __init__(self, db: DBSession):
        self.db = db
        self.permission_svc = PermissionsService(db)

    def get_members(self, board_id: str) -> list[BoardMember]:
        stmt = select(BoardMember).where(BoardMember.board_id == board_id)
        return list(self.db.execute(stmt).scalars().all())

    def add_member(self, board_id: str, data: BoardMemberCreate, actor_id: str) -> BoardMember:
        if not self.permission_svc.has_permission_to_board(
            actor_id, board_id, Permission.MANAGE_BOARD_ROLES
        ):
            raise PermissionError("Cannot manage board roles")

        now = int(time.time() * 1000)
        member = BoardMember(
            board_id=board_id,
            user_id=data.userId,
            roles=data.minimumRole.value if hasattr(data.minimumRole, "value") else data.minimumRole,
            scheme_admin=data.schemeAdmin,
            scheme_editor=data.schemeEditor,
            scheme_commenter=data.schemeCommenter,
            scheme_viewer=data.schemeViewer,
            create_at=now,
            update_at=now,
            delete_at=0,
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
            BoardMember.board_id == board_id,
            BoardMember.user_id == user_id,
        )
        member = self.db.execute(stmt).scalar_one_or_none()
        if not member:
            raise ValueError("Member not found")

        member.roles = data.minimumRole.value if hasattr(data.minimumRole, "value") else data.minimumRole
        member.scheme_admin = data.schemeAdmin
        member.scheme_editor = data.schemeEditor
        member.scheme_commenter = data.schemeCommenter
        member.scheme_viewer = data.schemeViewer
        member.update_at = int(time.time() * 1000)
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
            BoardMember.board_id == board_id,
            BoardMember.user_id == user_id,
        )
        member = self.db.execute(stmt).scalar_one_or_none()
        if not member:
            return False
        self.db.delete(member)
        self.db.commit()
        return True
