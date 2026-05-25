---
schemaVersion: 1
generatedAt: 2026-05-24T18:10:00-03:00
reversa:
  version: "1.0.0"
kind: target_screens
producedBy: screen-translator
mode: modernized
sourcePlatform: react-spa
targetPlatform: vue3-spa
adapter: web-spa__vue3-spa
screenCount: 20
hash: "sha256:screen-translator-target-screens-nexo"
---

# Target Screens

> Especificação executável das 20 telas do Nexo em modo `modernized`.
> Conteúdo textual principal preservado literalmente; layout e primitives migrados para Vue 3 + Bootstrap 5.3 + Pinia.

## Resumo

- **Modo aplicado**: modernizado
- **Telas geradas**: 20
- **Adapter**: `web-spa__vue3-spa`
- **Golden files**: 0 capturados; manifesto em `_reversa_sdd/screens/golden/manifest.yaml`
- **Deviations registradas**: 9 em `screen_deviation_log.md`

---

## Tela: LoginPage

**ID**: SCR-001
**Origem**: `webapp/src/pages/login_page.tsx:LoginPage`
**Modo aplicado**: modernizado
**Tela crítica?**: sim
**Screenshot de referência**: `_reversa_sdd/auth/screenshots/login-page.png`
**Componentes Vue alvo**: `features/identity/components/LoginPage.vue` | `shared/layouts/AuthLayout.vue`
**Pinia store**: `features/identity/stores/authStore.ts`
**Rota Vue Router**: `/login`
**Tokens consumidos**: [`layout.auth-card.width`, `shadow.base`, `radius.md`, `spacing.3`, `spacing.4`, `color.primary`, `color.danger`, `font.weight.semibold`, `color.white`]
**Pontos de interpolação**: `{{usernameOrEmail}}`, `{{errorMessage}}`
**Transições de saída**: [`HomePage (success)`, `RegisterPage (create an account)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.route: /login
spec.layout: AuthLayout
spec.root:
  component: AuthLayout
  children:
    - component: Card
      props:
        widthToken: layout.auth-card.width
        shadowToken: shadow.base
        radiusToken: radius.md
        backgroundToken: color.white
      children:
        - component: CardBody
          children:
            - component: Stack
              props:
                gapToken: spacing.3
              children:
                - component: Heading
                  level: 1
                  content: "Nexo"
                - component: Form
                  submitEvent: auth.login
                  children:
                    - component: FormLabel
                      content: "Username"
                    - component: FormControl
                      name: usernameOrEmail
                      type: text
                      placeholder: "Enter username"
                      model: "{{usernameOrEmail}}"
                    - component: FormLabel
                      content: "Password"
                    - component: FormControl
                      name: password
                      type: password
                      placeholder: "Enter password"
                    - component: Button
                      variant: primary
                      label: "Log in"
                      fullWidth: true
                    - component: Alert
                      variant: danger
                      visibleWhen: error
                      content: "{{errorMessage}}"
                - component: Button
                  variant: link
                  label: "create an account"
                  action: router.push('/register')
spec.state_messages:
  loading: "Logging in..."
  error: "{{errorMessage}}"
  success: "Redirecting..."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Formulário pronto para autenticação | Campos vazios e botão `Log in` habilitado |
| Loading | Requisição de login em andamento | Botão desabilitado e mensagem `Logging in...` |
| Error | Credencial inválida ou falha de rede | `{{errorMessage}}` |
| Success | Sessão criada com sucesso | Redireciona para a home/último board |

### Pontos de divergência aceitos

- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.
- DEV-007: branding textual usa `Nexo` em vez de `Focalboard`.

---

## Tela: RegisterPage

**ID**: SCR-002
**Origem**: `webapp/src/pages/register_page.tsx:RegisterPage`
**Modo aplicado**: modernizado
**Tela crítica?**: sim
**Screenshot de referência**: não disponível
**Componentes Vue alvo**: `features/identity/components/RegisterPage.vue` | `shared/layouts/AuthLayout.vue`
**Pinia store**: `features/identity/stores/authStore.ts`
**Rota Vue Router**: `/register`
**Tokens consumidos**: [`layout.auth-card.width`, `shadow.base`, `radius.md`, `spacing.3`, `spacing.4`, `color.primary`, `color.danger`, `color.white`]
**Pontos de interpolação**: `{{email}}`, `{{username}}`, `{{errorMessage}}`
**Transições de saída**: [`HomePage (success)`, `LoginPage (already have account)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.route: /register
spec.layout: AuthLayout
spec.root:
  component: AuthLayout
  children:
    - component: Card
      props:
        widthToken: layout.auth-card.width
        shadowToken: shadow.base
        radiusToken: radius.md
        backgroundToken: color.white
      children:
        - component: CardBody
          children:
            - component: Stack
              props:
                gapToken: spacing.3
              children:
                - component: Heading
                  level: 1
                  content: "Create an account"
                - component: Form
                  submitEvent: auth.register
                  children:
                    - component: FormLabel
                      content: "Email"
                    - component: FormControl
                      name: email
                      type: email
                      model: "{{email}}"
                    - component: FormLabel
                      content: "Username"
                    - component: FormControl
                      name: username
                      type: text
                      model: "{{username}}"
                    - component: FormLabel
                      content: "Password"
                    - component: FormControl
                      name: password
                      type: password
                    - component: FormLabel
                      content: "Confirm password"
                    - component: FormControl
                      name: confirmPassword
                      type: password
                    - component: Button
                      variant: primary
                      label: "Create account"
                      fullWidth: true
                    - component: Alert
                      variant: danger
                      visibleWhen: error
                      content: "{{errorMessage}}"
                - component: Button
                  variant: link
                  label: "Log in"
                  action: router.push('/login')
spec.state_messages:
  loading: "Creating account..."
  error: "{{errorMessage}}"
  success: "Redirecting..."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Formulário pronto para cadastro | Campos de email, username e senha visíveis |
| Loading | Criação de conta em andamento | Botão `Create account` desabilitado |
| Error | Falha de validação ou API | `{{errorMessage}}` |
| Success | Conta criada com sucesso | Redireciona para `HomePage` |

### Pontos de divergência aceitos

- DEV-001: tela inferida sem screenshot de referência.
- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.
- DEV-007: branding textual usa `Nexo` em vez de `Focalboard`.

---

## Tela: HomePage

**ID**: SCR-003
**Origem**: `webapp/src/pages/board_page.tsx:HomePage / BoardList`
**Modo aplicado**: modernizado
**Tela crítica?**: sim
**Screenshot de referência**: não disponível
**Componentes Vue alvo**: `features/boards/components/HomePage.vue` | `shared/layouts/AppLayout.vue` | `shared/components/Sidebar.vue`
**Pinia store**: `features/boards/stores/boardStore.ts`
**Rota Vue Router**: `/boards`
**Tokens consumidos**: [`layout.sidebar.width`, `spacing.3`, `spacing.4`, `color.primary`, `color.gray.100`, `color.gray.200`, `color.text.muted`, `shadow.sm`]
**Pontos de interpolação**: `{{teamName}}`, `{{boards[]}}`, `{{selectedBoardId}}`
**Transições de saída**: [`BoardTableView (select board)`, `BoardKanbanView (select board)`, `CreateBoardModal (+ Add board)`, `SettingsAppMenu (footer)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.route: /boards
spec.layout: AppLayout
spec.root:
  component: AppLayout
  children:
    - component: Sidebar.vue
      props:
        widthToken: layout.sidebar.width
        brandText: "Nexo"
        teamName: "{{teamName}}"
        boards: "{{boards[]}}"
        footerSettingsLabel: "Settings"
    - component: Container
      props:
        fluid: true
      children:
        - component: Stack
          props:
            gapToken: spacing.4
          children:
            - component: Header
              children:
                - component: Heading
                  level: 1
                  content: "Boards"
                - component: Button
                  variant: primary
                  label: "+ Add board"
                  action: open.createBoardModal
            - component: Row
              repeat: "{{boards[]}}"
              children:
                - component: Col
                  props:
                    md: 6
                    xl: 4
                  children:
                    - component: Card
                      props:
                        shadowToken: shadow.sm
                      children:
                        - component: CardBody
                          children:
                            - component: Heading
                              level: 2
                              content: "{{boards[].title}}"
                            - component: Text
                              toneToken: color.text.muted
                              content: "{{boards[].description}}"
                            - component: Button
                              variant: link
                              label: "Open"
                              action: open.board
spec.state_messages:
  loading: "Loading boards..."
  error: "{{errorMessage}}"
  success: "Boards loaded."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Estrutura inicial renderizada | Sidebar + cabeçalho `Boards` |
| Loading | Lista de boards sendo carregada | `Loading boards...` |
| Error | Falha ao listar boards | `{{errorMessage}}` |
| Success | Lista pronta para navegação | Cards/lista de boards interativos |

### Pontos de divergência aceitos

- DEV-002: tela inferida sem screenshot de referência.
- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.
- DEV-007: branding textual usa `Nexo` em vez de `Focalboard`.

---

## Tela: BoardTableView

**ID**: SCR-004
**Origem**: `webapp/src/components/table/table.tsx:TableComponent`
**Modo aplicado**: modernizado
**Tela crítica?**: sim
**Screenshot de referência**: `_reversa_sdd/paginas/screenshots/board-table-por-sprint.png`
**Componentes Vue alvo**: `features/views/table/components/BoardTableView.vue` | `shared/components/Sidebar.vue` | `shared/components/BoardPermissionGate.vue` | `shared/components/PropertyValueElement.vue`
**Pinia store**: `features/views/stores/viewStore.ts`
**Rota Vue Router**: `/boards/:boardId/table`
**Tokens consumidos**: [`layout.sidebar.width`, `spacing.2`, `spacing.3`, `color.primary`, `color.gray.200`, `color.gray.300`, `font.size.sm`, `font.weight.semibold`, `color.text.muted`]
**Pontos de interpolação**: `{{boardTitle}}`, `{{viewName}}`, `{{groupByProp}}`, `{{properties[]}}`, `{{groups[]}}`, `{{cards[]}}`
**Transições de saída**: [`CardDetailModal (click card)`, `NewCardTemplateSelector (New ▾)`, `GroupByDropdown`, `PropertiesPanel`, `FilterPanel`, `SortPanel`, `ShareBoardModal`, `ExportDropdown`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.route: /boards/:boardId/table
spec.layout: AppLayout
spec.root:
  component: AppLayout
  children:
    - component: Sidebar.vue
      props:
        widthToken: layout.sidebar.width
        activeBoard: "{{boardTitle}}"
    - component: BoardPermissionGate.vue
      children:
        - component: Container
          props:
            fluid: true
          children:
            - component: Stack
              props:
                gapToken: spacing.3
              children:
                - component: Header
                  children:
                    - component: Dropdown
                      label: "{{viewName}}"
                    - component: Button
                      label: "Properties"
                    - component: Dropdown
                      label: "Group by: {{groupByProp}}"
                    - component: Button
                      label: "Filter"
                    - component: Button
                      label: "Sort"
                    - component: FormControl
                      type: search
                      placeholder: "Search cards"
                    - component: Dropdown
                      label: "..."
                    - component: Dropdown
                      label: "New ▾"
                    - component: Button
                      variant: primary
                      label: "Share"
                - component: Card
                  children:
                    - component: Table
                      props:
                        responsive: true
                        hover: true
                      children:
                        - component: TableHead
                          columns: ["Name", "Status", "Sprint", "Prioridade"]
                        - component: TableBody
                          groupBy: "{{groupByProp}}"
                          groups: "{{groups[]}}"
                          rowComponent: PropertyValueElement.vue
                - component: Text
                  toneToken: color.text.muted
                  content: "COUNT {{cards.length}}"
spec.state_messages:
  loading: "Loading board..."
  error: "{{errorMessage}}"
  success: "Board loaded."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Shell do board pronto | Sidebar + toolbar + tabela vazia |
| Loading | Dados do board em trânsito | `Loading board...` |
| Error | Falha ao carregar board/view | `{{errorMessage}}` |
| Success | Tabela preenchida e agrupada | Grupos expansíveis por `{{groupByProp}}` |

### Pontos de divergência aceitos

- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.
- DEV-008: link externo `Give feedback` removido.

---

## Tela: BoardKanbanView

**ID**: SCR-005
**Origem**: `webapp/src/components/kanban/kanban.tsx:KanbanComponent`
**Modo aplicado**: modernizado
**Tela crítica?**: sim
**Screenshot de referência**: `_reversa_sdd/paginas/screenshots/board-kanban-por-status.png`
**Componentes Vue alvo**: `features/views/kanban/components/BoardKanbanView.vue` | `shared/components/Sidebar.vue` | `shared/components/BoardPermissionGate.vue` | `shared/components/PropertyValueElement.vue`
**Pinia store**: `features/views/stores/viewStore.ts`
**Rota Vue Router**: `/boards/:boardId/kanban`
**Tokens consumidos**: [`layout.sidebar.width`, `spacing.2`, `spacing.3`, `color.primary`, `color.gray.100`, `color.gray.200`, `shadow.sm`, `radius.base`, `color.text.muted`]
**Pontos de interpolação**: `{{boardTitle}}`, `{{viewName}}`, `{{groupByProp}}`, `{{columns[]}}`, `{{cards[]}}`
**Transições de saída**: [`CardDetailModal (click card)`, `NewCardTemplateSelector (New ▾)`, `GroupByDropdown`, `PropertiesPanel`, `FilterPanel`, `SortPanel`, `ShareBoardModal`, `ExportDropdown`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.route: /boards/:boardId/kanban
spec.layout: AppLayout
spec.root:
  component: AppLayout
  children:
    - component: Sidebar.vue
      props:
        widthToken: layout.sidebar.width
        activeBoard: "{{boardTitle}}"
    - component: BoardPermissionGate.vue
      children:
        - component: Container
          props:
            fluid: true
          children:
            - component: Stack
              props:
                gapToken: spacing.3
              children:
                - component: Header
                  children:
                    - component: Dropdown
                      label: "{{viewName}}"
                    - component: Button
                      label: "Properties"
                    - component: Dropdown
                      label: "Group by: {{groupByProp}}"
                    - component: Button
                      label: "Filter"
                    - component: Button
                      label: "Sort"
                    - component: FormControl
                      type: search
                      placeholder: "Search cards"
                    - component: Dropdown
                      label: "..."
                    - component: Dropdown
                      label: "New ▾"
                    - component: Button
                      variant: primary
                      label: "Share"
                - component: Row
                  repeat: "{{columns[]}}"
                  children:
                    - component: Col
                      children:
                        - component: Card
                          children:
                            - component: CardHeader
                              children:
                                - component: Text
                                  content: "{{columns[].title}}"
                                - component: Button
                                  variant: link
                                  label: "+"
                            - component: CardBody
                              repeat: "{{columns[].cards}}"
                              children:
                                - component: Card
                                  props:
                                    shadowToken: shadow.sm
                                    radiusToken: radius.base
                                  children:
                                    - component: PropertyValueElement.vue
                - component: Text
                  toneToken: color.text.muted
                  content: "COUNT {{cards.length}}"
spec.state_messages:
  loading: "Loading board..."
  error: "{{errorMessage}}"
  success: "Board loaded."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Estrutura kanban renderizada | Colunas vazias com toolbar pronta |
| Loading | Cards/colunas sendo carregados | `Loading board...` |
| Error | Falha ao carregar view | `{{errorMessage}}` |
| Success | Colunas por status preenchidas | Cards distribuídos por propriedade |

### Pontos de divergência aceitos

- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.
- DEV-008: link externo `Give feedback` removido.

---

## Tela: CardDetailModal

**ID**: SCR-006
**Origem**: `webapp/src/components/cardDetail/cardDetail.tsx:CardDetailModal`
**Modo aplicado**: modernizado
**Tela crítica?**: sim
**Screenshot de referência**: `_reversa_sdd/componentes/screenshots/card-detail-modal.png`
**Componentes Vue alvo**: `features/content/components/CardDetailModal.vue` | `shared/components/ContentRegistry.vue` | `shared/components/PropertyValueElement.vue`
**Pinia store**: `features/content/stores/cardStore.ts`
**Rota Vue Router**: N/A
**Tokens consumidos**: [`zindex.modal`, `zindex.modal-backdrop`, `spacing.3`, `spacing.4`, `color.primary`, `color.gray.200`, `color.gray.300`, `radius.base`, `shadow.base`, `color.white`]
**Pontos de interpolação**: `{{card.title}}`, `{{card.contents[]}}`, `{{card.properties}}`, `{{card.comments[]}}`, `{{card.assignees[]}}`, `{{errorMessage}}`
**Transições de saída**: [`Board (close)`, `PropertiesPanel (property click)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.layout: none
spec.root:
  component: Modal
  props:
    size: xl
    zIndexToken: zindex.modal
    backdropToken: zindex.modal-backdrop
  children:
    - component: ModalHeader
      children:
        - component: Button
          variant: link
          label: "×"
          action: modal.close
    - component: ModalBody
      children:
        - component: Row
          children:
            - component: Col
              props:
                lg: 8
              children:
                - component: FormControl
                  name: title
                  type: text
                  model: "{{card.title}}"
                - component: ContentRegistry.vue
                  props:
                    content: "{{card.contents[]}}"
                    mode: markdown
                - component: ListGroup
                  heading: "Comments"
                  repeat: "{{card.comments[]}}"
                - component: InputGroup
                  children:
                    - component: FormControl
                      name: comment
                      placeholder: "Add a comment"
                    - component: Button
                      variant: primary
                      label: "Add comment"
            - component: Col
              props:
                lg: 4
              children:
                - component: Card
                  children:
                    - component: CardHeader
                      content: "Properties"
                    - component: CardBody
                      children:
                        - component: PropertyValueElement.vue
                          label: "Status"
                        - component: PropertyValueElement.vue
                          label: "Sprint"
                        - component: PropertyValueElement.vue
                          label: "Prioridade"
                        - component: PropertyValueElement.vue
                          label: "Assignee"
spec.state_messages:
  loading: "Loading card..."
  error: "{{errorMessage}}"
  success: "Card updated."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Modal aberto com placeholders | Título, editor e painel de propriedades |
| Loading | Card/conteúdo sendo carregado | `Loading card...` |
| Error | Falha ao salvar ou carregar | `{{errorMessage}}` |
| Success | Alteração persistida | Modal permanece aberto com dados atualizados |

### Pontos de divergência aceitos

- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.

---

## Tela: NewCardTemplateSelector

**ID**: SCR-007
**Origem**: `webapp/src/components/newCardButton.tsx:NewCardTemplateDropdown`
**Modo aplicado**: modernizado
**Tela crítica?**: não
**Screenshot de referência**: `_reversa_sdd/componentes/screenshots/new-card-template-selector.png`
**Componentes Vue alvo**: `features/content/components/NewCardTemplateSelector.vue`
**Pinia store**: `features/boards/stores/templateStore.ts`
**Rota Vue Router**: N/A
**Tokens consumidos**: [`color.white`, `color.gray.200`, `shadow.base`, `zindex.dropdown`, `spacing.2`, `radius.base`, `color.primary`]
**Pontos de interpolação**: `{{templates[]}}`, `{{selectedTemplateId}}`
**Transições de saída**: [`CardDetailModal (select template)`, `Board (cancel)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.layout: none
spec.root:
  component: Dropdown
  props:
    zIndexToken: zindex.dropdown
  children:
    - component: DropdownMenu
      children:
        - component: DropdownHeader
          content: "Select a template"
        - component: DropdownItem
          label: "Empty Card"
          icon: square
          action: template.selectEmpty
        - component: DropdownItem
          repeat: "{{templates[]}}"
          label: "{{templates[].name}}"
          icon: "{{templates[].icon}}"
          action: template.select
spec.state_messages:
  loading: "Loading templates..."
  error: "{{errorMessage}}"
  success: "Template selected."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Dropdown pronto para seleção | `Empty Card` no topo e lista de templates |
| Loading | Templates em carregamento | `Loading templates...` |
| Error | Falha ao listar templates | `{{errorMessage}}` |
| Success | Template escolhido | Abre `CardDetailModal` com template aplicado |

### Pontos de divergência aceitos

- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.

---

## Tela: GroupByDropdown

**ID**: SCR-008
**Origem**: `webapp/src/components/viewHeader/viewHeaderGroupByMenu.tsx:GroupByMenu`
**Modo aplicado**: modernizado
**Tela crítica?**: não
**Screenshot de referência**: `_reversa_sdd/componentes/screenshots/group-by-dropdown.png`
**Componentes Vue alvo**: `features/views/components/GroupByDropdown.vue`
**Pinia store**: `features/views/stores/viewStore.ts`
**Rota Vue Router**: N/A
**Tokens consumidos**: [`color.white`, `color.primary.active.bg`, `color.gray.200`, `shadow.base`, `zindex.dropdown`, `spacing.2`, `color.primary`]
**Pontos de interpolação**: `{{properties[]}}`, `{{selectedProperty}}`
**Transições de saída**: [`BoardTableView (apply grouping)`, `BoardKanbanView (apply grouping)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.layout: none
spec.root:
  component: Dropdown
  props:
    zIndexToken: zindex.dropdown
  children:
    - component: DropdownMenu
      children:
        - component: DropdownItem
          label: "No grouping"
          activeWhen: "{{selectedProperty}} == null"
        - component: DropdownItem
          repeat: "{{properties[]}}"
          label: "{{properties[].name}}"
          checkmarkWhen: "{{properties[].name}} == {{selectedProperty}}"
          activeBackgroundToken: color.primary.active.bg
spec.state_messages:
  loading: "Loading properties..."
  error: "{{errorMessage}}"
  success: "Grouping updated."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Dropdown aberto | Lista de propriedades + `No grouping` |
| Loading | Propriedades sendo carregadas | `Loading properties...` |
| Error | Falha ao obter opções | `{{errorMessage}}` |
| Success | Agrupamento aplicado | Item ativo marcado com check |

### Pontos de divergência aceitos

- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.

---

## Tela: ShareBoardModal

**ID**: SCR-009
**Origem**: `webapp/src/components/shareboard/shareBoard.tsx:ShareBoardModal`
**Modo aplicado**: modernizado
**Tela crítica?**: sim
**Screenshot de referência**: `_reversa_sdd/componentes/screenshots/share-board-modal.png`
**Componentes Vue alvo**: `features/collaboration/components/ShareBoardModal.vue`
**Pinia store**: `features/collaboration/stores/sharingStore.ts`
**Rota Vue Router**: N/A
**Tokens consumidos**: [`zindex.modal`, `spacing.3`, `spacing.4`, `radius.base`, `color.primary`, `color.gray.200`, `color.gray.300`, `color.white`]
**Pontos de interpolação**: `{{board.title}}`, `{{searchQuery}}`, `{{searchResults[]}}`, `{{shareUrl}}`, `{{isPublicSharing}}`, `{{members[]}}`
**Transições de saída**: [`Board (close modal)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.layout: none
spec.root:
  component: Modal
  props:
    size: lg
    zIndexToken: zindex.modal
  children:
    - component: ModalHeader
      title: "Share Board"
    - component: ModalBody
      children:
        - component: Stack
          props:
            gapToken: spacing.3
          children:
            - component: FormControl
              type: search
              placeholder: "Search for people"
              model: "{{searchQuery}}"
            - component: FormCheck
              type: switch
              label: "Allow sharing"
              model: "{{isPublicSharing}}"
            - component: InputGroup
              children:
                - component: FormControl
                  type: text
                  readonly: true
                  model: "{{shareUrl}}"
                - component: Button
                  variant: primary
                  label: "Copy link"
            - component: Table
              columns: ["Member", "Role"]
              rows: "{{members[]}}"
spec.state_messages:
  loading: "Loading sharing settings..."
  error: "{{errorMessage}}"
  success: "Sharing settings updated."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Modal aberto para compartilhamento | Busca, toggle e lista de membros |
| Loading | Dados/permissões sendo carregados | `Loading sharing settings...` |
| Error | Falha ao compartilhar ou copiar link | `{{errorMessage}}` |
| Success | Ajuste de compartilhamento aplicado | Mantém modal com dados atualizados |

### Pontos de divergência aceitos

- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.

---

## Tela: ExportDropdown

**ID**: SCR-010
**Origem**: `webapp/src/components/viewHeader/viewHeaderActionsMenu.tsx:ExportMenu`
**Modo aplicado**: modernizado
**Tela crítica?**: não
**Screenshot de referência**: `_reversa_sdd/componentes/screenshots/export-dropdown.png`
**Componentes Vue alvo**: `features/boards/components/ExportDropdown.vue`
**Pinia store**: `features/boards/stores/boardStore.ts`
**Rota Vue Router**: N/A
**Tokens consumidos**: [`color.white`, `color.gray.200`, `shadow.base`, `zindex.dropdown`, `spacing.2`]
**Pontos de interpolação**: nenhum
**Transições de saída**: [`BoardTableView (trigger export)`, `BoardKanbanView (trigger export)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.layout: none
spec.root:
  component: Dropdown
  props:
    zIndexToken: zindex.dropdown
  children:
    - component: DropdownMenu
      children:
        - component: DropdownItem
          label: "Export to CSV"
          action: board.exportCsv
        - component: DropdownItem
          label: "Export Archive (.boardarchive)"
          action: board.exportArchive
spec.state_messages:
  loading: "Preparing export..."
  error: "{{errorMessage}}"
  success: "Export started."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Menu de exportação aberto | Dois itens de exportação |
| Loading | Arquivo sendo preparado | `Preparing export...` |
| Error | Falha ao gerar export | `{{errorMessage}}` |
| Success | Download iniciado | `Export started.` |

### Pontos de divergência aceitos

- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.

---

## Tela: SettingsAppMenu

**ID**: SCR-011
**Origem**: `webapp/src/components/sidebar/sidebarSettingsMenu.tsx:SettingsMenu`
**Modo aplicado**: modernizado
**Tela crítica?**: não
**Screenshot de referência**: `_reversa_sdd/componentes/screenshots/settings-app-menu.png`
**Componentes Vue alvo**: `features/boards/components/SettingsAppMenu.vue`
**Pinia store**: `features/boards/stores/appPreferencesStore.ts`
**Rota Vue Router**: N/A
**Tokens consumidos**: [`color.white`, `color.gray.200`, `shadow.base`, `zindex.dropdown`, `spacing.2`, `color.text.muted`]
**Pontos de interpolação**: `{{appVersion}}`
**Transições de saída**: [`SettingsPage`, `SetThemeSubmenu`, `SetLanguageSubmenu`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.layout: none
spec.root:
  component: Dropdown
  props:
    zIndexToken: zindex.dropdown
  children:
    - component: DropdownMenu
      children:
        - component: DropdownItem
          label: "Settings"
          action: router.push('/settings')
        - component: DropdownItem
          label: "Set theme ▶"
          action: open.themeSubmenu
        - component: DropdownItem
          label: "Set language ▶"
          action: open.languageSubmenu
        - component: Divider
        - component: Text
          toneToken: color.text.muted
          content: "{{appVersion}}"
spec.state_messages:
  loading: "Loading menu..."
  error: "{{errorMessage}}"
  success: "Menu ready."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Menu aberto no rodapé da sidebar | Itens e versão visíveis |
| Loading | Preferências em carregamento | `Loading menu...` |
| Error | Falha ao carregar preferências | `{{errorMessage}}` |
| Success | Menu pronto para navegação | Submenus acionáveis |

### Pontos de divergência aceitos

- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.
- DEV-007: branding textual usa `Nexo` em vez de `Focalboard`.

---

## Tela: CreateBoardModal

**ID**: SCR-012
**Origem**: `webapp/src/components/newBoardButton.tsx:CreateBoardModal`
**Modo aplicado**: modernizado
**Tela crítica?**: sim
**Screenshot de referência**: `_reversa_sdd/componentes/screenshots/create-board-modal.png`
**Componentes Vue alvo**: `features/boards/components/CreateBoardModal.vue`
**Pinia store**: `features/boards/stores/boardStore.ts`
**Rota Vue Router**: N/A
**Tokens consumidos**: [`zindex.modal`, `spacing.3`, `spacing.4`, `radius.base`, `color.primary`, `color.gray.200`, `shadow.base`, `color.white`]
**Pontos de interpolação**: `{{boardName}}`, `{{templates[]}}`, `{{selectedTemplate}}`, `{{preview}}`
**Transições de saída**: [`BoardTableView (on create)`, `HomePage (cancel)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.layout: none
spec.root:
  component: Modal
  props:
    size: xl
    zIndexToken: zindex.modal
  children:
    - component: ModalHeader
      title: "Create a board"
    - component: ModalBody
      children:
        - component: Stack
          props:
            gapToken: spacing.3
          children:
            - component: FormLabel
              content: "Board name"
            - component: FormControl
              name: boardName
              type: text
              model: "{{boardName}}"
            - component: Row
              children:
                - component: Col
                  props:
                    lg: 5
                  children:
                    - component: ListGroup
                      repeat: "{{templates[]}}"
                      activeItem: "{{selectedTemplate}}"
                - component: Col
                  props:
                    lg: 7
                  children:
                    - component: Card
                      children:
                        - component: CardHeader
                          content: "Preview"
                        - component: CardBody
                          content: "{{preview}}"
    - component: ModalFooter
      children:
        - component: Button
          variant: outline-secondary
          label: "Create empty board"
        - component: Button
          variant: primary
          label: "Use this template"
spec.state_messages:
  loading: "Creating board..."
  error: "{{errorMessage}}"
  success: "Board created."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Modal pronto para seleção | Campo de nome, templates e preview |
| Loading | Board em criação | `Creating board...` |
| Error | Falha ao criar board | `{{errorMessage}}` |
| Success | Board criado | Fecha modal e navega para o board |

### Pontos de divergência aceitos

- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.

---

## Tela: PropertiesPanel

**ID**: SCR-013
**Origem**: `webapp/src/components/viewHeader/viewHeaderPropertiesMenu.tsx:PropertiesMenu`
**Modo aplicado**: modernizado
**Tela crítica?**: não
**Screenshot de referência**: `_reversa_sdd/componentes/screenshots/properties-panel.png`
**Componentes Vue alvo**: `features/views/components/PropertiesPanel.vue`
**Pinia store**: `features/views/stores/viewStore.ts`
**Rota Vue Router**: N/A
**Tokens consumidos**: [`color.white`, `color.primary`, `color.gray.200`, `zindex.dropdown`, `spacing.2`, `spacing.3`, `radius.base`]
**Pontos de interpolação**: `{{properties[]}}`, `{{visibleProperties[]}}`, `{{hiddenProperties[]}}`
**Transições de saída**: [`BoardTableView (toggle property visibility)`, `BoardKanbanView (toggle property visibility)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.layout: none
spec.root:
  component: Offcanvas
  props:
    placement: end
  children:
    - component: OffcanvasHeader
      title: "Properties"
    - component: OffcanvasBody
      children:
        - component: ListGroup
          repeat: "{{properties[]}}"
          children:
            - component: ListGroupItem
              children:
                - component: Text
                  content: "{{properties[].name}}"
                - component: FormCheck
                  type: switch
                  checkedWhen: "{{properties[].visible}}"
spec.state_messages:
  loading: "Loading properties..."
  error: "{{errorMessage}}"
  success: "Properties updated."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Painel lateral aberto | Lista de propriedades com toggles |
| Loading | Configuração em carregamento | `Loading properties...` |
| Error | Falha ao salvar visibilidade | `{{errorMessage}}` |
| Success | Alteração aplicada | View ativa reflete colunas visíveis |

### Pontos de divergência aceitos

- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.

---

## Tela: SidebarCategoryContextMenu

**ID**: SCR-014
**Origem**: `webapp/src/components/sidebar/sidebarCategory.tsx:CategoryContextMenu`
**Modo aplicado**: modernizado
**Tela crítica?**: não
**Screenshot de referência**: `_reversa_sdd/componentes/screenshots/sidebar-category-context-menu.png`
**Componentes Vue alvo**: `features/boards/components/SidebarCategoryContextMenu.vue`
**Pinia store**: `features/boards/stores/sidebarStore.ts`
**Rota Vue Router**: N/A
**Tokens consumidos**: [`color.white`, `color.danger`, `color.gray.200`, `shadow.sm`, `zindex.dropdown`, `spacing.2`]
**Pontos de interpolação**: `{{category.name}}`, `{{moveTargets[]}}`
**Transições de saída**: [`Board (rename)`, `Board (move to)`, `Board (delete)`, `Board (cancel)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.layout: none
spec.root:
  component: Dropdown
  props:
    zIndexToken: zindex.dropdown
  children:
    - component: DropdownMenu
      children:
        - component: DropdownItem
          label: "Rename"
          action: category.rename
        - component: DropdownItem
          label: "Move to"
          action: category.moveTo
        - component: Divider
        - component: DropdownItem
          label: "Delete"
          variant: danger
          action: category.delete
spec.state_messages:
  loading: "Loading category actions..."
  error: "{{errorMessage}}"
  success: "Category updated."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Menu contextual aberto | Ações `Rename`, `Move to` e `Delete` |
| Loading | Ação contextual sendo processada | `Loading category actions...` |
| Error | Falha na ação selecionada | `{{errorMessage}}` |
| Success | Alteração aplicada | Sidebar refletida imediatamente |

### Pontos de divergência aceitos

- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.

---

## Tela: SetThemeSubmenu

**ID**: SCR-015
**Origem**: `webapp/src/components/sidebar/sidebarSettingsMenu.tsx:SetThemeSubmenu`
**Modo aplicado**: modernizado
**Tela crítica?**: não
**Screenshot de referência**: `_reversa_sdd/componentes/screenshots/set-theme-submenu.png`
**Componentes Vue alvo**: `features/boards/components/SetThemeSubmenu.vue`
**Pinia store**: `features/boards/stores/appPreferencesStore.ts`
**Rota Vue Router**: N/A
**Tokens consumidos**: [`color.white`, `color.primary.active.bg`, `color.gray.200`, `zindex.dropdown`, `spacing.2`, `color.primary`]
**Pontos de interpolação**: `{{currentTheme}}`
**Transições de saída**: [`SettingsAppMenu (back)`, `App (apply theme)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.layout: none
spec.root:
  component: Dropdown
  props:
    zIndexToken: zindex.dropdown
  children:
    - component: DropdownMenu
      children:
        - component: DropdownItem
          label: "← Back"
          action: open.settingsMenu
        - component: DropdownItem
          label: "Default"
          checkmarkWhen: "{{currentTheme}} == 'default'"
        - component: DropdownItem
          label: "Dark"
          checkmarkWhen: "{{currentTheme}} == 'dark'"
        - component: DropdownItem
          label: "Light"
          checkmarkWhen: "{{currentTheme}} == 'light'"
spec.state_messages:
  loading: "Loading themes..."
  error: "{{errorMessage}}"
  success: "Theme updated."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Submenu aberto | Opções de tema com item ativo marcado |
| Loading | Preferência sendo carregada | `Loading themes...` |
| Error | Falha ao aplicar tema | `{{errorMessage}}` |
| Success | Tema aplicado | Check migra para o item selecionado |

### Pontos de divergência aceitos

- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.

---

## Tela: SetLanguageSubmenu

**ID**: SCR-016
**Origem**: `webapp/src/components/sidebar/sidebarSettingsMenu.tsx:SetLanguageSubmenu`
**Modo aplicado**: modernizado
**Tela crítica?**: não
**Screenshot de referência**: `_reversa_sdd/componentes/screenshots/set-language-submenu.png`
**Componentes Vue alvo**: `features/boards/components/SetLanguageSubmenu.vue`
**Pinia store**: `features/boards/stores/appPreferencesStore.ts`
**Rota Vue Router**: N/A
**Tokens consumidos**: [`color.white`, `color.primary.active.bg`, `color.gray.200`, `zindex.dropdown`, `spacing.2`, `color.primary`]
**Pontos de interpolação**: `{{currentLanguage}}`, `{{languages[]}}`
**Transições de saída**: [`SettingsAppMenu (back)`, `App (apply language)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.layout: none
spec.root:
  component: Dropdown
  props:
    zIndexToken: zindex.dropdown
  children:
    - component: DropdownMenu
      children:
        - component: DropdownItem
          label: "← Back"
          action: open.settingsMenu
        - component: DropdownItem
          label: "English"
          checkmarkWhen: "{{currentLanguage}} == 'en'"
        - component: DropdownItem
          label: "Português"
          checkmarkWhen: "{{currentLanguage}} == 'pt-BR'"
        - component: DropdownItem
          label: "Español"
          checkmarkWhen: "{{currentLanguage}} == 'es'"
        - component: DropdownItem
          repeat: "{{languages[]}}"
          label: "{{languages[].label}}"
          visibleWhen: "{{languages[].label}} not in ['English', 'Português', 'Español']"
spec.state_messages:
  loading: "Loading languages..."
  error: "{{errorMessage}}"
  success: "Language updated."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Submenu aberto | Idiomas listados com item ativo marcado |
| Loading | Catálogo de idioma em carregamento | `Loading languages...` |
| Error | Falha ao trocar idioma | `{{errorMessage}}` |
| Success | Idioma aplicado | Interface é re-renderizada com novo locale |

### Pontos de divergência aceitos

- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.

---

## Tela: UserAccountDropdown

**ID**: SCR-017
**Origem**: `webapp/src/components/sidebar/userAccountMenu.tsx:UserAccountDropdown`
**Modo aplicado**: modernizado
**Tela crítica?**: não
**Screenshot de referência**: `_reversa_sdd/componentes/screenshots/user-account-dropdown.png`
**Componentes Vue alvo**: `features/identity/components/UserAccountDropdown.vue`
**Pinia store**: `features/identity/stores/authStore.ts`
**Rota Vue Router**: N/A
**Tokens consumidos**: [`layout.avatar.size`, `radius.circle`, `color.white`, `color.gray.200`, `color.danger`, `zindex.dropdown`, `spacing.2`, `font.size.sm`]
**Pontos de interpolação**: `{{user.initials}}`, `{{user.username}}`
**Transições de saída**: [`ChangePasswordPage`, `InviteUsersPage`, `LoginPage (log out)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.layout: none
spec.root:
  component: Dropdown
  props:
    zIndexToken: zindex.dropdown
  children:
    - component: DropdownMenu
      children:
        - component: DropdownHeader
          children:
            - component: Badge
              shapeToken: radius.circle
              sizeToken: layout.avatar.size
              content: "{{user.initials}}"
            - component: Text
              content: "{{user.username}}"
        - component: DropdownItem
          label: "Change password"
          action: router.push('/change-password')
        - component: DropdownItem
          label: "Invite users"
          action: open.inviteUsers
        - component: Divider
        - component: DropdownItem
          label: "Log out"
          variant: danger
          action: auth.logout
spec.state_messages:
  loading: "Loading account menu..."
  error: "{{errorMessage}}"
  success: "Logging out..."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Dropdown aberto | Avatar, username e ações de conta |
| Loading | Dados de conta sendo carregados | `Loading account menu...` |
| Error | Falha ao abrir ação de conta | `{{errorMessage}}` |
| Success | Logout ou ação concluída | `Logging out...` ou navegação para tela alvo |

### Pontos de divergência aceitos

- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.
- DEV-007: branding textual usa `Nexo` em vez de `Focalboard`.
- DEV-009: item `About Focalboard` removido.

---

## Tela: ChangePasswordPage

**ID**: SCR-018
**Origem**: `webapp/src/pages/change_password_page.tsx:ChangePasswordPage`
**Modo aplicado**: modernizado
**Tela crítica?**: não
**Screenshot de referência**: não disponível
**Componentes Vue alvo**: `features/identity/components/ChangePasswordPage.vue` | `shared/layouts/AuthLayout.vue`
**Pinia store**: `features/identity/stores/authStore.ts`
**Rota Vue Router**: `/change-password`
**Tokens consumidos**: [`layout.auth-card.width`, `shadow.base`, `radius.md`, `spacing.3`, `spacing.4`, `color.primary`, `color.danger`, `color.white`]
**Pontos de interpolação**: `{{errorMessage}}`
**Transições de saída**: [`LoginPage (success)`, `UserAccountDropdown (cancel)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.route: /change-password
spec.layout: AuthLayout
spec.root:
  component: AuthLayout
  children:
    - component: Card
      props:
        widthToken: layout.auth-card.width
        shadowToken: shadow.base
        radiusToken: radius.md
        backgroundToken: color.white
      children:
        - component: CardBody
          children:
            - component: Stack
              props:
                gapToken: spacing.3
              children:
                - component: Heading
                  level: 1
                  content: "Change password"
                - component: Form
                  submitEvent: auth.changePassword
                  children:
                    - component: FormLabel
                      content: "Current password"
                    - component: FormControl
                      name: currentPassword
                      type: password
                    - component: FormLabel
                      content: "New password"
                    - component: FormControl
                      name: newPassword
                      type: password
                    - component: FormLabel
                      content: "Confirm new password"
                    - component: FormControl
                      name: confirmPassword
                      type: password
                    - component: ButtonGroup
                      children:
                        - component: Button
                          variant: outline-secondary
                          label: "Cancel"
                        - component: Button
                          variant: primary
                          label: "Change password"
                    - component: Alert
                      variant: danger
                      visibleWhen: error
                      content: "{{errorMessage}}"
spec.state_messages:
  loading: "Changing password..."
  error: "{{errorMessage}}"
  success: "Password changed successfully."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Formulário pronto para troca de senha | Três campos de senha + ações |
| Loading | Atualização em andamento | `Changing password...` |
| Error | Senha inválida ou falha de API | `{{errorMessage}}` |
| Success | Senha alterada | `Password changed successfully.` |

### Pontos de divergência aceitos

- DEV-003: tela inferida sem screenshot de referência.
- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.

---

## Tela: FilterPanel

**ID**: SCR-019
**Origem**: `webapp/src/components/viewHeader/filterComponent.tsx:FilterPanel`
**Modo aplicado**: modernizado
**Tela crítica?**: não
**Screenshot de referência**: não disponível
**Componentes Vue alvo**: `features/views/components/FilterPanel.vue`
**Pinia store**: `features/views/stores/filterStore.ts`
**Rota Vue Router**: N/A
**Tokens consumidos**: [`color.white`, `color.primary`, `color.gray.200`, `zindex.dropdown`, `spacing.2`, `spacing.3`, `radius.base`]
**Pontos de interpolação**: `{{activeFilters[]}}`, `{{properties[]}}`, `{{operators[]}}`, `{{draftFilter}}`
**Transições de saída**: [`BoardTableView (apply filter)`, `BoardKanbanView (apply filter)`, `Board (clear filters)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.layout: none
spec.root:
  component: Offcanvas
  props:
    placement: end
  children:
    - component: OffcanvasHeader
      title: "Filter"
    - component: OffcanvasBody
      children:
        - component: ListGroup
          repeat: "{{activeFilters[]}}"
        - component: FormLabel
          content: "Property"
        - component: FormSelect
          name: property
          options: "{{properties[]}}"
        - component: FormLabel
          content: "Operator"
        - component: FormSelect
          name: operator
          options: "{{operators[]}}"
        - component: FormLabel
          content: "Value"
        - component: FormControl
          name: value
          type: text
        - component: ButtonGroup
          children:
            - component: Button
              variant: outline-secondary
              label: "Clear filters"
            - component: Button
              variant: primary
              label: "Apply"
spec.state_messages:
  loading: "Loading filters..."
  error: "{{errorMessage}}"
  success: "Filters applied."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Painel aberto para composição | Filtros ativos + editor de nova regra |
| Loading | Metadados ou aplicação em andamento | `Loading filters...` |
| Error | Filtro inválido ou falha de API | `{{errorMessage}}` |
| Success | Filtros aplicados | View do board é atualizada |

### Pontos de divergência aceitos

- DEV-004: tela inferida sem screenshot de referência.
- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.

---

## Tela: SortPanel

**ID**: SCR-020
**Origem**: `webapp/src/components/viewHeader/viewHeaderSortMenu.tsx:SortPanel`
**Modo aplicado**: modernizado
**Tela crítica?**: não
**Screenshot de referência**: não disponível
**Componentes Vue alvo**: `features/views/components/SortPanel.vue`
**Pinia store**: `features/views/stores/sortStore.ts`
**Rota Vue Router**: N/A
**Tokens consumidos**: [`color.white`, `color.primary`, `color.gray.200`, `zindex.dropdown`, `spacing.2`, `spacing.3`, `radius.base`]
**Pontos de interpolação**: `{{activeSorts[]}}`, `{{sortOptions[]}}`, `{{draftSort}}`
**Transições de saída**: [`BoardTableView (apply sort)`, `BoardKanbanView (apply sort)`]

### Especificação

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.layout: none
spec.root:
  component: Offcanvas
  props:
    placement: end
  children:
    - component: OffcanvasHeader
      title: "Sort"
    - component: OffcanvasBody
      children:
        - component: ListGroup
          repeat: "{{activeSorts[]}}"
        - component: FormLabel
          content: "Property"
        - component: FormSelect
          name: property
          options: "{{sortOptions[]}}"
        - component: FormLabel
          content: "Direction"
        - component: ButtonGroup
          children:
            - component: Button
              variant: outline-secondary
              label: "Ascending"
            - component: Button
              variant: outline-secondary
              label: "Descending"
        - component: ButtonGroup
          children:
            - component: Button
              variant: outline-secondary
              label: "Clear sort"
            - component: Button
              variant: primary
              label: "Apply"
spec.state_messages:
  loading: "Loading sort options..."
  error: "{{errorMessage}}"
  success: "Sort applied."
```

### Estados

| Estado | Descrição | Conteúdo / mensagem |
|---|---|---|
| Idle | Painel aberto para ordenação | Sorts ativos + editor de direção |
| Loading | Opções em carregamento | `Loading sort options...` |
| Error | Falha ao aplicar ordenação | `{{errorMessage}}` |
| Success | Ordenação aplicada | Board reordenado conforme seleção |

### Pontos de divergência aceitos

- DEV-005: tela inferida sem screenshot de referência.
- DEV-006: Bootstrap 5.3 substitui o Focalboard CSS.

---

## Apêndice: rastreabilidade ao inventário

| Tela do `target_screens.md` | Origem em `_reversa_sdd/ui/inventory.md` | Origem em `_reversa_sdd/screens/inventory.json` |
|---|---|---|
| `SCR-001 LoginPage` | `#15 Login Page` | `SCR-001` |
| `SCR-002 RegisterPage` | `tela pendente` | `SCR-002` |
| `SCR-003 HomePage` | `tela pendente` | `SCR-003` |
| `SCR-004 BoardTableView` | `#1 Board Table – Por Sprint` | `SCR-004` |
| `SCR-005 BoardKanbanView` | `#2 Board Kanban – Por Status` | `SCR-005` |
| `SCR-006 CardDetailModal` | `#3 Card Detail Modal` | `SCR-006` |
| `SCR-007 NewCardTemplateSelector` | `#4 New Card Template Selector` | `SCR-007` |
| `SCR-008 GroupByDropdown` | `#5 Group By Dropdown` | `SCR-008` |
| `SCR-009 ShareBoardModal` | `#6 Share Board Modal` | `SCR-009` |
| `SCR-010 ExportDropdown` | `#7 Export Dropdown` | `SCR-010` |
| `SCR-011 SettingsAppMenu` | `#8 Settings App Menu` | `SCR-011` |
| `SCR-012 CreateBoardModal` | `#9 Create a Board Modal` | `SCR-012` |
| `SCR-013 PropertiesPanel` | `#10 Properties Panel` | `SCR-013` |
| `SCR-014 SidebarCategoryContextMenu` | `#11 Sidebar Category Context Menu` | `SCR-014` |
| `SCR-015 SetThemeSubmenu` | `#12 Set Theme Submenu` | `SCR-015` |
| `SCR-016 SetLanguageSubmenu` | `#13 Set Language Submenu` | `SCR-016` |
| `SCR-017 UserAccountDropdown` | `#14 User Account Dropdown` | `SCR-017` |
| `SCR-018 ChangePasswordPage` | `tela pendente` | `SCR-018` |
| `SCR-019 FilterPanel` | `tela pendente` | `SCR-019` |
| `SCR-020 SortPanel` | `tela pendente` | `SCR-020` |
