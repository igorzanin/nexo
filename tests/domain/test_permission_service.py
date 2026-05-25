"""Unit tests for PermissionService (BR-MIGRAR-003, BR-MIGRAR-009)."""
import pytest

from nexo.domain.enums import BoardType, MinimumRole, Permission
from nexo.domain.exceptions import PermissionDeniedError
from nexo.domain.services.permission import PermissionService


# ── helpers ────────────────────────────────────────────────────────────────────

def _check(
    member_role: MinimumRole,
    permission: Permission,
    *,
    board_type: BoardType = BoardType.PRIVATE,
    minimum_role: MinimumRole = MinimumRole.NONE,
    is_team_member: bool = True,
) -> bool:
    return PermissionService.has_permission(
        member_role=member_role,
        board_minimum_role=minimum_role,
        board_type=board_type,
        is_team_member=is_team_member,
        permission=permission,
    )


# ── Admin ──────────────────────────────────────────────────────────────────────

class TestAdminPermissions:
    @pytest.mark.parametrize("perm", list(Permission))
    def test_admin_has_all_permissions(self, perm):
        assert _check(MinimumRole.ADMIN, perm)


# ── Editor ─────────────────────────────────────────────────────────────────────

class TestEditorPermissions:
    EDITOR_ALLOWED = {
        Permission.VIEW_BOARD,
        Permission.COMMENT_BOARD_CARDS,
        Permission.MANAGE_BOARD_CARDS,
        Permission.MANAGE_BOARD_PROPERTIES,
    }
    EDITOR_DENIED = {
        Permission.DELETE_OTHERS_COMMENTS,
        Permission.MANAGE_BOARD_ROLES,
        Permission.SHARE_BOARD,
        Permission.DELETE_BOARD,
        Permission.MANAGE_BOARD_TYPE,
    }

    @pytest.mark.parametrize("perm", list(EDITOR_ALLOWED))
    def test_editor_allowed(self, perm):
        assert _check(MinimumRole.EDITOR, perm)

    @pytest.mark.parametrize("perm", list(EDITOR_DENIED))
    def test_editor_denied(self, perm):
        assert not _check(MinimumRole.EDITOR, perm)


# ── Commenter ──────────────────────────────────────────────────────────────────

class TestCommenterPermissions:
    def test_commenter_can_view(self):
        assert _check(MinimumRole.COMMENTER, Permission.VIEW_BOARD)

    def test_commenter_can_comment(self):
        assert _check(MinimumRole.COMMENTER, Permission.COMMENT_BOARD_CARDS)

    def test_commenter_cannot_edit_cards(self):
        assert not _check(MinimumRole.COMMENTER, Permission.MANAGE_BOARD_CARDS)


# ── Viewer ─────────────────────────────────────────────────────────────────────

class TestViewerPermissions:
    def test_viewer_can_view(self):
        assert _check(MinimumRole.VIEWER, Permission.VIEW_BOARD)

    def test_viewer_cannot_comment(self):
        assert not _check(MinimumRole.VIEWER, Permission.COMMENT_BOARD_CARDS)


# ── MinimumRole floor ──────────────────────────────────────────────────────────

class TestMinimumRoleFloor:
    def test_floor_elevates_viewer_to_commenter(self):
        # Member has VIEWER role, but board minimum is COMMENTER
        assert _check(
            MinimumRole.VIEWER,
            Permission.COMMENT_BOARD_CARDS,
            minimum_role=MinimumRole.COMMENTER,
        )

    def test_floor_does_not_lower_admin(self):
        # Admin stays admin even if floor is viewer
        assert _check(
            MinimumRole.ADMIN,
            Permission.DELETE_BOARD,
            minimum_role=MinimumRole.VIEWER,
        )


# ── Open board synthetic membership ───────────────────────────────────────────

class TestOpenBoardAccess:
    def test_non_member_gets_viewer_on_open_board(self):
        """Team member with no explicit membership gets at least Viewer on Open board."""
        assert PermissionService.has_permission(
            member_role=MinimumRole.NONE,
            board_minimum_role=MinimumRole.NONE,
            board_type=BoardType.OPEN,
            is_team_member=True,
            permission=Permission.VIEW_BOARD,
        )

    def test_non_member_on_open_board_cannot_edit(self):
        assert not PermissionService.has_permission(
            member_role=MinimumRole.NONE,
            board_minimum_role=MinimumRole.NONE,
            board_type=BoardType.OPEN,
            is_team_member=True,
            permission=Permission.MANAGE_BOARD_CARDS,
        )

    def test_non_team_member_cannot_view_open_board(self):
        """Non-team members get no access even on Open boards."""
        assert not PermissionService.has_permission(
            member_role=MinimumRole.NONE,
            board_minimum_role=MinimumRole.NONE,
            board_type=BoardType.OPEN,
            is_team_member=False,
            permission=Permission.VIEW_BOARD,
        )


# ── assert_permission ──────────────────────────────────────────────────────────

class TestAssertPermission:
    def test_raises_on_denied(self):
        with pytest.raises(PermissionDeniedError):
            PermissionService.assert_permission(
                member_role=MinimumRole.VIEWER,
                board_minimum_role=MinimumRole.NONE,
                board_type=BoardType.PRIVATE,
                is_team_member=True,
                permission=Permission.DELETE_BOARD,
            )

    def test_no_raise_on_allowed(self):
        PermissionService.assert_permission(
            member_role=MinimumRole.ADMIN,
            board_minimum_role=MinimumRole.NONE,
            board_type=BoardType.PRIVATE,
            is_team_member=True,
            permission=Permission.DELETE_BOARD,
        )
