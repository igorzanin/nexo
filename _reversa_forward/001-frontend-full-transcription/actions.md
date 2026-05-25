# Actions: Transcrição completa do frontend legado

> Identificador: `001-frontend-full-transcription`
> Data: `2026-05-14`
> Roadmap: `_reversa_forward/001-frontend-full-transcription/roadmap.md`

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 32 |
| Paralelizáveis (`[//]`) | 14 |
| Maior cadeia de dependência | 6 (T001 → T008 → T012 → T016 → T017 → T020) |

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Re-analisar `focalboard-legacy/webapp/src/pages/` + `components/` e gerar inventário completo com classificação (transcrito/pendente/excluído/obsoleto) | - | `[//]` | `_reversa_sdd/frontend-inventory.md` | 🟢 | `[X]` |
| T002 | Re-analisar `focalboard-legacy/webapp/src/styles/` e extrair design system completo: cores, tipografia, espaçamentos, z-index, breakpoints, shadows, mapeando para tokens Bootstrap 5.3 + CSS custom properties | - | `[//]` | `_reversa_sdd/design-system/tokens.md` | 🟢 | `[X]` |
| T003 | Catalogar ícones SVG em `focalboard-legacy/webapp/src/svg/` e gerar mapeamento legado → Bootstrap Icons | T002 | `[//]` | `_reversa_sdd/design-system/icon-map.md` | 🟢 | `[X]` |
| T004 | Gerar matriz de paridade stores Redux (19) → Pinia (14) listando getters, actions e estado por store, com lacunas | - | `[//]` | `_reversa_sdd/frontend-inventory.md#stores` | 🟢 | `[X]` |
| T005 | Gerar matriz de paridade blocks/models legados → tipos TypeScript existentes, documentando factories e interfaces faltantes | - | `[//]` | `_reversa_sdd/frontend-inventory.md#blocks` | 🟢 | `[X]` |
| T006 | Gerar matriz de paridade hooks React → composables Vue, com mapeamento de cada hook para seu equivalente ou indicação de criação | - | `[//]` | `_reversa_sdd/frontend-inventory.md#hooks` | 🟢 | `[X]` |
| T007 | Re-analisar `focalboard-legacy/webapp/src/` utilitários (mutator, octoClient, cardFilter, csvExporter, archiver, etc.) e verificar cobertura no novo sistema | - | `[//]` | `_reversa_sdd/frontend-inventory.md#utilitarios` | 🟢 | `[X]` |

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T008 | Escrever specs individuais (requirements.md + design.md) para cada página legada: WelcomePage (nova), LoginPage, RegisterPage, ChangePasswordPage, ErrorPage, boardPage | T001 | - | `_reversa_sdd/paginas/` | 🟢 | `[X]` |
| T009 | Escrever specs individuais para cada property editor legado (19 tipos): text, number, select, multiSelect, date, person, checkbox, url, email, phone, createdBy, createdTime, updatedBy, updatedTime, unknown, etc. | T001 | `[//]` | `_reversa_sdd/properties/` | 🟢 | `[X]` |
| T010 | Escrever specs para widgets legados (30): menu, tooltip, modal, emojiPicker, switch, label, editable, personSelector, iconSelector, propertyMenu, etc. | T001 | `[//]` | `_reversa_sdd/widgets/` | 🟢 | `[X]` |

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T011 | Implementar página Welcome (onboarding tour) em Vue 3 + Bootstrap 5.3 | T008 | - | `webapp/src/pages/WelcomePage.vue` | 🟢 | `[X]` |
| T012 | Implementar sub-componentes de Layout faltantes: BoardsSwitcher, SidebarSettingsMenu, SidebarUserMenu, CreateCategory | T001 | - | `webapp/src/components/sidebar/` | 🟢 | `[X]` |
| T013 | Implementar ViewHeader completo com todos os menus: ViewMenu, PropertiesMenu, GroupByMenu, SortMenu, ActionsMenu, Search | T001 | - | `webapp/src/components/viewHeader/` | 🟢 | `[X]` |
| T014 | Completar Kanban View: DnD entre colunas e cards, collapse de colunas, filtro, agrupamento por propriedade | T001 | - | `webapp/src/components/kanban/` | 🟢 | `[X]` |
| T015 | Completar Table View: edição inline de propriedades, reordenação de linhas, seleção múltipla, filtros por coluna | T001 | - | `webapp/src/components/table/` | 🟢 | `[X]` |
| T016 | Completar Calendar View: integração FullCalendar, navegação mês/semana/dia, criação de cards por clique | T001 | - | `webapp/src/components/calendar/` | 🟢 | `[X]` |
| T017 | Completar Gallery View: layout responsivo de cards, ordenação, filtro | T001 | - | `webapp/src/components/gallery/` | 🟢 | `[X]` |
| T018 | Implementar CardDialog + CardDetail completos com todos os estados (abertura, edição, salvamento, undo/redo) | T001 | - | `webapp/src/components/cardDetail/` | 🟢 | `[X]` |
| T019 | Implementar CardDetailProperties: renderizar e editar todas as propriedades do card dinamicamente conforme schema do board | T009, T018 | - | `webapp/src/components/cardDetail/CardDetailProperties.vue` | 🟢 | `[X]` |
| T020 | Implementar property editors de input: TextProperty, NumberProperty, EmailProperty, UrlProperty, PhoneProperty, CheckboxProperty | T009 | `[//]` | `webapp/src/components/properties/` | 🟢 | `[X]` |
| T021 | Implementar property editors de seleção: SelectProperty, MultiSelectProperty, DateProperty, PersonProperty, MultiPersonProperty | T009 | `[//]` | `webapp/src/components/properties/` | 🟢 | `[X]` |
| T022 | Implementar property editors read-only: CreatedByProperty, CreatedTimeProperty, UpdatedByProperty, UpdatedTimeProperty | T009 | `[//]` | `webapp/src/components/properties/` | 🟢 | `[X]` |
| T023 | Implementar CommentsList + criação/edição/exclusão de comentários com WebSocket | T018 | - | `webapp/src/components/cardDetail/CommentsList.vue` | 🟢 | `[X]` |
| T024 | Implementar ContentElement registry: TextElement, ImageElement, CheckboxElement, DividerElement, H1Element, H2Element, H3Element, AttachmentElement | T018 | - | `webapp/src/components/content/` | 🟢 | `[X]` |
| T025 | Implementar widgets de overlay: Modal, Dialog, ConfirmationDialogBox, RootPortal | T010 | `[//]` | `webapp/src/components/widgets/` | 🟢 | `[X]` |
| T026 | Implementar widgets de interação: Menu, MenuWrapper, PropertyMenu, EmojiPicker, IconSelector, PersonSelector | T010 | `[//]` | `webapp/src/components/widgets/` | 🟢 | `[X]` |
| T027 | Implementar widgets de entrada: Editable, EditableArea, EditableDayPicker, Switch, Label, Tooltip | T010 | `[//]` | `webapp/src/components/widgets/` | 🟢 | `[X]` |
| T028 | Implementar BoardsSwitcher (dialog de troca rápida de board), SearchDialog (busca com debounce), ShareBoard (modal de compartilhamento público) | T001 | `[//]` | `webapp/src/components/` | 🟢 | `[X]` |
| T029 | Implementar FlashMessages (notificações toast), OnboardingTour (tour guiado), BoardPermissionGate (controle de permissões por role) | T001 | `[//]` | `webapp/src/components/` | 🟢 | `[X]` |
| T030 | Verificar e completar stores Pinia faltantes: attachments (getters de anexos por card), limits (card limits), searchText (busca global), globalTemplates | T004 | - | `webapp/src/stores/` | 🟢 | `[X]` |
| T031 | Implementar composables faltantes: usePermissions (verificação de role), useSortable (DnD reutilizável), useWebSocket completo (reconexão, subscribe/unsubscribe) | T006 | `[//]` | `webapp/src/composables/` | 🟢 | `[X]` |
| T032 | Implementar utilitários faltantes: csvExporter, archiver (boardArchive), cardFilter (filtro de cards com árvore FilterGroup/FilterClause) | T007 | `[//]` | `webapp/src/utils/` | 🟢 | `[X]` |

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T033 | Migrar usos de SVGs legados para Bootstrap Icones em toda a UI, removendo `svg/` import legado | T003 | - | `webapp/src/` | 🟢 | `[X]` |
| T034 | Integrar stores novas e composables com o Mutator existente, garantindo que toda mutação passe pela API | T030, T031 | - | `webapp/src/composables/useMutator.ts` | 🟢 | `[X]` |

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T035 | Verificar cobertura de i18n: comparar chaves legadas vs vue-i18n, adicionar chaves faltantes | T001 | `[//]` | `webapp/src/i18n/` | 🟢 | `[X]` |
| T036 | Gerar regression-watch.md documentando comportamento crítico do frontend que não pode regredir | T034 | - | `_reversa_forward/001-frontend-full-transcription/regression-watch.md` | 🟢 | `[X]` |
| T037 | Executar re-extração reversa e verificar regressão semântica | T036 | - | `.reversa/` | 🟢 | `[X]` |

## Notas de execução

- As ações T001 a T007 são de análise/documentação e podem rodar em paralelo. São pré-requisito para todo o restante
- A ordem de transcrição respeita a prioridade definida: Páginas → Layout → Visualizações → Card Detail → Properties → Widgets
- Abordagem híbrida: Bootstrap 5.3 para layout/formulários, JS custom (vuedraggable, etc.) para interações complexas
- Todas as ações de código devem seguir os padrões existentes em `webapp/src/` (Composition API, script setup, Pinia)

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-05-14 | Versão inicial gerada por `/reversa-to-do` | reversa |
