# Blocos, Tarefas de Implementação

## Tarefas

- [ ] T-01, Implementar Block e BlockPatch
- [ ] T-02, Implementar Board, BoardPatch, IPropertyTemplate, IPropertyOption
- [ ] T-03, Implementar Card com CardFields
- [ ] T-04, Implementar BoardView com BoardViewFields
- [ ] T-05, Implementar filtros (FilterClause, FilterGroup) — **15 condições**
- [ ] T-06, Implementar blocos de conteúdo (Text, Image, Checkbox, Divider, H1-H3)
- [ ] T-07, Implementar CommentBlock, AttachmentBlock
- [ ] T-08, Implementar factories para todos os tipos
- [ ] T-09, Implementar utilitários de diff/patch (createPatchesFromBlocks, etc.)
  - Crítico para undo/redo via Mutator
- [ ] T-10, Implementar interfaces auxiliares (IUser, ITeam, ISharing)

## Notas
- Board default type: `'P'` (Private) ✅
- Filter conditions: 15 (confirmado) ✅
- Código TypeScript puro, sem dependência de framework — consumido por Pinia stores
