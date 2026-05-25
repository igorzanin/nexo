# Frontend Inventory — Focalboard Legacy

> Gerado por `/reversa-coding` (T001, T004, T005, T006, T007)
> Data: `2026-05-14`
> Fonte: `focalboard-legacy/webapp/src/`
> Stack alvo: Vue 3 + Composition API + Pinia + Bootstrap 5.3 + TypeScript
> 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Sumário

| Módulo | Legacy | Novo | Status |
|--------|--------|------|--------|
| Páginas | 6 | 5 + Welcome (pendente) | 🟡 Parcial |
| Componentes | 92 entries | ~10 pastas | 🔴 Incompleto |
| Property Editors | 19 tipos | 0 | 🔴 Ausente |
| Widgets | 30 entries | 0 | 🔴 Ausente |
| Stores | 19 slices | 14 Pinia | 🟡 Parcial |
| Blocks/Models | 24 arquivos | 15 tipos | 🟡 Parcial |
| Hooks | 4 | 5 composables | 🟡 Parcial |
| Utilitários | 12+ | parcial | 🟡 Parcial |

---

## 1. Páginas (T001)

### Legacy (React)

| Página | Caminho legado | Status novo | Observação |
|--------|---------------|-------------|------------|
| Login | `pages/loginPage.tsx` | ✅ `pages/LoginPage.vue` | Verificar paridade de estados (erro, loading) |
| Register | `pages/registerPage.tsx` | ✅ `pages/RegisterPage.vue` | Verificar paridade |
| Change Password | `pages/changePasswordPage.tsx` | ✅ `pages/ChangePasswordPage.vue` | Verificar paridade |
| Error | `pages/errorPage.tsx` | ✅ `pages/ErrorPage.vue` | Verificar parâmetros de erro |
| Board | `pages/boardPage/boardPage.tsx` | ✅ `pages/board/` | Verificar sub-rotas e eventos WebSocket |
| Welcome | `pages/welcome/` | ❌ Ausente | Nova — onboarding tour inicial |

### Sub-módulos de BoardPage

| Utilitário legado | Composável novo | Status |
|-------------------|-----------------|--------|
| `boardPage/teamToBoardAndViewRedirect.tsx` | `router/index.ts` (guard) | 🟡 Verificar |
| `boardPage/setWindowTitleAndIcon.tsx` | - | 🔴 Ausente |
| `boardPage/undoRedoHotKeys.tsx` | - | 🔴 Ausente |
| `boardPage/websocketConnection.tsx` | `composables/useWebSocket.ts` | 🟡 Verificar |

---

## 2. Componentes (T001)

### 2.1 Layout

| Componente legado | Caminho | Status novo | Observação |
|-------------------|---------|-------------|------------|
| `workspace.tsx` | `components/workspace/` | ✅ `Workspace.vue` | Verificar |
| `centerPanel.tsx` | `components/centerPanel/` | ✅ `CenterPanel.vue` | Verificar |
| `topBar.tsx` | `components/topBar.tsx` | ❌ Ausente | 🔴 Não encontrado no novo |
| `sidebar.tsx` | `components/sidebar/` | ✅ `Sidebar.vue` | Apenas 1 arquivo vs 21 legados |

### 2.2 Sidebar (sub-componentes)

| Componente legado | Status novo |
|-------------------|-------------|
| `sidebarCategory.tsx` | ❌ Ausente |
| `sidebarBoardItem.tsx` | ❌ Ausente |
| `sidebarSettingsMenu.tsx` | ❌ Ausente |
| `sidebarUserMenu.tsx` | ❌ Ausente |
| `deleteBoardDialog.tsx` | ❌ Ausente |
| `registrationLink.tsx` | ❌ Ausente |

### 2.3 Visualizações de Board

| View | Legacy | Novo | Status |
|------|--------|------|--------|
| Kanban | `kanban/` (6 arquivos) | parcial | 🔴 Faltam sub-componentes (column, card, hiddenColumnItem) |
| Table | `table/` (15 arquivos) | parcial | 🔴 Faltam sub-componentes (row, header, headerMenu, group) |
| Calendar | `calendar/` (3 arquivos) | parcial | 🔴 Verificar integração FullCalendar |
| Gallery | `gallery/` (5 arquivos) | parcial | 🔴 Faltam card, estilos |

#### Kanban — sub-componentes legados

