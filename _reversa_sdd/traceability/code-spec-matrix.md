# Code/Spec Matrix — Rastreabilidade Spec → Implementação

## Nota

Esta matriz foi convertida de "Legado → SDD" para "Spec → Implementação".
As referências de código legado (Go/React) foram substituídas pela nova stack (Python/Vue 3).

---

## Backend Python

### Models (SQLAlchemy)

| Spec | Modelo Python | Status |
|------|--------------|--------|
| `modelo/requirements.md` | `nexo/models/board.py` | Pendente |
| `modelo/requirements.md` | `nexo/models/block.py` | Pendente |
| `modelo/requirements.md` | `nexo/models/card.py` | Pendente |
| `modelo/requirements.md` | `nexo/models/user.py` | Pendente |
| `modelo/requirements.md` | `nexo/models/team.py` | Pendente |
| `modelo/requirements.md` | `nexo/models/category.py` | Pendente |
| `modelo/requirements.md` | `nexo/models/session.py` | Pendente |
| `modelo/requirements.md` | `nexo/models/subscription.py` | Pendente |
| `modelo/requirements.md` | `nexo/models/sharing.py` | Pendente |

### Routers (FastAPI)

| Spec | Router Python | Status |
|------|--------------|--------|
| `api/requirements.md` | `nexo/routers/auth.py` | Pendente |
| `api/requirements.md` | `nexo/routers/boards.py` | Pendente |
| `api/requirements.md` | `nexo/routers/blocks.py` | Pendente |
| `api/requirements.md` | `nexo/routers/cards.py` | Pendente |
| `api/requirements.md` | `nexo/routers/categories.py` | Pendente |
| `api/requirements.md` | `nexo/routers/files.py` | Pendente |
| `api/requirements.md` | `nexo/routers/members.py` | Pendente |
| `api/requirements.md` | `nexo/routers/admin.py` | Pendente |

### Services

| Spec | Service Python | Status |
|------|---------------|--------|
| `aplicacao/requirements.md` | `nexo/services/board.py` | Pendente |
| `aplicacao/requirements.md` | `nexo/services/block.py` | Pendente |
| `aplicacao/requirements.md` | `nexo/services/card.py` | Pendente |
| `aplicacao/requirements.md` | `nexo/services/permission.py` | Pendente |
| `aplicacao/requirements.md` | `nexo/services/category.py` | Pendente |
| `aplicacao/requirements.md` | `nexo/services/file.py` | Pendente |

### Auth

| Spec | Auth Python | Status |
|------|------------|--------|
| `auth/requirements.md` | `nexo/auth/jwt.py` | Pendente |
| `auth/requirements.md` | `nexo/auth/password.py` | Pendente |
| `auth/requirements.md` | `nexo/auth/dependencies.py` | Pendente |

### WebSocket

| Spec | WS Python | Status |
|------|----------|--------|
| `ws/requirements.md` | `nexo/ws/server.py` | Pendente |

---

## Frontend Vue 3

| Spec | Componente | Status |
|------|-----------|--------|
| `blocos/requirements.md` | `webapp/src/types/*.ts` | Pendente |
| `store/requirements.md` | `webapp/src/stores/*.ts` | Pendente |
| `componentes/requirements.md` | `webapp/src/components/**/*.vue` | Pendente |
| `paginas/requirements.md` | `webapp/src/pages/*.vue` | Pendente |

---

## Desktop Electron

| Spec | Código | Status |
|------|--------|--------|
| `desktop/requirements.md` | `desktop/electron/main.ts` | Pendente |

---

## Importadores (TypeScript)

| Spec | Código | Status |
|------|--------|--------|
| `importadores/requirements.md` | `import/*/` | Mantido (apenas rename) |
