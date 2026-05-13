# Importador Nextcloud Deck, Tarefas de Implementação

## Pré-requisitos
- [ ] ArchiveUtils.buildBlockArchive implementado
- [ ] Modelos Block, Board, BoardView, Card, TextBlock, CommentBlock disponíveis
- [ ] Dependência npm: readline-sync

## Tarefas

- [ ] T-01, Implementar NextcloudDeckClient (API client)
  - Origem no legado: `import/nextcloud-deck/deck.ts`
  - Critério de pronto: Cliente HTTP com métodos getBoards, getBoardDetails, getStacks, getComments; autenticação básica com username/password
  - Confiança: 🟢

- [ ] T-02, Implementar parsing de argumentos CLI com input interativo
  - Origem no legado: `import/nextcloud-deck/importDeck.ts:35-51`
  - Critério de pronto: Flags --url, -u, -p, -b, -o; valores omitidos solicitados via readline-sync; -h exibe help
  - Confiança: 🟢

- [ ] T-03, Implementar seleção interativa de board
  - Origem no legado: `import/nextcloud-deck/importDeck.ts:82-87`
  - Critério de pronto: Lista boards com ID e título; aguarda input numérico do ID
  - Confiança: 🟢

- [ ] T-04, Implementar fetching de dados do board (board + stacks + cards + comments)
  - Origem no legado: `import/nextcloud-deck/importDeck.ts:58-70`
  - Critério de pronto: Busca board details, stacks com cards; comentários buscados condicionalmente por card; uso de Promise.all para paralelismo
  - Confiança: 🟢

- [ ] T-05, Implementar conversão de stacks, labels e due dates em propriedades
  - Origem no legado: `import/nextcloud-deck/importDeck.ts:98-149`
  - Critério de pronto: Stacks → Select "List"; Labels → MultiSelect "Label"; Due Date → Date "Due Date"
  - Confiança: 🟢

- [ ] T-06, Implementar conversão de cards com comentários
  - Origem no legado: `import/nextcloud-deck/importDeck.ts:161-209`
  - Critério de pronto: CardBlock com stack/label/due date mapeados; descrição como TextBlock; comentários como CommentBlock
  - Confiança: 🟢

- [ ] T-07, Implementar serialização e saída
  - Origem no legado: `import/nextcloud-deck/importDeck.ts:74-79`
  - Critério de pronto: Chama ArchiveUtils.buildBlockArchive; escreve arquivo de saída
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar conexão com Nextcloud Deck real ou mock
- [ ] TT-02, Testar seleção interativa de board
- [ ] TT-03, Testar card com stackId inválido (warn, não erro)
- [ ] TT-04, Testar card sem descrição, sem comentários, sem due date
- [ ] TT-05, Testar card com labels múltiplas (MultiSelect)

## Ordem Sugerida
1. T-01 (API client)
2. T-02, T-03 (CLI + seleção)
3. T-04 (fetching)
4. T-05 (propriedades)
5. T-06 (cards)
6. T-07 (serialização)
