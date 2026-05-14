import { createPinia } from "pinia";

export const pinia = createPinia();

export { useBoardStore } from "./boardStore";
export { useCardStore } from "./cardStore";
export { useViewStore } from "./viewStore";
export { useUserStore } from "./userStore";
export { useTeamStore } from "./teamStore";
export { useCommentStore } from "./commentStore";
export { useContentStore } from "./contentStore";
export { useAttachmentStore } from "./attachmentStore";
export { useSidebarStore } from "./sidebarStore";
export { useSearchStore } from "./searchStore";
export { useConfigStore } from "./configStore";
export { useErrorStore } from "./errorStore";
export { useTemplateStore } from "./templateStore";
export { useLanguageStore } from "./languageStore";
