---
schemaVersion: 1
generatedAt: 2026-05-24T18:30:00-03:00
reversa:
  version: "1.0.0"
kind: parity_specs
producedBy: inspector
paradigmTransition: "OO clássico → OO com DI"
primaryMetric: "índice de divergência funcional < 0.01% em 30 dias"
observationWindow: "30 dias após cutover"
cutoverBlockCriteria: "qualquer falha em cenário @critico nas últimas 24h"
---

# Parity Specs

## 1. Estratégia geral

- **Modos de validação selecionados**:
  - [ ] Shadow mode (não aplicável ao Big Bang Controlado; sem tráfego produtivo paralelo)
  - [x] Characterization tests derivados do legado
  - [x] Contract tests de API, WebSocket, importação/exportação e tela
  - [x] Data parity por snapshots semânticos e checksums lógicos
- **Base de caracterização usada**:
  - `_reversa_sdd/code-analysis.md`
  - `_reversa_sdd/domain.md`
  - `_reversa_sdd/migration/target_business_rules.md`
  - `_reversa_sdd/migration/target_screens.md`
- **Lacunas conhecidas**:
  - `_reversa_sdd/characterization_specs/` não existe.
  - `_reversa_sdd/sequences/` e `_reversa_sdd/flowcharts/` não foram encontrados.
  - A suíte de paridade foi derivada diretamente dos fluxos confirmados do legado e das regras BR-MIGRAR críticas.
- **Aplicação prática dos modos**:
  - **Characterization**: fixar comportamento observável legado para auth, boards, blocks, permissões, sharing, WebSocket, import/export e telas críticas.
  - **Contract tests**: validar contratos REST em `/api/v1/`, protocolo WS em `/ws/{teamId}`, formato `.boardarchive`, CSV e contratos de tela em modo modernizado.
  - **Data parity**: comparar presença/ausência de entidades, soft-delete, histórico de blocos, header/versionamento NDJSON, colunas CSV e efeitos de compartilhamento público.
- **Escopo de prova**:
  - Provar equivalência **comportamental**; não exigir equivalência de implementação entre Go/React e FastAPI/Vue.
  - Tratar o legado como oráculo para regras observáveis; o novo sistema pode usar SQLAlchemy async, Pinia e DI desde que preserve o contrato externo.

## 2. Paridade de telas

- **Modo de tela aplicado**: `modernized`, conforme `_reversa_sdd/migration/screen_modernization_decision.md`.
- **Estratégia de validação de UI**: contract test de tela, sem comparação byte-a-byte e sem golden diff obrigatório.
- **Cobertura mínima por tela crítica**:
  - hierarquia de componentes declarada em `target_screens.md`
  - 4 estados obrigatórios: `idle`, `loading`, `error`, `success`
  - conteúdo textual literal aprovado para o alvo
  - transições de navegação/evento declaradas pela tela
- **Telas críticas cobertas em `.feature`**:
  - `SCR-001 LoginPage`
  - `SCR-004 BoardTableView`
  - `SCR-005 BoardKanbanView`
  - `SCR-006 CardDetailModal`
  - `SCR-009 ShareBoardModal`
- **Regras específicas do modo modernizado**:
  - `Bootstrap 5.3` substitui o CSS legado sem gerar falha de paridade visual.
  - Textos canônicos aprovados para branding usam `Nexo`.
  - Componentes removidos por deviation aprovada (`Give feedback`, `About Focalboard`) não entram no oráculo de paridade.
  - Ausência de screenshot em DEV-001 a DEV-005 não bloqueia a paridade; a prova é semântica por contrato de tela.
- **Manifesto de golden files**:
  - `_reversa_sdd/screens/golden/manifest.yaml` existe, mas todas as entradas estão em `manual_required`.
  - Como o modo é `modernized`, o manifesto é complementar e não altera os critérios de aceite.

## 3. Cobertura adaptada ao paradigma

> A prova de equivalência do Nexo usa a transição operacional **OO clássico → OO com DI** como regra de cobertura mínima, evitando equivalência ingênua orientada apenas a endpoint.

- **Dimensões adicionais obrigatórias**:
  - **Sem dependência de Active Record**: cada fluxo crítico precisa provar o mesmo resultado observável quando executado com persistência real e com repositório equivalente injetado.
  - **Mocks/dublês de repositório**: a prova de paridade deve isolar regras em `services`/aggregates; divergência causada por troca do adaptador de persistência invalida a implementação.
  - **Invariantes em aggregates**: `Board`, `Block`, `User`, `Sharing` e `Subscription` devem preservar as regras BR-MIGRAR antes de qualquer efeito externo.
- **Tradução prática da cobertura**:
  - Cada fluxo `.feature` possui pelo menos um cenário `@composicao` para provar o contrato sob DI.
  - Casos naturalmente idempotentes permanecem explícitos (`delete inexistente`, `revoke token`, `logout`), mas não há exigência artificial de `@ordem` porque o alvo não migrou para event-driven.
  - A prova principal ocorre em fronteiras observáveis: resposta HTTP, mensagem WS, snapshot lógico, estado de tela e navegação.
- **Superfícies que não contam como prova suficiente**:
  - asserts em ORM/modelos isolados sem passar por service
  - equivalência visual pixel-perfect
  - dependência do mesmo schema interno do legado
