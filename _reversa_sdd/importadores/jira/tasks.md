# Importador Jira, Tarefas de Implementação

## Pré-requisitos
- [ ] ArchiveUtils.buildBlockArchive implementado
- [ ] Modelos Block, Board, BoardView, Card, TextBlock disponíveis
- [ ] Dependências npm: xml2js, turndown

## Tarefas

- [ ] T-01, Implementar parsing de argumentos CLI
  - Origem no legado: `import/jira/jiraImporter.ts:38-45`
  - Critério de pronto: `-i` obrigatório; valida existência; exibe help se ausente
  - Confiança: 🟢

- [ ] T-02, Implementar leitura e parsing do XML RSS
  - Origem no legado: `import/jira/jiraImporter.ts:47-69`
  - Critério de pronto: Lê XML com xml2js (explicitArray: false); extrai channel.item; encerra com código 2 se sem channel
  - Confiança: 🟢

- [ ] T-03, Implementar criação de propriedades Select a partir de valores
  - Origem no legado: `import/jira/jiraImporter.ts:186-216`
  - Critério de pronto: `buildCardPropertyFromValues` recebe nome + array de valores; retorna IPropertyTemplate com opções únicas e coloridas
  - Confiança: 🟢

- [ ] T-04, Implementar board com 8 propriedades
  - Origem no legado: `import/jira/jiraImporter.ts:90-138`
  - Critério de pronto: Board criado com 6 Select (Priority, Status, Resolution, Type, Assignee, Reporter), 1 URL (Original URL), 1 Date (Created Date); BoardView gerado
  - Confiança: 🟢

- [ ] T-05, Implementar conversão de issues em cards
  - Origem no legado: `import/jira/jiraImporter.ts:140-181`
  - Critério de pronto: Cada issue vira CardBlock; 8 propriedades mapeadas; descrição HTML convertida para Markdown e anexada como TextBlock
  - Confiança: 🟢

- [ ] T-06, Implementar serialização e saída
  - Origem no legado: `import/jira/jiraImporter.ts:76-82`
  - Critério de pronto: Chama ArchiveUtils.buildBlockArchive; escreve arquivo de saída; exibe total de blocks
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar importação com XML RSS de 10 issues variadas
- [ ] TT-02, Testar XML sem channel (código 2)
- [ ] TT-03, Testar issue com descrição HTML e sem descrição
- [ ] TT-04, Testar deduplicação de valores de propriedade
- [ ] TT-05, Testar issue com link e sem link

## Ordem Sugerida
1. T-01 (CLI)
2. T-02 (parsing XML)
3. T-03 (propriedades)
4. T-04 (board)
5. T-05 (cards + HTML→MD)
6. T-06 (serialização)
