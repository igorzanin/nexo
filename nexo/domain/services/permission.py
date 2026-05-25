"""PermissionService — pure domain logic for board permission evaluation.

Implements BR-MIGRAR-003 and BR-MIGRAR-009:
  - 9 permissions mapped by role (Admin / Editor / Commenter / Viewer)
  - Board.minimumRole acts as a floor for all members
  - Board type 'O' (Open): any team member implicitly gets Viewer access
  - No guest role; external access is read-only via readToken (handled in SharingService)
"""
from __future__ import annotations

from nexo.domain.enums import BoardType, MinimumRole, Permission

# Permission matrix: role → set of granted permissions
_PERMISSIONS_BY_ROLE: dict[MinimumRole, frozenset[Permission]] = {
    MinimumRole.VIEWER: frozenset({
        Permission.VIEW_BOARD,
    }),
    MinimumRole.COMMENTER: frozenset({
        Permission.VIEW_BOARD,
        Permission.COMMENT_BOARD_CARDS,
    }),
    MinimumRole.EDITOR: frozenset({
        Permission.VIEW_BOARD,
        Permission.COMMENT_BOARD_CARDS,
        Permission.MANAGE_BOARD_CARDS,
        Permission.MANAGE_BOARD_PROPERTIES,
    }),
    MinimumRole.ADMIN: frozenset({
        Permission.VIEW_BOARD,
        Permission.COMMENT_BOARD_CARDS,
        Permission.MANAGE_BOARD_CARDS,
        Permission.MANAGE_BOARD_PROPERTIES,
        Permission.DELETE_OTHERS_COMMENTS,
        Permission.MANAGE_BOARD_ROLES,
        Permission.SHARE_BOARD,
        Permission.DELETE_BOARD,
        Permission.MANAGE_BOARD_TYPE,
    }),
    MinimumRole.NONE: frozenset(),
}

_ROLE_ORDER: dict[MinimumRole, int] = {
    MinimumRole.NONE: 0,
    MinimumRole.VIEWER: 1,
    MinimumRole.COMMENTER: 2,
    MinimumRole.EDITOR: 3,
    MinimumRole.ADMIN: 4,
}


def _higher_role(a: MinimumRole, b: MinimumRole) -> MinimumRole:
    return a if _ROLE_ORDER[a] >= _ROLE_ORDER[b] else b


class PermissionService:
    """Evaluate board-level permissions for a given user context.

    This service is pure: it takes only in-memory values and has no
    dependency on databases, HTTP, or any other infrastructure.
    """

    @staticmethod
    def effective_role(
        *,
        member_role: MinimumRole,
        board_minimum_role: MinimumRole,
        board_type: BoardType,
        is_team_member: bool,
    ) -> MinimumRole:
        """Compute the effective role for a user on a board.

        Rules:
        - Start with member_role (from BoardMember.roles)
        - Apply board_minimum_role as a floor
        - If board_type is Open and user is a team member, guarantee at least Viewer
        """
        effective = member_role

        # Floor from board.minimumRole
        effective = _higher_role(effective, board_minimum_role)

        # Open boards: any team member gets at least viewer
        if board_type == BoardType.OPEN and is_team_member:
            effective = _higher_role(effective, MinimumRole.VIEWER)

        return effective

    @staticmethod
    def has_permission(
        *,
        member_role: MinimumRole,
        board_minimum_role: MinimumRole,
        board_type: BoardType,
        is_team_member: bool,
        permission: Permission,
    ) -> bool:
        """Return True if the user has `permission` on this board."""
        effective = PermissionService.effective_role(
            member_role=member_role,
            board_minimum_role=board_minimum_role,
            board_type=board_type,
            is_team_member=is_team_member,
        )
        return permission in _PERMISSIONS_BY_ROLE.get(effective, frozenset())

    @staticmethod
    def assert_permission(
        *,
        member_role: MinimumRole,
        board_minimum_role: MinimumRole,
        board_type: BoardType,
        is_team_member: bool,
        permission: Permission,
    ) -> None:
        """Raise PermissionDeniedError if the user lacks `permission`."""
        from nexo.domain.exceptions import PermissionDeniedError

        if not PermissionService.has_permission(
            member_role=member_role,
            board_minimum_role=board_minimum_role,
            board_type=board_type,
            is_team_member=is_team_member,
            permission=permission,
        ):
            raise PermissionDeniedError(
                f"Permission '{permission.value}' denied for role with effective "
                f"member_role={member_role.value!r}, "
                f"board_minimum_role={board_minimum_role.value!r}."
            )

    @staticmethod
    def permissions_for_role(role: MinimumRole) -> frozenset[Permission]:
        """Return the full set of permissions granted to `role` (ignoring floor rules)."""
        return _PERMISSIONS_BY_ROLE.get(role, frozenset())
