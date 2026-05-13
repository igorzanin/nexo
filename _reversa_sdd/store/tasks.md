# Store, Tarefas de Implementação

## Pré-requisitos
- [ ] Tipos em `types/` implementados
- [ ] API Service (axios) implementado

## Tarefas

- [ ] T-01, Configurar Pinia no Vue 3 app
- [ ] T-02, Implementar useBoardStore (boards, templates, membros)
  - Fonte legado: `webapp/src/store/boards.ts`
- [ ] T-03, Implementar useCardStore com getters complexos
  - Fonte legado: `webapp/src/store/cards.ts`
  - Getters: getCurrentViewCardsSortedFilteredAndGrouped
- [ ] T-04, Implementar useViewStore com smartViewUpdate
  - Fonte legado: `webapp/src/store/views.ts`
- [ ] T-05, Implementar useUserStore (me, boardUsers, subscriptions)
  - Fonte legado: `webapp/src/store/users.ts`
- [ ] T-06, Implementar useTeamStore
  - Fonte legado: `webapp/src/store/teams.ts`
- [ ] T-07, Implementar stores de conteúdo (comment, content, attachment)
- [ ] T-08, Implementar useSidebarStore (categorias, boards ocultos)
- [ ] T-09, Implementar stores auxiliares (search, config, error, template, language)
- [ ] T-10, Implementar initialLoad (action de boot que hidrata todas as stores)
  - Fonte legado: `webapp/src/store/initialLoad.ts`

## Notas
- 14 stores Pinia (vs 16 Redux slices — removidos `channels` e `limits`)
