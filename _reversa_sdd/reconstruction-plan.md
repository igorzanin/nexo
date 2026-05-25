# Reconstruction Plan — nexo

**Fonte:** migração
**Paradigma alvo:** OO com DI (backend) + Reativo + Composição (frontend)
**Topologia:** Híbrido — backend package-by-layer / frontend package-by-feature
**Stack:** FastAPI + Python 3.12 + SQLAlchemy + Alembic | Vue 3 + TypeScript + Pinia + Bootstrap 5.3 | Electron | Node.js TypeScript
**Estratégia:** Big Bang Controlado
**Gerado em:** 2026-05-24
**Status:** 20 tarefas | 18 concluídas | 2 pendentes

---

## Alertas de pré-voo

> Revise antes de iniciar. Itens REFERIDOS À CODIFICAÇÃO em `_reversa_sdd/migration/ambiguity_log.md` associados a tarefas específicas.

- ⚠️ **REF-001** — Flags `R25 scheme` mutuamente exclusivos (isPublic / isTemplate / isChannel / isGuest) sem validação. Afeta **Tarefa 06** (BC-Boards Backend). Adicionar validação de exclusividade em `MemberService` ou no schema Pydantic de Board.
- ⚠️ **REF-002** — Broadcast WebSocket síncrono pode bloquear event loop sob carga. Afeta **Tarefa 09** (BC-Collaboration Backend). Monitorar latência; migrar para `BackgroundTasks` ou `asyncio.gather` se necessário.
- ⚠️ **REF-003** — Logging estruturado ausente no legado; adicionar middleware FastAPI com campos padronizados. Afeta **Tarefa 10** (Transversal Backend).
- ⚠️ **REF-004** — Limite de payload não configurado no legado; implementar `ContentSizeLimit` middleware. Afeta **Tarefa 10** (Transversal Backend).
- ⚠️ **REF-005** — `ReadHeaderTimeout` no legado acoplado ao servidor Go; na stack nova exige nginx como proxy reverso obrigatório. Afeta **Tarefa 10** (Transversal Backend). Documentar nginx como pré-requisito de produção.
- ⚠️ **REF-006** — Bootstrap importado via CDN *e* npm no webapp legado; remover CDN, manter apenas import npm. Afeta **Tarefa 11** (Shared Frontend).

---

## Tarefas

### Tarefa 01 — Setup do Projeto Novo
**Status:** done
**Lê:** `_reversa_sdd/migration/topology_decision.md`, `_reversa_sdd/migration/paradigm_decision.md`
**Constrói:** estrutura de pastas do monorepo (`nexo/` FastAPI app, `webapp/` Vue 3, `desktop/` Electron, `import/` CLI), `pyproject.toml`, `package.json` raiz, `.env.example`, `docker-compose.yml`, CI skeleton (`.github/workflows/`)
**Pronto quando:** `python -m nexo` e `npm run dev` sobem sem erro; estrutura de pastas bate com topologia Híbrida aprovada

---

### Tarefa 02 — Schema do Banco Alvo + SQLAlchemy Models
**Status:** done
**Lê:** `_reversa_sdd/migration/target_data_model.md`
**Constrói:** `nexo/models/*.py` (declarative_base + todas as entidades), `alembic/`, migration inicial `001_initial_schema.py`
**Pronto quando:** `alembic upgrade head` cria todas as tabelas com tipos, constraints, índices e relações conforme ERD alvo; `alembic downgrade -1` reverte sem erro

---

### Tarefa 03 — Plano de Migração de Dados (Seeds)
**Status:** done
**Lê:** `_reversa_sdd/migration/data_migration_plan.md`, `_reversa_sdd/migration/target_data_model.md`
**Constrói:** `alembic/seeds/` — scripts de seed para dados de referência; `scripts/migrate_legacy.py` — ETL opcional para importar dados de instâncias existentes; validações de integridade pós-migração
**Pronto quando:** Seeds rodam sem erro; se houver dados de teste, registros importados correspondem ao modelo alvo
**Obs:** Sistema não está em produção (Big Bang Controlado); seeds são o foco principal; ETL completo é opcional

---

### Tarefa 04 — Entidades de Domínio Alvo + Regras de Negócio
**Status:** done
**Lê:** `_reversa_sdd/migration/target_domain_model.md`, `_reversa_sdd/migration/target_business_rules.md`
**Constrói:** `nexo/domain/` (value objects, enums, domain exceptions, interfaces de repositório); regras de negócio centrais como métodos de entidade ou domain services sem dependência de infra
**Pronto quando:** Domínio importável, regras de negócio cobertas por testes unitários sem dependência de BD ou HTTP

