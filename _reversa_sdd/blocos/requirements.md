# Blocos — Modelos de Dados e Factories (TypeScript)

## Visão Geral
Camada de definição de tipos e modelos de dados do frontend Vue 3. Contém todas as interfaces TypeScript que definem a estrutura dos dados da aplicação: Block (base), Board, Card, BoardView, ContentBlock, CommentBlock, AttachmentBlock e seus subtipos de conteúdo. Inclui factories para criação de instâncias e utilitários de diff/patch para suporte a undo/redo.

## Stack

| Componente | Tecnologia |
|------------|-----------|
| Language | TypeScript 5+ |
| Build | Vite |
| Test | Vitest |

## Regras de Negócio (mantidas do legado)
- Block é a base universal; Board, Card, BoardView, CommentBlock estendem Block por composição de tipo 🟢
- Board é um tipo separado (não extende Block) com cardProperties (schema de colunas) 🟢
- Card tem fields.contentOrder que define a ordem dos blocos de conteúdo filhos 🟢
- BoardView tem fields.filter como árvore aninhada de FilterGroup/FilterClause 🟢
- Propriedades de card (IPropertyTemplate) são definidas no Board e referenciadas por ID nos Cards 🟢
- Factories deep-clone arrays e objetos para prevenir mutação acidental 🟢
- Patches (BlockPatch, BoardPatch) suportam campos opcionais para delta tracking em undo/redo 🟢

## Interfaces (mantidas do legado — inalteradas)

| Interface | Definição | Uso |
|-----------|-----------|-----|
| `Block` | `{ id, boardId, parentId, type, title, fields, schema, createAt, updateAt, deleteAt }` | Base universal |
| `Board` | `{ id, teamId, type, minimumRole, title, cardProperties, ... }` | Board |
| `Card` | `{ ...Block, fields: { icon, isTemplate, properties, contentOrder } }` | Card |
| `BoardView` | `{ ...Block, fields: { viewType, groupById, sortOptions, filter, cardOrder } }` | View |
| `IPropertyTemplate` | `{ id, name, type, options[] }` | Schema de colunas |
| `FilterGroup` | `{ operation: 'and'|'or', filters[] }` | Filtros aninhados |
| `FilterClause` | `{ propertyId, condition, values[] }` | Condição de filtro |
| `IUser` | `{ id, username, email, roles }` | Usuário |
| `ITeam` | `{ id, title, icon }` | Time |

## Factories (mantidas)

- `createBlock()`, `createCard()`, `createBoard()`, `createBoardView()`
- `createTextBlock()`, `createImageBlock()`, `createCheckboxBlock()`
- `createDividerBlock()`, `createH1Block()`, `createH2Block()`, `createH3Block()`
- `createCommentBlock()`, `createAttachmentBlock()`
- `createContentBlock()`, `createFilterClause()`, `createFilterGroup()`

## Utilitários de Diff (mantidos)

- `createPatchesFromBlocks()` — gera [updatePatch, undoPatch] para undo/redo
- `createPatchesFromBoards()` — diff de Boards
- `createCardPropertiesPatches()` — diff de propriedades
- `smartViewUpdate()` — preserva referências de arrays inalterados

## Rastreabilidade

| Arquivo legado | Unit | Confiança |
|---------------|------|-----------|
| `webapp/src/blocks/*.ts` | `blocos/` | 🟢 |
