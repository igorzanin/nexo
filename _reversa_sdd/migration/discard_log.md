---
schemaVersion: 1
generatedAt: 2026-05-24T16:41:57-03:00
reversa:
  version: "1.0.0"
kind: discard_log
producedBy: curator
hash: "sha256:curator-discard-log-nexo"
---

# Discard Log

> Registro completo do que foi descartado da migração e por quê.
> Todos os 10 descartes são por escopo (fora do brief) ou decisões explícitas do usuário — nenhum por mudança de paradigma.

---

## Itens descartados

### BR-DESCARTAR-001 — Integração Mattermost (plugin mode completo)
- **Origem**: `_reversa_sdd/architecture.md` §"Dívidas Técnicas T7" + `code-analysis.md` (plugin_adapter.go, isMattermostAuth, plugin callbacks)
- **Descrição**: Todo o mecanismo de integração com o Mattermost: plugin adapter, autenticação via header Mattermost, callbacks de inicialização do plugin, clusters de WebSocket via API Mattermost, configuração `PluginSettings`, sistema de licenças cloud.
- **Justificativa**: Fora de escopo declarado no `migration_brief.md` §"Escopo declarado: Excluído". O sistema novo deve ser **totalmente standalone** sem qualquer dependência do Mattermost.
- **Vinculado a paradigma**: não
- **Reposição no sistema novo**: auth standalone via JWT próprio (`auth/jwt.py`) já especificado. WebSocket standalone via FastAPI WebSocket nativo.
- **Risco de descartar**: baixo — toda a integração era um add-on; o produto funciona completamente sem ela.

---

### BR-DESCARTAR-002 — BroadcastSubscriptionChange
- **Origem**: `_reversa_sdd/questions.md` P8 + `_reversa_sdd/architecture.md` T3
- **Descrição**: Evento de broadcast `BroadcastSubscriptionChange` — notificava clientes WebSocket quando uma subscription era criada ou cancelada (comportamento específico do plugin Mattermost).
- **Justificativa**: Decidido explicitamente pelo usuário em P8: "não necessário". Já marcado como `status: removido` em `architecture.md`.
- **Vinculado a paradigma**: não
- **Reposição no sistema novo**: não necessário. Subscriptions são gerenciadas via CRUD REST (`subscriptions.py` router).
- **Risco de descartar**: baixo — funcionalidade marcada como não necessária pelo product owner.

---

### BR-DESCARTAR-003 — BroadcastCardLimitTimestampChange
- **Origem**: `_reversa_sdd/architecture.md` T4
- **Descrição**: Broadcast de mudança no timestamp de limite de cards — funcionalidade ligada ao sistema de cloud limits do Mattermost (card limits por workspace).
- **Justificativa**: Mattermost-specific. Cloud limits foram descartados (BR-DESCARTAR-004). Sem o limite de cards, não há timestamp a broadcastar.
- **Vinculado a paradigma**: não
- **Reposição no sistema novo**: nenhuma. Sem limite de cards no sistema standalone.
- **Risco de descartar**: baixo — funcionalidade ligada a sistema de cobrança do Mattermost, sem relevância para uso interno.

---

### BR-DESCARTAR-004 — Cloud Limits Enforcement
- **Origem**: `_reversa_sdd/architecture.md` T1
- **Descrição**: Sistema de enforcement de limites cloud (máximo de boards, cards, members por workspace) com flags de enable/disable. Existia mas estava com enforcement desabilitado no legado.
- **Justificativa**: Funcionalidade de cobrança SaaS do Mattermost. Declarado como "removido" em `architecture.md`. Fora de escopo para um sistema standalone de time interno.
- **Vinculado a paradigma**: não
- **Reposição no sistema novo**: nenhuma.
- **Risco de descartar**: baixo — estava desabilitado; sem efeito prático.

---

### BR-DESCARTAR-005 — MFA (Autenticação Multifator)
- **Origem**: `_reversa_sdd/questions.md` P1 + `architecture.md` T2
- **Descrição**: Autenticação multifator (TOTP/OTP). Não estava implementada no legado — era dependência do Mattermost para o MFA do plugin.
- **Justificativa**: Decidido explicitamente pelo usuário em P1: "não implementar". Uso interno com time pequeno; JWT + bcrypt é suficiente.
- **Vinculado a paradigma**: não
- **Reposição no sistema novo**: nenhuma. Auth por senha + JWT.
- **Risco de descartar**: baixo para uso interno. Se no futuro houver requisito regulatório, pode ser adicionado como feature independente.

---

### BR-DESCARTAR-006 — CardLimitNotification
- **Origem**: `_reversa_sdd/questions.md` P11
- **Descrição**: Notificação ao usuário quando o board se aproxima do limite máximo de cards (ligada ao sistema de cloud limits).
- **Justificativa**: Decidido em P11: "manter desabilitado / não implementar". Depende do cloud limits que também foi descartado (BR-DESCARTAR-004).
- **Vinculado a paradigma**: não
- **Reposição no sistema novo**: nenhuma.
- **Risco de descartar**: baixo — dependência de funcionalidade já descartada.