---

### Tarefa 05 — BC-Identity Backend (Auth + User + Session)
**Status:** done
**Lê:** `_reversa_sdd/migration/target_architecture.md` (seção BC-Identity), `_reversa_sdd/migration/target_domain_model.md`, `_reversa_sdd/migration/target_business_rules.md`
**Constrói:** `nexo/auth/` (JWT utilities, password hashing bcrypt, rate limiter, `get_current_user` dependency, `require_admin`), `nexo/repositories/user_repository.py`, `nexo/repositories/session_repository.py`, `nexo/services/user_service.py`, `nexo/services/session_service.py`, `nexo/routers/auth.py`, `nexo/routers/users.py`
**Pronto quando:** Login retorna JWT válido; token expirado/inválido retorna 401; rate limit bloqueia após N tentativas; testes de contrato passam (`parity_tests/01-auth.feature`)

---

### Tarefa 06 — BC-Boards Backend (Board + Team + Category + Permission)
**Status:** done
**Lê:** `_reversa_sdd/migration/target_architecture.md` (seção BC-Boards), `_reversa_sdd/migration/target_domain_model.md`, `_reversa_sdd/migration/target_business_rules.md`
**Constrói:** `nexo/repositories/{board,team,category,permission}_repository.py`, `nexo/services/{board,team,category,permission}_service.py`, `nexo/routers/{boards,teams,categories}.py`
**Pronto quando:** CRUD de boards, equipes e categorias funciona; permissões ADMIN/EDITOR/VIEWER aplicadas corretamente; testes de contrato passam (`parity_tests/02-boards.feature`, `parity_tests/03-permissions.feature`)
**Alerta:** ⚠️ REF-001 — validar que `isPublic`, `isTemplate`, `isChannel` são mutuamente exclusivos no schema Pydantic de Board e/ou em `BoardService.create()`

---

### Tarefa 07 — BC-Content Backend (Block + BlockHistory + File)
**Status:** done
**Lê:** `_reversa_sdd/migration/target_architecture.md` (seção BC-Content), `_reversa_sdd/migration/target_domain_model.md`, `_reversa_sdd/migration/target_business_rules.md`
**Constrói:** `nexo/repositories/{block,block_history,file}_repository.py`, `nexo/services/{block_service,block_history_service,file_service}.py`, `nexo/routers/{blocks,files}.py`; armazenamento de arquivos local (S3-compatible interface opcional)
**Pronto quando:** Criação/edição/deleção de blocos funciona; histórico registra versões corretamente; upload de arquivo retorna URL válida; testes de contrato passam (`parity_tests/04-content.feature`)

---

### Tarefa 08 — BC-Views Backend (View + Filter)
**Status:** done
**Lê:** `_reversa_sdd/migration/target_architecture.md` (seção BC-Views), `_reversa_sdd/migration/target_domain_model.md`, `_reversa_sdd/migration/target_business_rules.md`
**Constrói:** `nexo/repositories/view_repository.py`, `nexo/services/view_service.py`, `nexo/routers/views.py`; lógica de filtro, ordenação e agrupamento de cards
**Pronto quando:** Views Kanban/Tabela/Galeria/Calendário retornam cards corretamente filtrados; testes de contrato passam (`parity_tests/05-views.feature`)

---

### Tarefa 09 — BC-Collaboration Backend (Sharing + Subscription + WebSocket)
**Status:** done
**Lê:** `_reversa_sdd/migration/target_architecture.md` (seção BC-Collaboration), `_reversa_sdd/migration/target_domain_model.md`, `_reversa_sdd/migration/target_business_rules.md`
**Constrói:** `nexo/repositories/{sharing,subscription}_repository.py`, `nexo/services/{sharing_service,subscription_service}.py`, `nexo/ws/server.py` (WSConnectionManager, broadcast handler), `nexo/routers/{sharing,subscriptions}.py`
**Pronto quando:** Compartilhamento de board via link público funciona; WebSocket envia eventos de mudança a todos os clientes conectados; testes de contrato passam (`parity_tests/06-collaboration.feature`)
**Alerta:** ⚠️ REF-002 — monitorar latência do broadcast síncrono; usar `asyncio.gather` ou `BackgroundTasks` se p99 > threshold definido em parity_specs.md

---

