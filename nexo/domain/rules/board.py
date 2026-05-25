"""Board invariant validators (BR-MIGRAR-001, BR-MIGRAR-003)."""
from __future__ import annotations

from nexo.domain.enums import BoardType, MinimumRole
from nexo.domain.exceptions import (
    InvalidBoardTypeError,
    InvalidMinimumRoleError,
    LastAdminError,
)


def validate_board_type(value: str) -> BoardType:
    """Raise InvalidBoardTypeError if value is not a valid BoardType."""
    try:
        return BoardType(value)
    except ValueError:
        raise InvalidBoardTypeError(
            f"Board type must be 'O' or 'P', got: {value!r}"
        )


def validate_minimum_role(value: str) -> MinimumRole:
    """Raise InvalidMinimumRoleError if value is not a valid MinimumRole."""
    try:
        return MinimumRole(value)
    except ValueError:
        raise InvalidMinimumRoleError(
            f"minimumRole must be one of {[r.value for r in MinimumRole]}, got: {value!r}"
        )


def assert_not_last_admin(admin_count: int, target_is_admin: bool) -> None:
    """Raise LastAdminError if removing/demoting would leave the board with no admin.

    Args:
        admin_count: current number of admins on the board.
        target_is_admin: whether the member being changed is currently an admin.
    """
    if target_is_admin and admin_count <= 1:
        raise LastAdminError(
            "Cannot remove or demote the last admin of a board."
        )
