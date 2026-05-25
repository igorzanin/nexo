<script setup lang="ts">
import { computed } from "vue";
import type { PermissionCheck } from "../../composables/useHasPermissions";

const props = defineProps<{
  permissions: PermissionCheck[];
  board: any;
  member: any;
}>();

const emit = defineEmits<{
  (e: "denied"): void;
}>();

const allowed = computed(() => {
  if (!props.board) return false;
  const role = props.member?.schemeAdmin ? "admin"
    : props.member?.schemeEditor ? "editor"
    : props.member?.schemeCommenter ? "commenter"
    : props.member?.schemeViewer ? "viewer"
    : "";

  if (role === "admin") return true;

  const permMap: Record<string, string[]> = {
    view_board: ["viewer", "commenter", "editor", "admin"],
    comment_board_cards: ["commenter", "editor", "admin"],
    manage_board_cards: ["editor", "admin"],
    manage_board_properties: ["editor", "admin"],
    manage_board_type: ["admin"],
    delete_board: ["admin"],
    share_board: ["admin"],
    manage_board_roles: ["admin"],
    delete_others_comments: ["admin"],
  };

  return props.permissions.every((p) => permMap[p]?.includes(role));
});
</script>

<template>
  <slot v-if="allowed" />
  <slot v-else name="fallback" />
</template>
