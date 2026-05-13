# Importadores — Migração de Dados Externos

## Visão Geral
Conjunto de scripts em TypeScript (Node.js) que importam boards, cards, listas e checklists de plataformas externas (Asana, Jira, Nextcloud Deck, Notion, Todoist, Trello) para o formato `.boardarchive` do Nexo. Cada importador é autônomo, lê exportações (ou API) da plataforma origem e escreve arquivos no formato NDJSON canônico.

## Responsabilidades
- Converter dados de plataformas externas para o modelo Block/Board do Nexo
- Preservar o máximo de informação possível (título, descrição, colunas, checklists)
- Gerar saída no formato `.boardarchive` (NDJSON) consumível pelo Nexo
- Compartilhar utilitário de serialização de archive (`archive.ts`)

## Regras de Negócio
- Todo importador gera saída no formato `.boardarchive` via `ArchiveUtils.buildBlockArchive()` 🟢
- IDs são gerados via UUID v4 exclusivamente 🟢
- Colunas/listas da origem viram propriedade Select no board destino 🟢
- Descrições HTML são convertidas para Markdown no importador Jira via TurndownService 🟢
- Labels do Nextcloud Deck viram propriedade MultiSelect; demais importadores usam Select 🟢
- Todoist é o único importador que produz múltiplos boards a partir de uma única entrada 🟢
- Checklists do Trello viram CheckboxBlock filhos do card 🟢
- Comentários são preservados apenas no importador Nextcloud Deck 🟢
- Nenhum importador mapeia usuários da origem para usuários do Nexo 🟢
- Todas as importações são one-shot (não incrementais) 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| IM-RF01 | Importar boards do Asana (JSON export) | Must | Board criado com seções como Select "Section" |
| IM-RF02 | Importar issues do Jira (XML export) | Must | Board criado com 8 propriedades; HTML desc → Markdown |
| IM-RF03 | Importar boards do Nextcloud Deck (API REST) | Must | Board criado com listas, labels, comentários e datas |
| IM-RF04 | Importar boards do Notion (CSV + Markdown) | Must | Board criado com colunas CSV como Select properties |
| IM-RF05 | Importar projetos do Todoist (JSON export) | Must | Múltiplos boards gerados; seções como List |
| IM-RF06 | Importar boards do Trello (JSON export) | Must | Board criado com listas e checklists |
| IM-RF07 | Serializar archive compartilhado no formato NDJSON | Must | ArchiveUtils.buildBlockArchive válido consumível pelo Nexo |
| IM-RF08 | Parsear archive NDJSON de volta para objetos | Must | ArchiveUtils.parseBlockArchive restaura blocks originais |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Performance | Leitura completa em memória (sem streaming) | `import/*/import*.ts:readFileSync` | 🟢 |
| Performance | Streaming para arquivos >500MB | Decisão do revisor | 🟢 |
| Confiabilidade | Validação prévia do arquivo de entrada com relatório de erros | Decisão do revisor | 🟢 |
| Compatibilidade | Formato NDJSON versionado (campo version no header) | `import/util/archive.ts:10` | 🟢 |
| Manutenibilidade | Cada importador é isolado com seu próprio package.json | `import/*/package.json` | 🟢 |

## Critérios de Aceitação

```gherkin
Dado um arquivo de exportação do Asana em JSON
Quando executado o importador asana com -i <arquivo>
Então um arquivo .boardarchive é gerado com board, view e cards

Dado um arquivo de exportação do Jira em XML
Quando executado o importador jira com -i <arquivo>
Então descrições HTML são convertidas para Markdown

Dado um Nextcloud Deck com board, stacks e cards
Quando executado o importador nextcloud-deck com -b <boardId>
Então labels viram MultiSelect e comentários viram CommentBlock

Dado um CSV de exportação do Notion
Quando executado o importador notion com -i <pasta>
Então cada linha do CSV vira um card com colunas como Select

Dado um JSON export do Todoist
Quando executado o importador todoist com -i <arquivo>
Então múltiplos boards são gerados, um por projeto

Dado um JSON export do Trello
Quando executado o importador trello com -i <arquivo>
Então checklists viram CheckboxBlock filhos do card
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Importação Trello | Must | Plataforma mais comum; checklists exclusivos |
| Importação Jira | Must | Formato XML complexo com HTML→MD |
| Importação Asana | Must | 5o mais popular; seções viram Select |
| Importação Todoist | Must | Único com suporte a múltiplos boards |
| Importação Nextcloud Deck | Should | Requer API ativa; comentários preservados |
| Importação Notion | Should | CSV limita tipos de propriedade |
| ArchiveUtils compartilhado | Must | Todos os importadores dependem dele |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `import/util/archive.ts` | `ArchiveUtils.buildBlockArchive`, `ArchiveUtils.parseBlockArchive` | 🟢 |
| `import/asana/importAsana.ts` | `convert()`, `main()` | 🟢 |
| `import/jira/jiraImporter.ts` | `run()`, `convert()` | 🟢 |
| `import/nextcloud-deck/importDeck.ts` | `convert()`, `main()` | 🟢 |
| `import/notion/importNotion.ts` | `convert()`, `main()` | 🟢 |
| `import/todoist/importTodoist.ts` | `convert()`, `main()` | 🟢 |
| `import/trello/importTrello.ts` | `convert()`, `main()` | 🟢 |
| `import/*/utils.ts` | `Utils.createGuid()` | 🟢 |