### Tarefa 10 — Transversal Backend (main.py + Middleware + Config)
**Status:** done
**Lê:** `_reversa_sdd/migration/target_architecture.md` (seção Transversal / infra), `_reversa_sdd/migration/target_business_rules.md`
**Constrói:** `nexo/main.py` (FastAPI app factory, lifespan, CORS, routers mount), `nexo/config.py` (Settings via pydantic-settings), `nexo/database.py` (engine, SessionLocal, get_db), `nexo/middleware/` (`logging_middleware.py`, `payload_limit_middleware.py`, `metrics_middleware.py`)
**Pronto quando:** App sobe com `uvicorn nexo.main:app`; todas as rotas acessíveis; middleware de logging emite JSON estruturado; payload > limite retorna 413; `/health` retorna 200
**Alertas:** ⚠️ REF-003 — logging estruturado (JSON, campos: timestamp, level, method, path, status, duration_ms) | ⚠️ REF-004 — `ContentSizeLimitMiddleware` configurável via env | ⚠️ REF-005 — documentar em `docs/deployment.md` que nginx é obrigatório em produção para headers timeout

---

### Tarefa 11 — Shared Frontend (API Client + WebSocket + Layouts + Composables)
**Status:** done
**Lê:** `_reversa_sdd/migration/target_architecture.md` (seção Shared Frontend), `_reversa_sdd/migration/target_screens.md` (layouts base)
**Constrói:** `webapp/src/shared/api/` (`http.ts` axios instance, `useMutator.ts`), `webapp/src/shared/ws/` (`useWebSocket.ts`), `webapp/src/shared/layouts/` (`AppShell.vue`, `Sidebar.vue`, `TopBar.vue`), `webapp/src/shared/components/` (BaseButton, BaseModal, BaseInput, etc.), `webapp/src/stores/` (Pinia root)
**Pronto quando:** `useMutator` e `useWebSocket` funcionam em componente de teste; AppShell renderiza sem erro; `npm run build` sem warnings
**Alerta:** ⚠️ REF-006 — usar Bootstrap **somente via npm** (`import 'bootstrap'` no `main.ts`); remover qualquer tag `<link>` CDN de `index.html`

---

### Tarefa 12 — Feature Identity Frontend (Login + Register + Preferências)
**Status:** done
**Lê:** `_reversa_sdd/migration/target_architecture.md` (seção BC-Identity Frontend), `_reversa_sdd/migration/target_screens.md` (SCR-001 Login, SCR-002 Register, SCR-018 ChangePassword, SCR-019 UserPreferences)
**Constrói:** `webapp/src/features/identity/` — `LoginPage.vue`, `RegisterPage.vue`, `ChangePasswordPage.vue`, `UserPreferencesPage.vue`, `useAuth.ts` store/composable, `authGuard.ts` router guard
**Pronto quando:** Login com credenciais corretas → redireciona para Home; credenciais erradas → mensagem de erro; guard bloqueia rota protegida sem token; testes Gherkin `01-auth.feature` passam

---

### Tarefa 13 — Feature Boards Frontend (Home + Board Members + Templates)
**Status:** done
**Lê:** `_reversa_sdd/migration/target_architecture.md` (seção BC-Boards Frontend), `_reversa_sdd/migration/target_screens.md` (SCR-003 HomePage, SCR-010 BoardMembers, SCR-011 BoardTemplates, SCR-012 CategoryManager, SCR-020 TeamSettings)
**Constrói:** `webapp/src/features/boards/` — `HomePage.vue`, `CreateBoardModal.vue`, `BoardMembersPage.vue`, `BoardTemplatesPage.vue`, `CategoryManagerPage.vue`, `TeamSettingsPage.vue`, `useBoards.ts`
**Pronto quando:** Home lista boards do usuário; criar board abre modal e board aparece na lista; SCR-003 e SCR-010 renderizam em todos os estados definidos em target_screens.md

---

### Tarefa 14 — Feature Content Frontend (ContentRegistry + CardDetail + Files)
**Status:** done
**Lê:** `_reversa_sdd/migration/target_architecture.md` (seção BC-Content Frontend), `_reversa_sdd/migration/target_screens.md` (SCR-006 CardDetail, SCR-007 ContentRegistry, SCR-008 PropertyValueElement, SCR-013 FileAttachments, SCR-014 BlockHistory)
**Constrói:** `webapp/src/features/content/` — `CardDetailModal.vue`, `ContentRegistry.vue` (registro de tipos de bloco), `PropertyValueElement.vue` (render dinâmico de propriedades), `FileAttachmentsPanel.vue`, `BlockHistoryPanel.vue`, `useContent.ts`
**Pronto quando:** Card abre modal com todos os tipos de bloco renderizados corretamente; upload de arquivo funciona; histórico exibe versões anteriores

