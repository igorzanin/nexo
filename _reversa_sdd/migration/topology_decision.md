---
schemaVersion: 1
generatedAt: 2026-05-24T17:15:00-03:00
reversa:
  version: "1.0.0"
kind: topology_decision
producedBy: designer
hash: "sha256:designer-topology-decision-nexo"
---

# Topology Decision

> Decisão consciente sobre como organizar o sistema novo: preservar a topologia do legado, adotar uma topologia moderna ou aplicar um híbrido.
> Este artefato é leitura obrigatória do próprio Designer (para decompor bounded contexts) e do agente de codificação (para criar a árvore de pastas).

---

## Topologia do legado detectada

- **Padrão organizacional**: Híbrido — **package-by-layer** no backend (Go original + FastAPI parcial) + **package-by-feature com stores separados** no frontend (React original → Vue 3 parcial)
- **Confiança**: 🟢 CONFIRMADO
- **Evidências**:
  - `_reversa_sdd/architecture.md` §"Arquitetura em Camadas": backend FastAPI organizado em `routers/`, `services/`, `repositories/`, `models/`, `schemas/` — corte horizontal por camada técnica, não por domínio.
  - `_reversa_sdd/inventory.md` §"webapp/": `components/` subdividido por feature (`workspace/`, `kanban/`, `table/`, `calendar/`); `stores/` organizados por domínio (16 stores — boards, cards, views, users, teams, comments, etc.); mas `pages/` é flat e `types/` é flat — sem encapsulamento vertical por feature.
  - `_reversa_sdd/inventory.md` §"import/": cada importador em própria pasta (`trello/`, `jira/`, etc.) — package-by-tool.
  - `_reversa_sdd/inventory.md` §"desktop/": módulo `desktop/` completamente isolado — bom encapsulamento.
  - `_reversa_sdd/architecture.md` §"Stack Tecnológica": backend Python 3.12+ / FastAPI / SQLAlchemy, frontend Vue 3 + Pinia + TypeScript — stack alvo já estabelecida na implementação parcial.

- **Mapa da árvore legada** (resumido):
  ```
  nexo/                          # Backend Python
  ├── main.py
  ├── settings.py
  ├── database.py
  ├── models/                    # Camada: ORM models (Board, Block, Card, User…)
  ├── schemas/                   # Camada: Pydantic schemas
  ├── repositories/              # Camada: SQLAlchemy CRUD
  ├── services/                  # Camada: business logic
  ├── routers/                   # Camada: FastAPI routes
  ├── auth/                      # Submódulo técnico: JWT, bcrypt, Depends
  ├── ws/                        # Submódulo técnico: WebSocket server
  └── tests/

  webapp/src/                    # Frontend Vue 3
  ├── main.ts
  ├── App.vue
  ├── router/index.ts            # Flat
  ├── pages/                     # Flat (LoginPage, BoardPage…)
  ├── components/
  │   ├── workspace/             # Por feature
  │   ├── kanban/                # Por feature
  │   ├── table/                 # Por feature
  │   ├── calendar/              # Por feature
  │   └── (outros flat)
  ├── stores/                    # Por domínio (flat, 16 stores)
  ├── types/                     # Flat (block.ts, board.ts…)
  └── composables/               # Flat (useMutator, useWebSocket)

  import/                        # Importadores CLI TypeScript
  ├── trello/ | jira/ | asana/   # Por ferramenta
  ├── todoist/ | notion/ | nextcloud-deck/
  └── archive.ts

  desktop/                       # Electron (isolado)
  migrations/                    # Alembic
  ```

---

## Diagnóstico estrutural

- **Acoplamento**: **médio** — backend tem camadas bem definidas com `Depends()` para injeção; frontend tem Pinia stores que componentes acessam diretamente (acoplamento leve store→componente), sem inversão de dependência explícita.
- **Coesão por módulo**: **média** — routers coesos por domínio (`routers/boards.py`, `routers/blocks.py`), mas a separação horizontal (todos os services em `services/`) significa que para entender um feature completo é necessário abrir 5 pastas diferentes. Frontend: components por feature são coesos, mas types e composables globais diluem a coesão.
- **Módulos órfãos / mortos**: nenhum detectado; todos os módulos previstos mapeiam para funcionalidade ativa.
- **Camadas redundantes**: `schemas/` e `models/` têm sobreposição conceitual (Pydantic schema vs. SQLAlchemy model para a mesma entidade) — necessário e intencional no FastAPI, mas exige manutenção dupla para cada entidade.
- **Violações de fronteira**: `auth/` mistura concern técnico (JWT/bcrypt) com concern de aplicação (Depends) — leve; aceitável no contexto FastAPI.
- **Mistura de paradigmas/estilos**: homogêneo. Backend = OO com DI (idiomatic FastAPI). Frontend = Reativo + Composição (idiomatic Vue 3 + Pinia). Sem inconsistências de estilo.
- **Avaliação geral**: **parcialmente problemática** — a arquitetura em camadas do backend é **saudável e idiomática para FastAPI**, mas o frontend tem organização **inconsistente**: components organizados por feature, mas types, composables e pages globais criam uma mistura que dificulta localizar todos os artefatos de um feature específico. A causa principal é a ausência de um padrão único para o frontend.

