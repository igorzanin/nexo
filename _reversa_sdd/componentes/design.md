# Componentes Vue 3, Design Técnico

## Estrutura de Arquivos

```
nexo/webapp/src/
├── components/
│   ├── workspace/
│   │   └── Workspace.vue
│   ├── sidebar/
│   │   ├── Sidebar.vue
│   │   ├── SidebarCategory.vue
│   │   └── SidebarBoardItem.vue
│   ├── centerPanel/
│   │   └── CenterPanel.vue
│   ├── kanban/
│   │   ├── Kanban.vue
│   │   ├── KanbanColumn.vue
│   │   └── KanbanCard.vue
│   ├── table/
│   │   ├── Table.vue
│   │   ├── TableRow.vue
│   │   └── TableHeader.vue
│   ├── calendar/
│   │   └── Calendar.vue
│   ├── gallery/
│   │   └── Gallery.vue
│   ├── cardDetail/
│   │   ├── CardDialog.vue
│   │   ├── CardDetail.vue
│   │   ├── CardDetailProperties.vue
│   │   ├── CardDetailContents.vue
│   │   ├── CommentsList.vue
│   │   └── PropertyValueElement.vue
│   ├── content/
│   │   ├── ContentRegistry.vue
│   │   ├── TextElement.vue
│   │   ├── ImageElement.vue
│   │   ├── CheckboxElement.vue
│   │   ├── DividerElement.vue
│   │   └── AttachmentElement.vue
│   ├── permissions/
│   │   └── BoardPermissionGate.vue
│   ├── search/
│   │   └── SearchDialog.vue
│   ├── share/
│   │   └── ShareBoard.vue
│   ├── onboarding/
│   │   └── OnboardingTour.vue
│   ├── flash/
│   │   └── FlashMessages.vue
│   └── common/
│       ├── ViewHeader.vue
│       ├── ViewTitle.vue
│       └── ...
├── composables/
│   ├── useWebSocket.ts
│   ├── useMutator.ts
│   ├── useHasPermissions.ts
│   ├── useCalculations.ts
│   └── useFlashMessage.ts
└── App.vue
```

## Fluxo de Dados

```
Ação do Usuário
    │
    ▼
Componente → useMutator().{insertBlock, deleteBlock, ...}
    │
    ▼
Mutator → API Service (axios) + store action
    │
    ▼
Pinia Store (storeToRefs → componente re-renderiza com reactivity)
    │
    ▼
WebSocket → composable useWebSocket → dispatch(store action) → re-renderiza
```

## Exemplo de Componente (Composition API + script setup)

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'
import { useBoardStore } from '@/stores/boardStore'
import { useCardStore } from '@/stores/cardStore'
import { useMutator } from '@/composables/useMutator'
import BoardPermissionGate from '@/components/permissions/BoardPermissionGate.vue'
import type { Card } from '@/types'

const props = defineProps<{ boardId: string }>()
const emit = defineEmits<{ cardClick: [cardId: string] }>()

const boardStore = useBoardStore()
const cardStore = useCardStore()
const mutator = useMutator()

const cards = computed(() => cardStore.getCardsByBoard(props.boardId))
const board = computed(() => boardStore.boards[props.boardId])

async function handleAddCard() {
  const card = await mutator.insertBlock(board.value!)
  emit('cardClick', card.id)
}
</script>

<template>
  <BoardPermissionGate :permissions="['manage_board_cards']">
    <button class="btn btn-primary" @click="handleAddCard">
      Novo Cartão
    </button>
  </BoardPermissionGate>

  <div class="row g-2">
    <div v-for="card in cards" :key="card.id" class="col-4">
      <div class="card" @click="emit('cardClick', card.id)">
        {{ card.title }}
      </div>
    </div>
  </div>
</template>
```

## Dependências
- `bootstrap` 5.3 + `@popperjs/core`
- `@fullcalendar/vue3`, `@fullcalendar/daygrid`, `@fullcalendar/interaction`
- `vuedraggable` (based on SortableJS)
- `axios`
- `vue-router`
- `pinia`
- `vue-i18n`
- `nanoevents` (pub/sub para flash messages)
