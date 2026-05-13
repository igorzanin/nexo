# Importador Notion, Design Técnico

## Interface

### CLI

```
npx ts-node import/notion/importNotion.ts -i <inputFolder> -o [outputFile]
```

| Argumento | Obrigatório | Padrão | Descrição |
|-----------|-------------|--------|-----------|
| `-i` | Sim | - | Caminho da pasta com exportação CSV do Notion |
| `-o` | Não | `archive.boardarchive` | Caminho do arquivo .boardarchive de saída |

### Entrada (pasta de export)

```
pasta_export/
├── Nome do Board.csv        ← dados tabulares (1 linha = 1 card)
└── Nome do Board/           ← subpasta com markdowns
    ├── Card Title 123.md
    └── Another Card 456.md
```

### Saída (.boardarchive)

Formato NDJSON (Newline-Delimited JSON):

```
{"version":1,"date":<timestamp>}          ← header
{"type":"board","data":{...Board...}}    ← board
{"type":"block","data":{...BoardView...}} ← view
{"type":"block","data":{...Card...}}     ← card
{"type":"block","data":{...TextBlock...}} ← markdown
...
```

## Fluxo Principal

1. **Parse de argumentos:** minimist lê `-i` e `-o` da linha de comando
2. **Validação:** verifica se pasta existe e contém arquivo .csv
3. **Leitura CSV:** csvtojson converte CSV em array de objetos JSON
4. **Extração de título:** nome do CSV sem extensão, removendo token numérico final
5. **Conversão (convert):**
   - Cria 1 Board com cardProperties select para cada coluna
   - Cria 1 BoardView do tipo board
   - Para cada linha: cria 1 Card, mapeia propriedades, busca markdown, cria TextBlock
6. **Serialização:** ArchiveUtils.buildBlockArchive(boards, blocks) → NDJSON
7. **Escrita:** fs.writeFileSync(outputFile, outputData)

## Fluxos Alternativos
- **Pasta sem CSV:** erro "No CSV file found"
- **Card sem markdown:** card criado sem TextBlock filho, contentOrder vazio
- **Coluna vazia no CSV:** propriedade não setada no card (ignorada)

## Dependências
- **csvtojson** (npm), conversão CSV → JSON
- **minimist** (npm), parse de argumentos CLI
- **ArchiveUtils** (`import/util/archive.ts`), serialização .boardarchive
- **webapp/src/blocks/** (board, boardView, card, textBlock, block), tipos e factories Focalboard

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Todas as propriedades mapeadas como 'select' (perda de tipo) | `import/notion/importNotion.ts:135` | 🟢 |
| HACK global.window = {} para compatibilidade de GUID | `import/notion/importNotion.ts:16` | 🟢 |
| Marcadores de posição (ordenação) removidos do título do board | `import/notion/importNotion.ts:100` | 🟢 |
| TODO conhecido: cabeçalho markdown incluído no TextBlock | `import/notion/importNotion.ts:179` | 🟢 |

## Riscos e Lacunas
- 🟢 Cabeçalho markdown repetido incluso no TextBlock (TODO não implementado)
