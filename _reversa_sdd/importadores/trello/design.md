# Importador Trello, Design Técnico

## Interface

### CLI

```
npx ts-node import/trello/importTrello.ts -i <input.json> -o [outputFile]
```

| Argumento | Obrigatório | Padrão | Descrição |
|-----------|-------------|--------|-----------|
| `-i` | Sim | - | Caminho do JSON de export do Trello |
| `-o` | Não | `archive.boardarchive` | Caminho do .boardarchive de saída |

### Entrada (JSON)

Formato de export nativo do Trello (Board Menu > Print and Export > Export to JSON), tipado em `trello.ts` (gerado via quicktype.io):

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `boards` (raiz implícita) | - | Objeto contendo cards, lists, labels, checklists |
| `cards` | `CardElement[]` | Cards com id, name, desc, idList, idChecklists |
| `lists` | `List[]` | Listas/colunas com id, name, closed |
| `checklists` | `ChecklistElement[]` | Checklists com checkItems[] (state: "complete"\|"incomplete") |
| `labels` | `Label[]` | Rótulos com name e color |
| `members` | `MemberElement[]` | Membros do board |

### Mapeamento Lista → Opção Select

| Origem | Destino |
|--------|---------|
| list.name | IPropertyOption.value |
| list.id → optionIdMap[list.id] = GUID | IPropertyOption.id |
| optionColorIndex++ | IPropertyOption.color (cíclico) |
| Todas as listas abertas | Agrupadas em IPropertyTemplate "List" type='select' |

### Mapeamento Checklist → CheckboxBlock

| Origem | Destino |
|--------|---------|
| checkItem.state === 'complete' | CheckboxBlock.fields.value = true |
| checkItem.state === 'incomplete' | CheckboxBlock.fields.value = false |
| checkItem | Ordenados em contentOrder do card pai |

## Fluxo Principal

1. **Parse de argumentos:** minimist lê `-i` e `-o`
2. **Leitura JSON:** fs.readFileSync + JSON.parse → objeto Trello tipado
3. **Conversão (convert):**
   - Cria 1 Board com title e description do Trello board
   - Cria optionIdMap: cada lista → IPropertyOption GUID
   - Cria IPropertyTemplate "List" com todas as opções
   - Cria 1 BoardView do tipo board
   - Para cada card em input.cards:
     - Cria 1 Card com título = card.name
     - Mapeia idList para optionId via optionIdMap
     - Se card.desc não vazio: cria TextBlock, adiciona em contentOrder
     - Se card.idChecklists: busca checklists, para cada checkitem cria CheckboxBlock
4. **Serialização:** ArchiveUtils.buildBlockArchive(boards, blocks) → NDJSON
5. **Escrita:** fs.writeFileSync(outputFile, outputData)

## Fluxos Alternativos
- **Card sem descrição:** nenhum TextBlock criado
- **Card sem checklists:** nenhum CheckboxBlock criado
- **Lista fechada (closed=true):** ainda incluída como opção (não filtrada)

## Dependências
- **minimist** (npm), parse de argumentos CLI
- **ArchiveUtils** (`import/util/archive.ts`), serialização .boardarchive
- **webapp/src/blocks/** (board, boardView, card, textBlock, checkboxBlock, block), tipos e factories

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Listas mapeadas como coluna "List" (perda de estrutura de colunas múltiplas) | `import/trello/importTrello.ts:83` | 🟢 |
| Descrição como TextBlock filho (não como propriedade do card) | `import/trello/importTrello.ts:101` | 🟢 |
| Checklists convertidos em CheckboxBlocks individuais | `import/trello/importTrello.ts:108` | 🟢 |
| Labels, anexos, comentários, membros não mapeados | Código não referência estes campos | 🟢 |

## Riscos e Lacunas
- 🟡 Labels, anexos, comentários, datas de vencimento, membros e custom fields do Trello não são importados — dado existe no JSON mas não é mapeado
