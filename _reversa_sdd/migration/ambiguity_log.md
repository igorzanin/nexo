---
schemaVersion: 1
generatedAt: 2026-05-24T16:41:57-03:00
reversa:
  version: "1.0.0"
kind: ambiguity_log
producedBy: curator
---

# Ambiguity Log

> Registro consolidado de itens pendentes, resolvidos e referidos à codificação.
> Atualizado incrementalmente por cada agente do Time de Migração.

---

## PENDENTES

> Deve chegar a zero após o Inspector concluir.

*(nenhum — todos os itens do Curator foram resolvidos na pausa humana)*

---

## RESOLVIDOS COM DECISÃO HUMANA

> Itens que passaram por BR-HUMANA e foram resolvidos na pausa pós-Curator (2026-05-24T17:01:53-03:00).

### AMB-001 — IsValidReadToken: cobertura de testes
- **Decisão**: ✅ IMPLEMENTAR `test_sharing.py` cobrindo token válido, inválido e sharing desabilitado.
- **Resolvido em**: pausa pós-Curator

### AMB-002 — CleanUpSessions: scheduler de limpeza
- **Decisão**: ✅ IMPLEMENTAR scheduler via `lifespan` + `asyncio.create_task`. Cleanup diário.
- **Resolvido em**: pausa pós-Curator

### AMB-003 — Nextcloud Deck: autenticação por token API
- **Decisão**: ✅ IMPLEMENTAR suporte a token API (`Authorization: Bearer`). Suportar ambos: user/password e token.
- **Resolvido em**: pausa pós-Curator

### AMB-004 — live-markdown-plugin: editor de markdown
- **Decisão**: ✅ SUBSTITUIR por melhor library para Vue 3 + Bootstrap 5.3. Library específica a definir durante planejamento.
- **Resolvido em**: pausa pós-Curator

### AMB-005 — Role "guest"
- **Decisão**: ❌ NÃO IMPLEMENTAR. Sem role guest. Acesso externo exclusivamente via readToken.
- **Resolvido em**: pausa pós-Curator

## REFERIDOS À CODIFICAÇÃO

> Itens que não bloqueiam o pipeline mas devem ser tratados pelo agente de codificação.

### REF-001 — R25: Scheme flags mutuamente exclusivos (🟡 inferido)
- **Origem**: `target_business_rules.md` BR-MIGRAR-003
- **Agente que detectou**: Curator
- **Descrição**: A mutualidade exclusiva dos scheme flags de BoardMember é inferida, não confirmada por teste. O agente de codificação deve garantir que o backend rejeite combinações inválidas (ex: SchemeAdmin + SchemeEditor simultaneamente).
- **Ação**: Adicionar validação no `MemberService` ou constraint de banco.

### REF-002 — Broadcast síncrono WebSocket (monitorar em load)
- **Origem**: `target_business_rules.md` BR-MIGRAR-022
- **Agente que detectou**: Curator
- **Descrição**: Broadcast HTTP é síncrono dentro do fluxo FastAPI. `asyncio.Lock()` mitiga mas não elimina o risco em alta carga.
- **Ação**: Monitorar latência em testes de carga. Se necessário, mover broadcast para `BackgroundTasks`.

### REF-003 — Logging estruturado de requisições
- **Origem**: `target_business_rules.md` BR-MIGRAR-023
- **Agente que detectou**: Curator
- **Descrição**: Logging estruturado não confirmado no legado — deve ser implementado.
- **Ação**: Adicionar middleware de logging no FastAPI (`uvicorn.access` ou middleware customizado).

### REF-004 — Limite de payload do body
- **Origem**: `target_business_rules.md` BR-MIGRAR-024
- **Agente que detectou**: Curator
- **Descrição**: Sem validação de tamanho máximo de payload (exceto files: 100KB).
- **Ação**: Implementar `ContentSizeLimit` middleware no FastAPI.

### REF-005 — ReadHeaderTimeout / deployment sem reverse proxy
- **Origem**: `discard_log.md` BR-DESCARTAR-010
- **Agente que detectou**: Curator
- **Descrição**: Ausência de timeout de headers pode ser vetor de ataque se exposto sem proxy.
- **Ação**: Documentar uso obrigatório de nginx/caddy em produção. Configurar `--timeout-keep-alive 5` no Uvicorn.

### REF-006 — Double Bootstrap import (CDN + npm)
- **Origem**: `_reversa_sdd/design-system/design-system.md` §"Gaps G-1"
- **Agente que detectou**: Curator (cross-referência com design-system)
- **Descrição**: Bootstrap 5.3 importado duas vezes: CDN no `index.html` + npm em `main.ts`.
- **Ação**: Remover import CDN do `index.html`. Manter apenas npm para builds reproduzíveis.
