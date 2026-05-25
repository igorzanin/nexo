"""Unit tests for board domain rules (BR-MIGRAR-001, BR-MIGRAR-003)."""
import pytest

from nexo.domain.enums import BoardType, MinimumRole
from nexo.domain.exceptions import (
    InvalidBoardTypeError,
    InvalidMinimumRoleError,
    LastAdminError,
)
from nexo.domain.rules.board import (
    assert_not_last_admin,
    validate_board_type,
    validate_minimum_role,
)


class TestValidateBoardType:
    def test_open_board(self):
        assert validate_board_type("O") == BoardType.OPEN

    def test_private_board(self):
        assert validate_board_type("P") == BoardType.PRIVATE

    def test_invalid_raises(self):
        with pytest.raises(InvalidBoardTypeError):
            validate_board_type("X")

    def test_empty_string_raises(self):
        with pytest.raises(InvalidBoardTypeError):
            validate_board_type("")


class TestValidateMinimumRole:
    @pytest.mark.parametrize("value", ["", "viewer", "commenter", "editor", "admin"])
    def test_valid_roles(self, value):
        result = validate_minimum_role(value)
        assert result.value == value

    def test_invalid_raises(self):
        with pytest.raises(InvalidMinimumRoleError):
            validate_minimum_role("superadmin")


class TestAssertNotLastAdmin:
    def test_can_remove_when_multiple_admins(self):
        assert_not_last_admin(admin_count=2, target_is_admin=True)

    def test_can_remove_non_admin_when_one_admin(self):
        assert_not_last_admin(admin_count=1, target_is_admin=False)

    def test_raises_when_last_admin_removed(self):
        with pytest.raises(LastAdminError):
            assert_not_last_admin(admin_count=1, target_is_admin=True)


class TestMinimumRoleOrdering:
    def test_admin_gt_editor(self):
        assert MinimumRole.ADMIN > MinimumRole.EDITOR

    def test_viewer_lt_commenter(self):
        assert MinimumRole.VIEWER < MinimumRole.COMMENTER

    def test_equal(self):
        assert MinimumRole.EDITOR >= MinimumRole.EDITOR