- **Invariantes mínimos por bounded context**:
  - **BC-Identity**: JWT bearer, refresh 30/60 dias, bcrypt, rate limiting.
  - **BC-Boards**: `teamId` obrigatório, ID gerado pelo servidor, `type` imutável sem permissão, `minimumRole` como piso, último admin protegido.
  - **BC-Content**: batch insert no mesmo board, limites de runes, `delete_at`, `blocks_history`, restore consistente.
  - **BC-Collaboration**: `readToken` válido para compartilhamento/subscription pública, auth pós-conexão no WS, broadcast para membros + inscritos.
  - **BC-Views**: contratos das views table/kanban e filtros/ações visíveis.

## 4. Critérios de paridade aceita

- **Métrica primária**: índice de divergência funcional `< 0.01%` em 30 dias.
- **Janela de observação**: 30 dias após o cutover.
- **Critério de bloqueio do cutover**: qualquer falha em cenário `@critico` nas últimas 24h bloqueia o cutover.
- **Regras complementares de aceite**:
  - zero divergência em contratos públicos de auth, board, block, sharing e WebSocket usados pelos cenários críticos
  - zero divergência semântica nos contratos de tela das 5 telas críticas, respeitando DEV-001 a DEV-009
  - zero divergência na semântica de soft-delete/histórico de blocos
  - `.boardarchive` exportado/importado preserva header NDJSON `{"version":1,"date":...}` e cardinalidade lógica de boards/blocos
  - cenários `@composicao` precisam manter o mesmo resultado observável com repositório SQLAlchemy async e com dublê equivalente
- **Interpretação de falha**:
  - qualquer diferença aprovada em DEV-001 a DEV-009 é tratada como exceção conhecida, não como falha
  - qualquer diferença fora das exceções aprovadas conta como divergência funcional

## 5. Fluxos críticos cobertos

| Arquivo | Fluxo crítico | Bounded contexts | BR-MIGRAR principais |
|---|---|---|---|
| `parity_tests/01-auth.feature` | login, refresh, logout, rate limiting | BC-Identity | BR-MIGRAR-006, BR-MIGRAR-021 |
| `parity_tests/02-board-lifecycle.feature` | criação, imutabilidade, duplicação e listagem de boards | BC-Boards | BR-MIGRAR-001, BR-MIGRAR-004 |
| `parity_tests/03-block-crud.feature` | criação, batch insert, soft-delete e restore de cards | BC-Content | BR-MIGRAR-002, BR-MIGRAR-007 |
| `parity_tests/04-permissions.feature` | último admin, pisos de acesso e restrições por papel | BC-Boards | BR-MIGRAR-003, BR-MIGRAR-009 |
| `parity_tests/05-sharing.feature` | readToken, acesso público e revogação | BC-Collaboration | BR-MIGRAR-006, BR-MIGRAR-013 |
| `parity_tests/06-websocket.feature` | auth pós-conexão, subscribe e broadcast | BC-Collaboration | BR-MIGRAR-008, BR-MIGRAR-022 |
| `parity_tests/07-import-export.feature` | CSV, `.boardarchive`, Trello e validação prévia | BC-Content, BC-Boards | BR-MIGRAR-015, BR-MIGRAR-016 |
| `parity_tests/08-screen-contracts.feature` | contratos de LoginPage, Table, Kanban, Card Detail e Share | BC-Identity, BC-Views, BC-Content, BC-Collaboration | BR-MIGRAR-010, BR-MIGRAR-012, BR-MIGRAR-013 |

## 6. Exceções

Todas as deviations abaixo estão aprovadas em `_reversa_sdd/migration/screen_deviation_log.md` e devem ser excluídas do cálculo de divergência funcional:

1. **DEV-001 — RegisterPage sem screenshot** (`plataforma`)
   - Provar apenas contrato semântico de campos, labels, rota e transição.
2. **DEV-002 — HomePage sem screenshot** (`plataforma`)
   - Provar navegação, lista de boards, `+ Add board` e `Settings`, sem oracle visual.
3. **DEV-003 — ChangePasswordPage sem screenshot** (`plataforma`)
   - Provar contrato funcional de campos, sucesso, erro e cancelamento.
4. **DEV-004 — FilterPanel sem screenshot** (`plataforma`)
   - Provar composição, aplicação e limpeza de filtros; não comparar pixels.
5. **DEV-005 — SortPanel sem screenshot** (`plataforma`)
   - Provar seleção de campo, direção e aplicação; não comparar pixels.
6. **DEV-006 — CSS legado trocado por Bootstrap 5.3** (`modernizacao`)
   - Espaçamento, grid, shadows, dropdowns e modais podem divergir visualmente, desde que preservem hierarquia, eventos e texto.
7. **DEV-007 — Branding `Nexo` substitui `Focalboard`** (`correcao`)
   - `Nexo` é o texto canônico aceito em LoginPage, RegisterPage, HomePage, SettingsAppMenu e UserAccountDropdown.
8. **DEV-008 — Remoção de `Give feedback`** (`modernizacao`)
   - BoardTableView e BoardKanbanView não devem falhar por ausência do link externo.
9. **DEV-009 — Remoção de `About Focalboard`** (`modernizacao`)
   - UserAccountDropdown não deve exigir o item/modal legado.
