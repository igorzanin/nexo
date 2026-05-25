---
schemaVersion: 1
generatedAt: 2026-05-24T16:41:57-03:00
reversa:
  version: "1.0.0"
kind: target_business_rules
producedBy: curator
hash: "sha256:curator-target-business-rules-nexo"
---

# Target Business Rules

> Catálogo das regras de negócio do legado com decisão de migração.
> Fontes: `_reversa_sdd/domain.md`, `permissions.md`, `gaps.md`, `questions.md`, design.md de cada unit.
> Paradigma de referência: `paradigm_decision.md` (balanced — OO com DI + Reativo, sem gap).

## Resumo

| Categoria | Quantidade |
|---|---|
| Total de regras/itens analisados | 58 |
| **MIGRAR** | **43** |
| **DESCARTAR** | **10** |
| **DECISÃO HUMANA** | **5** |

---

## Regras MIGRAR

### BR-MIGRAR-001 — Regras de Board (criação e gestão)
- **Origem**: `_reversa_sdd/domain.md` §"Regras de Board" (R1–R9)
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: Board deve ter TeamID e Type (`O`/`P`) válido; type é imutável após criação exceto por quem tem `PermissionManageBoardType`; MinimumRole válido (`""`, `"viewer"`, `"commenter"`, `"editor"`, `"admin"`); boards Open e Private requerem permissões distintas para criar; convidados não podem criar boards; boards não-template vão automaticamente para categoria padrão; servidor gera o ID (não aceita ID pré-definido); duplicação de board reverte se cópia de arquivos falhar.
- **Justificativa de migração**: Regras de negócio puras — nenhuma vinculação a paradigma legado.
- **Compatibilidade com paradigma alvo**: Implementar em `BoardService.create()` (validação) + `BoardRepository.create()` (persistência). Atributo `type = BoardType.PRIVATE` como default (resolvido em P4).

---

### BR-MIGRAR-002 — Regras de Card e Block (validação e integridade)
- **Origem**: `_reversa_sdd/domain.md` §"Regras de Card e Block" (R10–R20)
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: Card deve ter ID, BoardID, ContentOrder, Properties não-nulo, timestamps > 0; icon máximo 1 grafema; batch insert requer mesmo board para todos os blocos; Block title máximo 16383 runes, fields JSON máximo 800000 runes; Block deve pertencer ao board da rota; deletar bloco inexistente não é erro; restaurar bloco não-deletado não é erro; ContentOrder gerencia ordem dos blocos de conteúdo; BlocksAndBoards — todo block referencia um board no mesmo lote.
- **Justificativa de migração**: Invariantes de domínio — nunca descartáveis.
- **Compatibilidade com paradigma alvo**: Validações em `BlockService` e schemas Pydantic. `delete_at` soft-delete já está nos modelos SQLAlchemy.

---

### BR-MIGRAR-003 — Regras de Membro e Permissão
- **Origem**: `_reversa_sdd/domain.md` §"Regras de Membro e Permissão" (R21–R26) + `permissions.md` §"Resumo" (P1–P6)
- **Confiança original**: 🟢 CONFIRMADO (exceto R25 🟡)
- **Descrição**: Último admin de um board não pode ser removido nem rebaixado; comentários requerem `PermissionCommentBoardCards`; modificações requerem `PermissionManageBoardCards`; alterar type/minimumRole requer `PermissionManageBoardType`; scheme flags Admin/Editor/Commenter/Viewer mutuamente exclusivos (🟡); `Board.minimumRole` atua como piso de permissão para todos os membros.
  - Admin pode tudo; Editor não gerencia tipo/roles/share/delete; Commenter só comenta e vê; Viewer só vê.
  - Hierarquia: Admin > Editor > Commenter > Viewer (cada papel herda as permissões dos abaixo).
- **Justificativa de migração**: Regras de permissão — nunca descartáveis.
- **Compatibilidade com paradigma alvo**: `PermissionService.has_permission()` + `BoardPermissionGate.vue` + composable `useHasPermissions`. R25 (🟡) deve ser validado no agente de codificação.

---

### BR-MIGRAR-004 — Regras de Categoria
- **Origem**: `_reversa_sdd/domain.md` §"Regras de Categoria" (R27–R29)
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: Categoria deve ter ID, Name, UserID, TeamID não-vazios; tipo `"system"` ou `"custom"`; deletada via soft-delete (deleteAt > 0).
- **Justificativa de migração**: Invariantes de domínio.
- **Compatibilidade com paradigma alvo**: `CategoryRepository.soft_delete()` já usa `delete_at`.

