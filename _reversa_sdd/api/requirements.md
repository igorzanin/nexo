# API — FastAPI Routers

## Visão Geral
Camada de routers FastAPI que expõe a lógica de negócio do Nexo via API REST. Responsável por rotear requisições, validar autenticação JWT, delegar à camada de serviços e serializar respostas Pydantic.

## Responsabilidades
- Roteamento de todas as rotas REST (`/api/v1/*`)
- Autenticação de requisições via JWT Bearer token
- CRUD de boards, blocks/cards, categorias, membros, equipes
- Upload e download de arquivos
- Gerenciamento de inscrições de notificação
- Endpoints administrativos (config, métricas)
- Rate limiting em endpoints sensíveis

## Stack

| Componente | Tecnologia |
|------------|-----------|
| Framework | FastAPI |
| Validação | Pydantic v2 |
| Auth | JWT (python-jose) |
| Rate limiting | slowapi / fastapi-limiter |
| File upload | python-multipart |

## Regras de Negócio
- Toda rota (exceto login/register) exige JWT válido 🟢
- Block deve pertencer ao board da rota em toda operação CRUD 🟢
- Convidados não podem criar boards 🟢
- Último admin de um board não pode ser removido nem rebaixado 🟢
- Rate limiting: N requisições/minuto para login/register 🟢
- ReadHeaderTimeout configurado no servidor ASGI 🟢

## Rotas Principais

| Método | Caminho | Handler | Auth |
|--------|---------|---------|------|
| POST | `/api/v1/login` | `auth.login` | Não |
| POST | `/api/v1/register` | `auth.register` | Não |
| GET | `/api/v1/teams` | `teams.list` | JWT |
| POST | `/api/v1/boards` | `boards.create` | JWT |
| GET | `/api/v1/boards/{board_id}` | `boards.get` | JWT |
| PATCH | `/api/v1/boards/{board_id}` | `boards.patch` | JWT |
| DELETE | `/api/v1/boards/{board_id}` | `boards.delete` | JWT |
| POST | `/api/v1/boards/{board_id}/duplicate` | `boards.duplicate` | JWT |
| GET | `/api/v1/boards/{board_id}/blocks` | `blocks.list` | JWT |
| POST | `/api/v1/boards/{board_id}/blocks` | `blocks.create` | JWT |
| POST | `/api/v1/files/{team_id}/{board_id}` | `files.upload` | JWT |
| GET | `/api/v1/files/{team_id}/{board_id}/{file_id}` | `files.download` | JWT |
| GET | `/api/v1/admin/config` | `admin.get_config` | JWT+Admin |
| GET | `/metrics` | `metrics.endpoint` | - |

## Rastreabilidade

| Handler | Fonte legado | Confiança |
|---------|-------------|-----------|
| Auth handlers | `server/api/auth.go` | 🟢 |
| Boards CRUD | `server/api/boards.go` | 🟢 |
| Blocks CRUD | `server/api/blocks.go` | 🟢 |
| Cards CRUD | `server/api/cards.go` | 🟢 |
| Categories CRUD | `server/api/categories.go` | 🟢 |
| Members CRUD | `server/api/members.go` | 🟢 |
| Files upload/download | `server/api/files.go` | 🟢 |
| Admin endpoints | `server/api/admin.go` | 🟢 |
