# Gaps — Lacunas Remanescentes

> Gerado pelo Revisor em 2026-05-13
> Categorização por severidade: crítico / moderado / cosmético

---

## Crítico

Nenhuma — todas as lacunas críticas foram resolvidas com o usuário.

---

## Moderado

### IsValidReadToken test comentado
- **Spec:** `auth/design.md`
- **Descrição:** O teste de `IsValidReadToken` está comentado em `server/auth/auth_test.go:91`
- **Risco:** Funcionalidade de compartilhamento público pode não ter cobertura adequada
- **Status:** 🟡 Pendente de decisão

### CleanUpSessions sem scheduler
- **Spec:** `auth/design.md`
- **Descrição:** Não há scheduler confirmado para limpeza de sessões expiradas
- **Risco:** Sessões expiradas podem se acumular no banco
- **Status:** 🟡 Pendente de decisão

### Nextcloud Deck sem autenticação por token
- **Spec:** `importadores/design.md`
- **Descrição:** Importador Nextcloud Deck requer user/password; sem suporte a token API
- **Risco:** Pode não funcionar com instâncias que exigem OAuth ou token
- **Status:** 🟡 Pendente de decisão

### live-markdown-plugin subsistema frágil
- **Spec:** `componentes/design.md`
- **Descrição:** live-markdown-plugin + markdownEditorInput é subsistema complexo
- **Risco:** Pode quebrar durante consolidação blocksEditor vs contentElement
- **Status:** 🟡 Atenção durante implementação

---

## Cosmético

### Broadcast no mesmo goroutine
- **Spec:** `aplicacao/design.md`
- **Descrição:** Broadcast via WebSocket é síncrono dentro do mesmo goroutine
- **Risco:** Pode atrasar resposta HTTP se houver muitos listeners
- **Status:** 🟡 Inferido, monitorar durante testes de carga

### Logging de requisições não confirmado
- **Spec:** `api/design.md`
- **Descrição:** Logging estruturado de todas as requisições HTTP não foi confirmado
- **Risco:** Dificulta debugging em produção
- **Status:** 🟡 Inferido

### Limite de payload não validado
- **Spec:** `api/design.md`
- **Descrição:** Tamanho máximo de payload do body não validado explicitamente (exceto files: 100KB)
- **Risco:** Possível DoS via payload grande
- **Status:** 🟡 Inferido