---

### BR-MIGRAR-005 — Regras de Subscription
- **Origem**: `_reversa_sdd/domain.md` §"Regras de Subscription" (R30–R31)
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: Subscription requer BlockID, BlockType, SubscriberID, SubscriberType válidos; SubscriberType deve ser `"user"` (apenas standalone).
- **Justificativa de migração**: Regra de domínio do modo standalone.
- **Compatibilidade com paradigma alvo**: `SubscriptionRepository` + validação Pydantic.

---

### BR-MIGRAR-006 — Regras de Autenticação
- **Origem**: `_reversa_sdd/domain.md` §"Regras de Autenticação" (R32–R37) + `auth/design.md`
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: Auth via JWT Bearer token; access token expira em 30 dias; refresh token expira em 60 dias; token renovado automaticamente via refresh; ReadToken permite acesso anônimo a board quando habilitado; senha mínimo 8 caracteres (unificado — decidido em P12); rate limiting em login/registro (decidido em P2); ReadHeaderTimeout configurado (decidido em P3); bcrypt para hash de senha.
- **Justificativa de migração**: Regras de segurança e domínio.
- **Compatibilidade com paradigma alvo**: `auth/jwt.py`, `auth/password.py`, `auth/dependencies.py` + `slowapi` rate limiter.

---

### BR-MIGRAR-007 — Regras de Soft-Delete e Histórico de Blocos
- **Origem**: `_reversa_sdd/domain.md` §"Regras de Soft-Delete" (R38–R40)
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: Todas as entidades usam soft-delete via `deleteAt` (0 = ativo, > 0 = deletado); deletar bloco move para tabela histórico e depois remove; restaurar bloco re-insere do histórico com `deleteAt=0`.
- **Justificativa de migração**: Invariante de domínio — soft-delete é requisito para rastreabilidade.
- **Compatibilidade com paradigma alvo**: `delete_at` já está nos modelos SQLAlchemy; histórico deve ser implementado com tabela `blocks_history`.

---

### BR-MIGRAR-008 — Regras de WebSocket
- **Origem**: `_reversa_sdd/domain.md` §"Regras de WebSocket" (R41–R44) + `ws/design.md`
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: Cliente WebSocket deve autenticar via AUTH após conectar; subscribe/unsubscribe blocks pode ser feito com readToken válido (sem auth); subscribe/unsubscribe team requer auth; BroadcastBlockChange notifica membros do board + inscritos no bloco.
- **Justificativa de migração**: Regra de comportamento em tempo real — requisito funcional.
- **Compatibilidade com paradigma alvo**: `WSConnectionManager` em `nexo/ws/server.py` + `useWebSocket.ts` composable.

---

### BR-MIGRAR-009 — Matriz de Permissões de Board por Tipo de Ação
- **Origem**: `_reversa_sdd/permissions.md` §"Matriz de Permissões por Papel"
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: 9 permissões mapeadas (manage_board_type, delete_board, share_board, manage_board_roles, delete_others_comments, manage_board_cards, manage_board_properties, comment_board_cards, view_board) com granularidade por papel (Admin/Editor/Commenter/Viewer). Board Open: qualquer membro do team pode ver sem membership explícita (cria BoardMember sintético).
- **Justificativa de migração**: Direitos/permissões — nunca descartáveis.
- **Compatibilidade com paradigma alvo**: `PermissionService.has_permission_to_board()` + composable `useHasPermissions` no frontend.

---

### BR-MIGRAR-010 — 4 Tipos de View (Kanban, Tabela, Galeria, Calendário)
- **Origem**: `_reversa_sdd/architecture.md` §"Visão Geral" + `componentes/design.md`
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: 4 visualizações de board — Board (kanban), Table, Gallery, Calendar. Cada view tem filtros, ordenação e cardOrder próprio.
- **Justificativa de migração**: Funcionalidade central do produto.
- **Compatibilidade com paradigma alvo**: `Kanban.vue`, `Table.vue`, `Gallery.vue`, `Calendar.vue` com `@fullcalendar/vue3` para Calendar.

---

