---
schemaVersion: 1
generatedAt: 2026-05-24T17:45:00-03:00
reversa:
  version: "1.0.0"
kind: target_domain_model
producedBy: designer
hash: "sha256:designer-target_domain_model-nexo"
---

# Target Domain Model

## Aggregates

### AGG-Board
- **Aggregate root**: `Board`
- **Entidades**: `BoardMember`
- **Value objects**: `MinimumRole` (`"" | "viewer" | "commenter" | "editor" | "admin"`), `BoardType` (`"O" | "P"`)
- **Invariantes**:
  - `teamId` e `type` são obrigatórios e `type` deve ser válido (`BR-MIGRAR-001`; `domain.md` R1).
  - `Board.type` é imutável após criação; apenas fluxo autorizado pode alterá-lo (`BR-MIGRAR-001`; R2).
  - `minimumRole` deve estar no enum permitido e atua como piso de permissão (`BR-MIGRAR-001`, `BR-MIGRAR-003`, `BR-MIGRAR-009`; R3, R26, P6).
  - convidados não criam boards; no sistema novo não existe role guest, apenas usuários registrados e acesso externo via readToken (`BR-MIGRAR-001`; `BR-HUMANA-005`).
  - último admin não pode ser removido nem rebaixado (`BR-MIGRAR-003`; R21, P5).
  - o servidor gera o ID; cliente nunca persiste board com ID arbitrário (`BR-MIGRAR-001`; R8).
  - duplicação de board deve ser transacional: se falhar cópia de arquivos, o board duplicado é revertido (`BR-MIGRAR-001`; R9).
- **Comandos do sistema**:
  - `CreateBoard`
  - `UpdateBoardMetadata`
  - `ChangeBoardType`
  - `ChangeMinimumRole`
  - `AddBoardMember`
  - `ChangeBoardMemberRole`
  - `RemoveBoardMember`
  - `DuplicateBoard`
  - `DeleteBoard`
  - `AddBoardToDefaultCategory`
- **Origem no legado**: `_reversa_sdd/domain.md` R1–R9, R21–R26; `_reversa_sdd/permissions.md` P1–P6.

### AGG-Block
- **Aggregate root**: `Block`
- **Subtipos lógicos**: `Card`, `BoardView`, `Comment`, `Text`, `Image`, `Divider`, `Attachment`
- **Entidades**: `BlockHistory`
- **Value objects**: `ContentOrder`, `FieldsJSON`, `BlockType`
- **Invariantes**:
  - `boardId` é obrigatório para qualquer bloco (`BR-MIGRAR-002`; R13, R20).
  - `title` tem no máximo 16383 runes e `fields` no máximo 800000 runes (`BR-MIGRAR-002`; R14, R15).
  - card precisa de `id`, `boardId`, `contentOrder`, `properties`, `createAt` e `updateAt` válidos (`BR-MIGRAR-002`; R10).
  - `icon` de card aceita no máximo 1 grafema (`BR-MIGRAR-002`; R11).
  - batch insert só aceita blocos do mesmo board (`BR-MIGRAR-002`; R12).
  - deletar bloco inexistente não é erro; restaurar bloco não deletado não é erro (`BR-MIGRAR-002`; R17, R18).
  - qualquer delete move o snapshot para `BlockHistory`; restore reidrata o bloco com `delete_at = 0` (`BR-MIGRAR-007`; R39, R40).
- **Comandos do sistema**:
  - `CreateCard`
  - `InsertBlocksBatch`
  - `UpdateBlockFields`
  - `ArchiveBlock`
  - `RestoreBlock`
  - `DeleteBlock`
  - `AttachFileToBlock`
  - `ReorderContent`
  - `RegisterUndoPatch`
  - `RegisterRedoPatch`
- **Origem no legado**: `_reversa_sdd/domain.md` R10–R20, R38–R40; `_reversa_sdd/migration/target_business_rules.md` BR-MIGRAR-012, BR-MIGRAR-018, BR-MIGRAR-019.

### AGG-User
- **Aggregate root**: `User`
- **Entidades**: `Session`, `TeamMember`, `Preference`
- **Value objects**: `PasswordHash`, `Email`
- **Invariantes**:
  - `username` e `email` são únicos por sistema.
  - senha em texto puro nunca é persistida; hash é `bcrypt` (`BR-MIGRAR-006`).
  - senha deve ter no mínimo 8 caracteres (`BR-MIGRAR-006`; R36).
  - sessão possui token único, expiração de access em 30 dias e refresh em 60 dias (`BR-MIGRAR-006`; R32–R34).
  - cleanup periódico remove sessões expiradas (`BR-HUMANA-002`).
  - preferências armazenam estado do onboarding de 3 etapas (`BR-MIGRAR-014`).
