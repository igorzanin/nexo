# Páginas, Design Técnico

## Estrutura

```
nexo/webapp/src/
├── pages/
│   ├── LoginPage.vue
│   ├── RegisterPage.vue
│   ├── ChangePasswordPage.vue
│   ├── ErrorPage.vue
│   └── board/
│       ├── BoardPage.vue
│       └── router.ts           # Configuração do Vue Router
├── composables/
│   ├── useTeamRedirect.ts       # TeamToBoardAndViewRedirect
│   ├── useTitleAndIcon.ts      # SetWindowTitleAndIcon
│   ├── useUndoRedo.ts          # UndoRedoHotKeys
│   └── useWebSocket.ts         # WebSocket connection monitor
└── router/
    └── index.ts                # Vue Router setup
```

## Vue Router Configuration

```typescript
// router/index.ts
const routes = [
  { path: '/login', component: () => import('@/pages/LoginPage.vue') },
  { path: '/register', component: () => import('@/pages/RegisterPage.vue') },
  { path: '/change_password', component: () => import('@/pages/ChangePasswordPage.vue') },
  { path: '/error', component: () => import('@/pages/ErrorPage.vue') },
  {
    path: '/board/:boardId?/:viewId?/:cardId?',
    component: () => import('@/pages/board/BoardPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/team/:teamId/shared/:boardId?/:viewId?/:cardId?',
    component: () => import('@/pages/board/BoardPage.vue'),
    meta: { readonly: true }
  },
  { path: '/:boardId?/:viewId?/:cardId?', redirect: '/board/:boardId/:viewId/:cardId' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    return `/login?r=${to.fullPath}`
  }
})
```

## Páginas

| Página | Template Bootstrap |
|--------|-------------------|
| LoginPage | Formulário centralizado com `card` Bootstrap |
| RegisterPage | Formulário com validação inline |
| ChangePasswordPage | Formulário com feedback |
| ErrorPage | `alert` Bootstrap com botões contextuais |
| BoardPage | Layout fluido com sidebar + workspace |

## Erros

| ErrorId | Mensagem | Ação |
|---------|----------|------|
| `not-logged-in` | Sessão expirada | Link para login |
| `board-not-found` | Board não encontrado | Link para home |
| `invalid-read-only-board` | Sem acesso | Link para login |
| unknown | Erro desconhecido | Link para home |