### BR-MIGRAR-011 — FilterGroup aninhado (and/or)
- **Origem**: `_reversa_sdd/blocos/design.md` §"Decisões de Design"
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: FilterGroup como árvore aninhada suportando condições and/or; 15 condições de filtro (corrigido de 14 — P5).
- **Justificativa de migração**: Funcionalidade de filtragem é requisito funcional.
- **Compatibilidade com paradigma alvo**: Tipos `FilterGroup`/`FilterClause` em `webapp/src/types/filterGroup.ts`.

---

### BR-MIGRAR-012 — Patches com diff para undo/redo (Mutator pattern)
- **Origem**: `_reversa_sdd/blocos/design.md` §"Decisões de Design" + `componentes/design.md`
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: Patches com diff (não snapshots) para suporte a undo/redo; Mutator centraliza chamadas à API e atualiza stores após cada operação.
- **Justificativa de migração**: Comportamento funcional (undo/redo) é requisito do produto.
- **Compatibilidade com paradigma alvo**: Composable `useMutator.ts` já planejado.

---

### BR-MIGRAR-013 — Compartilhamento público via ReadToken
- **Origem**: `_reversa_sdd/domain.md` §"Sharing" + `api/design.md`
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: Board pode ser compartilhado via link público com readToken anônimo quando `enablePublicSharedBoards = true`. ReadToken permite acesso de leitura sem autenticação.
- **Justificativa de migração**: Funcionalidade de colaboração.
- **Compatibilidade com paradigma alvo**: `SharingRepository` + `sharing.py` router + rota `/team/:teamId/shared/...` no Vue Router.

---

### BR-MIGRAR-014 — Onboarding Tour
- **Origem**: `_reversa_sdd/domain.md` §"Onboarding"
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: Tour guiado de boas-vindas com 3 etapas (Board, Card, ShareBoard). Estado persistido em configuração do usuário.
- **Justificativa de migração**: Funcionalidade de UX que não viola nenhuma restrição.
- **Compatibilidade com paradigma alvo**: `OnboardingTour.vue`.

---

### BR-MIGRAR-015 — BoardArchive (.boardarchive) — Formato NDJSON
- **Origem**: `_reversa_sdd/importadores/design.md` §"Formato .boardarchive"
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: Formato de exportação/importação NDJSON versionado com header `{"version":1,"date":...}`. `ArchiveUtils.buildBlockArchive` e `parseBlockArchive` são pure functions.
- **Justificativa de migração**: Formato de interoperabilidade — necessário para importadores.
- **Compatibilidade com paradigma alvo**: Manter em TypeScript (`import/util/archive.ts`); importadores são autônomos.

---

### BR-MIGRAR-016 — 6 Importadores CLI (Trello, Jira, Asana, Todoist, Notion, Nextcloud Deck)
- **Origem**: `_reversa_sdd/importadores/design.md`
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: 6 scripts Node.js autônomos para importação de dados externos. Output: `.boardarchive`. Validação prévia com relatório de erros (P6). Streaming para arquivos >500MB (P7). HTML→MD no Jira (TurndownService). Todoist gera N boards de 1 arquivo. Labels Nextcloud viram MultiSelect.
- **Justificativa de migração**: Funcionalidade de migração de dados declarada no escopo.
- **Compatibilidade com paradigma alvo**: Mantidos em TypeScript, independentes da stack Python.

---

### BR-MIGRAR-017 — Modo Desktop (Electron)
- **Origem**: `_reversa_sdd/desktop/design.md`
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: App Electron inicia subprocess FastAPI em porta aleatória, gera token single-user e carrega a UI no BrowserWindow. Suporte a Mac (dmg), Windows (nsis), Linux (AppImage).
- **Justificativa de migração**: Modo de operação declarado no escopo.
- **Compatibilidade com paradigma alvo**: `desktop/electron/server.ts` já especificado.

---

### BR-MIGRAR-018 — Consolidação do editor de conteúdo (blocksEditor vs contentElement)
- **Origem**: `_reversa_sdd/questions.md` P9 + `gaps.md` §"live-markdown-plugin"
- **Confiança original**: 🟢 CONFIRMADO (decidido em P9)
- **Descrição**: Dois sistemas de edição de conteúdo coexistentes devem ser consolidados em um único sistema unificado (`ContentRegistry.vue`).
- **Justificativa de migração**: Decisão explícita do usuário (P9).
- **Compatibilidade com paradigma alvo**: `ContentRegistry.vue` + tipos de bloco específicos (`TextElement`, `ImageElement`, etc.).

---

