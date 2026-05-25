---
schemaVersion: 1
generatedAt: 2026-05-24T18:45:00-03:00
reversa:
  version: "1.0.0"
kind: handoff
producedBy: orchestrator
hash: "sha256:reversa-migrate-handoff-nexo-igorzanin"
---

# Handoff para o Agente de Codificação

> Este documento é a porta de entrada para o agente de codificação (Claude Code, Codex, Cursor, etc.) que vai escrever o sistema Nexo novo a partir das specs produzidas pelo Time de Migração.
> Sistema: **Nexo** — reescrita de Focalboard em **Vue 3 + FastAPI**.

---

## ⚠️ Leitura obrigatória primeiro

1. **`paradigm_decision.md`** — inegociável. Paradigma alvo: **OO com DI (balanced)**, Go procedural → Python OO + asyncio. Todo código deve honrar DI por construtor, sem ActiveRecord, sem global state.
2. **`topology_decision.md`** — inegociável. Topologia: **Híbrido (Opção 3)**. Backend package-by-layer preservado; frontend package-by-feature modernizado (`features/{identity,boards,content,views,collaboration}/` + `shared/`).
3. **`screen_modernization_decision.md`** — inegociável (sistema tem UI). Modo: **modernizado**. Implementar componentes Bootstrap 5.3 + Pinia, honrando os 4 estados (idle/loading/error/success) e o conteúdo textual literal de `target_screens.md`.

---

## Ordem de leitura recomendada

1. `paradigm_decision.md` ← primeiro
2. `topology_decision.md` ← segundo
3. `screen_modernization_decision.md` ← terceiro
4. `migration_brief.md`
5. `target_business_rules.md`
6. `migration_strategy.md`
7. `target_architecture.md`
8. `target_domain_model.md`
9. `target_data_model.md`
10. `data_migration_plan.md`
11. `target_screens.md`
12. `parity_specs.md` + `parity_tests/`
13. `screen_deviation_log.md` (consultivo)
14. `risk_register.md` + `cutover_plan.md`
15. `discard_log.md` (consultivo)
16. `ambiguity_log.md` (consultivo)

---

## Lista de artefatos produzidos

| Artefato | Produzido por | Caminho |
|---|---|---|
| `migration_brief.md` | orchestrator | `_reversa_sdd/migration/` |
| `paradigm_decision.md` | paradigm_advisor | `_reversa_sdd/migration/` |
| `target_business_rules.md` | curator | `_reversa_sdd/migration/` |
| `discard_log.md` | curator | `_reversa_sdd/migration/` |
| `ambiguity_log.md` | curator + orchestrator | `_reversa_sdd/migration/` |
| `migration_strategy.md` | strategist | `_reversa_sdd/migration/` |
| `risk_register.md` | strategist | `_reversa_sdd/migration/` |
| `cutover_plan.md` | strategist | `_reversa_sdd/migration/` |
| `topology_decision.md` | designer (Fase 1) | `_reversa_sdd/migration/` |
| `target_architecture.md` | designer (Fase 2) | `_reversa_sdd/migration/` |
| `target_domain_model.md` | designer (Fase 2) | `_reversa_sdd/migration/` |
| `target_data_model.md` | designer (Fase 2) | `_reversa_sdd/migration/` |
| `data_migration_plan.md` | designer (Fase 2) | `_reversa_sdd/migration/` |
| `screen_modernization_decision.md` | screen_translator (Fase 1) | `_reversa_sdd/migration/` |
| `target_screens.md` | screen_translator (Fase 2) | `_reversa_sdd/migration/` |
| `screen_deviation_log.md` | screen_translator (Fase 2) | `_reversa_sdd/migration/` |
| `screens/inventory.json` | screen_translator | `_reversa_sdd/screens/` |
| `screens/golden/manifest.yaml` | screen_translator | `_reversa_sdd/screens/golden/` |
| `parity_specs.md` | inspector | `_reversa_sdd/migration/` |
| `parity_tests/01-auth.feature` | inspector | `_reversa_sdd/migration/parity_tests/` |
| `parity_tests/02-board-lifecycle.feature` | inspector | `_reversa_sdd/migration/parity_tests/` |
| `parity_tests/03-block-crud.feature` | inspector | `_reversa_sdd/migration/parity_tests/` |
| `parity_tests/04-permissions.feature` | inspector | `_reversa_sdd/migration/parity_tests/` |
| `parity_tests/05-sharing.feature` | inspector | `_reversa_sdd/migration/parity_tests/` |
| `parity_tests/06-websocket.feature` | inspector | `_reversa_sdd/migration/parity_tests/` |
| `parity_tests/07-import-export.feature` | inspector | `_reversa_sdd/migration/parity_tests/` |
| `parity_tests/08-screen-contracts.feature` | inspector | `_reversa_sdd/migration/parity_tests/` |

**Total**: 27 artefatos

---

## Bloqueadores para começar a implementação

Nenhum. Pipeline executado em modo interativo; todos os BR-HUMANA foram resolvidos. PENDENTES no `ambiguity_log.md` = 0.

---

## Itens referidos à codificação (`ambiguity_log.md`)

O agente de codificação deve tratar estes 6 itens durante a implementação:

