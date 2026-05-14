# Data Delta — Transcrição completa do frontend legado

> Feature: `001-frontend-full-transcription`
> Data: `2026-05-14`

## Premissa

Esta feature **não altera o modelo de dados do backend**. O backend (Python FastAPI + SQLAlchemy) permanece inalterado. O delta descrito aqui é exclusivamente sobre modelos de dados do **frontend** (tipos TypeScript, interfaces, stores).

## 1. Tipos TypeScript (blocks/)

### Estado atual (`_reversa_sdd/blocos/requirements.md`)
| Interface | Status |
|-----------|--------|
| `Block` | ✅ Implementado |
| `Board` | ✅ Implementado |
| `Card` | ✅ Implementado |
| `BoardView` | ✅ Implementado |
| `FilterGroup` / `FilterClause` | ✅ Implementado |
| `IUser` / `ITeam` | ✅ Implementado |

### Possíveis lacunas
| Tipo legado | Status | Ação necessária |
|-------------|--------|-----------------|
| `ISharing` (sharing.ts) | 🔴 Não verificado | Verificar existência e criar se ausente |
| `Category` | 🔴 Não verificado | Modelo de categoria pode precisar de tipo específico |
| `Subscription` | 🔴 Não verificado | Pode estar usando tipo inline |

### Factories
| Factory | Status |
|---------|--------|
| `createBlock`, `createCard`, `createBoard`, `createBoardView` | ✅ |
| `createTextBlock`, `createImageBlock`, `createCheckboxBlock` | ✅ |
| `createDividerBlock`, `createCommentBlock`, `createAttachmentBlock` | ✅ |
| `createH1Block`, `createH2Block`, `createH3Block` | ✅ |
| `createContentBlock`, `createFilterClause`, `createFilterGroup` | ✅ |
| Factories de workspace, team, sharing | 🔴 Não verificado |

## 2. Stores Pinia

### Estado atual
| Store | Status |
|-------|--------|
| `useBoardStore` | ✅ |
| `useCardStore` | ✅ |
| `useViewStore` | ✅ |
| `useUserStore` | ✅ |
| `useTeamStore` | ✅ |
| `useCommentStore` | ✅ |
| `useContentStore` | ✅ |
| `useAttachmentStore` | ✅ |
| `useSidebarStore` | ✅ |
| `useSearchStore` | ✅ |
| `useConfigStore` | ✅ |
| `useErrorStore` | ✅ |
| `useTemplateStore` | ✅ |
| `useLanguageStore` | ✅ |

### Possíveis lacunas
| Store legada | Store Pinia | Status |
|-------------|-------------|--------|
| `attachments.ts` | `useAttachmentStore` | ✅ (verificar getters/actions) |
| `boards.ts` | `useBoardStore` | ✅ (verificar getters/actions) |
| `cards.ts` | `useCardStore` | ✅ (verificar getters/actions) |
| `channels.ts` | ❌ N/A | Excluído (Mattermost) |
| `clientConfig.ts` | `useConfigStore` | ✅ (verificar) |
| `comments.ts` | `useCommentStore` | ✅ (verificar) |
| `contents.ts` | `useContentStore` | ✅ (verificar) |
| `globalError.ts` | `useErrorStore` | ✅ (verificar) |
| `globalTemplates.ts` | `useTemplateStore` | ✅ (verificar) |
| `hooks.ts` | 🔴 Não verificado | Verificar se existe store equivalente |
| `initialLoad.ts` | 🔴 `initialLoad` action | Verificar se a action de boot está completa |
| `language.ts` | `useLanguageStore` | ✅ (verificar) |
| `limits.ts` | 🔴 Não existe | Criar store se necessário |
| `searchText.ts` | `useSearchStore` | ✅ (verificar) |
| `sidebar.ts` | `useSidebarStore` | ✅ (verificar) |
| `teams.ts` | `useTeamStore` | ✅ (verificar) |
| `users.ts` | `useUserStore` | ✅ (verificar) |
| `views.ts` | `useViewStore` | ✅ (verificar) |

## 3. Novos estados de componente

Nenhum novo estado de dados. Componentes podem precisar de novos estados de UI (loading, empty, error) que não existem hoje, mas isso é estado local do componente, não modelo de dados global.

## 4. Migrações

Nenhuma migração de banco de dados necessária.
