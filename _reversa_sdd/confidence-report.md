# Relatório de Confiança — nexo

> Gerado pelo Revisor em 2026-05-13

---

## Resumo Geral

| Nível | Quantidade | Percentual |
|-------|-----------|------------|
| 🟢 CONFIRMADO | 682 | 88.7% |
| 🟡 INFERIDO | 74 | 9.6% |
| 🔴 LACUNA | 13 | 1.7% |
| **Total** | 769 | 100% |

**Confiança geral:** 93.5% (🟢 + metade dos 🟡)

---

## Por Spec

| Spec | 🟢 | 🟡 | 🔴 | Confiança |
|------|----|----|-----|-----------|
| `modelo/` | 56 | 4 | 0 | 96% |
| `servicos/` | 58 | 6 | 0 | 95% |
| `ws/` | 62 | 4 | 1 | 95% |
| `auth/` | 68 | 12 | 2 | 91% |
| `web/` | 35 | 5 | 1 | 89% |
| `componentes/` | 102 | 6 | 1 | 95% |
| `importadores/` | 58 | 8 | 2 | 91% |
| `store/` | 76 | 4 | 0 | 97% |
| `paginas/` | 52 | 2 | 0 | 98% |
| `blocos/` | 68 | 2 | 0 | 98% |
| `api/` | 47 | 12 | 3 | 86% |
| `aplicacao/` | 42 | 7 | 3 | 89% |
| Globals (architecture, domain, etc.) | 58 | 2 | 0 | 97% |

---

## Reclassificações Realizadas

| De | Para | Afirmação | Evidência |
|----|------|-----------|-----------|
| 🔴 | 🟢 | Board default type | Decisão do usuário: `type='P'` (Private) |
| 🔴 | 🟢 | MFA | Decisão do usuário: não implementar |
| 🔴 | 🟢 | Rate limiting | Decisão do usuário: implementar |
| 🔴 | 🟢 | ReadHeaderTimeout | Decisão do usuário: implementar |
| 🔴 | 🟢 | Import error handling | Decisão do usuário: implementar validação prévia |
| 🔴 | 🟢 | Import streaming | Decisão do usuário: implementar streaming |
| 🔴 | 🟢 | BroadcastSubscriptionChange | Decisão do usuário: não implementar |
| 🔴 | 🟢 | blocksEditor vs contentElement | Decisão do usuário: consolidar |
| 🔴 | 🟢 | S3 backend | Decisão do usuário: não implementar |
| 🔴 | 🟢 | CardLimitNotification | Decisão do usuário: não implementar |
| 🔴 | 🟢 | Password length (6→8) | Decisão do usuário: adotar 8 caracteres |
| 🟡 | 🟢 | Filter conditions count | Decisão do usuário: corrigir para 15 |

---

## Lacunas Pendentes 🟡 (inferidas, sem confirmação direta)

### auth/
- Teste de `IsValidReadToken` comentado (`server/auth/auth_test.go:91`) — verificar se deve ser reativado
- Nenhum scheduler confirmado para `CleanUpSessions` — executado manualmente?

### importadores/
- Nextcloud Deck: sem suporte a autenticação por token (apenas user/pass)

### componentes/
- live-markdown-plugin + markdownEditorInput: subsistema complexo e frágil

### api/
- Logging estruturado de todas as requisições? Não confirmado
- Tamanho máximo de payload do body não validado explicitamente

### aplicacao/
- Broadcast via WebSocket: síncrono dentro do mesmo goroutine (pode bloquear?)

---

## Recomendações

- [ ] **auth** tem 2 inferências residuais — baixo risco, mas revisar CleanUpSessions
- [ ] **importadores** — Nextcloud Deck sem token auth pode ser limitante
- [ ] **componentes** — live-markdown-plugin merece atenção durante consolidação blocksEditor

---

## Histórico de Revisão

| Data | Revisor | Ação |
|------|---------|------|
| 2026-05-13 | Reversa Reviewer | Revisão cruzada completa: 12 units + globals. Q&A com usuário: 12 pontos resolvidos. |
