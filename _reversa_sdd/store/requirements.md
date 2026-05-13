# Store — Gerenciamento de Estado (Pinia)

## Visão Geral
Camada de estado global do frontend Vue 3, implementada com Pinia. Gerencia 14 stores que cobrem boards, cards, usuários, times, visualizações, blocos de conteúdo, comentários, anexos, sidebar, preferências e configuração do cliente. Toda mutação passa pelo Mutator, que persiste no servidor via API REST e depois dispatches ações Pinia.

## Stack

| Componente | Vue 3 |
|------------|-------|
| State management | Pinia |
| HTTP client | axios |
| WebSocket | WebSocket nativo |
| Build | Vite |

## Responsabilidades
- Gerenciar estado global de boards, cards, views, usuários e times
- Gerenciar estado de blocos de conteúdo, comentários e anexos por card
- Gerenciar categorias da sidebar e ordenação de boards
- Gerenciar preferências do usuário, onboarding e configuração do cliente
- Prover getters composables para consulta eficiente
- Prover actions assíncronas para CRUD via API

## Regras de Negócio (mantidas)
- Store é criada com `defineStore` do Pinia 🟢
- Toda escrita de dados passa pelo Mutator (API + dispatch), exceto atualizações via WebSocket 🟢
- `initialLoad` é a action de boot que hidrata todas as stores na carga da página 🟢
- Getters complexos cruzam múltiplas stores 🟢
- Comentários, conteúdos e anexos são armazenados por card pai 🟢
- Sidebar gerencia categorias customizadas e ocultação de boards 🟢

## Stores

| Store | Estado | Descrição |
|-------|--------|-----------|
| `useBoardStore` | `current`, `boards`, `templates`, `membersInBoards`, `myBoardMemberships` | Boards |
| `useCardStore` | `current`, `cards`, `templates` | Cards com getters complexos |
| `useViewStore` | `current`, `views` | Views com smartViewUpdate |
| `useUserStore` | `me`, `boardUsers`, `loggedIn`, `blockSubscriptions`, `myConfig` | Usuários |
| `useTeamStore` | `current`, `currentId`, `allTeams` | Times |
| `useCommentStore` | `comments`, `commentsByCard` | Comentários |
| `useContentStore` | `contents`, `contentsByCard` | Conteúdos de blocos |
| `useAttachmentStore` | `attachments`, `attachmentsByCard` | Anexos |
| `useSidebarStore` | `categoryAttributes`, `hiddenBoardIDs` | Sidebar |
| `useSearchStore` | `value` | Busca |
| `useConfigStore` | `value` | Config do cliente |
| `useErrorStore` | `value` | Erro global |
| `useTemplateStore` | `value` | Templates globais |
| `useLanguageStore` | `value` | Idioma |

## Rastreabilidade

| Store legado (Redux slice) | Nova store Pinia | Confiança |
|---------------------------|-----------------|-----------|
| `boards.ts` | `useBoardStore` | 🟢 |
| `cards.ts` | `useCardStore` | 🟢 |
| `views.ts` | `useViewStore` | 🟢 |
| `users.ts` | `useUserStore` | 🟢 |
| `teams.ts` | `useTeamStore` | 🟢 |
| `comments.ts` | `useCommentStore` | 🟢 |
| `contents.ts` | `useContentStore` | 🟢 |
| `attachments.ts` | `useAttachmentStore` | 🟢 |
| `sidebar.ts` | `useSidebarStore` | 🟢 |
| `searchText.ts` | `useSearchStore` | 🟢 |
| `clientConfig.ts` | `useConfigStore` | 🟢 |
| `globalError.ts` | `useErrorStore` | 🟢 |
| `globalTemplates.ts` | `useTemplateStore` | 🟢 |
| `language.ts` | `useLanguageStore` | 🟢 |
