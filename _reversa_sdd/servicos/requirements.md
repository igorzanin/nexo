# Repositories e Serviços de Infraestrutura

## Visão Geral
Camada de repositórios SQLAlchemy e serviços de infraestrutura (arquivos, permissões, notificações). Implementa o padrão Repository para encapsular consultas SQL complexas e serviços auxiliares.

## Responsabilidades
- Repositórios CRUD para todas as entidades (Board, Block, Card, User, Team, etc.)
- Migrações de schema via Alembic (SQLite, PostgreSQL, MySQL)
- Serviço de arquivos (upload/download, armazenamento local)
- Serviço de permissões RBAC (verificação por equipe, board)
- Serviço de notificações via subscriptions
- Serviço de limites cloud (removido por decisão)

## Stack

| Componente | Tecnologia |
|------------|-----------|
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Database | SQLite / PostgreSQL / MySQL |
| File storage | Local filesystem |
| Cache | (opcional, a definir) |
| Background tasks | FastAPI BackgroundTasks / Celery (opcional) |

## Regras de Negócio
- Repositórios seguem padrão interface + implementação SQLAlchemy 🟢
- Migrações têm controle de versão (up/down) via Alembic 🟢
- Permissões seguem modelo hierárquico: Team → Board 🟢
- Arquivos armazenados localmente (filesystem) 🟢
- Rate limiting implementado para endpoints sensíveis 🟢

## Rastreabilidade

| Componente | Fonte legado | Confiança |
|-----------|-------------|-----------|
| BoardRepository | `server/services/store/sqlstore/board.go` | 🟢 |
| BlockRepository | `server/services/store/sqlstore/blocks.go` | 🟢 |
| UserRepository | `server/services/store/sqlstore/user.go` | 🟢 |
| SessionRepository | `server/services/store/sqlstore/session.go` | 🟢 |
| CategoryRepository | `server/services/store/sqlstore/category.go` | 🟢 |
| FileService | `server/services/files/files.go` | 🟢 |
| PermissionsService | `server/services/permissions/` | 🟢 |
| NotificationService | `server/services/notifications/` | 🟢 |
