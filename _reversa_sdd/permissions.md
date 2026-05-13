# Permissions Matrix — nexo

> 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Papéis (Roles)

| Role | BoardMember Scheme Flag | Descrição |
|------|------------------------|-----------|
| **Admin** | `SchemeAdmin = true` | Administração total do board |
| **Editor** | `SchemeEditor = true` | Edição de cards e propriedades |
| **Commenter** | `SchemeCommenter = true` | Visualização + comentários |
| **Viewer** | `SchemeViewer = true` | Apenas visualização |
| **None** | Todos `false` | Sem papel definido |

**Hierarquia (Admin > Editor > Commenter > Viewer):**
Cada papel herda todas as permissões dos papéis abaixo dele.

---

## Matriz de Permissões por Papel

| ID | Permissão | Admin | Editor | Commenter | Viewer |
|----|-----------|:-----:|:------:|:---------:|:------:|
| `manage_board_type` | Alterar tipo do board (O/P) | ✅ | ❌ | ❌ | ❌ |
| `delete_board` | Deletar board | ✅ | ❌ | ❌ | ❌ |
| `share_board` | Compartilhar board | ✅ | ❌ | ❌ | ❌ |
| `manage_board_roles` | Gerenciar papéis dos membros | ✅ | ❌ | ❌ | ❌ |
| `delete_others_comments` | Deletar comentários de outros | ✅ | ❌ | ❌ | ❌ |
| `manage_board_cards` | Criar/editar/deletar cards | ✅ | ✅ | ❌ | ❌ |
| `manage_board_properties` | Gerenciar propriedades do board | ✅ | ✅ | ❌ | ❌ |
| `comment_board_cards` | Comentar em cards | ✅ | ✅ | ✅ | ❌ |
| `view_board` | Visualizar board | ✅ | ✅ | ✅ | ✅ |

---

## Modelo de Permissões (Standalone)

```
HasPermissionToBoard(userID, boardID, permission)
    │
    ├─ board existe?
    │   └─ Não → return false
    │
    ├─ BoardMember existe?
    │   ├─ Não, board é Open → Cria BoardMember sintético
    │   └─ Sim → continua
    │
    ├─ Aplica member.MinimumRole
    │
    └─ Switch por tipo de permissão
        └─ Verifica schemeAdmin/Editor/...
            └─ return true/false
```

### Client-side (Vue 3)

O frontend replica a lógica de permissões via composable `useHasPermissions`:

```typescript
viewerPermissions = schemeAdmin || schemeEditor || schemeCommenter || schemeViewer
                  || board.minimumRole === MemberRole.Viewer
                  || board.minimumRole === MemberRole.Commenter
                  || board.minimumRole === MemberRole.Editor

commenterPermissions = schemeAdmin || schemeEditor || schemeCommenter
                     || board.minimumRole === MemberRole.Commenter
                     || board.minimumRole === MemberRole.Editor

editorPermissions = schemeAdmin || schemeEditor
                  || board.minimumRole === MemberRole.Editor
```

**Componente de guarda:** `BoardPermissionGate.vue` — renderiza condicionalmente slots baseado em permission array.

---

## Permissões de Criação de Board

| Tipo de Board | Permissão Requerida |
|---------------|---------------------|
| Open (público) | `PermissionCreatePublicBoard` |
| Private (privado) | `PermissionCreatePrivateBoard` |

> Convidados (role `"guest"`) não podem criar boards de nenhum tipo.

---

## Permissões por Tipo de Bloco

| Tipo de Bloco | Permissão Requerida |
|---------------|---------------------|
| Comments (`block.type == "comment"`) | `PermissionCommentBoardCards` |
| Demais blocos (incluindo cards) | `PermissionManageBoardCards` |

---

## Modos de Acesso a Board

| Modo | Requisitos |
|------|------------|
| Board público (Open) | Qualquer membro do team pode ver (sem membership explícita) |
| Board privado (Private) | Requer BoardMember com SchemeViewer+ |
| Board compartilhado via readToken | Requer `enablePublicSharedBoards = true` + token válido na URL |

---

## Resumo de Regras de Permissão

| # | Regra | Confiança |
|---|-------|-----------|
| P1 | Admin pode tudo no board | 🟢 CONFIRMADO |
| P2 | Editor só não pode gerenciar tipo/roles/share/delete do board | 🟢 CONFIRMADO |
| P3 | Commenter só pode comentar e ver | 🟢 CONFIRMADO |
| P4 | Viewer só pode ver | 🟢 CONFIRMADO |
| P5 | Último admin não pode ser removido/rebaixado | 🟢 CONFIRMADO |
| P6 | Board.minimumRole atua como piso de permissão | 🟢 CONFIRMADO |

---

## Lacunas 🟡

| # | Item | Confiança |
|---|------|-----------|
| PM1 | Existem permissões a nível de card individual? | 🟡 INFERIDO — Não, permissões são apenas a nível de board |
| PM2 | Fluxo de convite para board privado via link? | 🟡 INFERIDO — Compartilhamento existe via shareBoard dialog |
