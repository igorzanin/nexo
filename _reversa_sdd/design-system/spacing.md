# Spacing, Grid & Breakpoints

> Sistema de espaçamento do Nexo webapp — Bootstrap 5.3 defaults.
> **Fonte:** Bootstrap 5.3 spec + análise de componentes `.vue`.
> Gerado por: reversa-design-system

## Escala de espaçamento

Bootstrap 5 usa base de `0.25rem` (4px), multiplicada por `0..5`:

| Nível | Rem | Pixels | Classes geradas |
|---|---|---|---|
| 0 | `0` | `0px` | `p-0`, `m-0`, `mb-0` |
| 1 | `0.25rem` | `4px` | `p-1`, `m-1`, `py-1`, `px-1`, `me-1`, `gap-1` |
| 2 | `0.5rem` | `8px` | `p-2`, `m-2`, `px-2`, `py-2`, `me-2`, `ms-2`, `gap-2`, `g-2` |
| 3 | `1rem` | `16px` | `p-3`, `m-3`, `px-3`, `py-3`, `mb-3`, `mt-3` |
| 4 | `1.5rem` | `24px` | `p-4`, `m-4`, `mb-4`, `py-4` |
| 5 | `3rem` | `48px` | `p-5`, `m-5`, `py-5` |

### Espaçamentos efetivamente usados no código

| Classe | Valor | Onde |
|---|---|---|
| `p-1` | 4px todos os lados | Contentor do botão "+ New Board" |
| `p-2` | 8px | Cards de board no grid, área do usuário no rodapé da sidebar |
| `p-3` | 16px | Cabeçalho da sidebar, área de scroll do centro, flash container |
| `p-4` | 24px | Card body nas páginas de login e registro |
| `px-2` | 8px H | Items da sidebar |
| `px-3` | 16px H | ViewHeader, dropdown do usuário |
| `py-1` | 4px V | Items da sidebar, rows de conteúdo no CardDialog |
| `py-2` | 8px V | ViewHeader, dropdown item |
| `py-4` | 24px V | Estado vazio de boards na sidebar |
| `py-5` | 48px V | Estado vazio do CenterPanel |
| `mb-2` | 8px inferior | Toasts/flash messages |
| `mb-3` | 16px inferior | Campos de formulário (login, register) |
| `mb-4` | 24px inferior | Título do card de auth |
| `mt-3` | 16px superior | Link de navegação auth (login/register) |
| `me-1` | 4px direito | Ícone emoji do board na sidebar |
| `me-2` | 8px direito | Ícone emoji no ViewHeader |
| `ms-2` | 8px esquerdo | Subtítulo "✏️" no CardDialog |
| `gap-1` | 4px | Gap no botão do usuário |
| `gap-2` | 8px | Gap de botões no ViewHeader e modal footer |
| `g-2` | 8px (gutter) | Grid de cards no CenterPanel |

## Dimensões inline (hardcoded)

| Elemento | Dimensão | Onde |
|---|---|---|
| Sidebar | `width: 240px` | `Sidebar.vue` |
| Altura da tela | `height: 100vh` | `Workspace.vue`, `Sidebar.vue` |
| Avatar do usuário | `width: 20px; height: 20px` | `Sidebar.vue` |
| Avatar font-size | `font-size: 11px` | `Sidebar.vue` |
| Card de auth | `width: 400px` | `LoginPage.vue`, `RegisterPage.vue` |
| Z-index dropdown usuário | `z-index: 10` | `Sidebar.vue` |
| Z-index flash messages | `z-index: 1060` | `FlashMessages.vue` |

## Grid

Bootstrap 5.3 usa um grid de **12 colunas** com flexbox.

| Propriedade | Valor |
|---|---|
| Colunas | 12 |
| Sistema | CSS Flexbox |
| Gutters padrão | `1.5rem` (24px) horizontal, `0` vertical |
| Gutter `g-2` | `0.5rem` (8px) — usado nos cards do CenterPanel |

**Colunas usadas no código:**

| Classe | Largura | Onde |
|---|---|---|
| `col-4` | 33.33% (base) | Cards de board no CenterPanel |
| `col-md-3` | 25% (≥768px) | Cards de board no CenterPanel |

## Breakpoints

| Nome | Min-width | Sufixo Bootstrap |
|---|---|---|
| xs | < 576px | (sem sufixo) |
| sm | ≥ 576px | `-sm` |
| md | ≥ 768px | `-md` |
| lg | ≥ 992px | `-lg` |
| xl | ≥ 1200px | `-xl` |
| xxl | ≥ 1400px | `-xxl` |

**Breakpoints usados no código:**

| Classe responsiva | Onde |
|---|---|
| `col-md-3` | Cards do CenterPanel (muda de 33% para 25% em ≥768px) |

## Container max-widths (Bootstrap padrão)

| Breakpoint | Max-width |
|---|---|
| sm | 540px |
| md | 720px |
| lg | 960px |
| xl | 1140px |
| xxl | 1320px |

> O app não usa `.container` — usa layout `d-flex` de tela cheia (`height: 100vh`).
