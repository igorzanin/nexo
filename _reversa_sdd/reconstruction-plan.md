# Reconstruction Plan — nexo

**Stack:** Python FastAPI + Vue 3 + TypeScript + Electron
**Fonte:** original
**Gerado em:** 2026-05-13
**Status:** 22 tarefas | 22 concluídas | 0 pendentes

---

## Alertas de pré-voo

> Revise estes pontos antes de iniciar. Gaps marcados com ⚠️ bloqueiam a tarefa associada.

- ⚠️ **IsValidReadToken test comentado** — bloqueia Tarefa 04 (Auth)
- ⚠️ **CleanUpSessions sem scheduler** — bloqueia Tarefa 04 (Auth)
- ⚠️ **Nextcloud Deck sem autenticação por token** — bloqueia Tarefa 18 (Importador Nextcloud Deck)
- ⚠️ **live-markdown-plugin subsistema frágil** — bloqueia Tarefa 11 (Componentes)

---

## Tarefas

### Tarefa 01 — Schema do Banco de Dados
**Status:** done
**Lê:** `_reversa_sdd/erd-complete.md`, `_reversa_sdd/data-dictionary.md`
**Constrói:** migrations, schema SQLAlchemy
**Pronto quando:** Todas as tabelas do ERD existem com tipos, constraints e foreign keys corretos

---

### Tarefa 02 — Entidades de Domínio (Models)
**Status:** done
**Lê:** `_reversa_sdd/domain.md`, `_reversa_sdd/modelo/requirements.md`, `_reversa_sdd/modelo/design.md`, `_reversa_sdd/modelo/tasks.md`
**Constrói:** SQLAlchemy models (Board, Block, Card, User, Team, Category, Session, Subscription, Sharing)
**Pronto quando:** Todos os modelos ORM implementados com campos, relacionamentos e constraints

---

### Tarefa 03 — Máquinas de Estado
**Status:** done
**Lê:** `_reversa_sdd/state-machines.md`
**Constrói:** implementação dos fluxos de estado
**Pronto quando:** Todos os estados e transições documentados estão implementados

---

### Tarefa 04 — Auth
**Status:** done
**Lê:** `_reversa_sdd/auth/requirements.md`, `_reversa_sdd/auth/design.md`, `_reversa_sdd/auth/tasks.md`, `_reversa_sdd/permissions.md`
**Constrói:** JWT, password hashing, auth dependencies, permissões
**Pronto quando:** Registro, login, refresh token, logout, read token e permissões implementados
**Alerta:** ⚠️ IsValidReadToken test comentado | ⚠️ CleanUpSessions sem scheduler

---

### Tarefa 05 — Serviços (servicos/)
**Status:** done
**Lê:** `_reversa_sdd/servicos/requirements.md`, `_reversa_sdd/servicos/design.md`, `_reversa_sdd/servicos/tasks.md`
**Constrói:** lógica de negócio (boards, blocks, cards)
**Pronto quando:** Operações CRUD e regras de negócio implementadas

---

### Tarefa 06 — Aplicação (aplicacao/)
**Status:** done
**Lê:** `_reversa_sdd/aplicacao/requirements.md`, `_reversa_sdd/aplicacao/design.md`, `_reversa_sdd/aplicacao/tasks.md`
**Constrói:** services de board, block, card, permission, category, file
**Pronto quando:** Todos os services implementados conforme specs

---

### Tarefa 07 — WebSocket
**Status:** done
**Lê:** `_reversa_sdd/ws/requirements.md`, `_reversa_sdd/ws/design.md`, `_reversa_sdd/ws/tasks.md`
**Constrói:** servidor WebSocket, broadcast de mudanças
**Pronto quando:** Conexão, autenticação e broadcast implementados

---

### Tarefa 08 — API / Routers
**Status:** done
**Lê:** `_reversa_sdd/api/requirements.md`, `_reversa_sdd/api/design.md`, `_reversa_sdd/api/tasks.md`, `_reversa_sdd/openapi/api.yaml`
**Constrói:** endpoints FastAPI (auth, boards, blocks, cards, categories, files, members, admin)
**Pronto quando:** Todos os endpoints REST implementados conforme OpenAPI

---

### Tarefa 09 — Frontend Types (blocos/)
**Status:** done
**Lê:** `_reversa_sdd/blocos/requirements.md`, `_reversa_sdd/blocos/design.md`, `_reversa_sdd/blocos/tasks.md`
**Constrói:** modelos TypeScript (Block, Board, Card, BoardView, etc.)
**Pronto quando:** Todos os tipos e interfaces implementados

---

### Tarefa 10 — Pinia Stores
**Status:** done
**Lê:** `_reversa_sdd/store/requirements.md`, `_reversa_sdd/store/design.md`, `_reversa_sdd/store/tasks.md`
**Constrói:** 16 stores Pinia (boards, cards, views, users, teams, comments, etc.)
**Pronto quando:** Todas as stores implementadas com actions e getters

---

### Tarefa 11 — Componentes Vue
**Status:** done
**Lê:** `_reversa_sdd/componentes/requirements.md`, `_reversa_sdd/componentes/design.md`, `_reversa_sdd/componentes/tasks.md`
**Constrói:** componentes Vue (Workspace, CenterPanel, Kanban/Table/Gallery/Calendar, CardDialog, Sidebar, etc.)
**Pronto quando:** Todos os componentes renderizam conforme especificado
**Alerta:** ⚠️ live-markdown-plugin subsistema frágil

---

### Tarefa 12 — Páginas
**Status:** done
**Lê:** `_reversa_sdd/paginas/requirements.md`, `_reversa_sdd/paginas/design.md`, `_reversa_sdd/paginas/tasks.md`
**Constrói:** BoardPage, LoginPage, RegisterPage, ChangePasswordPage, ErrorPage
**Pronto quando:** Todas as páginas navegáveis com integração de stores e componentes

---

### Tarefa 13 — Web App Shell
**Status:** done
**Lê:** `_reversa_sdd/web/requirements.md`, `_reversa_sdd/web/design.md`, `_reversa_sdd/web/tasks.md`
**Constrói:** app shell Vue 3, router, Bootstrap setup, i18n
**Pronto quando:** App inicializa com roteamento, tema e internacionalização

---

### Tarefa 14 — Desktop Electron
**Status:** done
**Lê:** `_reversa_sdd/desktop/requirements.md`, `_reversa_sdd/desktop/design.md`, `_reversa_sdd/desktop/tasks.md`
**Constrói:** Electron main process, subprocess Python, janela nativa
**Pronto quando:** App desktop inicia com servidor embutido

---

### Tarefa 15 — Importadores (framework)
**Status:** done

---

### Tarefa 16 — Importador Asana
**Status:** done

---

### Tarefa 17 — Importador Jira
**Status:** done

---

### Tarefa 18 — Importador Nextcloud Deck
**Status:** done

---

### Tarefa 19 — Importador Notion
**Status:** done

---

### Tarefa 20 — Importador Todoist
**Status:** done

---

### Tarefa 21 — Importador Trello
**Status:** done

---

### Tarefa 22 — Fluxos de Usuário (Integração E2E)
**Status:** done
**Lê:** `_reversa_sdd/user-stories/fluxos-principais.md`
**Constrói:** testes de integração e2e, fluxos completos
**Pronto quando:** Todos os critérios de aceitação das user stories estão satisfeitos