---

## Topologia moderna proposta

- **Padrão**: **Hybrid — Backend: package-by-layer (preservado) + Frontend: package-by-feature (Feature-centric)**
  - Backend mantém package-by-layer: é o padrão idiomático do FastAPI e já está corretamente implementado na estrutura parcial. Mudar para feature-sliced exigiria reorganizar 80 arquivos Python sem ganho proporcional para um backend de 1 desenvolvedor.
  - Frontend adota **package-by-feature**: cada feature (identity, boards, content, views, collaboration) tem sua própria pasta contendo components + store + types + composables locais. Apenas utilitários verdadeiramente globais (API client, WebSocket) permanecem em `shared/`.

- **Justificativa**: FastAPI com SQLAlchemy induz naturalmente ao package-by-layer (routers, services, repositories, models). O ganho de mudar para feature-sliced no backend seria marginal para um sistema de tamanho médio com 1 dev. No frontend Vue 3, feature-centric é hoje o padrão mais ergonômico: um PR que mexe em "boards" toca apenas `features/boards/` — não 5 pastas espalhadas. A estratégia Big Bang escolhida permite este redesign sem overhead de roteamento incremental.

- **Ganhos concretos esperados**:
  - Frontend mais navegável: entender ou modificar o feature "boards" exige abrir uma pasta, não cinco.
  - Limites naturais para o `reversa-reconstructor`: cada feature é uma tarefa de codificação autocontida.
  - Facilita onboarding futuro: novo dev encontra tudo relacionado a "kanban" em `features/views/kanban/`.
  - Reduz risco de import circular: stores + composables locais à feature não criam dependências globais.

- **Custo / risco**:
  - Reorganização do `webapp/src/` existente (baixo custo — o webapp atual é rascunho).
  - Curva de aprendizado zero: package-by-feature é intuitivo e sem setup especial.
  - Nenhum impacto no backend — não muda nenhum arquivo Python.

- **Esboço da árvore proposta**:
  ```
  nexo/                          # Backend (preservado — package-by-layer)
  ├── main.py + settings.py + database.py
  ├── models/                    # ORM: Board, Block, Card, User, Team, Session…
  ├── schemas/                   # Pydantic: request/response schemas
  ├── repositories/              # SQLAlchemy CRUD por entidade
  ├── services/                  # Business logic por domínio
  ├── routers/                   # FastAPI routes por domínio
  ├── auth/                      # JWT + bcrypt + Depends
  ├── ws/                        # WebSocket standalone
  └── tests/

  webapp/src/                    # Frontend (modernizado — package-by-feature)
  ├── main.ts + App.vue
  ├── router/index.ts
  ├── features/
  │   ├── identity/              # login, register, change-password
  │   │   ├── components/
  │   │   ├── stores/
  │   │   ├── composables/
  │   │   └── types/
  │   ├── boards/                # board list, board settings, members, templates
  │   │   ├── components/
  │   │   ├── stores/
  │   │   ├── composables/
  │   │   └── types/
  │   ├── content/               # cards, blocks, card dialog, properties
  │   │   ├── components/
  │   │   ├── stores/
  │   │   ├── composables/
  │   │   └── types/
  │   ├── views/                 # kanban, table, gallery, calendar + view config
  │   │   ├── kanban/
  │   │   ├── table/
  │   │   ├── gallery/
  │   │   ├── calendar/
  │   │   └── stores/
  │   └── collaboration/         # comments, subscriptions, sharing
  │       ├── components/
  │       ├── stores/
  │       └── types/
  ├── shared/                    # Global: API client, WebSocket, utils, i18n
  │   ├── api/
  │   ├── ws/
  │   └── utils/
  └── pages/                     # Route-level pages (thin wrappers)

  import/                        # Importadores (preservado — package-by-tool)
  desktop/                       # Electron (preservado — isolado)
  migrations/                    # Alembic (preservado)
  ```

---

## Opções apresentadas ao usuário

1. **Preservar topologia atual** (conservador)
   - Backend e frontend mantêm a organização atual (package-by-layer backend + hybrid frontend).
   - Consequências: menor esforço de reorganização; perpetua a inconsistência do frontend (types, composables e pages globais misturados com components por feature); não afeta o backend.

