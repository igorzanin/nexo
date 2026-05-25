/**
 * features/boards/stores/boards.store.ts
 * Feature-scoped re-export do store de boards global.
 * Componentes de boards importam daqui para desacoplar da camada global.
 */
export { useBoardStore as useBoardsStore } from "../../../stores/boardStore";
