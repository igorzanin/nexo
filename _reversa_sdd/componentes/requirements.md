# Componentes Vue 3

## Visão Geral
Conjunto de componentes Vue 3 + Composition API + Bootstrap 5.3 que implementam a interface de usuário do Nexo: layout, visualizações de quadro (Kanban, Tabela, Calendário, Galeria), detalhe de cartão, barra lateral, cabeçalhos de visualização, compartilhamento, busca, onboarding e notificações.

## Stack

| Componente | Tecnologia |
|------------|-----------|
| Framework | Vue 3 + Composition API + script setup |
| UI | Bootstrap 5.3 |
| State | Pinia |
| Router | Vue Router |
| DnD | vuedraggable |
| Calendar | @fullcalendar/vue3 |
| Modals | Bootstrap 5.3 modais + Teleport |
| i18n | vue-i18n |

## Responsabilidades (mantidas)
- Renderizar layout principal (Workspace, Sidebar, CenterPanel)
- Implementar 4 visualizações de quadro: Kanban, Tabela, Calendário e Galeria
- Gerenciar detalhe e edição de cartão (CardDialog, CardDetail)
- Renderizar blocos de conteúdo (texto, imagem, divisor, checkbox, anexo)
- Gerenciar barra lateral com categorias e boards (drag-and-drop)
- Controlar permissões de UI via BoardPermissionGate
- Gerenciar compartilhamento de boards
- Implementar busca com debounce e resultados
- Executar tour de onboarding
- Exibir notificações flash e banners

## Regras de Negócio (mantidas)
- Toda mutação de dados passa exclusivamente pelo Mutator (nunca por chamadas diretas à API) 🟢
- Componentes leem estado via `storeToRefs` das stores Pinia 🟢
- BoardPermissionGate condiciona renderização de elementos de UI 🟢
- Cartão pode ser arrastado entre colunas no Kanban e entre linhas na Tabela 🟢
- Categorias da sidebar podem ser reordenadas via drag-and-drop 🟢
- Modal de cartão (CardDialog) é renderizado via Teleport 🟢
- Conteúdo do cartão é extensível via registry de ContentHandler por BlockType 🟢
- **Consolidado**: blocksEditor + contentElement unificados ✅

## Árvore de Componentes

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
        ├── CardDialog.vue (Teleport para #app-modal)
        │   └── CardDetail.vue
        │       ├── CardDetailProperties.vue
        │       ├── CardDetailContents.vue
        │       │   └── ContentElement.vue (registry por BlockType)
        │       └── CommentsList.vue
        │
        └── CardLimitNotification.vue (não implementado)
```

## Rastreabilidade

| Componente legado | Componente Vue 3 | Confiança |
|------------------|-----------------|-----------|
| `workspace.tsx` | `Workspace.vue` | 🟢 |
| `centerPanel.tsx` | `CenterPanel.vue` | 🟢 |
| `sidebar/sidebar.tsx` | `Sidebar.vue` | 🟢 |
| `kanban/kanban.tsx` | `Kanban.vue` | 🟢 |
| `table/table.tsx` | `Table.vue` | 🟢 |
| `calendar/fullCalendar.tsx` | `Calendar.vue` | 🟢 |
| `gallery/gallery.tsx` | `Gallery.vue` | 🟢 |
| `cardDialog.tsx` | `CardDialog.vue` | 🟢 |
| `cardDetail/cardDetail.tsx` | `CardDetail.vue` | 🟢 |
| `content/contentRegistry.tsx` | `ContentRegistry.vue` | 🟢 |
| `permissions/boardPermissionGate.tsx` | `BoardPermissionGate.vue` | 🟢 |
| `flashMessages.tsx` | `FlashMessages.vue` | 🟢 |
| `withWebSockets.tsx` | `composables/useWebSocket.ts` | 🟢 |
| `searchDialog/searchDialog.tsx` | `SearchDialog.vue` | 🟢 |
| `shareBoard/shareBoard.tsx` | `ShareBoard.vue` | 🟢 |
| `onboardingTour/` | `OnboardingTour.vue` | 🟢 |
| `calculations/` | `composables/useCalculations.ts` | 🟢 |
