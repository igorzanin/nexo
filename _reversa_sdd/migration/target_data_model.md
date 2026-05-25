---
schemaVersion: 1
generatedAt: 2026-05-24T17:45:00-03:00
reversa:
  version: "1.0.0"
kind: target_data_model
producedBy: designer
hash: "sha256:designer-target_data_model-nexo"
---

# Target Data Model

## Entidades de Dados

| Nome da tabela | Aggregate dono | PK | Bounded context | Origem legado |
|---|---|---|---|---|
| `users` | AGG-User | `id` | BC-Identity | `users` |
| `sessions` | AGG-User | `id` | BC-Identity | `sessions` |
| `preferences` | AGG-User | `(user_id, category, name)` | BC-Identity | `preferences` |
| `teams` | AGG-Board | `id` | BC-Boards | `teams` |
| `team_members` | AGG-User | `(team_id, user_id)` | BC-Boards | `team_members` |
| `boards` | AGG-Board | `id` | BC-Boards | `boards` |
| `board_members` | AGG-Board | `(board_id, user_id)` | BC-Boards | `board_members` |
| `categories` | AGG-Category | `id` | BC-Boards | `categories` |
| `category_boards` | AGG-Category | `id` | BC-Boards | `category_boards` |
| `blocks` | AGG-Block | `id` | BC-Content / BC-Views / BC-Collaboration | `blocks` |
| `blocks_history` | AGG-Block | `(id, insert_at)` | BC-Content | `blocks_history` |
| `subscriptions` | AGG-Subscription | `(block_type, block_id, subscriber_type, subscriber_id)` | BC-Collaboration | `subscriptions` |
| `notification_hints` | AGG-Subscription | `(block_type, block_id)` | BC-Collaboration | `notification_hints` |
| `sharing` | AGG-Sharing | `id` | BC-Collaboration | `sharing` |
| `file_info` | AGG-Block | `id` | BC-Content | `file_info` |

## DDL — PostgreSQL/SQLite (SQLAlchemy-compatible)