### BR-MIGRAR-019 — 18 Tipos de Propriedade Customizável de Card
- **Origem**: `_reversa_sdd/domain.md` §"Glossário de Domínio" (Property)
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: Cards suportam 18 tipos de propriedade: text, number, select, multiSelect, date, person, checkbox, url, email, phone, createdTime, createdBy, updatedTime, updatedBy, e outros. Schema de propriedades armazenado em `Board.cardProperties` (JSON).
- **Justificativa de migração**: Funcionalidade central diferenciadora do produto.
- **Compatibilidade com paradigma alvo**: `PropertyValueElement.vue` + tipos no modelo `Block.fields`.

---

### BR-MIGRAR-020 — Prometheus Metrics (`/metrics` endpoint)
- **Origem**: `_reversa_sdd/architecture.md` §"Integrações"
- **Confiança original**: 🟢 CONFIRMADO
- **Descrição**: Endpoint `/metrics` expõe métricas Prometheus. Métricas de login sucesso/falha registradas no fluxo de auth.
- **Justificativa de migração**: Observabilidade operacional. `prometheus-client` já listado como dependência.
- **Compatibilidade com paradigma alvo**: `nexo/main.py` + `prometheus-client` middleware.

---

### BR-MIGRAR-021 — Rate Limiting para auth (decidido em P2)
- **Origem**: `_reversa_sdd/questions.md` P2 + `api/design.md`
- **Confiança original**: 🟢 CONFIRMADO (decidido)
- **Descrição**: 10 requisições/minuto por IP para endpoints `/api/v1/login` e `/api/v1/register`.
- **Justificativa de migração**: Segurança — requisito decidido explicitamente.
- **Compatibilidade com paradigma alvo**: `slowapi` já declarado como dependência.

---

### BR-MIGRAR-022 — Broadcast WebSocket síncrono (monitorar)
- **Origem**: `_reversa_sdd/gaps.md` §"Cosmético" + `ws/design.md`
- **Confiança original**: 🟡 INFERIDO
- **Descrição**: Broadcast via WebSocket é chamado de forma síncrona dentro do fluxo HTTP (sem filas). Pode atrasar resposta HTTP se houver muitos listeners.
- **Justificativa de migração**: Comportamento atual — migrar como está; monitorar em testes de carga.
- **Compatibilidade com paradigma alvo**: `WSConnectionManager.broadcast_to_team()` já usa `asyncio.Lock()`. **Validar no agente de codificação** se a implementação async é suficiente para o load esperado.

---

### BR-MIGRAR-023 — Logging estruturado de requisições HTTP
- **Origem**: `_reversa_sdd/gaps.md` §"Cosmético"
- **Confiança original**: 🟡 INFERIDO
- **Descrição**: Logging estruturado de todas as requisições HTTP não confirmado no legado — deve ser implementado no novo sistema para facilitar debugging.
- **Justificativa de migração**: Boa prática operacional; gap ativo que deve ser resolvido.
- **Compatibilidade com paradigma alvo**: Middleware FastAPI ou uvicorn access log. **Validar no agente de codificação**.

---

### BR-MIGRAR-024 — Limite de payload do body
- **Origem**: `_reversa_sdd/gaps.md` §"Cosmético"
- **Confiança original**: 🟡 INFERIDO
- **Descrição**: Tamanho máximo de payload não validado explicitamente (exceto files: 100KB). Deve ser implementado para proteção contra DoS.
- **Justificativa de migração**: Segurança — gap ativo que deve ser resolvido.
- **Compatibilidade com paradigma alvo**: `fastapi` suporta `Request.body` size limit via middleware. **Validar no agente de codificação**.

---

### BR-MIGRAR-025 — Permissões inferidas PM1/PM2
- **Origem**: `_reversa_sdd/permissions.md` §"Lacunas 🟡" (PM1–PM2)
- **Confiança original**: 🟡 INFERIDO
- **Descrição**: Permissões são apenas a nível de board (não de card individual). Compartilhamento via ShareBoard dialog (não via convite por link separado).
- **Justificativa de migração**: Comportamento inferido de alto grau de confiança.
- **Compatibilidade com paradigma alvo**: Confirmar na implementação que não há endpoints de permissão de card. **Validar no agente de codificação**.

---

## Regras DESCARTAR (resumo)