---

### BR-DESCARTAR-007 — S3 Backend para Arquivos
- **Origem**: `_reversa_sdd/questions.md` P10
- **Descrição**: Suporte a S3 (ou S3-compatible) como backend de armazenamento de arquivos e attachments. Existia código mas sem confirmação de funcionamento.
- **Justificativa**: Decidido em P10: "não relevante — apenas filesystem local". Para time interno local, filesystem é suficiente.
- **Vinculado a paradigma**: não
- **Reposição no sistema novo**: `FileService` com backend filesystem local em `nexo/services/file.py`.
- **Risco de descartar**: baixo para uso on-premise. Se houver necessidade de escalar para múltiplos servidores no futuro, S3 pode ser reintegrado como feature.

---

### BR-DESCARTAR-008 — React 17 + Webpack 5 (Frontend legado original)
- **Origem**: `_reversa_sdd/architecture.md` T6
- **Descrição**: Stack de frontend original do Focalboard (React 17, Redux Toolkit, Webpack 5, react-intl, styled-components legacy).
- **Justificativa**: Substituído por Vue 3 + Vite + Bootstrap 5.3 + Pinia — decisão já executada e confirmada. Não há nada desta stack a migrar; o frontend é reescrito.
- **Vinculado a paradigma**: não (a mudança de paradigma React→Vue foi uma decisão de projeto anterior ao pipeline, não causada por gap de paradigma detectado pelo Paradigm Advisor)
- **Reposição no sistema novo**: Vue 3 SFCs + Pinia stores + Bootstrap 5.3 (substituição completa).
- **Risco de descartar**: nenhum — decisão de arquitetura já tomada e em execução.

---

### BR-DESCARTAR-009 — Desktops Nativos (Mac, WPF/Windows, Linux)
- **Origem**: `_reversa_sdd/architecture.md` T8
- **Descrição**: Aplicativos desktop nativos por plataforma: mac app nativo, Windows WPF app, Linux AppImage com toolkit nativo. Eram distribuídos separadamente do plugin Mattermost.
- **Justificativa**: Substituídos por Electron cross-platform (BR-MIGRAR-017). Uma única codebase cobre Mac, Windows e Linux. Decisão já executada (`desktop/electron-builder.yml` com targets `dmg`, `nsis`, `AppImage`).
- **Vinculado a paradigma**: não
- **Reposição no sistema novo**: `desktop/` Electron (BR-MIGRAR-017).
- **Risco de descartar**: baixo. Electron implica bundle maior (~150MB) mas elimina 3 codebases nativas separadas.

---

### BR-DESCARTAR-010 — ReadHeaderTimeout (configuração Go)
- **Origem**: `_reversa_sdd/architecture.md` T9 + `code-analysis.md` (configuração Go net/http)
- **Descrição**: Configuração de `ReadHeaderTimeout` no servidor HTTP Go para proteção contra slowloris attacks.
- **Justificativa**: Parâmetro específico do servidor HTTP Go (`net/http.Server`). Não existe como conceito equivalente direto em Uvicorn. A proteção equivalente no FastAPI/Uvicorn é via `timeout_keep_alive` (padrão 5s) + firewall/reverse proxy (nginx, caddy) upstream.
- **Vinculado a paradigma**: não
- **Reposição no sistema novo**: Configurar `--timeout-keep-alive` no Uvicorn + documentar uso de reverse proxy para produção. Considerar como nota de deployment, não como código a implementar.
- **Risco de descartar**: médio se exposto diretamente à internet sem reverse proxy — baixo se usado com nginx/caddy na frente (recomendado para produção).

---

## Itens descartados por mudança de paradigma (subseção dedicada)

> **Nenhum item foi descartado por mudança de paradigma nesta migração.**
> O Paradigm Advisor confirmou que a migração não apresenta gap de paradigma (apetite: balanced). Todos os 10 descartes acima são por: escopo fora do brief (Mattermost), decisões explícitas do usuário (P1, P8, P10, P11), substituição tecnológica já executada (T6, T8), ou irrelevância técnica da configuração (T9).

| ID | Origem | Paradigma legado | Substituto no paradigma alvo |
|---|---|---|---|
| — | — | — | — |

---

## Notas

- **Risco acumulado moderado (BR-DESCARTAR-010)**: se o sistema for exposto à internet sem reverse proxy, a ausência de ReadHeaderTimeout pode ser um vetor de ataque. Documentar claramente nos deployment notes.
- **Todos os outros descartes**: risco baixo. O produto funciona completamente sem as features descartadas para o caso de uso de time interno standalone.
- **Mattermost (BR-DESCARTAR-001 a -004)**: o legado tem código de integração profundamente enredado (isMattermostAuth verificado no WebSocket handshake, callbacks no plugin lifecycle, cluster WebSocket). O novo código deve garantir que **nenhuma referência** a Mattermost permaneça.
