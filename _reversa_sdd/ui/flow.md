# UI Flow — Fluxo de Navegação

> Fluxo de navegação entre telas do Nexo (Focalboard), mapeado a partir das screenshots capturadas.
> Gerado por: reversa-visor — 2026-05-24

## Diagrama principal

```mermaid
flowchart TD
    APP_LOAD([Inicialização do App])
    LOGIN[Tela de Login\nauth]
    REGISTER[Tela de Registro\n⚠️ não capturada]
    HOME[Home — Lista de Boards\n⚠️ não capturada]

    SIDEBAR_BOARD[Sidebar: Seleciona Board]
    BOARD_TABLE[Board Table View\npaginas — Por Sprint]
    BOARD_KANBAN[Board Kanban View\npaginas — Por Status]
    BOARD_TYPE[Board View — Por Tipo\n⚠️ não capturada]
    BOARD_SPRINT_KANBAN[Sprint Kanban\n⚠️ não capturada]

    CARD_DETAIL[Card Detail Modal\ncomponentes]
    TEMPLATE_SELECTOR[Template Selector Dropdown\ncomponentes]
    GROUP_BY_DROPDOWN[Group By Dropdown\ncomponentes]
    PROPERTIES_PANEL[Properties Panel\ncomponentes]
    SHARE_MODAL[Share Board Modal\ncomponentes]
    EXPORT_DROPDOWN[Export Dropdown\ncomponentes]
    CREATE_BOARD_MODAL[Create a Board Modal\ncomponentes]
    SETTINGS_MENU[Settings App Menu\ncomponentes]
    SETTINGS_PAGE[Settings Page\n⚠️ não capturada]
    SET_THEME[Set Theme Submenu\ncomponentes]
    SET_LANG[Set Language Submenu\ncomponentes]
    ACCOUNT_DD[User Account Dropdown\ncomponentes]
    CHANGE_PWD[Change Password\n⚠️ não capturada]
    INVITE[Invite Users\n⚠️ não capturada]

    APP_LOAD --> LOGIN
    LOGIN -- "Credenciais válidas" --> HOME
    LOGIN -- "create an account" --> REGISTER
    HOME --> SIDEBAR_BOARD
    SIDEBAR_BOARD --> BOARD_TABLE
    SIDEBAR_BOARD --> BOARD_KANBAN
    SIDEBAR_BOARD --> BOARD_TYPE
    SIDEBAR_BOARD --> BOARD_SPRINT_KANBAN

    BOARD_TABLE -- "Clique no card" --> CARD_DETAIL
    BOARD_KANBAN -- "Clique no card" --> CARD_DETAIL

    BOARD_TABLE -- "New ▾" --> TEMPLATE_SELECTOR
    BOARD_KANBAN -- "New ▾" --> TEMPLATE_SELECTOR
    TEMPLATE_SELECTOR -- "Seleciona template" --> CARD_DETAIL

    BOARD_TABLE -- "Group by" --> GROUP_BY_DROPDOWN
    BOARD_KANBAN -- "Group by" --> GROUP_BY_DROPDOWN
    GROUP_BY_DROPDOWN -- "Aplica agrupamento" --> BOARD_TABLE
    GROUP_BY_DROPDOWN -- "Aplica agrupamento" --> BOARD_KANBAN

    BOARD_TABLE -- "Properties" --> PROPERTIES_PANEL
    BOARD_KANBAN -- "Properties" --> PROPERTIES_PANEL

    BOARD_TABLE -- "Share" --> SHARE_MODAL
    BOARD_KANBAN -- "Share" --> SHARE_MODAL

    BOARD_TABLE -- "..." --> EXPORT_DROPDOWN
    BOARD_KANBAN -- "..." --> EXPORT_DROPDOWN

    HOME -- "+ Add board" --> CREATE_BOARD_MODAL
    SIDEBAR_BOARD -- "+ Add board" --> CREATE_BOARD_MODAL

    HOME -- "Settings (rodapé)" --> SETTINGS_MENU
    SETTINGS_MENU -- "Settings link" --> SETTINGS_PAGE
    SETTINGS_MENU -- "Set theme ▶" --> SET_THEME
    SETTINGS_MENU -- "Set language ▶" --> SET_LANG

    HOME -- "Logo Focalboard" --> ACCOUNT_DD
    ACCOUNT_DD -- "Log out" --> LOGIN
    ACCOUNT_DD -- "Change password" --> CHANGE_PWD
    ACCOUNT_DD -- "Invite users" --> INVITE
```

## Fluxo: Autenticação (Login)

```mermaid
sequenceDiagram
    actor U as Usuário
    participant L as Login Page
    participant H as Home

    U->>L: Acessa URL do app (não autenticado)
    U->>L: Preenche username + password
    U->>L: Clica em "Log in"
    alt Credenciais válidas
        L->>H: Redireciona para Home / último board
    else Credenciais inválidas
        L-->>U: Exibe mensagem de erro
    end
    Note over L: Link "create an account" disponível para novos usuários
```

## Fluxo: Criar novo card

```mermaid
sequenceDiagram
    actor U as Usuário
    participant B as Board (Table/Kanban)
    participant TS as Template Selector
    participant CD as Card Detail Modal

    U->>B: Clica em "New ▾"
    B->>TS: Abre Template Selector
    U->>TS: Seleciona tipo (Bug, História, Épico, etc.)
    TS->>CD: Abre Card Detail com template pré-carregado
    U->>CD: Preenche título e propriedades
    U->>CD: Fecha modal
    CD->>B: Card aparece na view
```

## Fluxo: Compartilhar board

```mermaid
sequenceDiagram
    actor U as Usuário
    participant B as Board
    participant SM as Share Modal

    U->>B: Clica em "Share"
    B->>SM: Abre Share Board Modal
    U->>SM: Busca pessoa/canal ou copia link
    SM-->>U: Retorna confirmação ou link copiado
    U->>SM: Fecha modal
```

## Fluxo: Criar novo board

```mermaid
sequenceDiagram
    actor U as Usuário
    participant S as Sidebar
    participant CB as Create Board Modal
    participant B as Novo Board

    U->>S: Clica em "+ Add board"
    S->>CB: Abre Create a Board Modal
    U->>CB: Navega pela lista de templates
    alt Usar template
        U->>CB: Seleciona template → "Use this template"
    else Em branco
        U->>CB: "Create an empty board"
    end
    CB->>B: Board criado e aberto
    B-->>S: Board aparece na sidebar
```

## Pontos de entrada

| Ponto | Descrição |
|---|---|
| URL direta do board | `https://focalboard.fischerzanin.com.br/...` |
| Login → Home → Board | Fluxo padrão de primeiro acesso |
| Link "Share internally" | Acesso direto por link com permissão |

## Pontos de saída

| Ponto | Descrição |
|---|---|
| Settings Page | Configurações avançadas (idioma, tema, conta) |
| Exportação CSV/Archive | Download de dados — sai do contexto do board |
| "Give feedback" | Link externo para feedback ao time Focalboard |
