# Design System — Nexo Webapp

> Documento consolidado do sistema de design do Nexo.
> **Stack:** Vue 3.4 + Vite 5 + Bootstrap 5.3.3 + Sass 1.77 (sem overrides)
> Gerado por: reversa-design-system

---

## Visão geral

O Nexo webapp **não possui design system próprio**. Todo o sistema visual é herdado do **Bootstrap 5.3.3** sem customizações de variáveis Sass ou CSS custom properties. O estilo é aplicado exclusivamente via classes utilitárias do Bootstrap diretamente nos templates Vue.

| Aspecto | Decisão |
|---|---|
| Framework CSS | Bootstrap 5.3.3 |
| Customização | ❌ Nenhuma (zero overrides de variáveis) |
| Tokens próprios | ❌ Nenhum arquivo de tokens |
| CSS-in-JS | ❌ Não utilizado |
| Tailwind | ❌ Não utilizado |
| Tema | Light (padrão Bootstrap) |
| Dark mode | ❌ Não implementado |

---

## Arquitetura CSS

```
webapp/
├── index.html          ← importa bootstrap@5.3.3 via CDN (link tag)
└── src/
    └── main.ts         ← importa bootstrap/dist/css/bootstrap.min.css via npm
```

> **Dupla importação**: Bootstrap é carregado tanto via CDN no `index.html` quanto via `import` no `main.ts`. Na prática, o build (Vite) usa a versão npm; em produção a CDN pode sobrescrever. Isso é um gap a resolver na migração.

---

## Paleta de cores

Ver detalhes: [`color-palette.md`](./color-palette.md)

| Papel | Hex | Classe |
|---|---|---|
| Primário (ações principais) | `#0d6efd` | `btn-primary`, `text-primary`, `bg-primary` |
| Secundário (ações neutras) | `#6c757d` | `btn-outline-secondary`, `bg-secondary` |
| Sucesso | `#198754` | `text-bg-success` |
| Erro / Perigo | `#dc3545` | `alert-danger`, `btn-outline-danger` |
| Fundo suave | `#f8f9fa` | `bg-light` |
| Fundo branco | `#ffffff` | `bg-white` |
| Texto base | `#212529` | (padrão) |
| Texto secundário | `#6c757d` | `text-muted` |

---

## Tipografia

Ver detalhes: [`typography.md`](./typography.md)

| Elemento | Tamanho | Peso |
|---|---|---|
| Body base | 16px / 1rem | 400 |
| Heading (h4 — auth) | 1.5rem (24px) | 700 |
| Heading (h5 — modal) | 1.25rem (20px) | 700 |
| Heading (h6 — sidebar) | 1rem (16px) | 700 |
| Texto pequeno (.small) | 14px / 0.875em | 400 |
| Avatar | 11px | 400 |
| Font family | `system-ui` stack | — |

---

## Espaçamento

Ver detalhes: [`spacing.md`](./spacing.md)

Base: `0.25rem` (4px). Escala: `×1=4px, ×2=8px, ×3=16px, ×4=24px, ×5=48px`.

---

## Border Radius

| Token | Valor | Uso |
|---|---|---|
| `rounded` (padrão) | `0.375rem` (6px) | Cards, dropdowns, sidebar items |
| `rounded-circle` | `50%` | Avatar circular do usuário |

---

## Sombras

| Classe | Onde |
|---|---|
| `shadow-sm` | Cards de board (CenterPanel) |
| `shadow` | Cards de login/register |

---

## Layout e grid

| Propriedade | Valor |
|---|---|
| Layout principal | Flexbox (`d-flex`) full-height (`100vh`) |
| Sidebar | Fixed `240px` de largura |
| Conteúdo central | `flex-grow-1` |
| Grid de cards | Bootstrap 12 colunas, `g-2` gutter |
| Responsividade mínima | `col-4` → `col-md-3` (768px) |

---

## Componentes Bootstrap utilizados

| Componente | Onde |
|---|---|
| `btn` (primary, outline-primary, outline-secondary, outline-danger, sm, lg) | Toda a interface |
| `form-control` | Campos de input (login, register, card title edit) |
| `card` + `card-body` + `card-title` | Login, Register, CenterPanel cards |
| `modal` + `modal-dialog` + `modal-content` + `modal-header` + `modal-body` + `modal-footer` | CardDialog, ShareBoard |
| `modal-backdrop fade show` | Backdrop dos modais |
| `alert alert-danger` | Erros de formulário |
| `toast show` + `text-bg-{type}` | FlashMessages |
| `badge` | Tipo de view na ViewHeader |
| `form-check form-switch` | Toggle de public sharing (ShareBoard) |
| `input-group` | Copy link (ShareBoard) |
| `dropdown-item` | Items do menu do usuário (Sidebar) |
| `border-*` classes | Bordas da sidebar, ViewHeader |
| Layout utils | `d-flex`, `flex-grow-1`, `flex-column`, `align-items-center`, `justify-content-*` |
| Overflow | `overflow-auto`, `overflow-hidden` |

---

## Z-index hierarchy

```
z-index: 10       → user dropdown (Sidebar.vue)
z-index: 1000     → dropdowns Bootstrap
z-index: 1050     → modal backdrop Bootstrap
z-index: 1055     → modais Bootstrap (CardDialog, ShareBoard)
z-index: 1060     → flash messages (FlashMessages.vue)
```

---

## Gaps identificados

| # | Gap | Risco | Recomendação |
|---|---|---|---|
| G-1 | Bootstrap importado duas vezes (CDN + npm) | Médio | Remover um dos imports (manter npm para builds reproduzíveis) |
| G-2 | Nenhum token customizado | Médio | Criar `src/styles/variables.scss` com overrides das vars Bootstrap (`$primary`, etc.) |
| G-3 | Dark mode não suportado | Baixo | Bootstrap 5.3 tem `data-bs-theme="dark"` nativo; basta adicionar toggle |
| G-4 | Dimensões hardcoded inline | Baixo | Mover `240px` (sidebar), `400px` (auth card), `20px` (avatar) para variáveis CSS |
| G-5 | Sem escala de espaçamento documentada | Baixo | O código segue Bootstrap, mas não há guia explícito |
