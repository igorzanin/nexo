---
schemaVersion: 1
generatedAt: 2026-05-24T17:45:00-03:00
reversa:
  version: "1.0.0"
kind: target_architecture
producedBy: designer
hash: "sha256:designer-target_architecture-nexo"
---

# Target Architecture

## Visão Geral
O sistema alvo do nexo é um monólito modular standalone, com backend FastAPI em **package-by-layer** e frontend Vue 3 em **package-by-feature**, conforme a Opção 3 registrada em `topology_decision.md`.
A arquitetura preserva a organização idiomática do backend (`routers/`, `services/`, `repositories/`, `models/`, `auth/`, `ws/`) para manter testabilidade e clareza das dependências via `Depends()`.
No frontend, os bounded contexts viram features autocontidas em `webapp\src\features\`, deixando `shared\` apenas para infra transversal.
A estratégia de migração é **Big Bang Controlado**: não há roteamento parcial para produção, mas o legado permanece como referência comportamental e fallback de desenvolvimento.
Desktop e importadores continuam como bordas isoladas: Electron embute o backend FastAPI; os 6 importadores seguem em TypeScript e produzem `.boardarchive` NDJSON.

## Diagrama Mermaid

```mermaid
flowchart LR
    User[Usuário Web/Desktop]
    Public[Usuário anônimo via ReadToken]
    subgraph Frontend[Frontend Vue 3 + Pinia + Bootstrap]
        Router[Vue Router]
        Identity[features/identity]
        Boards[features/boards]
        Content[features/content]
        Views[features/views]
        Collab[features/collaboration]
        Shared[shared/api + shared/ws + shared/utils]
    end

    subgraph Desktop[Desktop]
        Electron[Electron Main Process]
    end

    subgraph Importers[Importadores CLI TypeScript]
        Trello[Trello]
        Jira[Jira]
        Asana[Asana]
        Todoist[Todoist]
        Notion[Notion]
        Nextcloud[Nextcloud Deck]
        Archive[ArchiveUtils NDJSON]
    end

    subgraph Backend[FastAPI Monolith]
        Routers[Routers]
        Auth[Auth]
        Services[Services]
        Repositories[Repositories]
        Models[Models]
        WS[WebSocket Server]
        Metrics[/metrics]
    end

    DB[(PostgreSQL / SQLite)]
    Files[(Filesystem local)]

    User --> Router
    Public --> Router
    Router --> Identity
    Router --> Boards
    Router --> Content
    Router --> Views
    Router --> Collab
    Identity --> Shared
    Boards --> Shared
    Content --> Shared
    Views --> Shared
    Collab --> Shared

    Shared -->|HTTP JSON| Routers
    Shared -->|WS AUTH / subscribe| WS

    Electron -->|spawn FastAPI subprocess| Routers
    Electron -->|load UI| Router

    Trello --> Archive
    Jira --> Archive
    Asana --> Archive
    Todoist --> Archive
    Notion --> Archive
    Nextcloud --> Archive
    Archive -->|import/export .boardarchive| Routers

    Routers --> Auth
    Routers --> Services
    Services --> Repositories
    Repositories --> Models
    Models --> DB
    Services --> Files
    WS --> Services
    Metrics --> Routers
