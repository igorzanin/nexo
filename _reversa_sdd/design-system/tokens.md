# Design System Tokens — Focalboard Legacy

> Gerado por `/reversa-coding` (T002)
> Data: `2026-05-14`
> Fonte: `focalboard-legacy/webapp/src/styles/`
> Stack alvo: Bootstrap 5.3 + CSS custom properties
> 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## 1. Cores

### 1.1 Core Tokens (CSS Custom Properties)

| Token legado | Valor | Cor | Mapeamento Bootstrap |
|-------------|-------|-----|---------------------|
| `--center-channel-bg-rgb` | `255, 255, 255` | Branco | `var(--bs-white)` ou `$white` |
| `--center-channel-color-rgb` | `63, 67, 80` | Cinza escuro | `var(--bs-dark)` ou `$gray-800` |
| `--sidebar-bg-rgb` | `30, 50, 92` | Azul escuro | `var(--bs-primary-dark)` ou custom |
| `--sidebar-text-rgb` | `255, 255, 255` | Branco | `var(--bs-light)` |
| `--button-color-rgb` | `255, 255, 255` | Branco | `var(--bs-btn-color)` |
| `--button-bg-rgb` | `28, 88, 217` | Azul | `var(--bs-primary)` |
| `--button-danger-color-rgb` | `255, 255, 255` | Branco | `var(--bs-danger-btn-color)` |
| `--button-danger-bg-rgb` | `210, 75, 78` | Vermelho | `var(--bs-danger)` |
| `--link-color-rgb` | `56, 111, 229` | Azul link | `var(--bs-link-color)` |
| `--error-text-rgb` | `#d24b4e` | Vermelho erro | `var(--bs-danger-text)` |
| `--link-visited-color-rgb` | `#551a8b` | Roxo | `var(--bs-link-color-visited)` |

### 1.2 Label/Property Colors

| Token legado | Cor | Mapeamento Bootstrap |
|-------------|-----|---------------------|
| `--prop-default` | `#ffffff` | `var(--bs-light)` |
| `--prop-gray` | `#ededed` | `var(--bs-gray-200)` |
| `--prop-brown` | `#f7ddc3` | Custom |
| `--prop-orange` | `#ffd3c1` | `var(--bs-orange-100)` |
| `--prop-yellow` | `#f7f0b6` | `var(--bs-warning-100)` |
| `--prop-green` | `#c7eac3` | `var(--bs-success-100)` |
| `--prop-blue` | `#b1d1f6` | `var(--bs-primary-100)` |
| `--prop-purple` | `#e6d0ff` | Custom |
| `--prop-pink` | `#ffd6e9` | Custom |
| `--prop-red` | `#ffa9a9` | `var(--bs-danger-100)` |

---

## 2. Tipografia

### 2.1 Font Family

| Propriedade | Valor legado | Mapeamento Bootstrap |
|------------|-------------|---------------------|
| Font padrão | `Open Sans, sans-serif` | `$font-family-sans-serif` (Bootstrap) |
| Font headings | `Metropolis, sans-serif` | `$headings-font-family` (custom) |
| Font weight semibold | `600` | `$font-weight-semibold` |

### 2.2 Font Sizes

| Classe legada | Size | Mapeamento Bootstrap |
|--------------|------|---------------------|
| `.text-heading8` | 32px | `fs-1` (2.5rem = 40px) 🟡 |
| `.text-heading7` | 28px | `fs-2` (2rem = 32px) 🟡 |
| `.text-heading6` | 25px | Custom |
| `.text-heading5` | 22px | Custom |
| `.text-heading4` | 20px | `fs-5` (1.25rem = 20px) ✅ |
| `.text-heading3` | 18px | `fs-6` (1rem = 16px) 🟡 |
| `.text-heading2` | 16px | `fs-6` (1rem = 16px) ✅ |
| `.text-heading1` | 14px | `.small` |
| `.text-base` | 16px | `fs-6` |
| `.text-75` | 12px | `small` |

---

## 3. Elevations (Shadows)

