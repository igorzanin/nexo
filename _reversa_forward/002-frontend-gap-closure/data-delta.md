# Data Delta — Fechamento de lacunas do frontend

> Feature: `002-frontend-gap-closure`
> Data: `2026-05-14`

## Premissa

Nenhuma mudança no modelo de dados do backend. Todas as alterações são no frontend.

## 1. Tipos TypeScript

### Estado atual
Todos os tipos necessários já existem:
- `FilterGroup`, `FilterClause` — em `types/filterGroup.ts`
- `BoardView.fields.filter`, `sortOptions`, `groupById`, `visiblePropertyIds` — em `types/boardView.ts`
- `Block`, `Board`, `Card`, `ContentBlock` — em `types/block.ts`, `types/board.ts`, `types/contentBlock.ts`

### Nenhum tipo novo necessário
Os filtros, cálculos, e undo/redo usam estruturas já definidas.

## 2. Stores Pinia

### Mudanças previstas
| Store | Mudança |
|-------|---------|
| `useMutator` (composable) | Estender com undo stack e geração de patches |
| `viewStore` | Adicionar métodos renameView, duplicateView, deleteView |


### Nenhuma store nova
Todas as stores necessárias já existem.

## 3. Migrações

Nenhuma migração de banco de dados.