```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_bot BOOLEAN NOT NULL DEFAULT FALSE,
    props JSON,
    create_at BIGINT NOT NULL,
    update_at BIGINT NOT NULL,
    delete_at BIGINT NOT NULL DEFAULT 0,
    CHECK (length(trim(username)) > 0),
    CHECK (length(trim(email)) > 0),
    CHECK (delete_at >= 0)
);

CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    token TEXT NOT NULL UNIQUE,
    user_id TEXT NOT NULL,
    create_at BIGINT NOT NULL,
    last_active_time BIGINT,
    expire_at BIGINT NOT NULL,
    CONSTRAINT fk_sessions_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (expire_at >= create_at)
);

CREATE TABLE teams (
    id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    type TEXT NOT NULL DEFAULT 'O',
    description TEXT,
    create_at BIGINT NOT NULL,
    update_at BIGINT NOT NULL,
    delete_at BIGINT NOT NULL DEFAULT 0,
    CHECK (type IN ('O', 'P')),
    CHECK (delete_at >= 0)
);

CREATE TABLE team_members (
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    roles TEXT,
    scheme_guest BOOLEAN NOT NULL DEFAULT FALSE,
    scheme_user BOOLEAN NOT NULL DEFAULT TRUE,
    scheme_admin BOOLEAN NOT NULL DEFAULT FALSE,
    create_at BIGINT NOT NULL,
    update_at BIGINT NOT NULL,
    delete_at BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (team_id, user_id),
    CONSTRAINT fk_team_members_team FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    CONSTRAINT fk_team_members_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (delete_at >= 0),
    CHECK (NOT (scheme_guest = TRUE AND scheme_user = TRUE)),
    CHECK (NOT (scheme_guest = TRUE AND scheme_admin = TRUE))
);

CREATE TABLE boards (
    id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    created_by TEXT,
    modified_by TEXT,
    type TEXT NOT NULL DEFAULT 'P',
    minimum_role TEXT NOT NULL DEFAULT '',
    title TEXT,
    description TEXT,
    icon TEXT,
    show_description BOOLEAN NOT NULL DEFAULT FALSE,
    is_template BOOLEAN NOT NULL DEFAULT FALSE,
    template_version INTEGER NOT NULL DEFAULT 0,
    properties JSON,
    card_properties JSON,
    create_at BIGINT NOT NULL,
    update_at BIGINT NOT NULL,
    delete_at BIGINT NOT NULL DEFAULT 0,
    CONSTRAINT fk_boards_team FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE RESTRICT,
    CONSTRAINT fk_boards_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_boards_modified_by FOREIGN KEY (modified_by) REFERENCES users(id) ON DELETE SET NULL,
    CHECK (type IN ('O', 'P')),
    CHECK (minimum_role IN ('', 'viewer', 'commenter', 'editor', 'admin')),
    CHECK (delete_at >= 0),
    CHECK (template_version >= 0)
);

CREATE TABLE board_members (
    board_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    roles TEXT,
    scheme_admin BOOLEAN NOT NULL DEFAULT FALSE,
    scheme_editor BOOLEAN NOT NULL DEFAULT FALSE,
    scheme_commenter BOOLEAN NOT NULL DEFAULT FALSE,
    scheme_viewer BOOLEAN NOT NULL DEFAULT TRUE,
    create_at BIGINT NOT NULL,
    update_at BIGINT NOT NULL,
    delete_at BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (board_id, user_id),
    CONSTRAINT fk_board_members_board FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE,
    CONSTRAINT fk_board_members_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (delete_at >= 0),
    CHECK (
        (CASE WHEN scheme_admin THEN 1 ELSE 0 END) +
        (CASE WHEN scheme_editor THEN 1 ELSE 0 END) +
        (CASE WHEN scheme_commenter THEN 1 ELSE 0 END) +
        (CASE WHEN scheme_viewer THEN 1 ELSE 0 END)
        <= 1
    )
);

CREATE TABLE blocks (
    id TEXT PRIMARY KEY,
    parent_id TEXT,
    root_id TEXT,
    created_by TEXT,
    modified_by TEXT,
    schema INTEGER NOT NULL DEFAULT 1,
    type TEXT NOT NULL,
    title TEXT,
    fields JSON,
    create_at BIGINT NOT NULL,
    update_at BIGINT NOT NULL,
    delete_at BIGINT NOT NULL DEFAULT 0,
    board_id TEXT NOT NULL,
    CONSTRAINT fk_blocks_parent FOREIGN KEY (parent_id) REFERENCES blocks(id) ON DELETE SET NULL,
    CONSTRAINT fk_blocks_root FOREIGN KEY (root_id) REFERENCES blocks(id) ON DELETE SET NULL,
    CONSTRAINT fk_blocks_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_blocks_modified_by FOREIGN KEY (modified_by) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_blocks_board FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE,
    CHECK (schema >= 1),
    CHECK (delete_at >= 0)
);

CREATE TABLE blocks_history (
    id TEXT NOT NULL,
    parent_id TEXT,
    root_id TEXT,
    created_by TEXT,
    modified_by TEXT,
    schema INTEGER,
    type TEXT NOT NULL,
    title TEXT,
    fields JSON,
    create_at BIGINT NOT NULL,
    update_at BIGINT NOT NULL,
    delete_at BIGINT NOT NULL,
    board_id TEXT NOT NULL,
    insert_at BIGINT NOT NULL,
    PRIMARY KEY (id, insert_at),
    CONSTRAINT fk_blocks_history_board FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE,
    CONSTRAINT fk_blocks_history_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_blocks_history_modified_by FOREIGN KEY (modified_by) REFERENCES users(id) ON DELETE SET NULL,
    CHECK (insert_at >= create_at),
    CHECK (delete_at > 0)
);

CREATE TABLE categories (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    user_id TEXT NOT NULL,
    team_id TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    type TEXT NOT NULL DEFAULT 'custom',
    create_at BIGINT NOT NULL,
    update_at BIGINT NOT NULL,
    delete_at BIGINT NOT NULL DEFAULT 0,
    CONSTRAINT fk_categories_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_categories_team FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    CHECK (type IN ('system', 'custom')),
    CHECK (delete_at >= 0)
);

CREATE TABLE category_boards (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    team_id TEXT NOT NULL,
    category_id TEXT NOT NULL,
    board_id TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    hide BOOLEAN NOT NULL DEFAULT FALSE,
    create_at BIGINT NOT NULL,
    update_at BIGINT NOT NULL,
    delete_at BIGINT NOT NULL DEFAULT 0,
    CONSTRAINT fk_category_boards_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    CONSTRAINT fk_category_boards_board FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE,
    CONSTRAINT fk_category_boards_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_category_boards_team FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    CONSTRAINT uq_category_boards_unique UNIQUE (category_id, board_id, user_id),
    CHECK (delete_at >= 0)
);

CREATE TABLE subscriptions (
    block_type TEXT NOT NULL,
    block_id TEXT NOT NULL,
    subscriber_type TEXT NOT NULL,
    subscriber_id TEXT NOT NULL,
    notify_frequency TEXT,
    create_at BIGINT NOT NULL,
    publish_at BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (block_type, block_id, subscriber_type, subscriber_id),
    CONSTRAINT fk_subscriptions_user FOREIGN KEY (subscriber_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (subscriber_type = 'user'),
    CHECK (publish_at >= 0)
);

CREATE TABLE notification_hints (
    block_type TEXT NOT NULL,
    block_id TEXT NOT NULL,
    create_at BIGINT NOT NULL,
    modify_at BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (block_type, block_id),
    CHECK (modify_at >= 0)
);

CREATE TABLE sharing (
    id TEXT PRIMARY KEY,
    enabled BOOLEAN NOT NULL DEFAULT FALSE,
    token TEXT NOT NULL UNIQUE,
    modified_by TEXT,
    update_at BIGINT NOT NULL,
    create_at BIGINT NOT NULL,
    CONSTRAINT fk_sharing_board FOREIGN KEY (id) REFERENCES boards(id) ON DELETE CASCADE,
    CONSTRAINT fk_sharing_modified_by FOREIGN KEY (modified_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE file_info (
    id TEXT PRIMARY KEY,
    creator_id TEXT,
    board_id TEXT,
    create_at BIGINT NOT NULL,
    update_at BIGINT NOT NULL,
    delete_at BIGINT NOT NULL DEFAULT 0,
    path TEXT,
    name TEXT,
    extension TEXT,
    size BIGINT,
    mime_type TEXT,
    has_preview_image BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_file_info_creator FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_file_info_board FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE SET NULL,
    CHECK (delete_at >= 0),
    CHECK (size IS NULL OR size >= 0)
);

CREATE TABLE preferences (
    user_id TEXT NOT NULL,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    value TEXT,
    PRIMARY KEY (user_id, category, name),
    CONSTRAINT fk_preferences_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (length(trim(category)) > 0),
    CHECK (length(trim(name)) > 0)
);

CREATE INDEX ix_users_delete_at ON users (delete_at);
CREATE INDEX ix_users_email_delete_at ON users (email, delete_at);
CREATE INDEX ix_sessions_user_id ON sessions (user_id);
CREATE INDEX ix_sessions_expire_at ON sessions (expire_at);
CREATE INDEX ix_teams_delete_at ON teams (delete_at);
CREATE INDEX ix_team_members_user_id_delete_at ON team_members (user_id, delete_at);
CREATE INDEX ix_boards_team_id_delete_at ON boards (team_id, delete_at);
CREATE INDEX ix_boards_created_by ON boards (created_by);
CREATE INDEX ix_boards_type_delete_at ON boards (type, delete_at);
CREATE INDEX ix_board_members_user_id_delete_at ON board_members (user_id, delete_at);
CREATE INDEX ix_blocks_board_id_delete_at ON blocks (board_id, delete_at);
CREATE INDEX ix_blocks_root_id ON blocks (root_id);
CREATE INDEX ix_blocks_parent_id ON blocks (parent_id);
CREATE INDEX ix_blocks_type_board_delete_at ON blocks (type, board_id, delete_at);
CREATE INDEX ix_blocks_history_board_id_insert_at ON blocks_history (board_id, insert_at);
CREATE INDEX ix_blocks_history_delete_at ON blocks_history (delete_at);
CREATE INDEX ix_categories_user_team_delete_at ON categories (user_id, team_id, delete_at);
CREATE INDEX ix_category_boards_board_id_delete_at ON category_boards (board_id, delete_at);
CREATE INDEX ix_category_boards_category_sort ON category_boards (category_id, sort_order);
CREATE INDEX ix_subscriptions_subscriber_id ON subscriptions (subscriber_id);
CREATE INDEX ix_subscriptions_block ON subscriptions (block_id, block_type);
CREATE INDEX ix_notification_hints_modify_at ON notification_hints (modify_at);
CREATE INDEX ix_sharing_enabled ON sharing (enabled);
CREATE INDEX ix_file_info_board_id_delete_at ON file_info (board_id, delete_at);
CREATE INDEX ix_file_info_creator_id ON file_info (creator_id);
CREATE INDEX ix_preferences_user_category ON preferences (user_id, category);
```

