# Design Tokens

> Tabela consolidada de todos os tokens visuais do Nexo webapp.
> **Fonte:** Bootstrap 5.3.3 + análise de uso em componentes Vue.
> Confiança: 🟢 extraído de arquivo | 🟡 inferido de uso | 🔴 referenciado mas não definido
> Gerado por: reversa-design-system

---

## Cores

| Token | Valor | Categoria | Confiança |
|---|---|---|---|
| `color.primary` | `#0d6efd` | Interação primária | 🟢 |
| `color.primary.hover` | `#0b5ed7` | Hover do primário | 🟢 |
| `color.primary.active.bg` | `rgba(13,110,253,0.10)` | Fundo item ativo na sidebar | 🟡 |
| `color.secondary` | `#6c757d` | Texto/borda secundária | 🟢 |
| `color.success` | `#198754` | Sucesso / confirmação | 🟢 |
| `color.danger` | `#dc3545` | Erro / perigo | 🟢 |
| `color.warning` | `#ffc107` | Alerta | 🟢 |
| `color.info` | `#0dcaf0` | Informação | 🟢 |
| `color.light` | `#f8f9fa` | Fundo suave | 🟢 |
| `color.dark` | `#212529` | Texto base | 🟢 |
| `color.white` | `#ffffff` | Fundo branco | 🟢 |
| `color.text.muted` | `#6c757d` | Texto secundário/inativo | 🟢 |
| `color.gray.100` | `#f8f9fa` | Escala cinza | 🟢 |
| `color.gray.200` | `#e9ecef` | Escala cinza | 🟢 |
| `color.gray.300` | `#dee2e6` | Bordas suaves | 🟢 |
| `color.gray.400` | `#ced4da` | Bordas de input | 🟢 |
| `color.gray.500` | `#adb5bd` | Ícones desabilitados | 🟢 |
| `color.gray.600` | `#6c757d` | = secondary | 🟢 |
| `color.gray.700` | `#495057` | Escala cinza | 🟢 |
| `color.gray.800` | `#343a40` | Escala cinza | 🟢 |
| `color.gray.900` | `#212529` | = dark | 🟢 |

---

## Tipografia

| Token | Valor | Confiança |
|---|---|---|
| `font.family.base` | `system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif` | 🟢 |
| `font.family.mono` | `SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace` | 🟢 |
| `font.size.root` | `16px` | 🟢 |
| `font.size.xs` | `11px` | 🟡 (avatar inline) |
| `font.size.sm` | `0.875rem` (14px) | 🟢 (.small) |
| `font.size.base` | `1rem` (16px) | 🟢 |
| `font.size.lg` | `1.125rem` (18px) | 🟢 |
| `font.size.h6` | `1rem` (16px) | 🟢 |
| `font.size.h5` | `1.25rem` (20px) | 🟢 |
| `font.size.h4` | `1.5rem` (24px) | 🟢 |
| `font.size.h3` | `1.75rem` (28px) | 🟢 |
| `font.size.h2` | `2rem` (32px) | 🟢 |
| `font.size.h1` | `2.5rem` (40px) | 🟢 |
| `font.weight.normal` | `400` | 🟢 |
| `font.weight.semibold` | `600` | 🟢 |
| `font.weight.bold` | `700` | 🟢 |
| `line.height.base` | `1.5` | 🟢 |
| `line.height.heading` | `1.2` | 🟢 |

---

## Espaçamento

| Token | Rem | Pixels | Confiança |
|---|---|---|---|
| `spacing.0` | `0` | `0px` | 🟢 |
| `spacing.1` | `0.25rem` | `4px` | 🟢 |
| `spacing.2` | `0.5rem` | `8px` | 🟢 |
| `spacing.3` | `1rem` | `16px` | 🟢 |
| `spacing.4` | `1.5rem` | `24px` | 🟢 |
| `spacing.5` | `3rem` | `48px` | 🟢 |

---

## Border Radius

| Token | Valor | Classe BS | Confiança |
|---|---|---|---|
| `radius.none` | `0` | `rounded-0` | 🟢 |
| `radius.sm` | `0.25rem` (4px) | `rounded-1` | 🟢 |
| `radius.base` | `0.375rem` (6px) | `rounded`, `rounded-2` | 🟢 |
| `radius.md` | `0.5rem` (8px) | `rounded-3` | 🟢 |
| `radius.lg` | `1rem` (16px) | `rounded-4` | 🟢 |
| `radius.xl` | `2rem` (32px) | `rounded-5` | 🟢 |
| `radius.circle` | `50%` | `rounded-circle` | 🟢 (avatar) |
| `radius.pill` | `50rem` | `rounded-pill` | 🟢 |

---

## Sombras / Elevações

| Token | CSS | Classe BS | Onde |
|---|---|---|---|
| `shadow.sm` | `0 .125rem .25rem rgba(0,0,0,.075)` | `shadow-sm` | Cards de board no CenterPanel |
| `shadow.base` | `0 .5rem 1rem rgba(0,0,0,.15)` | `shadow` | Cards de login/register |
| `shadow.lg` | `0 1rem 3rem rgba(0,0,0,.175)` | `shadow-lg` | — |

---

## Z-Index

| Token | Valor | Origem | Onde |
|---|---|---|---|
| `zindex.dropdown` | `1000` | Bootstrap | Dropdown nativo |
| `zindex.sticky` | `1020` | Bootstrap | — |
| `zindex.fixed` | `1030` | Bootstrap | — |
| `zindex.modal-backdrop` | `1050` | Bootstrap | Backdrop dos modais |
| `zindex.modal` | `1055` | Bootstrap | Modais (CardDialog, ShareBoard) |
| `zindex.flash` | `1060` | 🟡 Inline style | FlashMessages.vue |
| `zindex.sidebar-user-menu` | `10` | 🟡 Inline style | Sidebar.vue (user dropdown) |

---

## Dimensões fixas

| Token | Valor | Confiança | Onde |
|---|---|---|---|
| `layout.sidebar.width` | `240px` | 🟡 | Sidebar.vue |
| `layout.auth-card.width` | `400px` | 🟡 | LoginPage.vue, RegisterPage.vue |
| `layout.avatar.size` | `20px × 20px` | 🟡 | Sidebar.vue |
| `layout.avatar.font-size` | `11px` | 🟡 | Sidebar.vue |

---

## Transições (Bootstrap padrão)

| Propriedade | Valor |
|---|---|
| Transition base | `all .2s ease-in-out` |
| Fade transition | `opacity .15s linear` |
| Collapse transition | `height .35s ease` |

> O código fonte não define transições customizadas. As transições dos componentes Bootstrap (modais, toasts, collapses) seguem os defaults acima.
