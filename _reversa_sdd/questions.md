# Perguntas para Validação — nexo

> Gerado pelo Revisor em 2026-05-13
> Todas as perguntas foram respondidas pelo usuário (Igor) durante a sessão de revisão.

---

## Perguntas Respondidas

### P1 — MFA
**Pergunta:** MFA (autenticação multifator) não está implementado no legado. Deve ser implementado no novo sistema?
**Resposta:** ❌ Não implementar

### P2 — Rate Limiting
**Pergunta:** Rate limiting inexistente para endpoints de login/registro e API. Deve ser adicionado?
**Resposta:** ✅ Sim, implementar

### P3 — ReadHeaderTimeout
**Pergunta:** ReadHeaderTimeout não configurado no servidor web — risco de segurança. Corrigir?
**Resposta:** ✅ Sim, corrigir

### P4 — Board Default Type
**Pergunta:** Board default type: factory retorna `type='O'` (Open) mas tabela de tipos diz `'P'` (Private). Qual o correto?
**Resposta:** `'P'` (Private)

### P5 — Filter Conditions Count
**Pergunta:** Título fala em 14 condições mas lista tem 15. Corrigir para 15?
**Resposta:** ✅ Sim

### P6 — Import Error Handling
**Pergunta:** Falha de parsing interrompe o processo. Implementar validação prévia com relatório de erros?
**Resposta:** ✅ Sim, implementar

### P7 — Import File Size Limit
**Pergunta:** Leitura completa em memória (readFileSync) pode falhar em exports >500MB. Implementar streaming?
**Resposta:** ✅ Sim, implementar

### P8 — BroadcastSubscriptionChange
**Pergunta:** BroadcastSubscriptionChange não implementado no standalone. Necessário?
**Resposta:** ❌ Não necessário

### P9 — blocksEditor vs contentElement
**Pergunta:** Dois sistemas de editor de conteúdo coexistem. Consolidar?
**Resposta:** ✅ Sim, consolidar

### P10 — S3 Backend
**Pergunta:** S3 como backend de arquivos — não confirmado se funciona. Relevante?
**Resposta:** ❌ Não relevante (apenas filesystem local)

### P11 — CardLimitNotification
**Pergunta:** CardLimitNotification existe mas funcionalidade desabilitada. Implementar?
**Resposta:** ❌ Não implementar (manter desabilitado)

### P12 — Password Length
**Pergunta:** Inconsistência: model valida 8 caracteres, app usa 6. Qual padrão adotar?
**Resposta:** 8 caracteres (unificado)

---

## Perguntas Não Respondidas (🟡)

Nenhuma — todas as 🔴 foram resolvidas.
