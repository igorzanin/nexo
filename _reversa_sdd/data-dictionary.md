# Data Dictionary — nexo

> Gerado pelo Archaeologist em 2026-05-12
> 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Módulo: `server/ws`

### Server (Standalone)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `upgrader` | `websocket.Upgrader` | Sim | Upgrade HTTP para WebSocket |
| `listeners` | `map[*websocketSession]bool` | Sim | Conjunto de sessões conectadas |
| `listenersByTeam` | `map[string][]*websocketSession` | Sim | Índice de listeners por team |
| `listenersByBlock` | `map[string][]*websocketSession` | Sim | Índice de listeners por block |
| `mu` | `sync.RWMutex` | Sim | Controle de concorrência |
| `auth` | `*auth.Auth` | Sim | Serviço de autenticação |
| `singleUserToken` | `string` | Sim | Token para modo single user (vazio = multiusuário) |
| `isMattermostAuth` | `bool` | Sim | Se true, confia no header Mattermost-User-Id |
| `logger` | `mlog.LoggerIFace` | Sim | Logger estruturado |
| `store` | `Store` | Sim | Interface de acesso a dados |

### websocketSession

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `conn` | `*websocket.Conn` | Sim | Conexão WebSocket ativa |
| `userID` | `string` | Sim | ID do usuário autenticado (vazio = não autenticado) |
| `mu` | `sync.Mutex` | Sim | Mutex para escrita segura |
| `teams` | `[]string` | Sim | Teams aos quais o listener está inscrito |
| `blocks` | `[]string` | Sim | Blocks aos quais o listener está inscrito |

### PluginAdapter

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `api` | `servicesAPI` | Sim | Interface para API do Mattermost (PublishWebSocketEvent, PublishPluginClusterEvent) |
| `auth` | `auth.AuthInterface` | Sim | Interface de autenticação |
| `staleThreshold` | `time.Duration` | Sim | Tempo para considerar listener expirado (5 min) |
| `store` | `Store` | Sim | Interface de acesso a dados |
| `logger` | `mlog.LoggerIFace` | Sim | Logger estruturado |
| `listeners` | `map[string]*PluginAdapterClient` | Sim | Listeners indexados por webConnID |
| `listenersByUserID` | `map[string][]*PluginAdapterClient` | Sim | Listeners indexados por userID |
| `listenersMU` | `sync.RWMutex` | Sim | Mutex para listeners |
| `subscriptionsMU` | `sync.RWMutex` | Sim | Mutex para subscriptions |
| `listenersByTeam` | `map[string][]*PluginAdapterClient` | Sim | Listeners indexados por team |
| `listenersByBlock` | `map[string][]*PluginAdapterClient` | Sim | Listeners indexados por block |

### PluginAdapterClient

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `inactiveAt` | `int64` | Sim | Timestamp de desconexão (0 = ativo) |
| `webConnID` | `string` | Sim | ID da conexão WebSocket no Mattermost |
| `userID` | `string` | Sim | ID do usuário |
| `teams` | `[]string` | Sim | Teams inscritos |
| `blocks` | `[]string` | Sim | Blocks inscritos |
| `mu` | `sync.RWMutex` | Sim | Mutex para acesso concorrente |

### Mensagens WebSocket

#### WebsocketCommand (incoming)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `action` | `string` | Sim | Ação (AUTH, SUBSCRIBE_TEAM, etc.) |
| `teamId` | `string` | Sim | ID do team alvo |
| `token` | `string` | Não | Token de autenticação |
| `readToken` | `string` | Não | Token de leitura para blocks públicos |
| `blockIds` | `[]string` | Não | IDs de blocks para subscribe/unsubscribe |

#### UpdateBlockMsg (outgoing)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `action` | `string` | Sim | `"UPDATE_BLOCK"` |
| `teamId` | `string` | Sim | ID do team |
| `block` | `*model.Block` | Sim | Dados do bloco |

#### UpdateBoardMsg (outgoing)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `action` | `string` | Sim | `"UPDATE_BOARD"` |
| `teamId` | `string` | Sim | ID do team |
| `board` | `*model.Board` | Sim | Dados do board |

#### UpdateMemberMsg (outgoing)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `action` | `string` | Sim | `"UPDATE_MEMBER"` ou `"DELETE_MEMBER"` |
| `teamId` | `string` | Sim | ID do team |
| `member` | `*model.BoardMember` | Sim | Dados do membro |

#### UpdateCategoryMessage (outgoing)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `action` | `string` | Sim | `"UPDATE_CATEGORY"` ou `"UPDATE_BOARD_CATEGORY"` |
| `teamId` | `string` | Sim | ID do team |
| `category` | `*model.Category` | Não | Dados da categoria |
| `blockCategories` | `[]*model.BoardCategoryWebsocketData` | Não | Boards por categoria |

