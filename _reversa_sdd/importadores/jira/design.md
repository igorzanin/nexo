# Importador Jira, Design Técnico

## Interface

### CLI

| Parâmetro | Descrição | Obrigatório | Padrão |
|-----------|-----------|-------------|--------|
| `-i` | Caminho do XML export do Jira | Sim | — |
| `-o` | Caminho do arquivo de saída `.boardarchive` | Não | `archive.boardarchive` |

### Função exportada

| Símbolo | Assinatura | Retorno | Observação |
|---------|-----------|---------|------------|
| `run` | `(inputFile: string, outputFile: string)` | `Promise<number>` | Função principal assíncrona; retorna quantidade de blocks |

## Fluxo Principal

1. Validar `-i` presente 🟢 — `jiraImporter.ts:38-40`
2. Validar arquivo existe 🟢 — `jiraImporter.ts:42-45`
3. Ler XML com `readFileSync` 🟢 — `jiraImporter.ts:49`
4. Fazer parse com `xml2js.Parser.parseStringPromise` 🟢 — `jiraImporter.ts:61-62`
5. Extrair `channel.item` do RSS 🟢 — `jiraImporter.ts:68-69`
6. Criar board com título "Jira import" 🟢 — `jiraImporter.ts:90-91`
7. Para cada campo (Priority, Status, Resolution, Type, Assignee, Reporter): compilar valores únicos com `buildCardPropertyFromValues` e criar Select property 🟢 — `jiraImporter.ts:96-109`
8. Criar propriedades Original URL (url) e Created Date (date) 🟢 — `jiraImporter.ts:114-128`
9. Criar BoardView 🟢 — `jiraImporter.ts:133-138`
10. Para cada issue: criar CardBlock, mapear 8 propriedades, converter descrição HTML→MD via TurndownService, anexar como TextBlock 🟢 — `jiraImporter.ts:140-181`
11. Serializar com `ArchiveUtils.buildBlockArchive` 🟢 — `jiraImporter.ts:78`

## Fluxos Alternativos

- **Arquivo não encontrado:** Exibe `File not found` e sai com código 2 🟢
- **XML sem channel:** Exibe `No channels in xml` e sai com código 2 🟢 — `jiraImporter.ts:64-67`
- **Issue sem descrição:** Card é criado sem TextBlock filho 🟢 — `jiraImporter.ts:168`

## Dependências

- `xml2js` — Parsing de XML RSS
- `turndown` — Conversão HTML→Markdown
- `import/util/archive.ts` — ArchiveUtils.buildBlockArchive
- `import/jira/utils.ts` — Utils.createGuid
- `webapp/src/blocks/*` — Modelos Block/Board

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Parsing XML com `explicitArray: false` | `jiraImporter.ts:58-60` | 🟢 |
| Propriedades Select com valores deduplicados | `jiraImporter.ts:190-192` | 🟢 |
| Board único com título fixo "Jira import" | `jiraImporter.ts:91` | 🟢 |
| HTML→MD via TurndownService singleton | `jiraImporter.ts:32` | 🟢 |
| Propriedades custom não mapeadas (TODO) | `jiraImporter.ts:166` | 🟢 |
| Função assíncrona (run) vs síncrona nos demais importadores | `jiraImporter.ts:34` | 🟢 |

## Estado Interno

Nenhum — script one-shot sem estado. `optionColorIndex` global é resetado a cada execução.

## Observabilidade

- `console.log` para progresso (input, output, KB lidos, propriedades, blocks)
- `console.error` para erros fatais
