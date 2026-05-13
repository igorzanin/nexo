# Spec Impact Matrix — nexo

> Gerado pelo Architect em 2026-05-12
> 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Matriz de Impacto entre Componentes

| Componente | Impactado por | Impacta | Descrição |
|-----------|---------------|---------|-----------|
| **Board** (model) | - | BoardMember, Block, Sharing, CategoryBoard, BoardLimits, BoardHistory | Entidade central do sistema |
| **Block** (model) | Board | Block (self), Subscription, FileInfo, BlockHistory | Base polimórfica (card, view, comment, etc.) |
| **User** (model) | - | Session, BoardMember, Subscription, Category | Usuário do sistema |
| **Team** (model) | - | Board, Category, BoardMember | Agrupamento de usuários |
| **Board Handlers** (api) | App Boards, Permissions | HTTP Response | CRUD de boards |
| **Block Handlers** (api) | App Blocks, Permissions | HTTP Response | CRUD de blocks |
| **Auth Handlers** (api) | App Auth, Auth Service | HTTP Response | Login, registro, sessão |
| **App Boards** (app) | Board Handlers | Store, Permissions, WebSocket | Lógica de negócio de boards |
| **App Blocks** (app) | Block Handlers | Store, Permissions, WebSocket | Lógica de negócio de blocks |
| **App Auth** (app) | Auth Handlers | Store, Auth Service | Registro e autenticação |
| **Permissions** (services) | App Boards, App Blocks, App Auth | API Handlers | Matriz RBAC/ACL |
| **WebSocket Server** (ws) | App Boards, App Blocks | PluginAdapter | Broadcast de mudanças |
| **PluginAdapter** (ws) | WebSocket Server | Mattermost API | Clusterização |
| **Store** (services) | App Boards, App Blocks, App Auth | SQLite/PostgreSQL/MySQL | Acesso a dados |
| **Frontend Store** (Redux) | App render | Componentes UI | 16 slices de estado global |
| **Mutator** (frontend) | API Server | Redux Store | Centraliza chamadas + undo/redo |
| **CenterPanel** (frontend) | Redux Store | Kanban, Table, Gallery, Calendar | Orquestra view ativa |
| **BoardPermissionGate** (frontend) | Redux Store | CardDialog, Sidebar | Guarda de acesso |
| **Importadores** (CLI) | - | .boardarchive | 6 ferramentas de importação |

## Impacto por Camada

### Camada API (server/api)
| Handler | Endpoints | Impacto |
|---------|-----------|---------|
| AdminHandler | `GET/PUT /api/v1/admin/*` | Configurações, métricas |
| AuthHandler | `POST /api/v1/auth/login`, `POST /api/v1/auth/register`, `GET /api/v1/auth/logout` | Sessão de usuário |
| BlockHandler | `GET/POST/PUT/DELETE /api/v1/blocks` | Cards, views, comments, content |
| BoardHandler | `GET/POST/PUT/DELETE /api/v1/boards` | Boards, templates |
| CardHandler | `GET /api/v1/cards/*` | Cards (específico) |
| CategoryHandler | `GET/POST/PUT/DELETE /api/v1/categories` | Categorias da sidebar |
| FileHandler | `POST/GET /api/v1/files` | Attachments |
| SubscriptionHandler | `GET/POST/PUT/DELETE /api/v1/subscriptions` | Inscrições de notificação |
| TeamHandler | `GET/POST/PUT /api/v1/teams` | Times |
| UserHandler | `GET/PUT /api/v1/users` | Perfil de usuário |

### Camada App (server/app)
| Componente | Funções Críticas | Impacto |
|-----------|-----------------|---------|
| AppBoards | Create, Patch, Delete, Duplicate, Undelete | Integridade dos boards |
| AppBlocks | Insert, Patch, Delete, Undelete, GetCardLimit | Integridade dos cards |
| AppAuth | RegisterUser, RegisterGuest, Login | Fluxo de autenticação |
| AppCategories | Create, Patch, Delete, Reorder | Organização sidebar |

### Camada Frontend
| Componente | Funções Críticas | Impacto |
|-----------|-----------------|---------|
| initialLoad | Carrega dados iniciais (8 chamadas paralelas) | Experiência de entrada |
| sortCards | Ordenação multi-critério (8+ tipos de property) | Visualização correta |
| mutator.insertBlock | Cria card/block + undo/redo | Consistência operacional |
| WithWebSockets | Conexão WebSocket + autenticação | Tempo real |

## Análise de Risco

| Componente | Risco | Justificativa |
|-----------|-------|---------------|
| Permissions | 🔴 ALTO | Central para segurança. Erro pode expor boards privados |
| AppBoards | 🔴 ALTO | Lógica de negócio crítica (criação, duplicação, deleção) |
| Store (SQL) | 🟡 MÉDIO | Query builder complexo com suporte a 3 bancos |
| Mutator | 🟡 MÉDIO | Centraliza operações + undo/redo + chamadas API |
| WebSocket Server | 🟡 MÉDIO | Broadcast seletivo complexo (board members + block subscribers) |
| Importadores | 🟢 BAIXO | CLI isolada, sem impacto em produção |
| Desktop Apps | 🟢 BAIXO | Empacotamento, sem lógica de negócio própria |

## Confiança

| Item | Confiança |
|------|-----------|
| Matriz de impacto entre componentes | 🟢 CONFIRMADO |
| Análise de risco por componente | 🟡 INFERIDO (baseada em complexidade do código) |
| Dependências entre camadas | 🟢 CONFIRMADO |
