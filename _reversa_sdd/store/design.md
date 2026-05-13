# Store, Design Técnico

## Estrutura

```
nexo/webapp/src/stores/
├── index.ts            # createPinia + export
├── boardStore.ts       # useBoardStore
├── cardStore.ts        # useCardStore (getters complexos)
├── viewStore.ts        # useViewStore (smartViewUpdate)
├── userStore.ts        # useUserStore
├── teamStore.ts        # useTeamStore
├── commentStore.ts     # useCommentStore
├── contentStore.ts     # useContentStore
├── attachmentStore.ts  # useAttachmentStore
├── sidebarStore.ts     # useSidebarStore
├── searchStore.ts      # useSearchStore
├── configStore.ts      # useConfigStore
├── errorStore.ts       # useErrorStore
├── templateStore.ts    # useTemplateStore
└── languageStore.ts    # useLanguageStore
```

## Exemplo de Store (Pinia)

```typescript
// stores/boardStore.ts
export const useBoardStore = defineStore('boards', () => {
  // State
  const boards = ref<Record<string, Board>>({})
  const current = ref('')
  const templates = ref<Record<string, Board>>({})
  const membersInBoards = ref<Record<string, Record<string, BoardMember>>>({})
  const myBoardMemberships = ref<Record<string, BoardMember>>({})

  // Getters
  const currentBoard = computed(() => boards.value[current.value])
  const boardList = computed(() => Object.values(boards.value))

  // Actions
  async function fetchBoards() {
    const data = await api.getBoards()
    boards.value = keyById(data)
  }

  async function createBoard(data: BoardCreate) {
    const board = await api.createBoard(data)
    boards.value[board.id] = board
    return board
  }

  return { boards, current, templates, membersInBoards, myBoardMemberships,
           currentBoard, boardList, fetchBoards, createBoard, ... }
})
```

## Fluxo de Dados

```
Componente → Mutator (composable)
  → API Service (axios) → Persiste no servidor
  → dispatch(store.action) → Atualiza estado local

WebSocket → onmessage → dispatch(store.action) → Atualiza em tempo real
```

## Dependências
- `pinia`
- `axios`
- Tipos em `../types/`