| ID | Descrição | Ação |
|---|---|---|
| REF-001 | R25: scheme flags mutuamente exclusivos (🟡 inferido) | Validar no `MemberService` ou constraint de banco |
| REF-002 | Broadcast WebSocket síncrono — risco em alta carga | Monitorar latência; se necessário usar `BackgroundTasks` |
| REF-003 | Logging estruturado de requisições ausente no legado | Adicionar middleware de logging (uvicorn.access ou custom) |
| REF-004 | Limite de payload do body não implementado | `ContentSizeLimit` middleware no FastAPI |
| REF-005 | ReadHeaderTimeout — expor sem proxy é risco de ataque | Documentar nginx/caddy obrigatório; `--timeout-keep-alive 5` |
| REF-006 | Bootstrap importado duas vezes (CDN + npm) | Remover CDN do `index.html`; manter apenas npm |

---

## Próximos passos para o agente de codificação

1. **Ler `paradigm_decision.md` e internalizar**: paradigma alvo é OO com DI. Toda instanciação de serviço deve ser via injeção de dependência (FastAPI `Depends`, Vue composables). Sem ActiveRecord. Sem global state mutável.

2. **Ler `topology_decision.md` e internalizar**: topologia híbrida. Backend mantém `nexo/{auth,boards,blocks,categories,sharing,ws,notifications,importers}/`. Frontend usa `webapp/src/features/{identity,boards,content,views,collaboration}/` + `shared/`.

3. **Ler `screen_modernization_decision.md` e internalizar**: modo modernizado. Cada tela em `target_screens.md` é um contrato de componentes. Hierarquia, tokens, textos literais e 4 estados são obrigatórios. Sem golden diff byte-a-byte (9 deviations aprovadas, ver `screen_deviation_log.md`).

4. **Configurar o repositório**:
   - Backend: `poetry init`, `fastapi`, `sqlalchemy[asyncio]`, `alembic`, `python-jose`, `passlib[bcrypt]`, `slowapi`, `websockets`
   - Frontend: `npm create vue@latest`, adicionar `pinia`, `vue-router`, `bootstrap`, `axios`, `@fullcalendar/vue3`
   - Desktop: `npm init` em `desktop/`, `electron`, `electron-builder`

5. **Implementar bottom-up** (ordem de `target_architecture.md`):
   - Infraestrutura → dados (Alembic migrations, SQLAlchemy models) → domínio (services + repositories) → aplicação (FastAPI routers) → bordas (WebSocket, importadores, Electron)
   - Frontend: shared/ (tokens, layout, composables) → features/ (por bounded context)

6. **Implementar as 20 telas** consumindo `target_screens.md` como contrato. 5 telas críticas com cobertura obrigatória: `LoginPage`, `BoardTableView`, `BoardKanbanView`, `CardDetailModal`, `ShareBoardModal`.

7. **Escrever os testes** a partir de `parity_specs.md` e `parity_tests/*.feature`. Os 8 `.feature` cobrem: auth, board lifecycle, block CRUD, permissões, sharing, WebSocket, import/export e contratos de tela. Honrar seção `§ Exceções` que propaga as 9 deviations aprovadas.

8. **Validar paridade** a cada componente:
   - Critério primário: índice de divergência funcional < 0.01% em 30 dias
   - Janela de observação: 30 dias após cutover
   - Critério de bloqueio: qualquer falha em cenário `@critico` nas últimas 24h

9. **Migração de dados**: seguir `data_migration_plan.md`. Sistema não está em produção; não há dados de usuários reais para migrar. Seed data e Alembic initial migration são o escopo.

10. **Cutover**: seguir `cutover_plan.md` e critérios go/no-go. Estratégia: **Big Bang Controlado** (janela de manutenção, backup pré-cutover, rollback em < 15min).

---

## Decisões humanas chave (resumo para referência)

| Decisão | Escolha | Registrado em |
|---|---|---|
| Paradigma alvo | OO com DI (balanced) — sem gap | `paradigm_decision.md` |
| Estratégia de migração | Big Bang Controlado | `migration_strategy.md` |
| Topologia | Híbrido — backend layer, frontend feature | `topology_decision.md` |
| Modo de telas | Modernizado (Bootstrap 5.3 + Pinia) | `screen_modernization_decision.md` |
| Role guest | ❌ Não implementar — readToken como único acesso externo | `target_business_rules.md` BR-HUMANA-005 |
| Editor markdown | Substituir live-markdown-plugin por library Vue 3 (ex: Tiptap) | `target_business_rules.md` BR-HUMANA-004 |
| Nextcloud Deck auth | Bearer token + user/password (ambos) | `target_business_rules.md` BR-HUMANA-003 |
| Session cleanup | lifespan + asyncio.create_task | `target_business_rules.md` BR-HUMANA-002 |
| Test sharing | Implementar test_sharing.py | `target_business_rules.md` BR-HUMANA-001 |

---

## Itens auto-decididos

Nenhum — pipeline executado integralmente em modo interativo com aprovações humanas em cada gate.

---

## Notas finais

- O diretório `webapp/` existente no repositório contém um **rascunho** Vue anterior ao pipeline de migração. Os artefatos desta pipeline **substituem** esse rascunho. O agente de codificação deve ignorar `webapp/` e reconstruir a partir de `target_screens.md` e `target_architecture.md`.
- A pasta `_reversa_sdd/` é somente-leitura para o agente de codificação — ela é o repositório de specs, não deve receber código.
- Golden files de tela (`_reversa_sdd/screens/golden/`) estão vazios (oráculo React não executável automaticamente). Consulte `manifest.yaml` para os comandos de captura manual quando o ambiente legado estiver disponível.
- O sistema Nexo **não está em produção**. Não há usuários reais nem dados sensíveis. O cutover é uma substituição técnica, não uma migração de dados ao vivo.
