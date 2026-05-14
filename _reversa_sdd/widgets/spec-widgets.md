# Spec: Widgets Reutilizáveis

> Gerado por `/reversa-coding` (T010)
> Fonte legado: `focalboard-legacy/webapp/src/widgets/`
> Stack alvo: Vue 3 + Composition API + Bootstrap 5.3 + TypeScript
> 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## 1. Editable

Input inline que alterna entre display e edição.

| Aspecto | Descrição |
|---------|-----------|
| Uso | Editar título de board, view, card |
| Comportamento | Click → input, Enter salva, Escape cancela, blur salva |
| Props | `value`, `placeholder`, `validator`, `multiline` |
| Bootstrap | `form-control` + `border-0` + `bg-transparent` |

**Estados:** display, editing, saving, error

## 2. EditableArea

Versão multilinha do Editable.

| Aspecto | Descrição |
|---------|-----------|
| Uso | Editar descrições, conteúdo de texto |
| Bootstrap | `<textarea class="form-control">` |

## 3. EditableDayPicker

Editable com date picker integrado.

| Aspecto | Descrição |
|---------|-----------|
| Uso | Editar data de propriedade |
| Bootstrap | `<input type="date">` |

## 4. Menu

Dropdown de opções.

| Aspecto | Descrição |
|---------|-----------|
| Uso | Menus de ação (kebab menu, view header, etc.) |
| Comportamento | Click abre, click fora fecha, teclado (setas + Enter) |
| Bootstrap | `dropdown-menu` + Popper.js |
| Slots | `default` (itens), `trigger` |

**Estados:** closed, open

## 5. MenuWrapper

Wrapper que controla abertura/fechamento do Menu.

| Aspecto | Descrição |
|---------|-----------|
| Uso | Envolver trigger + menu |
| Comportamento | Gerencia toggle, posicionamento, fechamento |

## 6. PropertyMenu

Menu específico para configuração de propriedades.

| Aspecto | Descrição |
|---------|-----------|
| Uso | Renomear, duplicar, ocultar, alterar tipo de propriedade |
| Itens | Hide, Duplicate, Rename, Change Type, Delete |

## 7. ValueSelector

Seletor de valores de propriedade (opções de select/multiSelect).

| Aspecto | Descrição |
|---------|-----------|
| Uso | Selecionar/alterar valor de propriedade select |
| Itens | Lista de opções + "Empty" |

## 8. EmojiPicker

Seletor de emoji para ícone de board/card.

| Aspecto | Descrição |
|---------|-----------|
| Uso | Escolher emoji como ícone |
| Bootstrap | Modal ou Popover com grade de emojis |
| Dados | Lista de emojis (unicode) |

## 9. Switch

Toggle switch.

| Aspecto | Descrição |
|---------|-----------|
| Uso | Ativar/desativar configurações |
| Bootstrap | `form-check-input` com estilo switch |
| Props | `modelValue`, `disabled`, `label` |

## 10. Label

Badge de cor para propriedades select/multiSelect.

| Aspecto | Descrição |
|---------|-----------|
| Uso | Exibir valor de select com cor |
| Bootstrap | `badge` com background color custom |
| Props | `text`, `color`, `size` |

## 11. Tooltip

Tooltip de hover.

| Aspecto | Descrição |
|---------|-----------|
| Uso | Informação adicional em hover |
| Bootstrap | `data-bs-toggle="tooltip"` ou componente custom |

## 12. GuestBadge

Badge de usuário convidado.

| Aspecto | Descrição |
|---------|-----------|
| Uso | Indicar que usuário é guest no board |
| Bootstrap | `badge bg-warning` |

## 13. AdminBadge

Badge de administrador.

| Uso | Indicar que usuário é admin no board |
| Bootstrap | `badge bg-primary` |

## 14. NotificationBox

Caixa de notificações.

| Aspecto | Descrição |
|---------|-----------|
| Uso | Configurar notificações por inscrição em blocos |

## 15. PersonSelector

Seletor de pessoas.

| Aspecto | Descrição |
|---------|-----------|
| Uso | Selecionar usuário para propriedade person |
| Dados | Lista de usuários do board |
| Bootstrap | Dropdown com busca |

## 16. IconSelector

Seletor de ícone para board.

| Aspecto | Descrição |
|---------|-----------|
| Uso | Escolher ícone do board |
| Bootstrap Icons | Grade de ícones Bootstrap |

## 17. ConfirmationDialogBox

Caixa de confirmação.

| Aspecto | Descrição |
|---------|-----------|
| Uso | Confirmar ações destrutivas (delete, etc.) |
| Bootstrap | Modal de confirmação |
| Props | `title`, `message`, `confirmText`, `cancelText`, `variant` |

## 18. Dialog

Diálogo modal reutilizável.

| Aspecto | Descrição |
|---------|-----------|
| Bootstrap | `modal` + `modal-dialog` + `modal-content` |
| Slots | `header`, `body`, `footer` |

## 19. Modal

Modal de tela cheia.

| Aspecto | Descrição |
|---------|-----------|
| Bootstrap | `modal-fullscreen` ou `modal-lg` |

## 20. RootPortal

Portal para renderizar conteúdo no root do DOM.

| Vue | `Teleport to="body"` |

## Histórico

| Data | Alteração |
|------|-----------|
| 2026-05-14 | Spec gerada por `/reversa-coding` |
