# Blocos, Design Técnico

As interfaces TypeScript permanecem **idênticas** às do legado. Apenas o consumo muda (Vue 3 + Pinia em vez de React + Redux).

## Estrutura de Arquivos

```
nexo/webapp/src/types/
├── block.ts           # Block, BlockPatch, createBlock, createPatchesFromBlocks
├── board.ts           # Board, BoardPatch, BoardMember, IPropertyTemplate
├── boardView.ts       # BoardView, IViewType, ISortOption
├── card.ts            # Card, CardFields
├── contentBlock.ts    # ContentBlock
├── commentBlock.ts    # CommentBlock
├── textBlock.ts       # TextBlock
├── imageBlock.ts      # ImageBlock
├── checkboxBlock.ts   # CheckboxBlock
├── dividerBlock.ts    # DividerBlock
├── attachmentBlock.ts # AttachmentBlock
├── filterClause.ts    # FilterClause
├── filterGroup.ts     # FilterGroup
├── user.ts            # IUser
├── team.ts            # ITeam
└── sharing.ts         # ISharing
```

## Hierarquia de Tipos

```
Block (base — 15 campos)
├── Board (Board + cardProperties, minimumRole, etc.)
├── Card (Block + CardFields)
├── BoardView (Block + BoardViewFields)
├── CommentBlock (type fixo 'comment')
├── AttachmentBlock (type fixo 'attachment')
├── ContentBlock (alias para Block)
│   ├── TextBlock, ImageBlock, DividerBlock, CheckboxBlock
│   ├── H1Block, H2Block, H3Block
│   └── Video, Quote, ListItem (via contentBlockTypes)
└── FilterGroup / FilterClause
```

## Decisões de Design (mantidas)

| Decisão | Confiança |
|---------|-----------|
| Board como tipo separado (não extende Block) | 🟢 |
| Card com contentOrder (array ordenado de IDs) | 🟢 |
| FilterGroup como árvore aninhada (and/or) | 🟢 |
| Patches com diff para undo/redo (não snapshots) | 🟢 |
| Factories deep-clone dados mutáveis | 🟢 |