#### UpdateSubscription (outgoing)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `action` | `string` | Sim | `"UPDATE_SUBSCRIPTION"` |
| `subscription` | `*model.Subscription` | Sim | Dados da inscrição |

#### UpdateClientConfig (outgoing)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `action` | `string` | Sim | `"UPDATE_CLIENT_CONFIG"` |
| `clientconfig` | `model.ClientConfig` | Sim | Configuração do cliente |

#### UpdateCardLimitTimestamp (outgoing)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `action` | `string` | Sim | `"UPDATE_CARD_LIMIT_TIMESTAMP"` |
| `timestamp` | `int64` | Sim | Timestamp do limite |

#### CategoryReorderMessage (outgoing)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `action` | `string` | Sim | `"REORDER_CATEGORIES"` |
| `categoryOrder` | `[]string` | Sim | Ordem das categorias |
| `teamId` | `string` | Sim | ID do team |

#### CategoryBoardReorderMessage (outgoing)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `action` | `string` | Sim | `"REORDER_CATEGORY_BOARDS"` |
| `CategoryId` | `string` | Sim | ID da categoria |
| `BoardOrder` | `[]string` | Sim | Ordem dos boards |
| `teamId` | `string` | Sim | ID do team |

---

## Módulo: `server/auth`

### Auth

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `config` | `*config.Configuration` | Sim | Configuração do servidor (SessionExpireTime, SessionRefreshTime, EnablePublicSharedBoards) |
| `store` | `store.Store` | Sim | Acesso a dados (sessions, sharing) |
| `permissions` | `permissions.PermissionsService` | Sim | Serviço de permissões RBAC |

---

## Módulo: `webapp/src/components`

### Props

| Interface | Tipo de Propriedade | Tipo | Obrigatório | Descrição |
|-----------|---------------------|------|-------------|-----------|
| `Workspace` | `readonly` | `boolean` | Sim | Modo somente leitura |
| `CenterPanel` | `board` | `Board` | Sim | Board ativo |
| `CenterPanel` | `cards` | `Card[]` | Sim | Cards do board |
| `CenterPanel` | `activeView` | `BoardView` | Sim | View ativa |
| `CenterPanel` | `views` | `BoardView[]` | Sim | Todas as views do board |
| `CenterPanel` | `groupByProperty` | `IPropertyTemplate?` | Não | Propriedade de agrupamento |
| `CenterPanel` | `dateDisplayProperty` | `IPropertyTemplate?` | Não | Propriedade de data (calendar) |
| `CenterPanel` | `readonly` | `boolean` | Sim | Modo somente leitura |
| `CenterPanel` | `shownCardId` | `string?` | Não | Card aberto no dialog |
| `CenterPanel` | `showCard` | `(cardId?: string) => void` | Sim | Callback navegação card |
| `CenterPanel` | `hiddenCardsCount` | `number` | Sim | Cards ocultos por limite |
| `CardDialog` | `board` | `Board` | Sim | Board do card |
| `CardDialog` | `cardId` | `string` | Sim | ID do card aberto |
| `CardDialog` | `onClose` | `() => void` | Sim | Callback fechamento |
| `WithWebSockets` | `userId` | `string?` | Não | ID do usuário para autenticação |
| `WithWebSockets` | `webSocketClient` | `MMWebSocketClient?` | Não | Cliente WS customizado |
| `WithWebSockets` | `children` | `React.ReactNode` | Sim | Conteúdo encapsulado |

### ClusterMessage

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `TeamID` | `string` | Não | Team alvo |
| `BoardID` | `string` | Não | Board alvo |
| `UserID` | `string` | Não | Usuário alvo |
| `Payload` | `map[string]interface{}` | Sim | Dados da mensagem |
| `EnsureUsers` | `[]string` | Não | Usuários que devem receber |

---

## Módulo: `webapp/src/store` — Redux Store

### Slice: `users`

| Campo | Tipo | Inicial | Descrição |
|-------|------|---------|-----------|
| `me` | `IUser \| null` | `null` | Usuário logado |
| `boardUsers` | `{[key: string]: IUser}` | `{}` | Usuários do board atual indexados por ID |
| `loggedIn` | `boolean \| null` | `null` | Status de login |
| `blockSubscriptions` | `Subscription[]` | `[]` | Inscrições em blocks (WebSocket) |
| `myConfig` | `Record<string, UserPreference>` | `{}` | Preferências do usuário (parseadas via `parseUserProps`) |

### Slice: `teams`

