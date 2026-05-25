---
schemaVersion: 1
generatedAt: 2026-05-24T16:41:57-03:00
reversa:
  version: "1.0.0"
kind: paradigm_decision
producedBy: paradigm_advisor
hash: "sha256:paradigm-decision-nexo-no-gap-balanced"
---

# Paradigm Decision

> Decisão consciente sobre como tratar a mudança (ou ausência) de paradigma entre o legado e a stack alvo.
> **Leitura obrigatória** para todos os agentes posteriores e para o agente de codificação.

## Paradigma do legado detectado

- **Paradigma principal**: Híbrido (Go CSP/Procedural no backend original + React Funcional/Reativo no frontend original → já migrado parcialmente para Python OO com DI + Vue 3 Reativo)
- **Confiança**: 🟢 CONFIRMADO
- **Evidências**:
  - `_reversa_sdd/code-analysis.md` — documenta código Go (goroutines, gorilla/websocket, server.go imperativo). Paradigma original do backend: **CSP / Procedural com interfaces** (padrão Go).
  - `_reversa_sdd/architecture.md` §"Visão Geral" — menciona Redux Toolkit no histórico e o `Mutator` com undo/redo via patches. Paradigma original do frontend: **Funcional/Reativo (React + Redux unidirectional data flow)**.
  - `_reversa_sdd/architecture.md` §"Arquitetura em Camadas" — nova arquitetura já implementada parcialmente: **FastAPI Routers → Services → Repositories → SQLAlchemy Models**. Paradigma: **OO com DI**.
  - `_reversa_sdd/inventory.md` §"webapp/" — 16 Pinia stores, composables `useMutator.ts` e `useWebSocket.ts`. Paradigma: **Reativo + Composição (Vue 3)**.

- **Variações observadas (híbrido)**:
  - **Backend original (Go Focalboard)**: CSP / procedural com interfaces. Goroutines para WebSocket, channels, handlers lineares, zero classes.
  - **Frontend original (React 17 + Redux Toolkit)**: Funcional/Reativo. Reducers puros, selectors, hooks, estado imutável.
  - **Backend novo — parcial (FastAPI)**: OO com DI. Services com dependências injetadas, Repository pattern, SQLAlchemy ORM classes, Pydantic schemas.
  - **Frontend novo — parcial (Vue 3 + Pinia)**: Reativo + Composição. SFCs, composables, Pinia stores com actions/getters.

> **Nota crítica**: a transição de paradigma (Go → Python OO com DI; React Redux → Vue 3 Pinia) foi **decidida e parcialmente executada** como parte da reescrita inicial do projeto, antes deste pipeline de migração. O pipeline não precisa tomar essa decisão — ela já está feita.

## Stack alvo declarada

- **Linguagem (frontend)**: TypeScript com Vue 3.4
- **Framework (frontend)**: Vue 3 + Vite 5 + Bootstrap 5.3.3 + Pinia
- **Linguagem (backend)**: Python 3.12+
- **Framework (backend)**: FastAPI + SQLAlchemy + Alembic
- **Banco**: PostgreSQL (via `.env`) com fallback SQLite
- **Infra**: local / on-premise standalone

## Paradigma natural inferido

- **Paradigma**: Híbrido — **OO com DI** (backend) + **Reativo + Composição** (frontend)
- **Justificativa**: FastAPI com SQLAlchemy induz naturalmente ao padrão Repository + Service com injeção via `Depends()`. Vue 3 com Pinia e composables induz naturalmente ao padrão reativo com estado centralizado e composição de comportamento.
- **Alternativas viáveis**:
  - Backend procedural rico (FastAPI sem camadas) — viável mas cria acoplamento e dificulta testes.
  - Backend event-driven (asyncio + Celery) — viável para features assíncronas como notificações, mas excessivo para o escopo atual.

## Gap identificado

- **Severidade**: **nenhum**
- **Justificativa**: a stack alvo usa o mesmo paradigma já adotado na implementação parcial existente. Não há implicações de mudança de modelo mental a honrar nos agentes seguintes.
- **Implicações concretas**: não aplicável (sem gap).

## Opções apresentadas ao usuário

*(Regra do skill: quando paradigmas são iguais, apresentar confirmação em vez das 3 opções e prosseguir com apetite `balanced` se confirmado.)*

Pergunta feita ao usuário:
> "O sistema legado (Go + React/Redux) já foi parcialmente migrado para a stack alvo (FastAPI + Vue 3 + Pinia). Não há gap de paradigma a resolver — confirma?"

## Decisão do usuário

- **Escolha**: confirmação direta (sem gap, sem opções a decidir)
- **Justificativa do usuário**: "Sim, confirmo — sem mudança de paradigma (apetite: balanced)"
- **Decidido em**: 2026-05-24T16:41:57-03:00

## Apetite derivado

- `derived_appetite`: **balanced**

> Sem gap de paradigma, o apetite é balanced: o Curator, Strategist e Designer devem seguir as patterns já estabelecidas (OO com DI no backend, Reativo + Composição no frontend) sem propor transformações radicais de paradigma. Melhorias de completude, consistência e qualidade são bem-vindas.

## Implicações pendentes para próximos agentes

| Agente | Implicação | Como honrar |
|---|---|---|
| Curator | O paradigma OO com DI implica separação clara entre regras de negócio (services), persistência (repositories) e API (routers). | Ao decidir o que migrar/descartar, preservar regras que habitam a camada de services; não mesclar lógica de negócio com routers. |
| Strategist | Apetite balanced: estratégia de migração deve priorizar completude incremental, não reescrita radical. | Preferir estratégia strangler fig ou big bang controlado; não propor mudanças de paradigma no plano. |
| Designer | OO com DI no backend exige topology com camadas explícitas (routers / services / repositories / models). Vue 3 reativo exige topology com stores Pinia separadas de componentes. | Preservar essa separação de camadas na `target_architecture.md`. Não colapsar services em routers nem stores em componentes. |
| Inspector | Paridade funcional não exige paridade de implementação. O inspector pode usar Gherkin orientado a comportamento (not code). | Critérios de paridade baseados em comportamento de API + fluxos de UI, não em estrutura interna. |

## Notas

- O projeto já possui estrutura parcialmente correta (`nexo/services/`, `nexo/repositories/`, `nexo/routers/`). O principal desafio não é paradigma, é **completude e coerência da implementação**.
- O padrão `Mutator` do frontend original (undo/redo via patches) foi simplificado no novo sistema. O composable `useMutator.ts` deve abstrair chamadas à API e atualizar Pinia stores — isso é idiomático no paradigma Reativo + Composição.
- Bootstrap 5.3 como sistema de design é consistente com o paradigma: componentes nativos (modal, offcanvas, dropdown) mapeiam naturalmente para slots e eventos Vue.
- O agente de codificação deve manter: `Depends()` para injeção no FastAPI, `useStore()` para acesso a state no Vue, e nunca colocar lógica de negócio em routers ou em componentes Vue diretamente.
