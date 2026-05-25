from enum import Enum


class BoardType(str, Enum):
    OPEN = "O"
    PRIVATE = "P"


class MinimumRole(str, Enum):
    NONE = ""
    VIEWER = "viewer"
    COMMENTER = "commenter"
    EDITOR = "editor"
    ADMIN = "admin"

    def __le__(self, other: "MinimumRole") -> bool:
        return _ROLE_ORDER[self] <= _ROLE_ORDER[other]

    def __lt__(self, other: "MinimumRole") -> bool:
        return _ROLE_ORDER[self] < _ROLE_ORDER[other]

    def __ge__(self, other: "MinimumRole") -> bool:
        return _ROLE_ORDER[self] >= _ROLE_ORDER[other]

    def __gt__(self, other: "MinimumRole") -> bool:
        return _ROLE_ORDER[self] > _ROLE_ORDER[other]


_ROLE_ORDER: dict[MinimumRole, int] = {
    MinimumRole.NONE: 0,
    MinimumRole.VIEWER: 1,
    MinimumRole.COMMENTER: 2,
    MinimumRole.EDITOR: 3,
    MinimumRole.ADMIN: 4,
}


class BlockType(str, Enum):
    CARD = "card"
    VIEW = "view"
    COMMENT = "comment"
    TEXT = "text"
    IMAGE = "image"
    DIVIDER = "divider"
    ATTACHMENT = "attachment"
    CHECKBOX = "checkbox"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"


class CategoryType(str, Enum):
    SYSTEM = "system"
    CUSTOM = "custom"


class SubscriberType(str, Enum):
    USER = "user"


class Permission(str, Enum):
    VIEW_BOARD = "view_board"
    COMMENT_BOARD_CARDS = "comment_board_cards"
    MANAGE_BOARD_CARDS = "manage_board_cards"
    MANAGE_BOARD_PROPERTIES = "manage_board_properties"
    DELETE_OTHERS_COMMENTS = "delete_others_comments"
    MANAGE_BOARD_ROLES = "manage_board_roles"
    SHARE_BOARD = "share_board"
    DELETE_BOARD = "delete_board"
    MANAGE_BOARD_TYPE = "manage_board_type"
