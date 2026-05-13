# State Machines — nexo

> 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Nota importante

Este sistema **não possui máquinas de estado tradicionais com status fixos**. O "Status" é implementado como uma **propriedade customizável** de card do tipo `select`, definida pelo usuário em cada board. Não há transições hardcoded nem fluxos de estado pré-definidos.

Abaixo, as entidades que possuem campos com múltiplos estados ou tipos discretos.

---

## 1. Board Visibility Type

| Estado | Constante | Descrição |
|--------|-----------|-----------|
| Open | `BoardTypeOpen = "O"` | Visível a todos os membros do team (mesmo sem membership explícita) |
| Private | `BoardTypePrivate = "P"` | Visível apenas a membros explícitos do board |

**Transições:**
```
Open ⇄ Private (apenas com PermissionManageBoardType)
```

---

## 2. Board Minimum Role (Role Hierarchy)

```
None ("") → Viewer → Commenter → Editor → Admin
```

Cada nível herda as permissões do nível inferior:

```
Admin    = PermissionManageBoardType, DeleteBoard, ShareBoard, ManageBoardRoles, DeleteOthersComments
Editor   = ManageBoardCards, ManageBoardProperties
Commenter = CommentBoardCards
Viewer   = ViewBoard
```

**Transições:**
```
None ⇄ Viewer ⇄ Commenter ⇄ Editor ⇄ Admin
```

---

## 3. Board Membership Role (Scheme Flags)

| Role | SchemeAdmin | SchemeEditor | SchemeCommenter | SchemeViewer |
|------|:-----------:|:------------:|:---------------:|:------------:|
| Admin | ✅ | ❌ | ❌ | ❌ |
| Editor | ❌ | ✅ | ❌ | ❌ |
| Commenter | ❌ | ❌ | ✅ | ❌ |
| Viewer | ❌ | ❌ | ❌ | ✅ |
| None | ❌ | ❌ | ❌ | ❌ |

A role do membro é **elevada** pelo `minimumRole` do board se aplicável.

---

## 4. Block Types

```
Block (base)
├── Board        → BoardType: O | P
├── Card         → CardFields: properties, contentOrder, isTemplate, icon
├── View         → BoardViewFields: viewType, sortOptions, filter, cardOrder
├── Comment      → type='comment', child de Card
├── Text         → bloco de texto, child de Card
├── Image        → imagem, child de Card
├── Attachment   → anexo, child de Card
├── Checkbox     → checkbox, child de Card
├── Divider      → divisor, child de Card
```

**Webapp adiciona:**
```
ContentBlockTypes = text, image, divider, checkbox, h1, h2, h3, list-item, attachment, quote, video
```

---

## 5. Card Lifecycle (via deleteAt)

```
[*] → Active: Block insert
Active → Deleted: Block delete (soft-delete)
Deleted → Active: Block undelete
Deleted → [*]: Block hard-delete (não usado)
```

- **Active:** deleteAt = 0, conteúdo completo acessível
- **Deleted:** deleteAt > 0, movido para tabela de histórico

---

## 6. Board Lifecycle (via deleteAt)

```
[*] → Active: Board create
Active → Deleted: Board delete (soft-delete)
Deleted → Active: Board undelete
```

---

## 7. Category Types

| Tipo | Descrição |
|------|-----------|
| `system` | Categorias criadas automaticamente pelo sistema |
| `custom` | Categorias criadas pelo usuário |

**Transições:** Imutável após criação.

---

## 8. View Types (4)

```
Board (kanban)
Table
Gallery
Calendar
```

Cada board pode ter múltiplas views de tipos diferentes. Não há transição automática entre tipos — o usuário escolhe/cria a view desejada.

---

## 9. Card Property Types (18)

```
text, number, select, multiSelect, date, person, multiPerson,
file, checkbox, url, email, phone,
createdTime, createdBy, updatedTime, updatedBy, unknown
```
