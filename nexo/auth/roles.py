from enum import Enum
from functools import total_ordering


class Role(str, Enum):
    NONE = ""
    VIEWER = "viewer"
    COMMENTEUR = "commenter"
    EDITOR = "editor"
    ADMIN = "admin"


ROLE_HIERARCHY: list[Role] = [Role.NONE, Role.VIEWER, Role.COMMENTEUR, Role.EDITOR, Role.ADMIN]


class Permission(str, Enum):
    VIEW_BOARD = "view_board"
    COMMENT_BOARD_CARDS = "comment_board_cards"
    MANAGE_BOARD_CARDS = "manage_board_cards"
    MANAGE_BOARD_PROPERTIES = "manage_board_properties"
    MANAGE_BOARD_TYPE = "manage_board_type"
    DELETE_BOARD = "delete_board"
    SHARE_BOARD = "share_board"
    MANAGE_BOARD_ROLES = "manage_board_roles"
    DELETE_OTHERS_COMMENTS = "delete_others_comments"


ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.NONE: set(),
    Role.VIEWER: {Permission.VIEW_BOARD},
    Role.COMMENTEUR: {Permission.VIEW_BOARD, Permission.COMMENT_BOARD_CARDS},
    Role.EDITOR: {
        Permission.VIEW_BOARD,
        Permission.COMMENT_BOARD_CARDS,
        Permission.MANAGE_BOARD_CARDS,
        Permission.MANAGE_BOARD_PROPERTIES,
    },
    Role.ADMIN: {
        Permission.VIEW_BOARD,
        Permission.COMMENT_BOARD_CARDS,
        Permission.MANAGE_BOARD_CARDS,
        Permission.MANAGE_BOARD_PROPERTIES,
        Permission.MANAGE_BOARD_TYPE,
        Permission.DELETE_BOARD,
        Permission.SHARE_BOARD,
        Permission.MANAGE_BOARD_ROLES,
        Permission.DELETE_OTHERS_COMMENTS,
    },
}


def has_permission(role: Role | str, permission: Permission) -> bool:
    if isinstance(role, str):
        role = Role(role) if role else Role.NONE
    return permission in ROLE_PERMISSIONS.get(role, set())


def min_role_for_permission(permission: Permission) -> Role:
    for role in ROLE_HIERARCHY:
        if permission in ROLE_PERMISSIONS[role]:
            return role
    return Role.ADMIN


def resolve_effective_role(member_role: Role, board_minimum_role: Role) -> Role:
    member_idx = ROLE_HIERARCHY.index(member_role)
    board_idx = ROLE_HIERARCHY.index(board_minimum_role)
    return member_role if member_idx >= board_idx else board_minimum_role


def can_manage_board_type(current_role: Role) -> bool:
    return has_permission(current_role, Permission.MANAGE_BOARD_TYPE)


def can_delete_board(current_role: Role) -> bool:
    return has_permission(current_role, Permission.DELETE_BOARD)


def can_share_board(current_role: Role) -> bool:
    return has_permission(current_role, Permission.SHARE_BOARD)


def can_manage_board_roles(current_role: Role) -> bool:
    return has_permission(current_role, Permission.MANAGE_BOARD_ROLES)


def can_delete_others_comments(current_role: Role) -> bool:
    return has_permission(current_role, Permission.DELETE_OTHERS_COMMENTS)
