# Color Palette

> Design system do Nexo webapp — Vue 3 + Bootstrap 5.3.3 (sem overrides customizados).
> **Fonte:** `webapp/package.json`, `webapp/index.html`, análise de componentes `.vue`.
> Gerado por: reversa-design-system

## Notas de contexto

O webapp não define variáveis CSS ou tokens próprios. O design system **é o Bootstrap 5.3 padrão**.
A coluna "Usado em" lista onde cada cor aparece no código-fonte atual.

---

## Cores semânticas (Bootstrap 5.3 defaults)

| Token BS | Hex | Descrição | Confiança | Usado em |
|---|---|---|---|---|
| `--bs-primary` | `#0d6efd` | Azul primário | 🟢 | `btn-primary`, `btn-outline-primary`, `text-primary`, `bg-primary` |
| `--bs-secondary` | `#6c757d` | Cinza secundário | 🟢 | `btn-outline-secondary`, `bg-secondary`, `badge bg-secondary` |
| `--bs-success` | `#198754` | Verde sucesso | 🟢 | `text-bg-success` (flash messages) |
| `--bs-danger` | `#dc3545` | Vermelho erro/perigo | 🟢 | `btn-outline-danger`, `alert-danger`, `text-danger`, `text-bg-danger` |
| `--bs-warning` | `#ffc107` | Amarelo alerta | 🟢 | Disponível (não usado diretamente) |
| `--bs-info` | `#0dcaf0` | Ciano informação | 🟢 | Disponível (não usado diretamente) |
| `--bs-light` | `#f8f9fa` | Cinza muito claro | 🟢 | `bg-light` (sidebar, páginas de login/register, cards) |
| `--bs-dark` | `#212529` | Quase preto | 🟢 | Disponível (não usado diretamente) |
| `--bs-white` | `#ffffff` | Branco | 🟢 | `bg-white` (ViewHeader), modal backgrounds |

## Variações de primary utilizadas

| Classe | Valor | Onde |
|---|---|---|
| `bg-primary bg-opacity-10` | `rgba(13, 110, 253, 0.10)` | Item de board ativo na sidebar |
| `text-primary` | `#0d6efd` | Texto do board ativo |
| `btn-primary` | `#0d6efd` bg, `#fff` text | Botão "New Board", "Sign in", "Create account", etc. |
| `btn-outline-primary` | border+text `#0d6efd` | "+ Add Card", "+ Card" |

## Cores de texto

| Classe | Hex aproximado | Uso |
|---|---|---|
| `text-muted` | `#6c757d` | Subtítulos, placeholders, labels secundários |
| `text-danger` | `#dc3545` | Mensagens de erro inline |
| `text-white` | `#ffffff` | Texto em avatar circular |
| `text-dark` (default) | `#212529` | Texto base do body |

## Escala de cinzas Bootstrap 5

| Nome | Hex |
|---|---|
| gray-100 | `#f8f9fa` |
| gray-200 | `#e9ecef` |
| gray-300 | `#dee2e6` |
| gray-400 | `#ced4da` |
| gray-500 | `#adb5bd` |
| gray-600 | `#6c757d` |
| gray-700 | `#495057` |
| gray-800 | `#343a40` |
| gray-900 | `#212529` |

## Cores de feedback visual (flash messages / toasts)

Usa `text-bg-{type}` do Bootstrap:

| Tipo | Classe | Bg | Texto |
|---|---|---|---|
| Sucesso | `text-bg-success` | `#198754` | `#fff` |
| Erro | `text-bg-danger` | `#dc3545` | `#fff` |
| Alerta | `text-bg-warning` | `#ffc107` | `#000` |
| Info | `text-bg-info` | `#0dcaf0` | `#000` |

## Observação: legado Focalboard vs. webapp atual

As screenshots documentadas pelo `reversa-visor` mostram o sistema **legado Focalboard**, que possui uma paleta distinta (sidebar azul-escura `#1e2a3a` / `#2d3748`, backgrounds brancos, badges coloridas). Essa paleta é **do legado** e não corresponde ao novo `webapp/` Vue 3 + Bootstrap.