- **Comandos do sistema**:
  - `RegisterUser`
  - `LoginUser`
  - `RefreshSession`
  - `LogoutUser`
  - `CleanupExpiredSessions`
  - `UpdateUserPreference`
  - `CompleteOnboardingStep`
  - `AddUserToTeam`
- **Origem no legado**: `_reversa_sdd/domain.md` R32–R37; `_reversa_sdd/migration/target_business_rules.md` BR-MIGRAR-006, BR-MIGRAR-014, BR-HUMANA-002.

### AGG-Category
- **Aggregate root**: `Category`
- **Entidades**: `CategoryBoard`
- **Value objects**: `CategoryType` (`"system" | "custom"`)
- **Invariantes**:
  - `id`, `name`, `userId` e `teamId` são obrigatórios (`BR-MIGRAR-004`; R27).
  - `type` aceita apenas `system` ou `custom` (`BR-MIGRAR-004`; R28).
  - remoção é sempre via soft-delete (`BR-MIGRAR-004`; R29).
  - board não-template recém-criado entra na categoria padrão do usuário (`BR-MIGRAR-001`; R7).
- **Comandos do sistema**:
  - `CreateCategory`
  - `RenameCategory`
  - `SoftDeleteCategory`
  - `AttachBoardToCategory`
  - `DetachBoardFromCategory`
  - `ReorderCategoryBoards`
  - `EnsureDefaultCategory`
- **Origem no legado**: `_reversa_sdd/domain.md` R27–R29, R7.

### AGG-Sharing
- **Aggregate root**: `Sharing`
- **Value objects**: `ReadToken`
- **Invariantes**:
  - token é único, aleatório e não previsível (`BR-MIGRAR-013`).
  - compartilhamento público só funciona quando `enablePublicSharedBoards = true` (`BR-MIGRAR-013`; R35).
  - não existe role guest; acesso externo é exclusivamente por readToken (`BR-HUMANA-005`).
  - o fluxo precisa de cobertura automatizada de integração (`BR-HUMANA-001`).
- **Comandos do sistema**:
  - `EnableBoardSharing`
  - `DisableBoardSharing`
  - `RotateReadToken`
  - `ValidateReadToken`
  - `GetSharedBoard`
- **Origem no legado**: `_reversa_sdd/domain.md` glossário `ReadToken`; `_reversa_sdd/migration/target_business_rules.md` BR-MIGRAR-013, BR-HUMANA-001, BR-HUMANA-005.

### AGG-Subscription
- **Aggregate root**: `Subscription`
- **Entidades**: `NotificationHint`
- **Value objects**: `SubscriberType` (`"user"`)
- **Invariantes**:
  - `blockId`, `blockType`, `subscriberId` e `subscriberType` são obrigatórios (`BR-MIGRAR-005`; R30).
  - `subscriberType` deve ser sempre `user` (`BR-MIGRAR-005`; R31).
  - `BroadcastBlockChange` entrega atualização a membros do board e inscritos no bloco (`BR-MIGRAR-008`; R44).
  - broadcast WebSocket é síncrono no primeiro corte e deve ser monitorado (`BR-MIGRAR-022`).
- **Comandos do sistema**:
  - `SubscribeToBlock`
  - `UnsubscribeFromBlock`
  - `MarkNotificationHint`
  - `BroadcastBlockChange`
  - `BroadcastCommentChange`
- **Origem no legado**: `_reversa_sdd/domain.md` R30–R31, R41–R44; `_reversa_sdd/migration/target_business_rules.md` BR-MIGRAR-022.

## Entidades e Value Objects