```

## Componentes

| Nome | Tipo | Responsabilidade | Bounded context | Caminho |
|---|---|---|---|---|
| API Routers | API | Expor endpoints REST, validar payload e autenticação por caso de uso | transversal | `nexo\routers\` |
| Auth Module | Serviço técnico | JWT bearer, refresh token, bcrypt, rate limit, dependências FastAPI | BC-Identity | `nexo\auth\` |
| BoardService | Serviço | Criar boards, duplicar board, aplicar invariantes de tipo e minimumRole | BC-Boards | `nexo\services\board_service.py` |
| PermissionService | Serviço | Resolver matriz de 9 permissões e membership sintética para boards Open | BC-Boards | `nexo\services\permission_service.py` |
| CategoryService | Serviço | Categorias padrão, vínculo board↔categoria e soft-delete | BC-Boards | `nexo\services\category_service.py` |
| BlockService | Serviço | CRUD polimórfico de Block/Card/View/Comment/Text/Image/Attachment | BC-Content | `nexo\services\block_service.py` |
| BlockHistoryService | Serviço | Arquivar/restaurar blocos via `blocks_history` | BC-Content | `nexo\services\block_history_service.py` |
| ViewService | Serviço | Filtros, ordenação, cardOrder e materialização das 4 views | BC-Views | `nexo\services\view_service.py` |
| SharingService | Serviço | Habilitar compartilhamento público, gerar/validar readToken | BC-Collaboration | `nexo\services\sharing_service.py` |
| SubscriptionService | Serviço | Assinaturas em blocos e hints de notificação | BC-Collaboration | `nexo\services\subscription_service.py` |
| WSConnectionManager | Serviço técnico | AUTH, subscribe/unsubscribe, broadcast síncrono com `asyncio.Lock()` | BC-Collaboration | `nexo\ws\server.py` |
| SQLAlchemy Repositories | Repositório | Persistência por aggregate e consultas especializadas | transversal | `nexo\repositories\` |
| SQLAlchemy Models | Modelo | Representação relacional, soft-delete e constraints | transversal | `nexo\models\` |
| Metrics/Logging Middleware | Serviço técnico | `/metrics`, logs HTTP estruturados e limite de payload | transversal | `nexo\main.py`, `nexo\middleware\` |
| Identity Feature | Frontend feature | Login, register, sessão, onboarding, preferências | BC-Identity | `webapp\src\features\identity\` |
| Boards Feature | Frontend feature | Lista de boards, membros, times, categorias, templates | BC-Boards | `webapp\src\features\boards\` |
| Content Feature | Frontend feature | Editor unificado, cards, propriedades, histórico local, arquivos | BC-Content | `webapp\src\features\content\` |
| Views Feature | Frontend feature | Kanban, Table, Gallery, Calendar, filtros e ordenação | BC-Views | `webapp\src\features\views\` |
| Collaboration Feature | Frontend feature | Share board, comentários, subscriptions, readToken access | BC-Collaboration | `webapp\src\features\collaboration\` |
| Shared API Client | Frontend shared | Cliente HTTP, `useMutator`, tratamento de patches/undo/redo | transversal | `webapp\src\shared\api\` |
| Shared WS Client | Frontend shared | Conexão WebSocket, AUTH, subscribe/unsubscribe | transversal | `webapp\src\shared\ws\` |
| Electron Shell | Desktop | Empacotar app single-user, gerar porta aleatória e token local | BC-Identity / transversal | `desktop\` |
| Importadores CLI | Worker/CLI | Importar Trello/Jira/Asana/Todoist/Notion/Nextcloud para `.boardarchive` | BC-Content / BC-Boards | `import\` |
| PostgreSQL / SQLite | DB | Persistência OLTP com mesmo schema lógico | transversal | `database` |
| Filesystem local | Infra | Armazenamento de anexos e cópias de board | BC-Content | `files\` |

## Bounded Contexts

### BC-Identity
- **Responsabilidade**: identidade de usuário, sessões, autenticação JWT, onboarding e preferências.
- **Justificativa de agrupamento/separação**: autenticação, sessão e preferências mudam juntas e compartilham invariantes de segurança; foram separadas de boards para evitar misturar policy de acesso com colaboração.
- **Componentes backend**: `auth\jwt.py`, `auth\password.py`, `auth\dependencies.py`, `routers\auth.py`, `services\user_service.py`, `services\session_service.py`, `repositories\user_repository.py`, `repositories\session_repository.py`, `models\user.py`, `models\session.py`, `models\preference.py`.
- **Componentes frontend**: `features\identity\components\`, `features\identity\stores\auth.store.ts`, `features\identity\stores\preferences.store.ts`, `features\identity\composables\useSession.ts`, `features\identity\pages\`.

### BC-Boards
- **Responsabilidade**: boards, memberships, teams, categorias, templates e política de acesso em nível de board.
- **Justificativa de agrupamento/separação**: Board, BoardMember, Team, TeamMember, Category e CategoryBoard compartilham transações locais e invariantes de permissão; `minimumRole` e proteção do último admin exigem modelagem conjunta.
- **Componentes backend**: `routers\boards.py`, `routers\teams.py`, `routers\categories.py`, `services\board_service.py`, `services\permission_service.py`, `services\team_service.py`, `services\category_service.py`, repositórios e models correspondentes.
- **Componentes frontend**: `features\boards\components\`, `features\boards\stores\boards.store.ts`, `features\boards\stores\teams.store.ts`, `features\boards\stores\categories.store.ts`, `features\boards\composables\useHasPermissions.ts`.

### BC-Content
- **Responsabilidade**: bloco polimórfico, cards, propriedades customizadas, histórico, anexos e ordem de conteúdo.
- **Justificativa de agrupamento/separação**: a raiz de invariantes é `Block`; Card, Comment, View e demais tipos são especializações de um mesmo ciclo de vida com soft-delete e histórico. Separar por subtipo geraria decomposição 1-para-1 proibida.
- **Componentes backend**: `routers\blocks.py`, `routers\cards.py`, `routers\files.py`, `services\block_service.py`, `services\block_history_service.py`, `services\file_service.py`, `repositories\block_repository.py`, `repositories\file_repository.py`, `models\block.py`, `models\block_history.py`, `models\file_info.py`.
- **Componentes frontend**: `features\content\components\ContentRegistry.vue`, `features\content\components\PropertyValueElement.vue`, `features\content\stores\content.store.ts`, `features\content\stores\files.store.ts`, `features\content\composables\useContentEditor.ts`.

### BC-Views
- **Responsabilidade**: 4 tipos de view, filtros aninhados, sort options e card ordering por view.
- **Justificativa de agrupamento/separação**: filtros, ordenação e cardOrder evoluem juntos com BoardView; embora persistidos dentro de `blocks.fields`, formam um subdomínio de consulta/apresentação próprio.
- **Componentes backend**: `routers\views.py`, `services\view_service.py`, `repositories\block_repository.py` (para BoardView), `schemas\views.py`.
- **Componentes frontend**: `features\views\kanban\`, `features\views\table\`, `features\views\gallery\`, `features\views\calendar\`, `features\views\stores\views.store.ts`, `features\views\types\filter-group.ts`.

### BC-Collaboration
- **Responsabilidade**: compartilhamento público, readToken, subscriptions, notification hints, comentários e WebSocket.
- **Justificativa de agrupamento/separação**: compartilhamento e realtime compartilham a noção de audiência e entrega; comentários permanecem subtipo de Block, mas seus fluxos colaborativos e de permissão vivem neste contexto.
- **Componentes backend**: `routers\sharing.py`, `routers\subscriptions.py`, `ws\server.py`, `services\sharing_service.py`, `services\subscription_service.py`, `repositories\sharing_repository.py`, `repositories\subscription_repository.py`, `models\sharing.py`, `models\subscription.py`, `models\notification_hint.py`.
- **Componentes frontend**: `features\collaboration\components\ShareBoardDialog.vue`, `features\collaboration\components\CommentsPanel.vue`, `features\collaboration\stores\sharing.store.ts`, `features\collaboration\stores\subscriptions.store.ts`, `shared\ws\useWebSocket.ts`.

## Decisões Arquiteturais (ADRs)

### ADR-001 — Package-by-layer no backend (preservado)
- **Contexto**: `paradigm_decision.md` exige separação de camadas explícita para OO com DI; `architecture.md` e `topology_decision.md` mostram backend já alinhado com FastAPI idiomático.
- **Decisão**: manter backend em `routers/`, `services/`, `repositories/`, `models/`, `auth/`, `ws/`.
- **Consequências**: reduz retrabalho, mantém onboarding simples e favorece testes isolados por camada; leitura de um fluxo exige navegar por várias pastas, mas isso é aceitável no backend atual.
- **Rastreabilidade**: `_reversa_sdd/architecture.md` §"Arquitetura em Camadas"; `_reversa_sdd/migration/topology_decision.md`.

### ADR-002 — Package-by-feature no frontend (modernizado)
- **Contexto**: o frontend legado/parcial mistura `components/` por feature com `stores/`, `types/` e `composables/` globais, diagnosticado como parcialmente problemático.
- **Decisão**: mover o frontend para `webapp\src\features\identity|boards|content|views|collaboration` e reservar `shared\` para infra transversal.
- **Consequências**: PRs ficam mais localizados, a navegação por feature melhora e a fronteira com bounded contexts fica explícita; há custo de reorganização do rascunho atual.
- **Rastreabilidade**: `_reversa_sdd/migration/topology_decision.md`; `_reversa_sdd/inventory.md` §`webapp/`.

### ADR-003 — Block como entidade polimórfica base
- **Contexto**: `domain.md` R10–R20 e BR-MIGRAR-018 indicam que cards, views, comments e elementos de conteúdo compartilham identidade, boardId, fields e histórico.
- **Decisão**: modelar `Block` como aggregate root polimórfico, com subtipos lógicos `Card`, `BoardView`, `Comment`, `Text`, `Image`, `Divider` e `Attachment`.
- **Consequências**: evita explosão de tabelas e preserva rastreabilidade 1-para-1 com o legado; exige validações por subtipo em service/schema.
- **Rastreabilidade**: `_reversa_sdd/domain.md` R10–R20; `_reversa_sdd/migration/target_business_rules.md` BR-MIGRAR-018 e BR-MIGRAR-019.

### ADR-004 — Soft-delete via `delete_at` e histórico de blocos
- **Contexto**: `domain.md` R38–R40 exige soft-delete universal e histórico específico para blocos.
- **Decisão**: manter `delete_at` em entidades persistentes e usar `blocks_history` para archive/restore de blocos.
- **Consequências**: restauração e auditoria ficam simples; toda query precisa filtrar ativos por padrão e índices precisam considerar `delete_at`.
- **Rastreabilidade**: `_reversa_sdd/domain.md` R38–R40; BR-MIGRAR-007.

### ADR-005 — WebSocket standalone sem filas externas
- **Contexto**: a stack alvo não usa mensageria; BR-MIGRAR-008 e BR-MIGRAR-022 preservam AUTH por ação e broadcast síncrono com monitoramento de performance.
- **Decisão**: manter WebSocket nativo FastAPI com `WSConnectionManager`, `asyncio.Lock()` e assinatura por team/block, sem broker externo.
- **Consequências**: simplicidade operacional e zero infraestrutura extra; throughput deve ser validado em carga e pode exigir otimizações futuras.
- **Rastreabilidade**: `_reversa_sdd/domain.md` R41–R44; `_reversa_sdd/migration/target_business_rules.md` BR-MIGRAR-022.

### ADR-006 — Importadores mantidos em TypeScript
- **Contexto**: `migration_brief.md` inclui importação como escopo; BR-MIGRAR-015 e BR-MIGRAR-016 descrevem 6 CLIs já conceitualmente separados da API.
- **Decisão**: manter `import\` como toolchain Node/TypeScript que lê fontes externas e produz `.boardarchive` NDJSON consumido pelo backend.
- **Consequências**: reaproveita ecossistema existente e isola parsing de terceiros fora do backend Python; requer manutenção de dois runtimes no projeto.
- **Rastreabilidade**: BR-MIGRAR-015; BR-MIGRAR-016; `_reversa_sdd/architecture.md` §"Escala de Confiança".

### ADR-007 — PostgreSQL primário com fallback SQLite
- **Contexto**: `migration_brief.md` e `architecture.md` definem PostgreSQL 16 via `.env` com fallback SQLite para desenvolvimento/desktop.
- **Decisão**: adotar um schema único SQLAlchemy/Alembic compatível com PostgreSQL e SQLite, com JSON em colunas compatíveis e IDs `TEXT`.
- **Consequências**: simplifica portabilidade e modo desktop; algumas constraints e índices precisam ficar no subconjunto comum aos dois bancos.
- **Rastreabilidade**: `_reversa_sdd/migration/migration_brief.md` §"Stack alvo"; `_reversa_sdd/architecture.md` §"Stack Tecnológica".

### ADR-008 — Mutator como borda única de mutações no frontend
- **Contexto**: BR-MIGRAR-012 pede patches com diff e centralização das chamadas à API; `paradigm_decision.md` proíbe lógica de negócio em componentes Vue.
- **Decisão**: concentrar mutações do frontend em `shared\api\useMutator.ts`, com Pinia stores como única fonte de verdade e componentes apenas reagindo ao estado.
- **Consequências**: undo/redo, otimizações otimistas e tratamento uniforme de erro ficam padronizados; exige disciplina para não chamar API diretamente de componentes.
- **Rastreabilidade**: `_reversa_sdd/domain.md` glossário `Mutator`; BR-MIGRAR-012; `_reversa_sdd/migration/paradigm_decision.md`.

## Honra ao paradigma escolhido

- **Paradigma alvo**: backend **OO com DI** + frontend **Reativo + Composição**, sem gap de paradigma (`paradigm_decision.md`).
- **Materialização no backend**:
  - `Depends()` funciona como container de injeção leve, ligando router → service → repository sem service locator manual.
  - Regras de negócio vivem em `services\`; persistência vive em `repositories\`; `routers\` só coordenam HTTP/auth/schema.
  - Interfaces são implícitas por duck typing Python: contratos são mantidos por métodos esperados dos repositórios e testes, sem boilerplate de interfaces artificiais.
  - `models\` e `schemas\` permanecem separados para evitar colapso entre domínio de API e domínio relacional.
- **Materialização no frontend**:
  - Pinia stores são a única fonte de verdade para estado de sessão, boards, content, views e colaboração.
  - Componentes Vue SFC são finos: renderizam UI Bootstrap 5.3 e delegam comportamento para stores/composables.
  - Composables encapsulam comportamento reutilizável (`useMutator`, `useWebSocket`, `useHasPermissions`) e evitam duplicação de lógica imperativa em componentes.
  - Não há eventos de domínio explícitos nem mensageria assíncrona de negócio: a coordenação permanece síncrona por chamadas de serviço, coerente com o paradigma escolhido.

## Honra à topologia escolhida

A topologia escolhida foi **Híbrido — Opção 3**: preservar o backend em camadas e modernizar o frontend para package-by-feature.
Isso materializa exatamente a recomendação registrada em `topology_decision.md`: manter o que já é idiomático no FastAPI e modernizar apenas o ponto estruturalmente inconsistente, o frontend.
Importadores, migrations e desktop permanecem preservados como módulos isolados porque já possuem fronteiras naturais e não se beneficiam de realocação por bounded context.

### Esboço final da árvore completa

```text
nexo\
├── main.py
├── settings.py
├── database.py
├── middleware\
│   ├── logging_middleware.py
│   ├── payload_limit_middleware.py
│   └── metrics_middleware.py
├── auth\
│   ├── jwt.py
│   ├── password.py
│   ├── dependencies.py
│   └── rate_limit.py
├── models\
│   ├── user.py
│   ├── session.py
│   ├── preference.py
│   ├── team.py
│   ├── team_member.py
│   ├── board.py
│   ├── board_member.py
│   ├── block.py
│   ├── block_history.py
│   ├── category.py
│   ├── category_board.py
│   ├── sharing.py
│   ├── subscription.py
│   ├── notification_hint.py
│   └── file_info.py
├── schemas\
│   ├── auth.py
│   ├── boards.py
│   ├── blocks.py
│   ├── views.py
│   ├── sharing.py
│   └── common.py
├── repositories\
│   ├── user_repository.py
│   ├── session_repository.py
│   ├── board_repository.py
│   ├── permission_repository.py
│   ├── block_repository.py
│   ├── block_history_repository.py
│   ├── category_repository.py
│   ├── sharing_repository.py
│   ├── subscription_repository.py
│   └── file_repository.py
├── services\
│   ├── user_service.py
│   ├── session_service.py
│   ├── board_service.py
│   ├── permission_service.py
│   ├── category_service.py
│   ├── block_service.py
│   ├── block_history_service.py
│   ├── view_service.py
│   ├── sharing_service.py
│   ├── subscription_service.py
│   └── file_service.py
├── routers\
│   ├── auth.py
│   ├── users.py
│   ├── teams.py
│   ├── boards.py
│   ├── blocks.py
│   ├── views.py
│   ├── categories.py
│   ├── sharing.py
│   ├── subscriptions.py
│   ├── files.py
│   └── metrics.py
├── ws\
│   ├── server.py
│   ├── actions.py
│   └── auth.py
└── tests\
    ├── integration\
    └── unit\

