# Importador Trello, Tarefas de Implementação

## Pré-requisitos
- [ ] Tipos e factories Focalboard implementados (webapp/src/blocks/)
- [ ] ArchiveUtils implementado (import/util/archive.ts)

## Tarefas

- [ ] T-01, Implementar CLI com minimist para args -i e -o
  - Origem no legado: `import/trello/importTrello.ts:31`
  - Critério de pronto: script aceita -i (obrigatório) e -o (opcional)
  - Confiança: 🟢

- [ ] T-02, Implementar função convert com criação de Board, BoardView, Cards
  - Origem no legado: `import/trello/importTrello.ts:70`
  - Critério de pronto: board com title/description; listas como opções select "List"; boardView; cards
  - Confiança: 🟢

- [ ] T-03, Implementar criação de TextBlock para descrição do card
  - Origem no legado: `import/trello/importTrello.ts:99`
  - Critério de pronto: card.desc não vazio → TextBlock filho com contentOrder
  - Confiança: 🟢

- [ ] T-04, Implementar conversão de checklists em CheckboxBlocks
  - Origem no legado: `import/trello/importTrello.ts:106`
  - Critério de pronto: cada checkitem → CheckboxBlock com value=true se "complete"
  - Confiança: 🟢

- [ ] T-05, Implementar serialização e escrita do .boardarchive
  - Origem no legado: `import/trello/importTrello.ts:55`
  - Critério de pronto: ArchiveUtils.buildBlockArchive + writeFileSync
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar conversão com board de 3 listas e 5 cards
- [ ] TT-02, Testar card com descrição + checklists (mistos complete/incomplete)
- [ ] TT-03, Testar card sem descrição e sem checklists

## Ordem Sugerida
1. T-01 (CLI)
2. T-02 (conversão principal)
3. T-03 (descrição como TextBlock)
4. T-04 (checklists como CheckboxBlocks)
5. T-05 (serialização)

## Lacunas Pendentes (🔴)
Nenhuma — extraído diretamente do código legado.
