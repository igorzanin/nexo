# Dependências do Projeto — nexo

> Stack: Python FastAPI + Vue 3 + Electron

---

## Backend (Python)

### Produção

| Pacote | Finalidade |
|--------|-----------|
| `fastapi` | Framework web |
| `uvicorn[standard]` | ASGI server |
| `sqlalchemy` | ORM |
| `alembic` | Migrations |
| `pydantic` | Validação de dados |
| `python-jose[cryptography]` | JWT |
| `passlib[bcrypt]` | Password hashing |
| `python-multipart` | File upload |
| `slowapi` | Rate limiting |
| `prometheus-client` | Métricas |
| `aiofiles` | Async file operations |
| `aiosqlite` | Async SQLite driver |
| `psycopg2-binary` | PostgreSQL driver |
| `pymysql` | MySQL driver |

### Desenvolvimento

| Pacote | Finalidade |
|--------|-----------|
| `pytest` | Testes |
| `httpx` | Testes (TestClient) |
| `pytest-asyncio` | Testes async |
| `coverage` | Cobertura |

---

## Frontend (npm)

### Produção

| Pacote | Finalidade |
|--------|-----------|
| `vue` | Framework |
| `vue-router` | Roteamento |
| `pinia` | Gerenciamento de estado |
| `bootstrap` | UI framework |
| `@popperjs/core` | Bootstrap JS |
| `axios` | HTTP client |
| `vuedraggable` | Drag-and-drop |
| `@fullcalendar/vue3` | Calendário |
| `@fullcalendar/daygrid` | Calendário grid |
| `@fullcalendar/interaction` | Calendário interativo |
| `vue-i18n` | Internacionalização |
| `nanoevents` | Pub/sub (flash messages) |
| `uuid` | UUID generation |

### Desenvolvimento

| Pacote | Finalidade |
|--------|-----------|
| `typescript` | Language |
| `vite` | Build |
| `vitest` | Testes |
| `@vue/test-utils` | Testes de componente |
| `sass` | SCSS (temas Bootstrap) |

---

## Desktop (npm)

| Pacote | Finalidade |
|--------|-----------|
| `electron` | Framework desktop |
| `electron-builder` | Build/packaging |

---

## Importadores (npm — mantidos TypeScript)

| Pacote | Finalidade |
|--------|-----------|
| `minimist` | CLI argument parsing |
| `xml2js` | XML parsing (Jira) |
| `turndown` | HTML→Markdown (Jira) |
| `csv-parse` | CSV parsing (Notion) |
| `readline-sync` | Input interativo (Nextcloud) |