| Nome | Tipo | Aggregate dono | Atributos principais | Validações / observações |
|---|---|---|---|---|
| User | Entidade | AGG-User | id, username, email, passwordHash, isBot, props | username/email únicos; `delete_at` soft-delete |
| Session | Entidade | AGG-User | id, token, userId, expireAt, lastActiveTime | token único; cleanup diário |
| Preference | Entidade | AGG-User | userId, category, name, value | onboarding fica aqui |
| TeamMember | Entidade | AGG-User | teamId, userId, roles, scheme flags | membership de time; guest desativado no novo sistema |
| Board | Entidade | AGG-Board | id, teamId, type, minimumRole, title, properties, cardProperties | type imutável; ID gerado pelo servidor |
| BoardMember | Entidade | AGG-Board | boardId, userId, roles, scheme flags | último admin protegido; flags mutuamente exclusivas |
| Category | Entidade | AGG-Category | id, name, userId, teamId, type | type `system|custom` |
| CategoryBoard | Entidade | AGG-Category | id, categoryId, boardId, sortOrder, hide | board entra na categoria padrão |
| Block | Entidade | AGG-Block | id, boardId, parentId, rootId, type, title, fields | raiz polimórfica |
| BlockHistory | Entidade | AGG-Block | id, boardId, type, title, fields, deleteAt, insertAt | snapshot para restore |
| FileInfo | Entidade | AGG-Block | id, creatorId, boardId, path, name, size, mimeType | anexo ligado ao conteúdo |
| Sharing | Entidade | AGG-Sharing | id, enabled, token, modifiedBy | `id` representa o board compartilhado |
| Subscription | Entidade | AGG-Subscription | blockType, blockId, subscriberType, subscriberId, notifyFrequency | `subscriberType = user` |
| NotificationHint | Entidade | AGG-Subscription | blockType, blockId, createAt, modifyAt | hint de publicação |
| MinimumRole | Value Object | AGG-Board | value | enum `""|viewer|commenter|editor|admin` |
| BoardType | Value Object | AGG-Board | value | enum `O|P` |
| ContentOrder | Value Object | AGG-Block | orderedBlockIds | ordem de conteúdo por card/view |
| FieldsJSON | Value Object | AGG-Block | payload JSON | schema varia por `BlockType` |
| BlockType | Value Object | AGG-Block | value | `card|view|comment|text|image|divider|attachment|...` |
| PasswordHash | Value Object | AGG-User | bcryptHash | nunca exposto em API |
| Email | Value Object | AGG-User | normalizedEmail | formato válido e normalizado |
| CategoryType | Value Object | AGG-Category | value | enum `system|custom` |
| ReadToken | Value Object | AGG-Sharing | token | string aleatória única |
| SubscriberType | Value Object | AGG-Subscription | value | enum único: `user` |

## Tabela: Regras de Domínio → Local no Sistema Novo