| ID | Origem | Motivo curto | Vínculo a paradigma? |
|---|---|---|---|
| BR-DESCARTAR-001 | `architecture.md` §"Dívidas Técnicas T7" + `code-analysis.md` | Mattermost plugin mode (plugin_adapter, isMattermostAuth, plugin callbacks) — fora de escopo (migration_brief) | não |
| BR-DESCARTAR-002 | `questions.md` P8 + `architecture.md` T3 | BroadcastSubscriptionChange — não necessário em standalone (decidido em P8) | não |
| BR-DESCARTAR-003 | `architecture.md` T4 | BroadcastCardLimitTimestampChange — removido (Mattermost-specific) | não |
| BR-DESCARTAR-004 | `architecture.md` T1 | Cloud limits enforcement com limites desabilitados — removido (funcionalidade descartada) | não |
| BR-DESCARTAR-005 | `questions.md` P1 + `architecture.md` T2 | MFA (autenticação multifator) — decidido não implementar (P1) | não |
| BR-DESCARTAR-006 | `questions.md` P11 | CardLimitNotification — decidido manter desabilitado / não implementar (P11) | não |
| BR-DESCARTAR-007 | `questions.md` P10 | S3 como backend de arquivos — decidido não relevante (P10); apenas filesystem local | não |
| BR-DESCARTAR-008 | `architecture.md` T6 | React 17 + Webpack 5 — substituído por Vue 3 + Vite; decisão já executada | não |
| BR-DESCARTAR-009 | `architecture.md` T8 | Desktops nativos Mac/WPF/Linux — substituídos por Electron universal | não |
| BR-DESCARTAR-010 | `architecture.md` T9 | ReadHeaderTimeout do servidor Go — não aplicável ao FastAPI/Uvicorn (uvicorn tem `timeout_keep_alive`; configurar via settings) | não |

> Detalhe completo em `discard_log.md`.

---

## Regras DECISÃO HUMANA

### BR-HUMANA-001 — IsValidReadToken: cobertura de testes
- **Origem**: `_reversa_sdd/gaps.md` §"Moderado — IsValidReadToken test comentado"
- **Tipo de ambiguidade**: 🟡 Pain point — risco de funcionalidade sem cobertura
- **Descrição**: O teste de `IsValidReadToken` estava comentado no legado. A funcionalidade de compartilhamento público depende desse token. No sistema novo, não está claro se o endpoint de validação do readToken terá cobertura de testes automatizados.
- **Opções**:
  1. Implementar testes de integração para o fluxo `readToken` no novo sistema (recomendado)
  2. Documentar como manual testing coverage e prosseguir
- **Recomendação do Curator**: **Opção 1** — a funcionalidade de board sharing é crítica o suficiente para exigir cobertura automatizada. Implementar `test_sharing.py` cobrindo: geração do token, acesso com token válido, acesso com token inválido, acesso com board sharing desabilitado.
- **DECISÃO**: ✅ **IMPLEMENTAR** — testes de integração para o fluxo readToken. Criar `test_sharing.py`.
- **Status**: RESOLVIDO

---

### BR-HUMANA-002 — CleanUpSessions: scheduler de limpeza
- **Origem**: `_reversa_sdd/gaps.md` §"Moderado — CleanUpSessions sem scheduler"
- **Tipo de ambiguidade**: 🔴 GAP — comportamento sem implementação confirmada
- **Descrição**: Não há scheduler confirmado para limpeza de sessões JWT expiradas. Com o tempo, a tabela de sessões pode crescer indefinidamente (tokens inválidos acumulando).
- **Opções**:
  1. Implementar background task do FastAPI (`BackgroundTasks` ou `asyncio` periodic task) para limpar sessões expiradas diariamente (recomendado)
  2. Limpar sessões no momento do login (lazy cleanup)
  3. Não limpar (aceitável se o volume for baixo em uso interno)
- **Recomendação do Curator**: **Opção 1** — `lifespan` event do FastAPI com `asyncio.create_task` para cleanup periódico. Simples e sem dependência de Celery/scheduler externo.
- **DECISÃO**: ✅ **IMPLEMENTAR** — scheduler de limpeza via `lifespan` + `asyncio.create_task`. Cleanup diário de sessões expiradas.
- **Status**: RESOLVIDO

---

