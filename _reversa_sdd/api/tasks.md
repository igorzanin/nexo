# API, Tarefas de Implementação

## Pré-requisitos
- [ ] Modelos SQLAlchemy implementados
- [ ] Repositories implementados
- [ ] Services layer implementada

## Tarefas

- [ ] T-01, Criar FastAPI app com configuração inicial
  - Critério: app criado com middlewares (CORS, rate limit, trust host)

- [ ] T-02, Implementar auth router (login, register, logout, change_password)
  - Fonte legado: `server/api/auth.go`
  - Critério: JWT emitido no login; refresh token; rate limiting ativo

- [ ] T-03, Implementar boards router (CRUD + duplicate)
  - Fonte legado: `server/api/boards.go`
  - Critério: CRUD completo com validação de permissões

- [ ] T-04, Implementar blocks router (CRUD + batch)
  - Fonte legado: `server/api/blocks.go`
  - Critério: CRUD + batch insert; block pertence ao board

- [ ] T-05, Implementar cards router (CRUD)
  - Fonte legado: `server/api/cards.go`

- [ ] T-06, Implementar categories router (CRUD + reorder)
  - Fonte legado: `server/api/categories.go`

- [ ] T-07, Implementar members router (CRUD + proteção último admin)
  - Fonte legado: `server/api/members.go`

- [ ] T-08, Implementar files router (upload/download)
  - Fonte legado: `server/api/files.go`
  - Critério: Limite 100KB; armazenamento local

- [ ] T-09, Implementar admin router (config)
  - Fonte legado: `server/api/admin.go`

- [ ] T-10, Implementar subscriptions router
  - Fonte legado: `server/api/subscriptions.go`

- [ ] T-11, Implementar sharing router
  - Fonte legado: `server/api/sharing.go`

- [ ] T-12, Implementar rate limiting + ReadHeaderTimeout
  - Decisão do revisor
  - Critério: login/register limitados; timeout configurado no uvicorn

## Lacunas
- Rate limiting: implementado (decisão do revisor)
- ReadHeaderTimeout: implementado (decisão do revisor)
