# C4 Components Diagram — nexo (Frontend Vue 3)

> 🟢 CONFIRMADO

```
Pages (Vue Router)
    │
    ▼
Workspace.vue
    ├── Sidebar.vue
    │   ├── BoardsSwitcher.vue
    │   ├── SidebarCategory.vue (N)
    │   │   └── SidebarBoardItem.vue (N)
    │   ├── CreateCategory.vue
    │   ├── SidebarSettingsMenu.vue
    │   └── SidebarUserMenu.vue
    │
    └── CenterPanel.vue
        ├── ViewTitle.vue
        ├── ViewHeader.vue
        │   ├── ViewMenu.vue
        │   ├── ViewHeaderPropertiesMenu.vue
        │   ├── ViewHeaderGroupByMenu.vue
        │   ├── ViewHeaderSortMenu.vue
        │   ├── ViewHeaderActionsMenu.vue
        │   ├── ViewHeaderSearch.vue → FilterComponent → FilterEntry
        │   └── NewCardButton.vue
        │
        ├── {Kanban.vue | Table.vue | Calendar.vue | Gallery.vue}
        │   └── (sub-componentes específicos da view)
        │
        └── CardDialog.vue (Teleport)
            └── CardDetail.vue
                ├── CardDetailProperties.vue
                ├── CardDetailContents.vue
                │   └── ContentElement.vue (registry por BlockType)
                └── CommentsList.vue
```

## Fluxo de Dados

```
Ação do Usuário
    │
    ▼
Componente → Mutator (composable)
    │
    ▼
Mutator → API Service (axios/fetch) + dispatch(Pinia action)
    │
    ▼
Pinia Store (storeToRefs → componente re-renderiza)
    │
    ▼
WebSocket → dispatch(Pinia action) → re-renderiza (tempo real)
```

## Componentes Principais

| Componente | Função |
|-----------|--------|
| `Workspace.vue` | Layout raiz com sidebar + center panel |
| `Sidebar.vue` | Navegação lateral com categorias e drag-and-drop |
| `CenterPanel.vue` | Orquestra ViewHeader + view ativa (Kanban/Table/Calendar/Gallery) |
| `Kanban.vue` | Quadro kanban com colunas por propriedade de agrupamento |
| `Table.vue` | Visualização em tabela com colunas, agrupamento e redimensionamento |
| `Calendar.vue` | Visualização em calendário com @fullcalendar/vue3 |
| `Gallery.vue` | Visualização em galeria de cards |
| `CardDialog.vue` | Modal de detalhe do card (Teleport) |
| `CardDetail.vue` | Edição de propriedades e conteúdos |
| `BoardPermissionGate.vue` | Controle de acesso por permissão |
| `ContentRegistry.vue` | Registry de componentes por BlockType |

## Pinia Stores

| Store | Estado |
|-------|--------|
| `useBoardStore` | Boards, membros, templates |
| `useCardStore` | Cards, selectores complexos |
| `useViewStore` | Views (Board/Table/Gallery/Calendar) |
| `useUserStore` | Usuário logado, membros do board |
| `useTeamStore` | Times |
| `useCommentStore` | Comentários por card |
| `useContentStore` | Conteúdos de blocos por card |
| `useAttachmentStore` | Anexos com progresso de upload |
| `useSidebarStore` | Categorias sidebar, boards ocultos |
| `useSearchStore` | Texto de busca |
| `useConfigStore` | Configuração do cliente |
| `useErrorStore` | Erro global |
| `useTemplateStore` | Templates globais |
| `useLanguageStore` | Idioma |
