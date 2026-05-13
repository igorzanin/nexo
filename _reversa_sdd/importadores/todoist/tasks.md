# Importador Todoist, Tarefas de Implementação

## Pré-requisitos
- [ ] Tipos e factories Focalboard implementados (webapp/src/blocks/)
- [ ] ArchiveUtils implementado (import/util/archive.ts)

## Tarefas

- [ ] T-01, Implementar tipos Todoist no todoist.ts
  - Origem no legado: `import/todoist/todoist.ts`
  - Critério de pronto: interfaces Todoist, Project, Section, Item, Note, Due definidas
  - Confiança: 🟢

- [ ] T-02, Implementar CLI com minimist para args -i e -o
  - Origem no legado: `import/todoist/importTodoist.ts:41`
  - Critério de pronto: script aceita -i (obrigatório) e -o (opcional)
  - Confiança: 🟢

- [ ] T-03, Implementar getProjectColumns com fallback para seções padrão
  - Origem no legado: `import/todoist/importTodoist.ts:128`
  - Critério de pronto: seções do projeto retornadas; se apenas "No Section", retorna 5 defaults
  - Confiança: 🟢

- [ ] T-04, Implementar convert para criar Board, BoardView, Cards e TextBlocks
  - Origem no legado: `import/todoist/importTodoist.ts:86`
  - Critério de pronto: board por projeto; card por item; select "List" para seções
  - Confiança: 🟢

- [ ] T-05, Implementar getCardDescription com concatenação de notas
  - Origem no legado: `import/todoist/importTodoist.ts:160`
  - Critério de pronto: notas concatenadas com \n\n; file_attachment como link markdown
  - Confiança: 🟢

- [ ] T-06, Implementar serialização e escrita do .boardarchive
  - Origem no legado: `import/todoist/importTodoist.ts:64`
  - Critério de pronto: ArchiveUtils.buildBlockArchive + writeFileSync
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar conversão com projeto de 1 seção (fallback p/ defaults)
- [ ] TT-02, Testar getCardDescription com notas e file_attachment
- [ ] TT-03, Testar que "Inbox" não é convertido

## Ordem Sugerida
1. T-01 (tipos Todoist)
2. T-02 (CLI)
3. T-03, T-04 (conversão com seções)
4. T-05 (notas)
5. T-06 (serialização)

## Lacunas Pendentes (🔴)
Nenhuma — extraído diretamente do código legado.
