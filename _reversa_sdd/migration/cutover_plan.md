---
schemaVersion: 1
generatedAt: 2026-05-24T17:05:00-03:00
reversa:
  version: "1.0.0"
kind: cutover_plan
producedBy: strategist
hash: "sha256:strategist-cutover-plan-nexo"
---

# Cutover Plan

> Plano de corte do legado para o sistema novo, alinhado à estratégia recomendada em `migration_strategy.md`.
> **Estratégia base**: Big Bang Controlado (em ordem lógica de módulos).
> Se o usuário escolher outra estratégia, este plano deve ser revisado.

---

## Estratégia base

- **Estratégia confirmada**: Big Bang Controlado — `migration_strategy.md` Estratégia A
- **Premissa central**: sistema não está em produção; legado (Focalboard original) permanece intacto e acessível durante todo o desenvolvimento como oráculo de comportamento e fallback.

---

## Pré-requisitos

Antes do go-live, os seguintes critérios devem estar satisfeitos:

- [ ] Todos os 43 itens MIGRAR do `target_business_rules.md` implementados e verificados
- [ ] `parity_specs.md` (Inspector) com ≥ 95% de cenários Gherkin passando nos testes automatizados
- [ ] `test_sharing.py` implementado e passando (AMB-001)
- [ ] Scheduler de sessões implementado (AMB-002)
- [ ] Bootstrap double import resolvido (REF-006 — CDN removido do `index.html`)
- [ ] Todas as 15 telas do visor com equivalente funcional no sistema novo
- [ ] Fluxos end-to-end críticos testados manualmente: login, criar board, criar card, drag-and-drop, compartilhar board, importar de Trello/Jira
- [ ] Nenhum erro 500 não tratado nos logs de 24h de testes em staging
- [ ] Migrations Alembic aplicadas e banco íntegro com dados de seed

---

## Fases de implementação (ordem recomendada)

> Não é cutover por fases (não há roteamento incremental), mas sim **sequência de sprints** de implementação que minimiza dependências.

| Fase | Conteúdo | Critério de conclusão |
|---|---|---|
| **F1 — Backend Core** | auth, boards, blocks, cards, permissions, sharing | Testes pytest passando; API documentada via OpenAPI |
| **F2 — Backend Avançado** | WebSocket, categorias, subscriptions, file service, scheduler de sessões | WebSocket conectando; cleanup scheduler rodando; uploads funcionais |
| **F3 — Frontend Core** | login, workspace, board page, card modal, Pinia stores | Fluxo básico end-to-end: login → criar board → criar card |
| **F4 — Views e Filtros** | kanban, tabela, galeria, calendário, filtros, ordenação, group-by | Todas as views renderizando com dados reais; filtros funcionais |
| **F5 — UI Completa** | editor markdown (library escolhida), templates, settings, user management | Nenhuma tela do visor sem equivalente; editor funcionando |
| **F6 — Importadores** | Trello, Jira, Asana, Todoist, Notion, Nextcloud Deck (com token auth) | Importação round-trip com dados reais de cada plataforma |
| **F7 — Desktop** | Electron build (dmg, nsis, AppImage) | Build bem-sucedido nas 3 plataformas |
| **F8 — Parity + Hardening** | parity tests, correções de regressão, Bootstrap double import, audit de segurança | ≥ 95% parity tests passando; 0 erros críticos |

---

## Janela de cutover

- **Data alvo**: indefinido (sem prazo declarado)
- **Duração estimada**: 2–4 horas (switching de ambiente — não migração de dados)
- **Ambiente afetado**: local / on-premise (sem cloud, sem SLA)
- **Comunicação prévia**: time interno avisado com 1 semana de antecedência
- **Janela ideal**: sprint final de F8 concluído + validação de parity specs + aprovação de Igor

---

## Passos do cutover

| # | Passo | Owner | Duração | Reversível? |
|---|---|---|---|---|
| 1 | Verificar todos os critérios de go/no-go | Igor | 30 min | N/A |
| 2 | Criar backup completo do banco de dados (se houver dados de teste/staging) | Igor | 15 min | ✅ (restaurar dump) |
| 3 | Aplicar migrations Alembic no banco de produção (`alembic upgrade head`) | Igor | 5 min | ✅ (alembic downgrade) |
| 4 | Subir `uvicorn nexo.main:app` em produção (ou docker-compose up) | Igor | 10 min | ✅ (stop + rollback) |
| 5 | Subir `npm run build` + servir `webapp/dist/` via nginx/caddy | Igor | 15 min | ✅ (apontar para Focalboard) |
| 6 | Smoke tests manuais: login, criar board, criar card, drag-and-drop, WebSocket | Igor + time | 30 min | ✅ |
| 7 | Execução de parity tests automatizados em produção | Igor | 20 min | ✅ |
| 8 | Comunicar time interno que sistema está ativo | Igor | 5 min | N/A |
| 9 | Monitoramento ativo por 48h pós-cutover | Igor | 48h | N/A |

**Duração total estimada**: ~2h (pasos 1–8) + 48h monitoramento.

---

## Plano de rollback

- **Critérios de acionamento**:
  - Parity tests falhando em > 5% dos cenários críticos após go-live
  - Usuário incapaz de completar fluxo crítico (criar board, criar card, login)
  - Erro 500 não tratado em fluxo crítico
  - Perda de dados

- **Passos**:
  1. Parar uvicorn / docker-compose do sistema novo
  2. Restaurar banco de dados do backup (se houve migração de dados)
  3. Redirecionar tráfego para Focalboard legado (Go server na porta original)
  4. Notificar time interno sobre rollback e previsão de nova tentativa
  5. Registrar causa do rollback e atualizar risk_register.md

- **Tempo máximo aceitável até rollback**: 2 horas após detecção do problema
- **Owner do rollback**: Igor Zanin

---

## Critérios de go / no-go

### ✅ Go
- Todos os pré-requisitos marcados como concluídos
- ≥ 95% dos cenários Gherkin de `parity_specs.md` passando
- Smoke tests manuais dos 6 fluxos críticos bem-sucedidos
- 0 erros críticos nos últimos 7 dias de testes em staging
- Bootstrap double import removido
- Time interno informado e disponível para testes pós-cutover

### ❌ No-go
- Qualquer fluxo crítico (login, criar board, criar card) com bug não resolvido
- Parity tests abaixo de 90%
- Migrations Alembic com erro em aplicação
- `test_sharing.py` falhando
- Scheduler de sessões não implementado
- Double Bootstrap import ainda presente

---

## Pós-cutover

- [ ] Monitoramento de logs uvicorn por 48h após go-live
- [ ] Coleta de feedback do time interno na primeira semana
- [ ] Validação de paridade conforme `parity_specs.md` com dados reais
- [ ] Decisão de decommission do Focalboard legado em 30 dias após go-live bem-sucedido
- [ ] Documentar lições aprendidas em `_reversa_sdd/migration/.logs/`
- [ ] Arquivar `_reversa_sdd/` como documentação permanente do projeto

---

## Notas

- O "cutover" neste projeto é principalmente uma questão de **apontar usuários para o sistema novo**, não uma migração de dados de produção (não há usuários em produção hoje). Isso reduz drasticamente o risco da janela de cutover.
- O Focalboard legado (Go server) pode continuar rodando em porta diferente (ex: `:8888`) durante o período de monitoramento pós-cutover, servindo como oráculo de comportamento para qualquer dúvida.
- Se o time decidir por estratégia B (Strangler Fig), este plano deve ser substituído por um plano de cutover por módulo, com roteamento incremental via proxy reverso.
