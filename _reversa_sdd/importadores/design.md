# Importadores, Design Técnico

## Interface

### CLI — Cada importador é um script Node.js autônomo

| Importador | Comando | Entrada | Saída |
|-----------|---------|---------|-------|
| Trello | `importTrello.ts -i <input.json> -o [output]` | JSON export do Trello | `.boardarchive` |
| Asana | `importAsana.ts -i <input.json> -o [output]` | JSON export do Asana | `.boardarchive` |
| Jira | `jiraImporter.ts -i <input.xml> -o [output]` | XML export do Jira | `.boardarchive` |
| Notion | `importNotion.ts -i <folder> -o [output]` | Pasta com CSV + Markdown | `.boardarchive` |
| Todoist | `importTodoist.ts -i <input.json> -o [output]` | JSON export do Todoist | `.boardarchive` |
| Nextcloud Deck | `importDeck.ts --url <url> -u <user> -p <pass> -b <boardId> -o [output]` | API REST do Nextcloud | `.boardarchive` |

Todos usam `minimist` para parsing de argumentos. `-o` opcional com default `archive.boardarchive`.

### ArchiveUtils (compartilhado)

| Símbolo | Assinatura | Retorno | Observação |
|---------|-----------|---------|------------|
| `ArchiveUtils.buildBlockArchive` | `(boards: readonly Board[], blocks: readonly Block[])` | `string` | Serializa boards + blocks em NDJSON com header versionado |
| `ArchiveUtils.parseBlockArchive` | `(contents: string)` | `Block[]` | Restaura blocks do NDJSON; valida header e versão |

### Formato `.boardarchive` (NDJSON)

```
{"version":1,"date":1680000000000}       ← header
{"type":"board","data":{...}}            ← board
{"type":"block","data":{...}}            ← block (0+ linhas)
```

## Fluxo Principal — Importação via Arquivo

1. Ler arquivo de entrada (`readFileSync`) 🟢 — `import/*/import*.ts`
2. Parsear formato específico da origem (JSON, XML, CSV) 🟢
3. Converter cada entidade origem para modelo Block/Board do Nexo 🟢 — funções `convert()` específicas
4. Chamar `ArchiveUtils.buildBlockArchive(boards, blocks)` para serializar 🟢 — `import/util/archive.ts:28`
5. Escrever saída `.boardarchive` com `writeFileSync` 🟢 — `import/*/import*.ts`

## Fluxo Principal — Importação Nextcloud Deck (API)

1. Conectar via API REST com credenciais (URL, usuário, senha) 🟢 — `import/nextcloud-deck/importDeck.ts`
2. Listar boards disponíveis (modo interativo se `-b` omitido) 🟢
3. Buscar stacks, cards, labels e comentários via API 🟢
4. Converter para modelo Nexo com labels como `MultiSelect` 🟢
5. Chamar `ArchiveUtils.buildBlockArchive` e escrever saída 🟢

## Fluxo Alternativo — Todoist (Múltiplos Boards)

- **Todoist gera N boards a partir de 1 arquivo:** cada projeto vira um board separado no mesmo archive 🟢 — `import/todoist/importTodoist.ts:convert()`

## Fluxo Alternativo — Jira HTML → Markdown

- **Descrições HTML são convertidas para Markdown** via `TurndownService` antes de compor o block 🟢 — `import/jira/jiraImporter.ts`

## Fluxo Alternativo — Trello Checklists

- **Checklists do Trello viram `CheckboxBlock` filhos do card** no board destino 🟢 — `import/trello/importTrello.ts:convert()`

## Dependências

- `import/util/archive.ts` — Utilitário de serialização NDJSON compartilhado
- `webapp/src/blocks/block.ts` — Tipo `Block`
- `webapp/src/blocks/board.ts` — Tipo `Board`
- `xml2js` — Parsing de XML (apenas Jira)
- `turndown` — HTML → Markdown (apenas Jira)
- `csv-parse` — Parsing de CSV (apenas Notion)
- `minimist` — Parsing de argumentos CLI (todos)
- `readline-sync` — Input interativo (apenas Nextcloud Deck)

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Formato NDJSON versionado com header | `import/util/archive.ts:28-57` | 🟢 |
| Leitura completa em memória (sem streaming) | `import/*/import*.ts:readFileSync` | 🟢 |
| Cada importador é autônomo com seu próprio package.json | `import/*/package.json` | 🟢 |
| IDs gerados via UUID v4 | `import/*/utils.ts:createGuid()` | 🟢 |
| HTML→MD apenas no Jira via TurndownService | `import/jira/jiraImporter.ts` | 🟢 |
| Todoist é o único importador multi-board | `import/todoist/importTodoist.ts:convert()` | 🟢 |
| Nenhum importador mapeia usuários | todos os importadores | 🟢 |
| Todas as importações são one-shot (não incrementais) | sem lógica de diff/delta em nenhum importador | 🟢 |
| Labels Nextcloud viram MultiSelect; demais usam Select | `import/nextcloud-deck/importDeck.ts` | 🟢 |

## Estado Interno

Nenhum — importadores são scripts one-shot sem estado entre execuções. `ArchiveUtils` é pure function: dada mesma entrada, produz mesma saída.

## Observabilidade

- Logs no console via `console.log` / `console.error` durante execução 🟢
- Sem logging estruturado, métricas ou traces

## Riscos e Lacunas — Decidido

- 🟢 Tratamento de erros — **DECIDIDO: implementar validação prévia com relatório de erros por linha**
- 🟡 Nextcloud Deck requer API ativa e credenciais; sem suporte a autenticação por token
- 🟡 Nenhum teste de integração confirmado para os cenários de importação
- 🟢 Leitura em memória — **DECIDIDO: implementar streaming para arquivos >500MB**
- 🟡 Comentários preservados apenas no Nextcloud Deck; demais importadores descartam