| Arquivo | Status novo |
|---------|-------------|
| `kanban.tsx` | `Kanban.vue` (parcial) |
| `kanbanColumn.tsx` | ❌ Ausente |
| `kanbanCard.tsx` | ❌ Ausente |
| `kanbanColumnHeader.tsx` | ❌ Ausente |
| `kanbanHiddenColumnItem.tsx` | ❌ Ausente |
| `calculation/` | ❌ Ausente |

#### Table — sub-componentes legados

| Arquivo | Status novo |
|---------|-------------|
| `table.tsx` | `Table.vue` (parcial) |
| `tableRow.tsx` | ❌ Ausente |
| `tableHeader.tsx` | ❌ Ausente |
| `tableHeaderMenu.tsx` | ❌ Ausente |
| `tableHeaders.tsx` | ❌ Ausente |
| `tableRows.tsx` | ❌ Ausente |
| `tableGroup.tsx` | ❌ Ausente |
| `tableGroupHeaderRow.tsx` | ❌ Ausente |
| `horizontalGrip.tsx` | ❌ Ausente |
| `tableColumnResizeContext.tsx` | ❌ Ausente |
| `calculation/` | ❌ Ausente |

### 2.4 ViewHeader

| Arquivo legado | Status novo |
|----------------|-------------|
| `viewHeader.tsx` | ✅ `ViewHeader.vue` (parcial) |
| `viewHeaderActionsMenu.tsx` | ❌ Ausente |
| `viewHeaderGroupByMenu.tsx` | ❌ Ausente |
| `viewHeaderPropertiesMenu.tsx` | ❌ Ausente |
| `viewHeaderSortMenu.tsx` | ❌ Ausente |
| `viewHeaderDisplayByMenu.tsx` | ❌ Ausente |
| `viewHeaderSearch.tsx` | ❌ Ausente |
| `viewTitle.tsx` | ❌ Ausente |
| `viewMenu.tsx` | ❌ Ausente |
| `newCardButton.tsx` | ❌ Ausente |
| `newCardButtonTemplateItem.tsx` | ❌ Ausente |
| `emptyCardButton.tsx` | ❌ Ausente |
| `filterComponent.tsx` | ❌ Ausente |
| `filterEntry.tsx` | ❌ Ausente |
| `filterValue.tsx` | ❌ Ausente |
| `dateFilter.tsx` | ❌ Ausente |
| `multipersonFilterValue.tsx` | ❌ Ausente |

### 2.5 Card Detail

| Arquivo legado | Status novo |
|----------------|-------------|
| `cardDetail.tsx` | ❌ Ausente |
| `cardDetailContents.tsx` | ❌ Ausente |
| `cardDetailContentsMenu.tsx` | ❌ Ausente |
| `cardDetailContentsUtility.ts` | ❌ Ausente |
| `cardDetailProperties.tsx` | ❌ Ausente |
| `cardDetailContext.tsx` | ❌ Ausente |
| `cardDialog.tsx` | ✅ `CardDialog.vue` (parcial) |
| `comment.tsx` | ❌ Ausente |
| `commentsList.tsx` | ❌ Ausente |
| `attachment.tsx` | ❌ Ausente |
| `imagePaste.tsx` | ❌ Ausente |

### 2.6 Content Blocks

| Arquivo legado | Status novo |
|----------------|-------------|
| `contentElement.tsx` | ❌ Ausente |
| `contentRegistry.tsx` | ✅ `ContentRegistry.vue` |
| `textElement.tsx` | ❌ Ausente |
| `imageElement.tsx` | ❌ Ausente |
| `checkboxElement.tsx` | ❌ Ausente |
| `dividerElement.tsx` | ❌ Ausente |
| `attachmentElement.tsx` | ❌ Ausente |
| `archivedFile/` | ❌ Ausente |

### 2.7 Blocks Editor

| Arquivo legado | Status novo |
|----------------|-------------|
| `blocksEditor.tsx` | ❌ Ausente |
| `blockContent.tsx` | ❌ Ausente |
| `editor.tsx` | ❌ Ausente |
| `rootInput.tsx` | ❌ Ausente |
| `devmain.tsx` | ❌ (dev only) |

### 2.8 Outros Componentes

