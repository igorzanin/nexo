# Investigation — Fechamento de lacunas do frontend

> Feature: `002-frontend-gap-closure`
> Data: `2026-05-14`

## 1. Legado vs Novo por módulo

### 1.1 Kanban

| Funcionalidade | Legado | Novo | Ação |
|---------------|--------|------|------|
| DnD cards entre colunas | `kanbanCard.tsx` + `sortable.tsx` | ❌ | Implementar com vuedraggable (já no projeto) |
| Column calculations | `kanban/calculation/` | ❌ | Criar `<Calculation>` component no KanbanColumn |
| Card badges | `cardBadges.tsx` | ❌ | Criar `<CardBadges>` component |
| Column header menu | `kanbanColumnHeader.tsx` | ❌ | Adicionar menu no header |
| Hidden column items | `kanbanHiddenColumnItem.tsx` | ❌ | Criar componente collapsed view |

### 1.2 Table

| Funcionalidade | Legado | Novo | Ação |
|---------------|--------|------|------|
| Row grouping | `tableGroup.tsx`, `tableGroupHeaderRow.tsx` | ❌ | Criar `<TableGroup>` component |
| Column resize | `horizontalGrip.tsx`, `tableColumnResizeContext.tsx` | ❌ | Criar `<HorizontalGrip>` component |
| Header menu | `tableHeaderMenu.tsx` | ❌ | Adicionar context menu no header |
| Column calculations | `table/calculation/` | ❌ | Adicionar footer row |
| Inline row add | `emptyCardButton.tsx`, `newCardButton.tsx` | ❌ | Adicionar botão "+" na última linha |

### 1.3 Calendar

| Funcionalidade | Legado | Novo | Ação |
|---------------|--------|------|------|
| FullCalendar integration | `fullCalendar.tsx` (wrapper) | ❌ grid simples | Substituir por `@fullcalendar/vue3` (já instalado) |
| Create card by date click | via FullCalendar callback | ❌ | Adicionar `dateClick` handler |
| Drag reschedule | via FullCalendar | ❌ | Adicionar `eventDrop` handler |
| Week/day views | `initialView` prop | ❌ | Adicionar view switcher |

### 1.4 Card Detail

| Funcionalidade | Legado | Novo | Ação |
|---------------|--------|------|------|
| Content block CRUD | `cardDetailContents.tsx`, `blocksEditor/` | ❌ read-only | Implementar edit mode no ContentRegistry |
| Content add menu | `cardDetailContentsMenu.tsx` | ❌ | Menu flutuante "+" com tipos de bloco |
| Image upload | `imagePaste.tsx` | ❌ | Upload via input file + API |
| Attachment upload | `attachment.tsx` | ❌ | Upload via input file + API |
| Comment edit/delete | `comment.tsx` | ❌ | Adicionar edit/delete em CommentsList |

## 2. Dependências utilizáveis

| Biblioteca | Já instalada | Uso |
|-----------|-------------|-----|
| `vuedraggable` | ✅ | DnD Kanban, Table, content blocks |
| `@fullcalendar/vue3` | ✅ | Calendar completo |
| `@fullcalendar/daygrid`, `interaction` | ✅ | Calendar plugins |
| `nanoevents` | ✅ | Flash messages pub/sub |
| `axios` | ✅ | Upload de arquivos |

## 3. Padrões aplicáveis

### Undo/redo via patches
```typescript
// useMutator.ts
async function insertBlock(board: Board, partial?: Partial<Block>): Promise<{block: Block, undoPatch: BlockPatch}> {
  const block = createBlock({ boardId: board.id, ...partial });
  const created = await api.createBlock(board.id, block);
  const undoPatch = { deleteAt: created.id }; // reverse operation
  undoStack.push({ type: 'insert', blockId: created.id, undoPatch });
  return { block: created, undoPatch };
}
```

### Filter UI
```vue
<FilterComponent :filter="view.fields.filter" @update="updateFilter">
  <FilterEntry :clause="clause" @change="onClauseChange">
    <FilterValue :property="prop" :value="val" @select="onValueSelect" />
  </FilterEntry>
</FilterComponent>
```

## 4. Dependências a adicionar

Nenhuma. Todas já estão no `package.json`.