---

### Tarefa 15 — Feature Views Frontend (Kanban + Table + Gallery + Calendar)
**Status:** done
**Lê:** `_reversa_sdd/migration/target_architecture.md` (seção BC-Views Frontend), `_reversa_sdd/migration/target_screens.md` (SCR-004 BoardTable, SCR-005 Kanban, SCR-015 GalleryView, SCR-016 CalendarView, SCR-017 FilterPanel)
**Constrói:** `webapp/src/features/views/` — `KanbanView.vue`, `TableView.vue`, `GalleryView.vue`, `CalendarView.vue`, `FilterPanel.vue`, `SortPanel.vue`, `GroupByPanel.vue`, `useViews.ts`, drag-and-drop para Kanban
**Pronto quando:** Todas as 4 views renderizam cards corretos; filtros aplicam em tempo real; arrastar card no Kanban atualiza status via API; testes Gherkin `05-views.feature` passam

---

### Tarefa 16 — Feature Collaboration Frontend (Share + Comments + Subscriptions)
**Status:** done
**Lê:** `_reversa_sdd/migration/target_architecture.md` (seção BC-Collaboration Frontend), `_reversa_sdd/migration/target_screens.md` (SCR-009 ShareBoard, SCR-016 CommentsPanel — se presente)
**Constrói:** `webapp/src/features/collaboration/` — `ShareBoardModal.vue`, `CommentsPanel.vue`, `SubscriptionToggle.vue`, `useCollaboration.ts`, integração WebSocket (usando `useWebSocket` de shared)
**Pronto quando:** Modal de compartilhamento gera link público; comentários aparecem em tempo real via WS; toggle de notificações persiste; testes Gherkin `06-collaboration.feature` passam

---

### Tarefa 17 — Desktop Electron
**Status:** done
**Lê:** `_reversa_sdd/migration/target_architecture.md` (seção Desktop)
**Constrói:** `desktop/` — `main.ts` (BrowserWindow, spawn nexo backend subprocess), `preload.ts`, `electron-builder.config.ts`; single-user JWT auto-gerado na inicialização; packaging scripts
**Pronto quando:** `npm run electron:dev` abre janela com webapp funcionando; backend FastAPI sobe como subprocesso; fechar janela desliga o backend

---

### Tarefa 18 — Importadores CLI TypeScript (6 importers)
**Status:** done
**Lê:** `_reversa_sdd/migration/target_architecture.md` (seção Importadores CLI)
**Constrói:** `import/` — `trello.ts`, `jira.ts`, `asana.ts`, `todoist.ts`, `notion.ts`, `nextcloud-deck.ts`; cada importer lê formato fonte e chama API nexo via HTTP; `import/index.ts` CLI entry point com `commander`
**Pronto quando:** `npx nexo-import trello --file export.json --board <id>` importa cards sem erros; schema do JSON de entrada validado com Zod

---

### Tarefa 19 — Cutover
**Status:** pending
**Lê:** `_reversa_sdd/migration/cutover_plan.md`
**Constrói:** `scripts/cutover/` — checklist executável, script de switch de configuração, plano de rollback documentado; guia de implantação em `docs/deployment.md`
**Pronto quando:** Checklist de cutover executado end-to-end em ambiente de staging; rollback testado e < 30min

---

### Tarefa 20 — Validação de Paridade
**Status:** pending
**Lê:** `_reversa_sdd/migration/parity_specs.md`, `_reversa_sdd/migration/parity_tests/01-auth.feature`, `_reversa_sdd/migration/parity_tests/02-boards.feature`, `_reversa_sdd/migration/parity_tests/03-permissions.feature`, `_reversa_sdd/migration/parity_tests/04-content.feature`, `_reversa_sdd/migration/parity_tests/05-views.feature`, `_reversa_sdd/migration/parity_tests/06-collaboration.feature`, `_reversa_sdd/migration/parity_tests/07-data-migration.feature`, `_reversa_sdd/migration/parity_tests/08-screen-contracts.feature`
**Constrói:** configuração do runner Gherkin (ex: pytest-bdd ou Vitest + `@cucumber/cucumber`); implementação dos step definitions; relatório de divergências
**Pronto quando:** Todos os cenários definidos nos 8 `.feature` files passam; divergência funcional < 0.01% em execução de 30 dias (conforme critério em parity_specs.md); 9 DEV aprovados documentados em `screen_deviation_log.md` não causam falha