| Componente legado | Status novo |
|-------------------|-------------|
| `addContentMenuItem.tsx` | ❌ Ausente |
| `blockIconSelector.tsx` | ❌ Ausente |
| `boardIconSelector.tsx` | ❌ Ausente |
| `boardTemplateSelector/` | ❌ Ausente |
| `boardsSwitcher/boardsSwitcher.tsx` | ❌ Ausente |
| `boardsSwitcherDialog/` | ❌ Ausente |
| `cardActionsMenu/` | ❌ Ausente |
| `cardBadges.tsx` | ❌ Ausente |
| `cardLimitNotification.tsx` | ❌ Ausente |
| `confirmAddUserForNotifications.tsx` | ❌ Ausente |
| `confirmationDialogBox.tsx` | ❌ Ausente |
| `createCategory/` | ❌ Ausente |
| `dialog.tsx` | ❌ Ausente |
| `flashMessages.tsx` | ✅ `flash/` (verificar) |
| `guestNoBoards.tsx` | ❌ Ausente |
| `hiddenCardCount/` | ❌ Ausente |
| `iconSelector.tsx` | ❌ Ausente |
| `live-markdown-plugin/` | ❌ Ausente |
| `markdownEditor.tsx` | ❌ Ausente |
| `markdownEditorInput/` | ❌ Ausente |
| `messages/` | ❌ Ausente |
| `modal.tsx` | ❌ Ausente |
| `modalWrapper.tsx` | ❌ Ausente |
| `newVersionBanner.tsx` | ❌ Ausente |
| `onboardingTour/` (12 subdirs) | ❌ Ausente |
| `permissions/boardPermissionGate.tsx` | ✅ `permissions/BoardPermissionGate.vue` |
| `personSelector.tsx` | ❌ Ausente |
| `propertyValueElement.tsx` | ❌ Ausente |
| `pulsating_dot/` | ❌ Ausente |
| `rootPortal.tsx` | ❌ Ausente |
| `searchDialog/searchDialog.tsx` | ✅ `search/SearchDialog.vue` |
| `shareBoard/` (7 arquivos) | ✅ `share/` (verificar) |
| `tutorial_tour_tip/` | ❌ Ausente |
| `withWebSockets.tsx` (HOC) | ❌ (substituído por composable) |

---

## 3. Property Editors (T001)

| # | Tipo | Caminho legado | Status novo |
|---|------|----------------|-------------|
| 1 | `text` | `properties/text/` | ❌ Ausente |
| 2 | `number` | `properties/number/` | ❌ Ausente |
| 3 | `select` | `properties/select/` | ❌ Ausente |
| 4 | `multiSelect` | `properties/multiselect/` | ❌ Ausente |
| 5 | `date` | `properties/date/` | ❌ Ausente |
| 6 | `person` | `properties/person/` | ❌ Ausente |
| 7 | `multiPerson` | `properties/multiperson/` | ❌ Ausente |
| 8 | `checkbox` | `properties/checkbox/` | ❌ Ausente |
| 9 | `url` | `properties/url/` | ❌ Ausente |
| 10 | `email` | `properties/email/` | ❌ Ausente |
| 11 | `phone` | `properties/phone/` | ❌ Ausente |
| 12 | `createdBy` | `properties/createdBy/` | ❌ Ausente |
| 13 | `createdTime` | `properties/createdTime/` | ❌ Ausente |
| 14 | `updatedBy` | `properties/updatedBy/` | ❌ Ausente |
| 15 | `updatedTime` | `properties/updatedTime/` | ❌ Ausente |
| 16 | `unknown` | `properties/unknown/` | ❌ Ausente |
| 17 | `baseTextEditor` | `properties/baseTextEditor.tsx` | ❌ Ausente |
| 18 | `types.tsx` | `properties/types.tsx` | ❌ Ausente |
| 19 | `index.tsx` | `properties/index.tsx` | ❌ Ausente |

---

## 4. Widgets (T001)

| Widget | Caminho legado | Status novo |
|--------|----------------|-------------|
| `Editable` | `widgets/editable.tsx` | ❌ Ausente |
| `EditableArea` | `widgets/editableArea.tsx` | ❌ Ausente |
| `EditableDayPicker` | `widgets/editableDayPicker.tsx` | ❌ Ausente |
| `EmojiPicker` | `widgets/emojiPicker.tsx` | ❌ Ausente |
| `GuestBadge` | `widgets/guestBadge.tsx` | ❌ Ausente |
| `Label` | `widgets/label.tsx` | ❌ Ausente |
| `Menu` | `widgets/menu/` | ❌ Ausente |
| `MenuWrapper` | `widgets/menuWrapper.tsx` | ❌ Ausente |
| `NotificationBox` | `widgets/notificationBox/` | ❌ Ausente |
| `PropertyMenu` | `widgets/propertyMenu.tsx` | ❌ Ausente |
| `Switch` | `widgets/switch.tsx` | ❌ Ausente |
| `Tooltip` | `widgets/tooltip.tsx` | ❌ Ausente |
| `ValueSelector` | `widgets/valueSelector.tsx` | ❌ Ausente |
| `AdminBadge` | `widgets/adminBadge/` | ❌ Ausente |
| `Buttons` | `widgets/buttons/` | ❌ Ausente |
| `Icons` | `widgets/icons/` | ❌ Ausente (substituído por Bootstrap Icons) |