## Relacionamentos

| Origem | Destino | Cardinalidade | Integridade |
|---|---|---|---|
| `sessions.user_id` | `users.id` | N:1 | `ON DELETE CASCADE` |
| `team_members.team_id` | `teams.id` | N:1 | `ON DELETE CASCADE` |
| `team_members.user_id` | `users.id` | N:1 | `ON DELETE CASCADE` |
| `boards.team_id` | `teams.id` | N:1 | `ON DELETE RESTRICT` |
| `boards.created_by` | `users.id` | N:1 | `ON DELETE SET NULL` |
| `boards.modified_by` | `users.id` | N:1 | `ON DELETE SET NULL` |
| `board_members.board_id` | `boards.id` | N:1 | `ON DELETE CASCADE` |
| `board_members.user_id` | `users.id` | N:1 | `ON DELETE CASCADE` |
| `blocks.parent_id` | `blocks.id` | N:1 recursivo | `ON DELETE SET NULL` |
| `blocks.root_id` | `blocks.id` | N:1 recursivo | `ON DELETE SET NULL` |
| `blocks.board_id` | `boards.id` | N:1 | `ON DELETE CASCADE` |
| `blocks.created_by` | `users.id` | N:1 | `ON DELETE SET NULL` |
| `blocks.modified_by` | `users.id` | N:1 | `ON DELETE SET NULL` |
| `blocks_history.board_id` | `boards.id` | N:1 | `ON DELETE CASCADE` |
| `categories.user_id` | `users.id` | N:1 | `ON DELETE CASCADE` |
| `categories.team_id` | `teams.id` | N:1 | `ON DELETE CASCADE` |
| `category_boards.category_id` | `categories.id` | N:1 | `ON DELETE CASCADE` |
| `category_boards.board_id` | `boards.id` | N:1 | `ON DELETE CASCADE` |
| `category_boards.user_id` | `users.id` | N:1 | `ON DELETE CASCADE` |
| `category_boards.team_id` | `teams.id` | N:1 | `ON DELETE CASCADE` |
| `subscriptions.subscriber_id` | `users.id` | N:1 | `ON DELETE CASCADE` |
| `sharing.id` | `boards.id` | 1:1 | `ON DELETE CASCADE` |
| `sharing.modified_by` | `users.id` | N:1 | `ON DELETE SET NULL` |
| `file_info.creator_id` | `users.id` | N:1 | `ON DELETE SET NULL` |
| `file_info.board_id` | `boards.id` | N:1 | `ON DELETE SET NULL` |
| `preferences.user_id` | `users.id` | N:1 | `ON DELETE CASCADE` |

