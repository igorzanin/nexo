# Spec: Páginas (Vue Router)

> Gerado por `/reversa-coding` (T008)
> Fonte legado: `focalboard-legacy/webapp/src/pages/`
> Stack alvo: Vue 3 + Composition API + Bootstrap 5.3 + Vue Router
> 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## 1. WelcomePage (NOVA)

### Origem legado
`focalboard-legacy/webapp/src/pages/welcome/` — onboarding tour

### Comportamento
- Exibida na primeira vez que o usuário acessa o sistema
- Tour guiado com etapas: Board, Card, ShareBoard
- Estado de conclusão persistido em configuração do usuário

### Design alvo
```vue
<script setup lang="ts">
// Estado controlado por userStore.myConfig.onboardingComplete
// Etapas: board-step, card-step, share-step
// Botão "Pular tour" no final
</script>
```

### Estados
| Estado | Comportamento |
|--------|---------------|
| Loading | Esqueleto de carregamento |
| Step 1 | Introdução ao Board (criar primeiro board) |
| Step 2 | Introdução ao Card (criar primeiro card) |
| Step 3 | Introdução ao Share (compartilhar board) |
| Complete | Botão "Ir para o Workspace" |
| Skipped | Redireciona para BoardPage |

### Rota
`/welcome` — requer autenticação

---

## 2. LoginPage

### Origem legado
`focalboard-legacy/webapp/src/pages/loginPage.tsx`

### Comportamento
- Formulário de login com username + senha
- Validação de campos obrigatórios
- Exibição de erro de autenticação (credenciais inválidas)
- Link para registro
- Rate limiting no servidor

### Status novo
✅ `pages/LoginPage.vue` — verificar paridade de estados

### Verificações pendentes
- [ ] Estado de loading durante requisição
- [ ] Mensagem de erro específica (não genérica)
- [ ] Redirect após login bem-sucedido para página anterior

### Rota
`/login` — sem autenticação

---

## 3. RegisterPage

### Origem legado
`focalboard-legacy/webapp/src/pages/registerPage.tsx`

### Comportamento
- Formulário de registro com username, email, senha, confirmar senha
- Validação: senha ≥ 8 caracteres, email válido, senhas coincidem
- Token de signup opcional (para convites)
- Rate limiting

### Status novo
✅ `pages/RegisterPage.vue` — verificar paridade

### Verificações pendentes
- [ ] Validação de força de senha
- [ ] Token de signup na URL (`?t=token`)
- [ ] Redirect após registro

### Rota
`/register` — sem autenticação

---

## 4. ChangePasswordPage

### Origem legado
`focalboard-legacy/webapp/src/pages/changePasswordPage.tsx`

### Comportamento
- Formulário: senha atual + nova senha + confirmar nova senha
- Validação: nova senha ≥ 8, diferente da atual
- Token de reset opcional para fluxo "esqueci senha"

### Status novo
✅ `pages/ChangePasswordPage.vue` — verificar paridade

### Verificações pendentes
- [ ] Fluxo "esqueci senha" com token de reset
- [ ] Mensagens de erro específicas

### Rota
`/change_password` — não requer auth (token interno)

---

## 5. ErrorPage

### Origem legado
`focalboard-legacy/webapp/src/pages/errorPage.tsx`

### Comportamento
- Exibe mensagem de erro com base no parâmetro `?id=`
- Botões de ação contextuais (voltar, tentar novamente, login)
- Ícone de erro ilustrativo

### Status novo
✅ `pages/ErrorPage.vue` — verificar paridade

### Rota
`/error?id=<code>`

### Códigos de erro
| Código | Mensagem | Ação |
|--------|----------|------|
| `not-logged-in` | Sessão expirada | Ir para login |
| `board-not-found` | Board não encontrado | Voltar ao workspace |
| `team-not-found` | Time não encontrado | Voltar ao workspace |
| `system-error` | Erro interno | Tentar novamente |

---

## 6. BoardPage

### Origem legado
`focalboard-legacy/webapp/src/pages/boardPage/boardPage.tsx`

### Comportamento
- Workspace principal: carrega board, gerencia WebSocket, join em boards privados
- Workspace → Sidebar + CenterPanel (Kanban/Table/Calendar/Gallery)
- Undo/Redo via Ctrl+Z / Ctrl+Shift+Z
- Título da aba dinâmico
- Banner de conexão WebSocket

### Status novo
✅ `pages/board/` — verificar paridade

### Verificações pendentes
- [ ] Undo/Redo com atalhos globais
- [ ] Título da aba dinâmico (`document.title`)
- [ ] Banner de reconexão WebSocket
- [ ] Redirect automático entre team/board/view
- [ ] Join automático em boards privados com readToken

### Rotas
| Caminho | Requer Auth |
|---------|-------------|
| `/board/:boardId?/:viewId?/:cardId?` | Sim |
| `/team/:teamId/:boardId?/:viewId?/:cardId?` | Sim |
| `/team/:teamId/shared/:boardId?/:viewId?/:cardId?` | Não (readToken) |
| `/shared/:boardId?/:viewId?/:cardId?` | Não (readToken) |
| `/` | Sim |

---

## Histórico

| Data | Alteração |
|------|-----------|
| 2026-05-14 | Spec gerada por `/reversa-coding` |