---

## 5. Stores — Matriz de Paridade (T004)

### Legacy (Redux slices) vs Novo (Pinia)

| Store legada | Arquivo legado | Store Pinia | Status |
|-------------|----------------|-------------|--------|
| `boards` | `store/boards.ts` | `useBoardStore` | ✅ |
| `cards` | `store/cards.ts` | `useCardStore` | ✅ |
| `views` | `store/views.ts` | `useViewStore` | ✅ |
| `users` | `store/users.ts` | `useUserStore` | ✅ |
| `teams` | `store/teams.ts` | `useTeamStore` | ✅ |
| `comments` | `store/comments.ts` | `useCommentStore` | ✅ |
| `contents` | `store/contents.ts` | `useContentStore` | ✅ |
| `attachments` | `store/attachments.ts` | `useAttachmentStore` | ✅ |
| `sidebar` | `store/sidebar.ts` | `useSidebarStore` | ✅ |
| `searchText` | `store/searchText.ts` | `useSearchStore` | ✅ |
| `clientConfig` | `store/clientConfig.ts` | `useConfigStore` | ✅ |
| `globalError` | `store/globalError.ts` | `useErrorStore` | ✅ |
| `globalTemplates` | `store/globalTemplates.ts` | `useTemplateStore` | ✅ |
| `language` | `store/language.ts` | `useLanguageStore` | ✅ |
| `channels` | `store/channels.ts` | ❌ | Excluído (Mattermost) |
| `limits` | `store/limits.ts` | ❌ | 🔴 Ausente |
| `initialLoad` | `store/initialLoad.ts` | 🔴 Verificar | Action de boot pode estar incompleta |
| `hooks` | `store/hooks.ts` | 🔴 Verificar | Pode conter lógica de subscription |
| `boardCloudLimits` | `store/boardCloudLimits.ts` | ❌ | Excluído (Mattermost cloud) |

### Ações necessárias

- Verificar se `initialLoad` do legado carrega dados que o novo `initialLoad` não carrega
- Verificar se `limits` store tem equivalente ou se lógica foi movida para `boardStore`

---

## 6. Blocks/Models — Matriz de Paridade (T005)

### Legacy (TypeScript) vs Novo

| Tipo/Arquivo legado | Tipo novo | Status |
|---------------------|-----------|--------|
| `blocks/block.ts` | `types/block.ts` | ✅ |
| `blocks/board.ts` | `types/board.ts` | ✅ |
| `blocks/boardView.ts` | `types/boardView.ts` | ✅ |
| `blocks/card.ts` | `types/card.ts` | ✅ |
| `blocks/team.ts` | `types/team.ts` | ✅ |
| `blocks/workspace.ts` | ✅ (inline em Board) | 🟡 |
| `blocks/sharing.ts` | `types/sharing.ts` | ✅ |
| `blocks/commentBlock.ts` | `types/commentBlock.ts` | ✅ |
| `blocks/contentBlock.ts` | `types/contentBlock.ts` | ✅ |
| `blocks/textBlock.ts` | factory em `types/contentBlock.ts` | 🟡 |
| `blocks/imageBlock.ts` | factory em `types/contentBlock.ts` | 🟡 |
| `blocks/checkboxBlock.ts` | factory em `types/contentBlock.ts` | 🟡 |
| `blocks/dividerBlock.ts` | factory em `types/contentBlock.ts` | 🟡 |
| `blocks/h1Block.tsx` | 🔴 Verificar | Pode ser factory ausente |
| `blocks/h2Block.tsx` | 🔴 Verificar | Pode ser factory ausente |
| `blocks/h3Block.tsx` | 🔴 Verificar | Pode ser factory ausente |
| `blocks/attachmentBlock.tsx` | `types/attachmentBlock.ts` | ✅ |
| `blocks/filterClause.ts` | `types/filterClause.ts` | ✅ |
| `blocks/filterGroup.ts` | `types/filterGroup.ts` | ✅ |
| `blocks/block.test.ts` | ❌ | Testes ausentes |
| `blocks/board.test.ts` | ❌ | Testes ausentes |
| `blocks/boardView.test.ts` | ❌ | Testes ausentes |
| `blocks/filterClause.test.ts` | ❌ | Testes ausentes |