| Regra | Local no sistema novo | Observação de implementação |
|---|---|---|
| BR-MIGRAR-001 | `BoardService`, `BoardRepository`, `boards` router, `boards.store.ts` | criação/duplicação de board, type imutável, category default |
| BR-MIGRAR-002 | `BlockService`, schemas `blocks.py`, `content.store.ts` | validação de campos, batch insert, idempotência de delete/restore |
| BR-MIGRAR-003 | `PermissionService`, `BoardService`, `useHasPermissions.ts`, `BoardPermissionGate.vue` | último admin, hierarquia de papéis, minimumRole piso |
| BR-MIGRAR-004 | `CategoryService`, `CategoryRepository`, `categories.store.ts` | category type, soft-delete e organização pessoal |
| BR-MIGRAR-005 | `SubscriptionService`, `SubscriptionRepository`, `subscriptions.store.ts` | assinatura por bloco e tipo de assinante único |
| BR-MIGRAR-006 | `auth\jwt.py`, `auth\password.py`, `auth\dependencies.py`, `SessionService`, `auth.store.ts` | JWT, refresh, bcrypt, senha mínima, rate limiting |
| BR-MIGRAR-007 | `BlockHistoryService`, `BlockRepository`, `blocks_history`, `content.store.ts` | archive/restore e soft-delete |
| BR-MIGRAR-008 | `ws\server.py`, `sharing` router, `shared\ws\useWebSocket.ts` | AUTH action, subscribe por token e por team |
| BR-MIGRAR-009 | `PermissionService`, `useHasPermissions.ts` | matriz de 9 permissões e membership sintética |
| BR-MIGRAR-010 | `ViewService`, `features\views\*`, `views.store.ts` | 4 view types |
| BR-MIGRAR-011 | `ViewService`, tipos `FilterGroup`, componentes de filtros | árvore and/or com 15 condições |
| BR-MIGRAR-012 | `shared\api\useMutator.ts`, `patch-history.ts`, stores Pinia | undo/redo por diff |
| BR-MIGRAR-013 | `SharingService`, `sharing` router, `sharing.store.ts`, `SharedBoardPage.vue` | readToken e shared board |
| BR-MIGRAR-014 | `PreferenceRepository`, `PreferenceService`, `OnboardingTour.vue`, `preferences.store.ts` | 3 etapas persistidas em prefs |
| BR-MIGRAR-015 | `import\util\archive.ts` | `.boardarchive` NDJSON versionado |
| BR-MIGRAR-016 | `import\trello|jira|asana|todoist|notion|nextcloud-deck\` | importadores CLI TS mantidos |
| BR-MIGRAR-017 | `desktop\electron\server.ts`, `desktop\electron\main.ts` | subprocess FastAPI, porta aleatória, token single-user |
| BR-MIGRAR-018 | `ContentRegistry.vue`, `content.store.ts`, componentes de blocos | unificação de edição de conteúdo |
| BR-MIGRAR-019 | `Board.cardProperties`, `PropertyValueElement.vue`, `Block.fields` | 18 tipos de propriedade |
| BR-MIGRAR-020 | `main.py`, middleware de métricas | endpoint `/metrics` |
| BR-MIGRAR-021 | `auth` router + `slowapi` | 10 req/min por IP em login/register |
| BR-MIGRAR-022 | `WSConnectionManager.broadcast_*` | broadcast síncrono, validar carga |
| BR-MIGRAR-023 | middleware HTTP estruturado | request id, status, latency, user/board quando houver |
| BR-MIGRAR-024 | middleware de limite de payload | proteção DoS em body HTTP |
| BR-MIGRAR-025 | `PermissionService`, contratos de API | permissões só em nível de board |
| BR-HUMANA-001 | `tests\integration\test_sharing.py` | cobertura para token válido/inválido/feature flag |
| BR-HUMANA-002 | `main.py` lifespan + `SessionService.cleanup_expired()` | `asyncio.create_task` periódico |
| BR-HUMANA-003 | `import\nextcloud-deck\` | user/password e Bearer token |
| BR-HUMANA-004 | `features\content\components\markdown\` | library markdown Vue 3 a definir durante coding |
| BR-HUMANA-005 | `SharingService`, `PermissionService`, fluxos de auth | sem role guest; acesso externo só por readToken |

## Tabela: Rastreabilidade para Legado

| Elemento novo | Origem legado | Tipo de mapeamento |
|---|---|---|
| AGG-Board | `_reversa_sdd/domain.md` §Regras de Board + §Regras de Membro e Permissão | fundido |
| Board | `boards` do legado/Focalboard + backend parcial FastAPI | 1-para-1 |
| BoardMember | `board_members` + `permissions.md` | 1-para-1 |
| AGG-Block | `_reversa_sdd/domain.md` §Regras de Card e Block + §Soft-Delete | fundido |
| Card como subtipo de Block | Card do legado + Block base | fundido |
| BoardView como subtipo de Block | View block do legado | 1-para-1 conceitual |
| Comment como subtipo de Block | Comment block do legado | 1-para-1 conceitual |
| ContentRegistry | `blocksEditor` + `contentElement` | fundido |
| BlockHistory | `blocks_history` legado | 1-para-1 |
| FileInfo | arquivo/anexo do legado | 1-para-1 |
| AGG-User | `users`, `sessions`, `preferences`, `team_members` | fundido |
| Session | `sessions` legado | 1-para-1 |
| Preference | `preferences` legado | 1-para-1 |
| TeamMember | `team_members` legado | 1-para-1 |
| AGG-Category | `categories` + `category_boards` | fundido |
| AGG-Sharing | `sharing` + regra `ReadToken` | fundido |
| ReadToken access externo | share dialog do legado | 1-para-1 comportamental |
| AGG-Subscription | `subscriptions` + `notification_hints` + regras WS | fundido |
| PermissionService | regras dispersas em `permissions.md`, `domain.md` e `api/` | novo (serviço explícito) |
| useMutator | Mutator do legado React/Redux | 1-para-1 conceitual |
| useWebSocket | cliente WS legado | 1-para-1 conceitual |
| Importadores TypeScript | `_reversa_sdd/importadores/design.md` | 1-para-1 |
| Electron shell | `_reversa_sdd/desktop/design.md` | 1-para-1 |
| Logging/Metrics/Payload middleware | gaps documentados em `_reversa_sdd/gaps.md` | novo |

## Notas
- O modelo evita decomposição 1-para-1 por tabela: aggregates seguem invariantes, não artefatos físicos.
- Não há eventos de domínio explícitos porque o paradigma aprovado não é event-driven; realtime continua coordenado por services + WebSocket.
- `BoardView`, `Comment` e outros tipos especializados permanecem dentro de `AGG-Block` para preservar consistência de soft-delete, histórico e persistência polimórfica.