| Campo | Tipo | Inicial | Descrição |
|-------|------|---------|-----------|
| `currentId` | `string` | `''` | ID do time ativo |
| `current` | `Team \| null` | `null` | Time ativo |
| `allTeams` | `Team[]` | `[]` | Todos os times disponíveis |

### Slice: `boards`

| Campo | Tipo | Inicial | Descrição |
|-------|------|---------|-----------|
| `current` | `string` | _não definido_ | ID do board ativo |
| `loadingBoard` | `boolean` | `false` | Indicador de carregamento |
| `linkToChannel` | `string` | `''` | Link para canal Mattermost |
| `boards` | `{[key: string]: Board}` | `{}` | Boards indexados por ID |
| `templates` | `{[key: string]: Board}` | `{}` | Templates de board |
| `membersInBoards` | `{[key: string]: {[key: string]: BoardMember}}` | `{}` | Membros por board |
| `myBoardMemberships` | `{[key: string]: BoardMember}` | `{}` | Memberships do usuário logado |

### Slice: `views`

| Campo | Tipo | Inicial | Descrição |
|-------|------|---------|-----------|
| `current` | `string` | `''` | ID da view ativa |
| `views` | `{[key: string]: BoardView}` | `{}` | Views indexadas por ID |

### Slice: `cards`

| Campo | Tipo | Inicial | Descrição |
|-------|------|---------|-----------|
| `current` | `string` | `''` | ID do card ativo |
| `limitTimestamp` | `number` | `0` | Timestamp de limite cloud |
| `cards` | `{[key: string]: Card}` | `{}` | Cards indexados por ID |
| `templates` | `{[key: string]: Card}` | `{}` | Templates de card |
| `cardHiddenWarning` | `boolean` | `false` | Aviso de cards ocultos por limite |

### Slice: `sidebar`

| Campo | Tipo | Inicial | Descrição |
|-------|------|---------|-----------|
| `categoryAttributes` | `CategoryBoards[]` | `[]` | Categorias da sidebar com metadados dos boards |
| `hiddenBoardIDs` | `string[]` | `[]` | IDs de boards ocultos |

### Slice: `limits`

| Campo | Tipo | Inicial | Descrição |
|-------|------|---------|-----------|
| `limits` | `BoardsCloudLimits` | `{cards: 0, used_cards: 0, card_limit_timestamp: 0, views: 0}` | Limites do cloud |

### Slice: `clientConfig`

| Campo | Tipo | Inicial | Descrição |
|-------|------|---------|-----------|
| `value` | `ClientConfig` | `{telemetry: false, enablePublicSharedBoards: false, ...}` | Configuração do cliente |

### Slice: `channels`

| Campo | Tipo | Inicial | Descrição |
|-------|------|---------|-----------|
| `current` | `Channel \| null` | `null` | Canal Mattermost ativo |

### Slices Simples

| Slice | Estado | Descrição |
|-------|--------|-----------|
| `searchText` | `{value: string}` | Texto de busca (`''`) |
| `globalError` | `{value: string}` | Mensagem de erro global (`''`) |
| `language` | `{value: string}` | Código do idioma (`'en'`) |
| `globalTemplates` | `{value: Board[]}` | Templates globais (`[]`) |

### Types Auxiliares

| Type | Definição |
|------|-----------|
| `Team` | `{id, title, signupToken, modifiedBy, updateAt}` |
| `Channel` | `{id, name, display_name, type: 'O'\|'P'\|'D'\|'G'}` |
| `CategoryBoards` | `{id, name, userID, teamID, createAt, updateAt, deleteAt, collapsed, sortOrder, type, isNew, boardMetadata[]}` |
| `CategoryBoardMetadata` | `{boardID, hidden}` |
| `UserPreference` | Objeto de preferência do usuário (ex: `onboardingTourStarted`, `tourCategory`) |

---

## Módulo: `webapp/src/blocks` — Modelos de Dados

### Block (base)

| Campo | Tipo | Obrigatório | Default | Descrição |
|-------|------|-------------|---------|-----------|
| `id` | `string` | Sim | GUID | ID único |
| `boardId` | `string` | Sim | `''` | Board pai |
| `parentId` | `string` | Sim | `''` | Bloco pai |
| `createdBy` | `string` | Sim | `''` | Criador |
| `modifiedBy` | `string` | Sim | `''` | Modificador |
| `schema` | `number` | Sim | `1` | Versão do schema |
| `type` | `BlockTypes` | Sim | `'unknown'` | Tipo do bloco |
| `title` | `string` | Sim | `''` | Título |
| `fields` | `Record<string, any>` | Sim | `{}` | Campos específicos |
| `createAt` | `number` | Sim | `Date.now()` | Timestamp criação |
| `updateAt` | `number` | Sim | `Date.now()` | Timestamp modificação |
| `deleteAt` | `number` | Sim | `0` | Timestamp deleção |
| `limited` | `boolean` | Não | `false` | Dados parciais |

