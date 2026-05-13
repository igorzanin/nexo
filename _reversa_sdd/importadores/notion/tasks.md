# Importador Notion, Tarefas de Implementação

## Pré-requisitos
- [ ] Tipos e factories Focalboard implementados (webapp/src/blocks/)
- [ ] ArchiveUtils implementado (import/util/archive.ts)

## Tarefas

- [ ] T-01, Implementar CLI com minimist para args -i e -o
  - Origem no legado: `import/notion/importNotion.ts:34`
  - Critério de pronto: script aceita -i (obrigatório) e -o (opcional)
  - Confiança: 🟢

- [ ] T-02, Implementar leitura e parse do CSV com csvtojson
  - Origem no legado: `import/notion/importNotion.ts:95`
  - Critério de pronto: CSV é convertido em array de objetos JSON
  - Confiança: 🟢

- [ ] T-03, Implementar função convert que cria Board, BoardView, Cards e TextBlocks
  - Origem no legado: `import/notion/importNotion.ts:121`
  - Critério de pronto: Board com cardProperties para cada coluna; Card por linha; TextBlock por markdown
  - Confiança: 🟢

- [ ] T-04, Implementar getMarkdown para buscar arquivos .md na subpasta
  - Origem no legado: `import/notion/importNotion.ts:158`
  - Critério de pronto: arquivo markdown encontrado por correspondência de nome
  - Confiança: 🟢

- [ ] T-05, Implementar serialização e escrita do .boardarchive
  - Origem no legado: `import/notion/importNotion.ts:60`
  - Critério de pronto: ArchiveUtils.buildBlockArchive + writeFileSync
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar conversão de CSV simples com 2 linhas
- [ ] TT-02, Testar extração de título do board (com e sem números)
- [ ] TT-03, Testar getMarkdown com correspondência exata e parcial

## Ordem Sugerida
1. T-01 (CLI)
2. T-02 (leitura CSV)
3. T-03 (conversão)
4. T-04 (markdown)
5. T-05 (serialização)

## Lacunas Pendentes (🔴)
Nenhuma — extraído diretamente do código legado.