### Observação

O legado tem `h1Block.tsx`, `h2Block.tsx`, `h3Block.tsx` como componentes React (JSX). No novo sistema, H1, H2, H3 são blocos de conteúdo renderizados pelo `ContentRegistry.vue`. Verificar se as factories `createH1Block`, `createH2Block`, `createH3Block` existem nos tipos do novo sistema.

---

## 7. Hooks/Composables — Matriz de Paridade (T006)

| Hook legado | Composável novo | Status |
|-------------|-----------------|--------|
| `hooks/permissions.tsx` | `composables/useHasPermissions.ts` | ✅ |
| `hooks/sortable.tsx` | ❌ Ausente | 🔴 DnD reutilizável |
| `hooks/websockets.tsx` | `composables/useWebSocket.ts` | 🟡 Verificar paridade (subscribe/unsubscribe, reconexão) |
| `hooks/useGetAllTemplates.ts` | `useTemplateStore` (action) | 🟡 |

### Composables extras no novo

| Composável | Descrição |
|-----------|-----------|
| `useCalculations.ts` | Cálculos de colunas (count, sum, avg, etc.) |
| `useFlashMessage.ts` | Notificações toast |
| `useMutator.ts` | Central de mutações via API + undo/redo |

---

## 8. Utilitários — Matriz de Paridade (T007)

| Utilitário legado | Descrição | Status novo |
|-------------------|-----------|-------------|
| `mutator.ts` | Central de mutações | ✅ `composables/useMutator.ts` |
| `octoClient.ts` | HTTP client | ✅ `api/client.ts` |
| `octoUtils.tsx` | Utilitários de board/card | 🔴 Verificar |
| `boardUtils.ts` | Utilitários de board | 🔴 Verificar |
| `cardFilter.ts` | Filtro de cards | 🔴 Verificar |
| `csvExporter.ts` | Export CSV | 🔴 Ausente |
| `archiver.ts` | BoardArchive (import/export) | 🔴 Ausente |
| `undoManager.ts` | Undo/redo manager | 🔴 Verificar |
| `user.tsx` | User utils | 🔴 Verificar |
| `userSettings.ts` | Configurações do usuário | 🔴 Verificar |
| `utils.ts` | Misc utilitários | 🔴 Verificar |
| `blockIcons.ts` | Mapa block type → ícone | 🔴 Substituído por Bootstrap Icons |
| `fileIcons.ts` | Mapa extensão → ícone | 🔴 Substituído por Bootstrap Icons |
| `theme.ts` | Tema (Mattermost) | ❌ Excluído |
| `nativeApp.ts` | Interface com Electron nativo | ❌ Excluído |
| `errors.ts` | Error types | 🔴 Verificar |
| `constants.ts` | Constantes globais | 🔴 Verificar |
| `emojiList.ts` | Lista de emojis | 🔴 Verificar |

---

## 9. Ícones SVG

| Arquivo | Conteúdo | Plano |
|---------|----------|-------|
| `svg/card-skeleton.tsx` | Card skeleton SVG | Substituir por Bootstrap Icons + CSS |
| `svg/error-illustration.tsx` | Error page illustration | Manter ou substituir |
| `svg/search-illustration.tsx` | Search empty state | Manter ou substituir |

---

## 10. i18n

38 arquivos de idioma em `focalboard-legacy/webapp/i18n/`. O novo sistema usa `vue-i18n`. Verificar cobertura de chaves.

---

## Resumo de Lacunas

| Categoria | Total legado | Coberto | % Coberto |
|-----------|-------------|---------|-----------|
| Páginas | 6 | 5 | 83% |
| Componentes | ~92 | ~10 | 11% |
| Property Editors | 19 | 0 | 0% |
| Widgets | 30 | 0 | 0% |
| Stores | 19 | 14 | 74% |
| Blocks/Models | 24 | 15 | 63% |
| Hooks | 4 | 1-2 | 25-50% |
| Utilitários | ~18 | ~6 | 33% |