### Board (extends Block)

| Campo | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `teamId` | `string` | `''` | Time |
| `channelId` | `string` | `''` | Canal |
| `type` | `'O'\|'P'` | `'P'` | Open ou Private |
| `minimumRole` | `MemberRole` | `None` | Papel mínimo |
| `title` | `string` | `''` | Título |
| `description` | `string` | `''` | Descrição |
| `icon` | `string` | `''` | Ícone |
| `showDescription` | `boolean` | `false` | Mostrar descrição |
| `isTemplate` | `boolean` | `false` | É template |
| `templateVersion` | `number` | `0` | Versão template |
| `properties` | `Record<string, string \| string[]>` | `{}` | Propriedades custom |
| `cardProperties` | `IPropertyTemplate[]` | `[{name:'Status', type:'select', options:[]}]` | Schema das propriedades |

### BoardView (extends Block)

| Campo | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `viewType` | `'board'\|'table'\|'gallery'\|'calendar'` | `'board'` | Tipo de visualização |
| `groupById` | `string` | opcional | Agrupamento kanban |
| `sortOptions` | `ISortOption[]` | `[]` | Opções de ordenação |
| `filter` | `FilterGroup` | `{operation:'and', filters:[]}` | Filtro |
| `cardOrder` | `string[]` | `[]` | Ordem manual |
| `visiblePropertyIds` | `string[]` | `[]` | Propriedades visíveis |
| `columnWidths` | `Record<string, number>` | `{}` | Larguras colunas |
| `columnCalculations` | `Record<string, string>` | `{}` | Cálculos por coluna |
| `kanbanCalculations` | `Record<string, {calculation, propertyId}>` | `{}` | Cálculos kanban |

### Card (extends Block)

| Campo | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `icon` | `string` | `''` | Ícone |
| `isTemplate` | `boolean` | `false` | É template |
| `properties` | `Record<string, string \| string[]>` | `{}` | Valores das propriedades |
| `contentOrder` | `Array<string \| string[]>` | `[]` | Ordem do conteúdo |

### IPropertyTemplate

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | `string` | ID |
| `name` | `string` | Nome exibido |
| `type` | `PropertyTypeEnum` | Tipo (18 tipos) |
| `options` | `IPropertyOption[]` | Opções (select/multiSelect) |

### IPropertyOption

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | `string` | ID |
| `value` | `string` | Valor exibido |
| `color` | `string` | Cor (ex: `"propColorBlue"`) |

### FilterGroup

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `operation` | `'and' \| 'or'` | Operador lógico |
| `filters` | `Array\<FilterClause \| FilterGroup\>` | Filtros aninhados |

### FilterClause

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `propertyId` | `string` | ID da propriedade |
| `condition` | `FilterCondition` | Condição (14 tipos) |
| `values` | `string[]` | Valores de comparação |

### BoardMember

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `boardId` | `string` | Board |
| `userId` | `string` | Usuário |
| `minimumRole` | `MemberRole` | Papel mínimo |
| `schemeAdmin` | `boolean` | Admin |
| `schemeEditor` | `boolean` | Editor |
| `schemeCommenter` | `boolean` | Commenter |
| `schemeViewer` | `boolean` | Viewer |
| `synthetic` | `boolean` | Sintético (não persiste) |

### MemberRole (enum)

| Valor | Descrição |
|-------|-----------|
| `'viewer'` | Apenas visualização |
| `'commenter'` | Visualização + comentários |
| `'editor'` | Edição |
| `'admin'` | Administração |
| `''` (None) | Sem papel definido |

### Enums

| Enum | Valores |
|------|---------|
| `BoardTypes` | `'O'` (Open), `'P'` (Private) |
| `BlockTypes` | `board, view, card, comment, text, image, divider, checkbox, h1, h2, h3, attachment, list-item, quote, video, unknown` |
| `ContentBlockTypes` | `text, image, divider, checkbox, h1, h2, h3, list-item, attachment, quote, video` |
| `FilterCondition` | `includes, notIncludes, isEmpty, isNotEmpty, isSet, isNotSet, is, contains, notContains, startsWith, notStartsWith, endsWith, notEndsWith, isBefore, isAfter` (15) |
| `IViewType` | `board, table, gallery, calendar` |

---

## Módulo: `webapp/src/pages`

### BoardPage Props

| Propriedade | Tipo | Obrigatório | Descrição |
|-------------|------|-------------|-----------|
| `readonly` | `boolean` | Não | Modo somente leitura |
| `new` | `boolean` | Não | Indica se é um board novo |
