# Typography

> Sistema tipográfico do Nexo webapp — Bootstrap 5.3 defaults.
> **Fonte:** Bootstrap 5.3 spec + análise de componentes `.vue`.
> Gerado por: reversa-design-system

## Font Family

| Papel | Stack | Confiança |
|---|---|---|
| Body (base) | `system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans", "Liberation Sans", Arial, sans-serif` | 🟢 |
| Emoji / ícones inline | `"Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"` | 🟢 |
| Monospace (code) | `SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace` | 🟢 |

> O projeto usa `system-ui` sem sobrescrever a font family do Bootstrap.

## Tamanho base

| Propriedade | Valor |
|---|---|
| `font-size` (root) | `16px` (1rem) |
| `line-height` (base) | `1.5` |
| `color` (base) | `#212529` (`--bs-body-color`) |

## Escala de headings

| Tag / Classe | Tamanho | Line-height | Peso | Usado em |
|---|---|---|---|---|
| `h1` / `.h1` | `2.5rem` (40px) | `1.2` | 700 | — |
| `h2` / `.h2` | `2rem` (32px) | `1.2` | 700 | — |
| `h3` / `.h3` | `1.75rem` (28px) | `1.2` | 700 | — |
| `h4` / `.card-title` | `1.5rem` (24px) | `1.2` | 700 | LoginPage, RegisterPage (título do card) |
| `h5` / `.modal-title` | `1.25rem` (20px) | `1.2` | 700 | Modal titles, ViewHeader board title |
| `h6` / `.h6` | `1rem` (16px) | `1.2` | 700 | Sidebar workspace name |

## Escala de font-size (classes utilitárias)

| Classe | Tamanho | Onde |
|---|---|---|
| `fs-1` | `2.5rem` | — |
| `fs-2` | `2rem` | — |
| `fs-3` | `1.75rem` | — |
| `fs-4` | `1.5rem` | — |
| `fs-5` | `1.25rem` | Ícone emoji do board (ViewHeader) |
| `fs-6` | `1rem` | — |
| `.small` | `0.875em` (14px) | Labels, textos secundários, botões da sidebar, flash messages |
| Inline `font-size: 11px` | `11px` | Avatar circular (inicial do username) |

## Font Weights

| Classe | Peso | Onde |
|---|---|---|
| `fw-normal` | `400` | Padrão do body |
| `fw-semibold` | `600` | Labels de seção na sidebar ("Boards", "Categories") |
| `fw-bold` | `700` | Headings |

## Utilitários tipográficos usados

| Classe | Efeito | Onde |
|---|---|---|
| `text-truncate` | `overflow: hidden; text-overflow: ellipsis` | Títulos de boards na sidebar |
| `text-center` | `text-align: center` | Títulos de cards nas páginas de auth |
| `text-start` | `text-align: start` | Botão do usuário na sidebar |

## Hierarquia semântica aplicada

```
h4 — Título da página (Login, Register card)
  h5 — Títulos de modais (Share Board, Card Detail)
    h6 — Nome do workspace/equipe na sidebar
      .small — Texto auxiliar, contadores, labels
        inline 11px — Avatar de usuário
```
