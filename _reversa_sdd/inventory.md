# Inventário do Projeto — nexo

> Stack: Python FastAPI + Vue 3 + Electron

---

## Descrição

Nexo é um workspace moderno auto-hospedado para organização de projetos, gerenciamento de tarefas e colaboração em equipe.

---

## Estrutura de Diretórios (nova stack)

### Raiz
- `pyproject.toml` — Configuração do projeto Python
- `uv.lock` — Lock de dependências Python
- `docker-compose.yml` — Deploy containerizado

### `nexo/` — Backend Python

```
nexo/
├── main.py                 # FastAPI app + uvicorn entry point
├── settings.py             # Pydantic Settings
├── database.py             # SQLAlchemy engine + session
├── models/                 # SQLAlchemy ORM models
│   ├── board.py
│   ├── block.py
│   ├── card.py
│   ├── user.py
│   ├── team.py
│   ├── session.py
│   ├── category.py
│   ├── subscription.py
│   └── sharing.py
├── schemas/                # Pydantic schemas
│   ├── board.py
│   ├── block.py
│   ├── auth.py
│   └── ...
├── repositories/           # SQLAlchemy repositories
│   ├── board.py
│   ├── block.py
│   ├── user.py
│   └── ...
├── services/               # Business logic layer
│   ├── board.py
│   ├── block.py
│   ├── permission.py
│   ├── file.py
│   └── ...
├── routers/                # FastAPI routers
│   ├── auth.py
│   ├── boards.py
│   ├── blocks.py
│   ├── cards.py
│   └── ...
├── auth/                   # JWT auth
│   ├── jwt.py
│   ├── password.py
│   └── dependencies.py
├── ws/                     # WebSocket
│   ├── server.py
│   └── models.py
└── tests/                  # Testes
    ├── conftest.py
    ├── test_auth.py
    └── ...
```

### `migrations/` — Alembic migrations

### `webapp/` — Frontend Vue 3

```
webapp/
├── package.json
├── vite.config.ts
├── tsconfig.json
├── index.html
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── router/
│   │   └── index.ts
│   ├── stores/
│   │   ├── boardStore.ts
│   │   ├── cardStore.ts
│   │   └── ...
│   ├── types/
│   │   ├── block.ts
│   │   ├── board.ts
│   │   └── ...
│   ├── components/
│   │   ├── workspace/
│   │   ├── kanban/
│   │   ├── table/
│   │   ├── calendar/
│   │   └── ...
│   ├── composables/
│   │   ├── useMutator.ts
│   │   ├── useWebSocket.ts
│   │   └── ...
│   └── pages/
│       ├── LoginPage.vue
│       ├── BoardPage.vue
│       └── ...
```

### `desktop/` — Electron app

```
desktop/
├── package.json
├── electron-builder.yml
├── electron/
│   ├── main.ts
│   ├── preload.ts
│   └── server.ts
```

### `import/` — Importadores CLI (mantidos TypeScript)

```
import/
├── archive.ts         # ArchiveUtils compartilhado
├── trello/
├── jira/
├── asana/
├── todoist/
├── notion/
└── nextcloud-deck/
```

---

## Estatísticas (projetadas)

| Camada | Arquivos | Linguagem |
|--------|----------|-----------|
| Backend | ~80 | Python 3.12+ |
| Frontend | ~200 | TypeScript + Vue 3 |
| Desktop | ~5 | TypeScript + Electron |
| Importadores | ~60 | TypeScript (mantidos) |
| **Total** | **~345** | |