## Restrições e Constraints

- **Enums de negócio**:
  - `boards.type IN ('O', 'P')`
  - `boards.minimum_role IN ('', 'viewer', 'commenter', 'editor', 'admin')`
  - `categories.type IN ('system', 'custom')`
  - `subscriptions.subscriber_type = 'user'`
- **Unicidade**:
  - `users.username`, `users.email`, `sessions.token`, `sharing.token`
  - `category_boards (category_id, board_id, user_id)` para evitar vínculo duplicado
  - PKs compostas em memberships, subscriptions, notification_hints e preferences
- **Soft-delete**:
  - toda entidade mutável de negócio usa `delete_at BIGINT DEFAULT 0`
  - `blocks_history.delete_at > 0` garante que só snapshots deletados vão para histórico
- **Permissões / roles**:
  - `board_members` restringe no máximo um scheme flag ativo por linha
  - `team_members` impede combinações inválidas de guest/user/admin
- **Checks operacionais**:
  - timestamps não negativos
  - `template_version >= 0`
  - `size >= 0` em `file_info`
- **Índices críticos**:
  - consultas por ativos: `delete_at` em `users`, `teams`, `boards`, `blocks`, `categories`, `file_info`
  - acesso por board: `ix_blocks_board_id_delete_at`, `ix_board_members_user_id_delete_at`, `ix_category_boards_board_id_delete_at`
  - limpeza e auth: `ix_sessions_expire_at`, `ix_users_email_delete_at`
  - realtime e assinaturas: `ix_subscriptions_block`, `ix_notification_hints_modify_at`

