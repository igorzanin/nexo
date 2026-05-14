# Icon Map — Focalboard Legacy → Bootstrap Icons

> Gerado por `/reversa-coding` (T003)
> Data: `2026-05-14`
> Fonte: `focalboard-legacy/webapp/src/svg/` + uso de ícones no código
> 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## SVG Files (src/svg/)

| Arquivo legado | Conteúdo | Bootstrap Icons substituto |
|---------------|----------|---------------------------|
| `svg/card-skeleton.tsx` | Card placeholder skeleton | `bi-card-text` + CSS skeleton |
| `svg/error-illustration.tsx` | Error page illustration | `bi-exclamation-triangle-fill` + ilustração custom |
| `svg/search-illustration.tsx` | Search empty state | `bi-search` + ilustração custom |

## Ícones por contexto de uso

Com base nos componentes e na estrutura de código legado, estes são os ícones Bootstrap Icons equivalentes para uso no novo sistema:

### Navegação e Layout

| Uso | Ícone legado (inferido) | Bootstrap Icon |
|-----|------------------------|----------------|
| Board | - | `bi-kanban` |
| Card | - | `bi-card-text` |
| Team | - | `bi-people-fill` |
| User | - | `bi-person-circle` |
| Settings | - | `bi-gear` |
| Sidebar toggle | - | `bi-layout-sidebar` |
| Workspace | - | `bi-grid-3x3-gap-fill` |

### Ações

| Uso | Bootstrap Icon |
|-----|----------------|
| Add/Create | `bi-plus` |
| Edit | `bi-pencil` |
| Delete | `bi-trash` |
| Duplicate | `bi-files` |
| Share | `bi-share` |
| Search | `bi-search` |
| Filter | `bi-funnel` |
| Sort | `bi-arrow-up-down` |
| Close | `bi-x` |
| Back | `bi-arrow-left` |
| Menu (kebab) | `bi-three-dots-vertical` |
| Menu (horizontal) | `bi-three-dots` |
| Drag handle | `bi-grip-vertical` |
| Download | `bi-download` |
| Upload | `bi-upload` |
| Copy link | `bi-link-45deg` |

### Visualizações

| Uso | Bootstrap Icon |
|-----|----------------|
| Board/Kanban view | `bi-kanban-fill` |
| Table view | `bi-table` |
| Calendar view | `bi-calendar3` |
| Gallery view | `bi-images` |
| View switcher | `bi-grid-3x3` |

### Card Detail

| Uso | Bootstrap Icon |
|-----|----------------|
| Comment | `bi-chat` |
| Attachment | `bi-paperclip` |
| Image | `bi-image` |
| Text content | `bi-type` |
| Checkbox | `bi-check-square` |
| Divider | `bi-hr` |
| Heading | `bi-fonts` |
| Properties | `bi-list-columns` |
| Description | `bi-card-heading` |

### Status e Notificações

| Uso | Bootstrap Icon |
|-----|----------------|
| Flash success | `bi-check-circle-fill` |
| Flash error | `bi-x-circle-fill` |
| Flash warning | `bi-exclamation-triangle-fill` |
| Flash info | `bi-info-circle-fill` |
| Loading | `bi-arrow-repeat` (spinning) |

### Sidebar

| Uso | Bootstrap Icon |
|-----|----------------|
| Boards | `bi-kanban` |
| Templates | `bi-file-earmark` |
| Categories | `bi-folder` |
| Create category | `bi-folder-plus` |
| Collapse | `bi-chevron-down` |
| Expand | `bi-chevron-right` |

### Permissions e Usuários

| Uso | Bootstrap Icon |
|-----|----------------|
| Admin | `bi-shield-check` |
| Member | `bi-person` |
| Guest | `bi-person-badge` |
| Public link | `bi-globe2` |
| Board permission | `bi-lock` / `bi-unlock` |

### Onboarding

| Uso | Bootstrap Icon |
|-----|----------------|
| Step complete | `bi-check-circle-fill` (green) |
| Step current | `bi-circle-fill` (primary) |
| Step pending | `bi-circle` |

---

## Regra de uso

```vue
<!-- Uso padrão -->
<i class="bi bi-kanban"></i>

<!-- Com tamanho -->
<i class="bi bi-kanban fs-5"></i>

<!-- Com cor -->
<i class="bi bi-kanban text-primary"></i>
```

Instalação (caso não esteja incluso no Bootstrap 5.3):
```
npm i bootstrap-icons
```

Import no `main.ts`:
```ts
import 'bootstrap-icons/font/bootstrap-icons.css'
```
