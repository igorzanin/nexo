# Páginas — Componentes de Rota (Vue Router)

## Visão Geral
Componentes de página do frontend Vue 3 que correspondem às rotas da aplicação. Inclui páginas de autenticação (login, registro, alterar senha), página de erro, e a página principal de workspace (BoardPage) com seus sub-componentes auxiliares.

## Stack

| Componente | Tecnologia |
|------------|-----------|
| Router | Vue Router (history mode) |
| UI | Bootstrap 5.3 |

## Responsabilidades (mantidas)
- LoginPage: autenticar usuário com username/senha e redirecionar
- RegisterPage: criar nova conta de usuário com token de signup opcional
- ChangePasswordPage: permitir usuário logado alterar sua senha
- ErrorPage: exibir erro legível com base no parâmetro `?id=` e botões de ação contextuais
- BoardPage: workspace principal — carrega board, gerencia WebSocket, join em boards privados
- TeamToBoardAndViewRedirect: garantir que a URL tenha boardId e viewId válidos
- SetWindowTitleAndIcon: definir título da aba e favicon dinamicamente
- UndoRedoHotKeys: atalhos globais Ctrl+Z / Ctrl+Shift+Z
- WebsocketConnection: monitorar conexão WebSocket e exibir banner de alerta

## Rotas

| Caminho | Componente | Requer Auth |
|---------|-----------|-------------|
| `/login` | `LoginPage.vue` | Não |
| `/register` | `RegisterPage.vue` | Não |
| `/change_password` | `ChangePasswordPage.vue` | Não (trata internamente) |
| `/error` | `ErrorPage.vue` | Não |
| `/board/:boardId?/:viewId?/:cardId?` | `BoardPage.vue` | Sim |
| `/team/:teamId/:boardId?/:viewId?/:cardId?` | `BoardPage.vue` | Sim |
| `/team/:teamId/shared/:boardId?/:viewId?/:cardId?` | `BoardPage.vue` | Não (read-only) |
| `/shared/:boardId?/:viewId?/:cardId?` | `BoardPage.vue` | Não (read-only) |
| `/` | `BoardPage.vue` | Sim |

## Rastreabilidade

| Página legada | Componente Vue | Confiança |
|--------------|----------------|-----------|
| `loginPage.tsx` | `LoginPage.vue` | 🟢 |
| `registerPage.tsx` | `RegisterPage.vue` | 🟢 |
| `changePasswordPage.tsx` | `ChangePasswordPage.vue` | 🟢 |
| `errorPage.tsx` | `ErrorPage.vue` | 🟢 |
| `boardPage/boardPage.tsx` | `BoardPage.vue` | 🟢 |
| `boardPage/teamToBoardAndViewRedirect.tsx` | `composables/useTeamRedirect.ts` | 🟢 |
| `boardPage/setWindowTitleAndIcon.tsx` | `composables/useTitleAndIcon.ts` | 🟢 |
| `boardPage/undoRedoHotKeys.tsx` | `composables/useUndoRedo.ts` | 🟢 |
| `boardPage/websocketConnection.tsx` | `composables/useWebSocket.ts` | 🟢 |