webapp\src\
├── main.ts
├── App.vue
├── router\index.ts
├── pages\
│   ├── LoginPage.vue
│   ├── RegisterPage.vue
│   ├── BoardsPage.vue
│   ├── BoardPage.vue
│   └── SharedBoardPage.vue
├── shared\
│   ├── api\
│   │   ├── client.ts
│   │   ├── useMutator.ts
│   │   └── patch-history.ts
│   ├── ws\
│   │   ├── client.ts
│   │   └── useWebSocket.ts
│   ├── ui\
│   ├── utils\
│   └── types\
└── features\
    ├── identity\
    │   ├── components\
    │   ├── stores\
    │   ├── composables\
    │   └── types\
    ├── boards\
    │   ├── components\
    │   ├── stores\
    │   ├── composables\
    │   └── types\
    ├── content\
    │   ├── components\
    │   ├── stores\
    │   ├── composables\
    │   └── types\
    ├── views\
    │   ├── kanban\
    │   ├── table\
    │   ├── gallery\
    │   ├── calendar\
    │   ├── stores\
    │   └── types\
    └── collaboration\
        ├── components\
        ├── stores\
        ├── composables\
        └── types\

import\
├── trello\
├── jira\
├── asana\
├── todoist\
├── notion\
├── nextcloud-deck\
└── util\archive.ts

desktop\
├── electron\main.ts
├── electron\server.ts
└── preload\index.ts

migrations\
└── versions\
```
