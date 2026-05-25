# Actions: Fechamento de lacunas do frontend

> Identificador: `002-frontend-gap-closure`
> Data: `2026-05-14`
> Roadmap: `_reversa_forward/002-frontend-gap-closure/roadmap.md`

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 26 |
| Paralelizáveis (`[//]`) | 12 |
| Maior cadeia de dependência | 4 (T001 → T005 → T010 → T012) |

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Estender Mutator com undo/redo: gerar `[updatePatch, undoPatch]` em insertBlock, patchBlock, deleteBlock; implementar undo stack | - | - | `webapp/src/composables/useMutator.ts` | 🟢 | `[X]` |
| T002 | Implementar Modal/Dialog genérico reutilizável com Bootstrap 5.3, slots header/body/footer, suporte a tamanhos | - | `[//]` | `webapp/src/components/widgets/Modal.vue` | 🟢 | `[X]` |
| T003 | Adicionar store methods para undo stack: pushAction, undo, canUndo | T001 | - | `webapp/src/stores/` | 🟢 | `[X]` |

## Fase 2, Testes

*Omitida — sem TDD no escopo atual.*

## Fase 3, Núcleo

### Módulo 1: Kanban

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Implementar DnD de cards entre colunas no Kanban usando vuedraggable | - | - | `webapp/src/components/kanban/Kanban.vue` | 🟢 | `[X]` |
| T005 | Implementar exibição de cálculos (count, sum, avg, min, max) no header das colunas Kanban | T001 | `[//]` | `webapp/src/components/kanban/KanbanColumn.vue` | 🟢 | `[X]` |
| T006 | Implementar card badges (contagem de comentários, indicador de descrição, data) | - | `[//]` | `webapp/src/components/kanban/KanbanCard.vue` | 🟢 | `[X]` |

### Módulo 2: Table

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T007 | Implementar agrupamento de linhas na Table: TableGroup, TableGroupHeaderRow colapsável | T004 | - | `webapp/src/components/table/` | 🟢 | `[ ]` |
| T008 | Implementar redimensionamento de colunas na Table com HorizontalGrip | - | `[//]` | `webapp/src/components/table/` | 🟢 | `[ ]` |
| T009 | Implementar header menu na Table (sort, hide, group by, wrap) | - | `[//]` | `webapp/src/components/table/TableHeader.vue` | 🟢 | `[ ]` |
| T010 | Implementar footer de cálculos na Table (count, sum, avg, min, max) | T005 | - | `webapp/src/components/table/Table.vue` | 🟢 | `[ ]` |

### Módulo 3: Calendar

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T011 | Substituir grid simples por FullCalendar: navegação mês/semana/dia, criação de card por clique, drag para reagendar | - | - | `webapp/src/components/calendar/Calendar.vue` | 🟢 | `[ ]` |

### Módulo 4: Card Detail

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T012 | Implementar editor de blocos de conteúdo no CardDialog: adicionar, editar (click-to-edit), reordenar (drag), deletar blocos de texto, imagem, checkbox, divisor, h1-h3 | T001 | - | `webapp/src/components/cardDetail/` | 🟢 | `[ ]` |
| T013 | Implementar content add menu flutuante "+" com tipos de bloco (text, image, checkbox, divider, heading) | T012 | - | `webapp/src/components/cardDetail/` | 🟢 | `[ ]` |
| T014 | Implementar upload de imagem e anexo no CardDialog | - | `[//]` | `webapp/src/components/cardDetail/` | 🟢 | `[ ]` |
| T015 | Implementar property editors faltantes (8): multiPerson, createdBy, createdTime, updatedBy, updatedTime, unknown | - | `[//]` | `webapp/src/components/properties/` | 🟢 | `[ ]` |

### Módulo 5: Demais

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T016 | Implementar UI de filtros completa no ViewHeader: FilterComponent, FilterEntry, FilterValue, dateFilter, multipersonFilter | - | - | `webapp/src/components/common/` | 🟢 | `[ ]` |
| T017 | Implementar view menu com rename, duplicate, delete | - | `[//]` | `webapp/src/components/common/ViewHeader.vue` | 🟢 | `[X]` |
| T018 | Implementar view type switcher (display-by) no ViewHeader | - | `[//]` | `webapp/src/components/common/ViewHeader.vue` | 🟢 | `[X]` |
| T019 | Implementar PropertyMenu e ValueSelector widgets | T002 | `[//]` | `webapp/src/components/widgets/` | 🟢 | `[ ]` |
| T020 | Implementar board archive import/export (boardarchive JSON) | - | `[//]` | `webapp/src/utils/archiver.ts` | 🟢 | `[ ]` |
| T021 | Implementar NewCardButton com suporte a template items | - | `[//]` | `webapp/src/components/common/` | 🟢 | `[ ]` |

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T022 | Integrar undo stack com store mutations: toda ação do Mutator alimenta pilha, Ctrl+Z desfaz | T003 | - | `webapp/src/composables/useUndoRedo.ts` | 🟢 | `[X]` |
| T023 | Integrar filtros com BoardView.fields.filter: persistir ao salvar view | T016 | - | `webapp/src/composables/useMutator.ts` | 🟢 | `[ ]` |

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T024 | Adicionar estilos e refinamentos de UI para todos os novos componentes (consistência Bootstrap 5.3) | T022, T023 | `[//]` | `webapp/src/components/` | 🟢 | `[ ]` |
| T025 | Gerar regression-watch.md documentando comportamento crítico que não pode regredir | T024 | - | `_reversa_forward/002-frontend-gap-closure/regression-watch.md` | 🟢 | `[ ]` |
| T026 | Executar re-extração reversa e verificar regressão semântica | T025 | - | `.reversa/` | 🟢 | `[ ]` |

## Notas de execução

- Ordem respeita módulos: Kanban → Table → Calendar → Card Detail → Demais
- T001 (undo/redo) é pré-requisito para T005, T010, T012
- T002 (Modal genérico) é pré-requisito para T019
- vuedraggable e @fullcalendar/vue3 já estão instalados
- Nenhuma mudança no backend

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-05-14 | Versão inicial gerada por `/reversa-to-do` | reversa |