### BR-HUMANA-003 — Nextcloud Deck: autenticação por token API
- **Origem**: `_reversa_sdd/gaps.md` §"Moderado — Nextcloud Deck sem autenticação por token" + `importadores/design.md`
- **Tipo de ambiguidade**: 🔴 GAP — limitação técnica conhecida
- **Descrição**: Importador Nextcloud Deck usa user/password. Instâncias com autenticação por token API (OAuth, app password, token) não são suportadas. Isso pode bloquear usuários com instâncias mais seguras.
- **Opções**:
  1. Manter como está (user/password apenas) e documentar a limitação
  2. Adicionar suporte a token API do Nextcloud (`Authorization: Bearer <token>`)
  3. Suportar ambos: user/password e token
- **Recomendação do Curator**: **Opção 1** para MVP — documentar a limitação. Adicionar como issue/melhoria futura (Opção 3 seria ideal mas escopo adicional).
- **DECISÃO**: ✅ **IMPLEMENTAR SUPORTE A TOKEN** — adicionar `Authorization: Bearer <token>` ao importador Nextcloud Deck. Suportar ambos: user/password e token API.
- **Status**: RESOLVIDO

---

### BR-HUMANA-004 — live-markdown-plugin: fragilidade do subsistema
- **Origem**: `_reversa_sdd/gaps.md` §"Moderado — live-markdown-plugin subsistema frágil"
- **Tipo de ambiguidade**: ⚠️ AMBÍGUA — risco de implementação durante consolidação
- **Descrição**: O subsistema `live-markdown-plugin` + `markdownEditorInput` é identificado como complexo e frágil. Durante a consolidação de `blocksEditor` vs `contentElement` (BR-MIGRAR-018), existe risco de quebra da edição markdown.
- **Opções**:
  1. Consolidar blocksEditor+contentElement mantendo live-markdown-plugin como está (menor risco de regressão)
  2. Substituir live-markdown-plugin por editor markdown mais simples (ex: `@vueup/vue-quill`, `tiptap`, ou markdown textarea nativo)
  3. Implementar editor markdown do zero alinhado ao Bootstrap 5.3
- **Recomendação do Curator**: **Opção 2** — avaliar `tiptap` que é leve, extensível, Vue-friendly e não depende de plugin externo frágil. Decisão final deve considerar conjunto de features necessárias (apenas texto? imagens? headings?).
- **DECISÃO**: ✅ **IMPLEMENTAR COM MELHOR LIBRARY** — pesquisar e selecionar a library markdown mais adequada para Vue 3 + Bootstrap 5.3 com as features necessárias do sistema. Não usar o live-markdown-plugin legado.
- **Status**: RESOLVIDO (library a confirmar durante planejamento)

---

### BR-HUMANA-005 — Permissões de criação de board: convidados vs. membros
- **Origem**: `_reversa_sdd/permissions.md` §"Permissões de Criação de Board"
- **Tipo de ambiguidade**: 🟡 INFERIDA — sem regras explícitas para o role "guest" no sistema standalone
- **Descrição**: No Focalboard, `"guest"` não pode criar boards. No sistema standalone, o conceito de "guest" (usuário convidado sem conta própria) precisa ser definido: existe? Tem acesso apenas via readToken? Pode se registrar?
- **Opções**:
  1. Não implementar role "guest" — todos os usuários do sistema têm conta registrada
  2. Implementar "guest" como acesso read-only via readToken (sem conta)
  3. Implementar role "guest" com conta limitada
- **Recomendação do Curator**: **Opção 2** — dado que a aplicação é para time interno, o acesso de "convidado" é melhor servido pelo mecanismo de readToken já existente (BR-MIGRAR-013). Não implementar role "guest" separado.
- **DECISÃO**: ❌ **NÃO IMPLEMENTAR ROLE GUEST** — sem role guest. Acesso externo é exclusivamente via readToken (board sharing). Todos os usuários ativos têm conta registrada.
- **Status**: RESOLVIDO

---

## Notas

1. **Sem gap de paradigma** (confirmado pelo Paradigm Advisor): nenhuma regra foi descartada por mudança de paradigma — todos os descartes são por escopo (Mattermost) ou decisões explícitas do usuário.

2. **Qualidade das specs**: a ausência de `requirements.md` nas units (apenas `design.md`) limita a granularidade. As regras de negócio foram extraídas de `domain.md` (fonte primária) e design técnicos. Confiança geral: alta.

3. **Itens resolvidos em `questions.md`**: 12 perguntas respondidas; todas absorvidas em regras MIGRAR ou DESCARTAR conforme a decisão registrada.

4. **Itens BR-HUMANA** serão replicados em `ambiguity_log.md` como PENDENTES.
