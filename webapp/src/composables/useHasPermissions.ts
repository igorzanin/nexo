import { computed } from "vue";
import type { Board, BoardMember } from "../types/board";

export type PermissionCheck =
  | "view_board"
  | "comment_board_cards"
  | "manage_board_cards"
  | "manage_board_properties"
  | "manage_board_type"
  | "delete_board"
  | "share_board"
  | "manage_board_roles"
  | "delete_others_comments";

const ROLE_PERMISSIONS: Record<string, PermissionCheck[]> = {
  viewer: ["view_board"],
  commenter: ["view_board", "comment_board_cards"],
  editor: ["view_board", "comment_board_cards", "manage_board_cards", "manage_board_properties"],
  admin: [
    "view_board", "comment_board_cards", "manage_board_cards",
    "manage_board_properties", "manage_board_type", "delete_board",
    "share_board", "manage_board_roles", "delete_others_comments",
  ],
};

export function useHasPermissions(board: Board | null, member: BoardMember | null) {
  const effectiveRole = computed(() => {
    if (!board) return "";

    const memberRole = member?.schemeAdmin ? "admin"
      : member?.schemeEditor ? "editor"
      : member?.schemeCommenter ? "commenter"
      : member?.schemeViewer ? "viewer"
      : "";

    const boardMinRole = board.minimumRole || "";

    const hierarchy = ["", "viewer", "commenter", "editor", "admin"];
    const memberIdx = hierarchy.indexOf(memberRole);
    const boardIdx = hierarchy.indexOf(boardMinRole);
    return hierarchy[Math.max(memberIdx, boardIdx)];
  });

  function hasPermission(permission: PermissionCheck): boolean {
    return ROLE_PERMISSIONS[effectiveRole.value]?.includes(permission) ?? false;
  }

  const canView = computed(() => hasPermission("view_board"));
  const canComment = computed(() => hasPermission("comment_board_cards"));
  const canManageCards = computed(() => hasPermission("manage_board_cards"));
  const canManageProperties = computed(() => hasPermission("manage_board_properties"));
  const canManageType = computed(() => hasPermission("manage_board_type"));
  const canDelete = computed(() => hasPermission("delete_board"));
  const canShare = computed(() => hasPermission("share_board"));
  const canManageRoles = computed(() => hasPermission("manage_board_roles"));

  return {
    effectiveRole, hasPermission,
    canView, canComment, canManageCards, canManageProperties,
    canManageType, canDelete, canShare, canManageRoles,
  };
}
