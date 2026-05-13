# Importadores, Tarefas de Implementação

## Pré-requisitos
- [ ] Modelos Block e Board implementados (`webapp/src/blocks/`)
- [ ] Utilitário `ArchiveUtils.buildBlockArchive` implementado (`import/util/archive.ts`)
- [ ] Dependências: minimist, xml2js, turndown, csv-parse, readline-sync

## Tarefas

- [ ] T-01, Implementar ArchiveUtils (buildBlockArchive + parseBlockArchive)
  - Origem no legado: `import/util/archive.ts`
  - Critério de pronto: Serializa boards + blocks em NDJSON com header versionado; parseBlockArchive restaura blocks e valida header
  - Confiança: 🟢

- [ ] T-02, Implementar importador Trello
  - Origem no legado: `import/trello/importTrello.ts`
  - Critério de pronto: Lê JSON export do Trello, converte listas em colunas Select, checklists em CheckboxBlock filhos do card, gera .boardarchive
  - Confiança: 🟢

- [ ] T-03, Implementar importador Asana
  - Origem no legado: `import/asana/importAsana.ts`
  - Critério de pronto: Lê JSON export do Asana, converte seções em propriedade Select "Section", gera .boardarchive
  - Confiança: 🟢

- [ ] T-04, Implementar importador Jira
  - Origem no legado: `import/jira/jiraImporter.ts`
  - Critério de pronto: Lê XML export do Jira via xml2js, converte descrições HTML para Markdown via TurndownService, gera .boardarchive com 8 propriedades
  - Confiança: 🟢

- [ ] T-05, Implementar importador Notion
  - Origem no legado: `import/notion/importNotion.ts`
  - Critério de pronto: Lê pasta com CSV + Markdown, converte colunas CSV em propriedades Select, gera .boardarchive
  - Confiança: 🟢

- [ ] T-06, Implementar importador Todoist
  - Origem no legado: `import/todoist/importTodoist.ts`
  - Critério de pronto: Lê JSON export do Todoist, gera múltiplos boards (um por projeto), seções viram List, gera .boardarchive
  - Confiança: 🟢

- [ ] T-07, Implementar importador Nextcloud Deck
  - Origem no legado: `import/nextcloud-deck/importDeck.ts`
  - Critério de pronto: Conecta via API REST com credenciais, lista boards interativamente se -b omitido, labels viram MultiSelect, preserva comentários como CommentBlock, gera .boardarchive
  - Confiança: 🟢

- [ ] T-08, Implementar CLI compartilhada com minimist
  - Origem no legado: `import/*/import*.ts`
  - Critério de pronto: Todos os importadores usam `-i` (input), `-o` (output opcional, default archive.boardarchive); Nextcloud Deck usa `--url`, `-u`, `-p`, `-b`
  - Confiança: 🟢

- [ ] T-09, Implementar conversão HTML → Markdown (TurndownService)
  - Origem no legado: `import/jira/jiraImporter.ts`
  - Critério de pronto: Converte HTML de descrições Jira para Markdown no board destino
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar ArchiveUtils.buildBlockArchive com boards e blocks vazios
- [ ] TT-02, Testar ArchiveUtils.parseBlockArchive com NDJSON válido e inválido
- [ ] TT-03, Testar cada importador com arquivo de exportação válido
- [ ] TT-04, Testar cada importador com arquivo mal-formado (falha de parsing)
- [ ] TT-05, Testar Jira com descrições HTML e sem HTML
- [ ] TT-06, Testar Todoist com 1 projeto e com múltiplos projetos
- [ ] TT-07, Testar Trello com checklists e sem checklists
- [ ] TT-08, Testar Nextcloud Deck com boardId inválido (erro de API)

## Ordem Sugerida
1. T-01 (ArchiveUtils base — todos dependem)
2. T-08 (CLI compartilhada)
3. T-02 a T-07 (importadores específicos, ordem não importa — são independentes entre si)
4. T-09 (conversão HTML, parte do Jira)

## Lacunas Pendentes — Decidido
- 🟢 Validação prévia do arquivo de entrada com relatório de erros por linha — **DECIDIDO: implementar**
- 🟡 Nextcloud Deck requer API ativa e credenciais; sem suporte a autenticação por token — decidir se token deve ser suportado
- 🟢 Streaming para arquivos grandes (>500MB) — **DECIDIDO: implementar**