2. **Adotar Feature-Sliced Design (FSD) completo** (transformacional)
   - Backend reorganizado em feature modules (`features/boards/router.py`, `features/boards/service.py`, etc.). Frontend FSD com camadas `app/`, `pages/`, `widgets/`, `features/`, `entities/`, `shared/`.
   - Consequências: rompe com o padrão idiomático do FastAPI; maior curva de aprendizado; FSD completo é poderoso mas pode ser over-engineering para um time de 1 dev; ganho máximo de organização.

3. **Híbrido — Backend preservado + Frontend feature-centric** ⭐ RECOMENDADO
   - Backend: mantém package-by-layer (idiomático, correto, sem retrabalho).
   - Frontend: adota package-by-feature (features/ por domínio, shared/ para globais, pages/ como wrappers finos).
   - Consequências: nenhum impacto no backend parcialmente implementado; frontend reorganizado a partir do rascunho atual (baixo custo); cada feature do `reversa-reconstructor` mapeia para uma pasta autocontida.

---

## Decisão do usuário

- **Escolha**: **Opção 3 — Híbrido** (backend layers preservadas + frontend package-by-feature)
- **Justificativa do usuário**: recomendação do Designer aceita
- **Decidido em**: 2026-05-24T17:30:00-03:00

---

## Mapeamento legado → novo

| Módulo / pasta legada | Bounded context novo | Tipo | Observações |
|---|---|---|---|
| `nexo/routers/auth.py` + `nexo/auth/` | BC-Identity (backend) | preservado | auth/ e routers/auth.py mantidos na camada |
| `nexo/routers/boards.py` + `nexo/services/board.py` + `nexo/repositories/board.py` | BC-Boards (backend) | preservado | camadas mantidas, nomes preservados |
| `nexo/routers/blocks.py` + `nexo/routers/cards.py` + serviços | BC-Content (backend) | preservado | blocks e cards permanecem em camadas separadas |
| `nexo/ws/` | BC-Realtime (backend) | preservado | WebSocket standalone |
| `webapp/src/components/workspace/` | `features/boards/components/` | reorganizado | movido para feature folder |
| `webapp/src/components/kanban/` | `features/views/kanban/` | reorganizado | movido para feature folder |
| `webapp/src/components/table/` | `features/views/table/` | reorganizado | movido para feature folder |
| `webapp/src/components/calendar/` | `features/views/calendar/` | reorganizado | movido para feature folder |
| `webapp/src/stores/` (16 stores flat) | distribuídos em `features/*/stores/` | reorganizado | cada store vai para a feature dona |
| `webapp/src/types/` (flat) | distribuídos em `features/*/types/` | reorganizado | tipos movidos para feature dona |
| `webapp/src/composables/useMutator.ts` | `shared/api/useMutator.ts` | reorganizado | global — abstrai chamadas à API |
| `webapp/src/composables/useWebSocket.ts` | `shared/ws/useWebSocket.ts` | reorganizado | global — conexão WebSocket |
| `import/` (6 ferramentas) | `import/` (preservado) | preservado | mantido package-by-tool |
| `desktop/` | `desktop/` (preservado) | preservado | Electron isolado |
| Mattermost, cloud limits, MFA, native desktops | (descartado) | removido | ver `discard_log.md` |

---

## Implicações pendentes para próximos passos do Designer

| Etapa do Designer | Implicação | Como honrar |
|---|---|---|
| Bounded contexts | Frontend: 5 features = 5 bounded contexts frontend. Backend: contextos espelham domínios da camada de services. | Definir BC-Identity, BC-Boards, BC-Content, BC-Views, BC-Collaboration como bounded contexts primários. |
| target_architecture | Backend: diagrama mostra as 4 camadas (routers→services→repositories→models) + auth + ws como componentes separados. Frontend: diagrama mostra features → shared. | Refletir topologia preservada no backend e reorganizada no frontend. |
| target_domain_model | Aggregates agrupados por bounded context, não por tabela legada. Board + BoardMember = 1 aggregate. Block + Card = 1 aggregate (Card é tipo de Block). | Não criar 1 aggregate por tabela — agrupar por invariante de negócio. |
| target_data_model | Schema do banco não muda por causa da topologia de pastas. Alembic migrations podem permanecer em `migrations/`. | DDL é derivado do domain model, independente da organização de pastas. |

---

## Notas

- A reorganização do frontend (`webapp/src/`) tem custo zero real pois o `webapp/` atual é rascunho — nenhum componente Vue no rascunho deve ser assumido como correto ou final (conforme `migration_brief.md`).
- O `reversa-reconstructor`, ao executar, deve criar cada feature como uma tarefa separada, preservando a boundary entre features.
- O backend **não muda de organização** — o agente de codificação escreve `nexo/services/board.py`, `nexo/repositories/board.py`, etc. exatamente como já está estruturado.
- O padrão `features/*/stores/` no frontend segue a convenção de que cada store Pinia pertence ao feature que a usa. Stores que cruzam features usam `shared/`. Isso elimina o problema dos 16 stores globais que atualmente não têm frontend correspondente.