| Token legado | Valor | Mapeamento Bootstrap |
|-------------|-------|---------------------|
| `--elevation-1` | `0 2px 3px 0 rgba(0,0,0,0.08)` | `shadow-sm` |
| `--elevation-2` | `0 4px 6px 0 rgba(0,0,0,0.12)` | `shadow` |
| `--elevation-3` | `0 6px 14px 0 rgba(0,0,0,0.12)` | `shadow` 🟡 |
| `--elevation-4` | `0 8px 24px 0 rgba(0,0,0,0.12)` | `shadow-lg` |
| `--elevation-5` | `0 12px 32px 0 rgba(0,0,0,0.12)` | `shadow-lg` 🟡 |
| `--elevation-6` | `0 20px 32px 0 rgba(0,0,0,0.12)` | Custom |

---

## 4. Border Radius

| Token legado | Valor | Mapeamento Bootstrap |
|-------------|-------|---------------------|
| `--default-rad` | 4px | `rounded-1` |
| `--modal-rad` | 8px | `rounded-2` |

---

## 5. Z-Index Map

| Key legado | Valor | Mapeamento Bootstrap |
|-----------|-------|---------------------|
| `modal-permissions-label` | 1000 | `$zindex-tooltip` (1080) |
| `board-template-selector` | 1000 | `$zindex-dropdown` (1000) |
| `notification-box` | 1000 | `$zindex-popover` (1070) |
| `calculation-dropdown` | 999 | `$zindex-dropdown` (1000) |
| `flash-messages` | 999 | Custom |
| `tour-tip-backdrop` | 999 | `$zindex-modal-backdrop` (1040) |
| `tour-tip-overlay` | 999 | `$zindex-modal` (1055) |
| `confirmation-dialog-box` | 300 | `$zindex-modal` (1055) |
| `dialog-back` | 200 | `$zindex-modal-backdrop` (1040) |
| `sidebar-hidden` | 105 | Custom |
| `center-panel` | 100 | `z-index-1` |
| `hover-tooltip-body` | 100 | `$zindex-tooltip` (1080) |
| `menu` | 15 | `$zindex-dropdown` (1000) |
| `modal` | 10 | `$zindex-modal` (1055) |

---

## 6. Spacing

O legado usa `_modifiers.scss` com classes utilitárias:
- Padding: `.p{t|b|l|r}-{0-20}` (incrementos de 4px)
- Margin: `.m{t|b|l|r}-{0-20}` (incrementos de 4px)
- `px-{0-20}`, `py-{0-20}`

**Mapeamento Bootstrap:**
- `p-{1-5}` equivale aproximadamente a `p-4, p-8, p-16, p-24, p-48`
- Classes Bootstrap `gap-{1-5}`, `m-{1-5}`, `p-{1-5}` são preferíveis
- Para valores específicos, usar CSS custom properties ou utilitários adicionais

---

## 7. Breakpoints

O legado não define breakpoints customizados. Bootstrap 5.3 fornece:
| Breakpoint | Largura |
|-----------|---------|
| `xs` | <576px |
| `sm` | ≥576px |
| `md` | ≥768px |
| `lg` | ≥992px |
| `xl` | ≥1200px |
| `xxl` | ≥1400px |

---

## Recomendações

1. **Cores sidebar:** Criar variáveis CSS custom `--nexo-sidebar-bg` e `--nexo-sidebar-text` para substituir `--sidebar-bg-rgb` / `--sidebar-text-rgb`
2. **Cores de label:** Manter como variáveis CSS `--prop-{color}` no novo sistema, mapeando quando possível para cores Bootstrap
3. **Font Metropolis:** Manter (já presente em `webapp/src/fonts/`) ou substituir por font system do Bootstrap
4. **Elevations:** Usar classes `shadow-*` do Bootstrap, com variante custom para elevation-3, 5, 6
5. **Z-index:** Usar variáveis `$zindex-*` do Bootstrap, com exceções no `$zindex-custom` próprio
6. **Spacing:** Adotar sistema de spacing do Bootstrap (`p-*`, `m-*`, `gap-*`), criar utilitários extras se necessário
