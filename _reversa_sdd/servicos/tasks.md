# Repositories, Tarefas de Implementação

## Pré-requisitos
- [ ] Modelos SQLAlchemy implementados
- [ ] Conexão com banco configurada (SQLite dev, PostgreSQL prod)

## Tarefas

- [ ] T-01, Configurar SQLAlchemy engine, SessionLocal, Base declarativa
  - Fonte legado: `server/services/store/sqlstore/store.go`
  - Critério: Engine configurada com pool, suporte a SQLite/PostgreSQL/MySQL

- [ ] T-02, Implementar BoardRepository com CRUD + soft-delete
  - Fonte legado: `server/services/store/sqlstore/board.go`
  - Critério: get, create, patch, soft_delete, get_by_team, get_board_count

- [ ] T-03, Implementar BlockRepository com CRUD + batch insert + undelete
  - Fonte legado: `server/services/store/sqlstore/blocks.go`
  - Critério: get_blocks_for_board, patch, delete, undelete, batch_create atômico

- [ ] T-04, Implementar UserRepository, SessionRepository, TeamRepository
  - Fonte legado: `server/services/store/sqlstore/user.go`, `session.go`
  - Critério: CRUD completo + busca por username/email

- [ ] T-05, Implementar CategoryRepository com reorder
  - Fonte legado: `server/services/store/sqlstore/category.go`
  - Critério: CRUD + reorder_categories, reorder_category_boards

- [ ] T-06, Configurar Alembic com migration inicial
  - Fonte legado: migrations SQL
  - Critério: `alembic upgrade head` cria schema completo

- [ ] T-07, Implementar FileService (local filesystem)
  - Fonte legado: `server/services/files/files.go`
  - Critério: store_file, read_file, remove_file

- [ ] T-08, Implementar PermissionsService RBAC
  - Fonte legado: `server/services/permissions/`
  - Critério: has_permission_to_team, has_permission_to_board

- [ ] T-09, Implementar NotificationService (subscriptions)
  - Fonte legado: `server/services/notifications/`
  - Critério: notificar usuário inscrito em block changes

## Lacunas
- S3 backend removido por decisão (apenas filesystem local)