## Considerações SQLAlchemy

- **Mapeamento tabela → model**:
  - `users` → `UserModel`
  - `sessions` → `SessionModel`
  - `preferences` → `PreferenceModel`
  - `teams` / `team_members` → `TeamModel`, `TeamMemberModel`
  - `boards` / `board_members` → `BoardModel`, `BoardMemberModel`
  - `blocks` / `blocks_history` → `BlockModel`, `BlockHistoryModel`
  - `categories` / `category_boards` → `CategoryModel`, `CategoryBoardModel`
  - `subscriptions` / `notification_hints` → `SubscriptionModel`, `NotificationHintModel`
  - `sharing` → `SharingModel`
  - `file_info` → `FileInfoModel`
- **Session management**:
  - uma `Session` SQLAlchemy por request HTTP, injetada via `Depends(get_db)`.
  - serviços coordenam transações multi-repositório; `DuplicateBoard` e `ArchiveBlock` usam `session.begin()` para atomicidade.
  - cleanup de sessões expiradas roda em tarefa periódica de `lifespan`, abrindo sua própria sessão transacional.
- **Filtros de soft-delete**:
  - repositórios expõem por padrão apenas registros com `delete_at = 0`.
  - consultas administrativas/restauração usam métodos explícitos `include_deleted=True`.
  - `blocks_history` nunca participa do filtro padrão de ativos; é consultada apenas em rotinas de restore/auditoria.
- **Compatibilidade PostgreSQL/SQLite**:
  - `JSON` é declarado no modelo SQLAlchemy; em PostgreSQL vira `JSONB` se desejado na implementação, mas o contrato lógico aqui permanece `JSON` para portabilidade.
  - IDs `TEXT` acomodam UUIDv4 gerado em Python sem depender de tipo `UUID` específico do PostgreSQL.
  - checks e índices foram mantidos no subconjunto suportado pelos dois bancos para evitar divergência de schema.

## Origem no Legado

| Tabela nova | Origem no legado | Transformação |
|---|---|---|
| `users` | `users` | 1-para-1; IDs passam a ser tratados como `TEXT` UUIDv4 |
| `sessions` | `sessions` | 1-para-1; cleanup periódico explícito no novo sistema |
| `preferences` | `preferences` | 1-para-1; onboarding 3-step formalizado |
| `teams` | `teams` | 1-para-1 |
| `team_members` | `team_members` | 1-para-1; `guest` fica semanticamente desativado |
| `boards` | `boards` | 1-para-1; constraints de `minimum_role` e `type` formalizadas |
| `board_members` | `board_members` | 1-para-1; exclusividade de role explicitada |
| `blocks` | `blocks` | 1-para-1; continua sendo supertipo polimórfico |
| `blocks_history` | `blocks_history` | 1-para-1 |
| `categories` | `categories` | 1-para-1 |
| `category_boards` | `category_boards` | 1-para-1; unicidade explícita |
| `subscriptions` | `subscriptions` | 1-para-1 |
| `notification_hints` | `notification_hints` | 1-para-1 |
| `sharing` | `sharing` | 1-para-1; `id` assume formalmente semântica de `board_id` |
| `file_info` | `file_info` | 1-para-1 |

## Notas
- `BoardView`, `FilterGroup`, `SortOption`, `CardOrder`, `Comment` e propriedades customizadas não ganham tabelas próprias no primeiro corte; ficam serializados em `blocks.fields` ou `boards.card_properties`, preservando a estrutura do legado e a flexibilidade do editor.
- O modelo de dados segue a estratégia Big Bang Controlado: uma migration inicial Alembic cria o schema completo, sem necessidade de tabelas temporárias de coexistência.
