# Importador Todoist, Design Técnico

## Interface

### CLI

```
npx ts-node import/todoist/importTodoist.ts -i <input.json> -o [outputFile]
```

| Argumento | Obrigatório | Padrão | Descrição |
|-----------|-------------|--------|-----------|
| `-i` | Sim | - | Caminho do JSON de export do Todoist |
| `-o` | Não | `archive.boardarchive` | Caminho do .boardarchive de saída |

### Entrada (JSON)

Formato produzido por [darekkay.com/todoist-export/](https://darekkay.com/todoist-export/), tipado pela interface `Todoist` em `todoist.ts`:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `projects` | `Project[]` | Lista de projetos (id, name, color) |
| `sections` | `Section[]` | Seções dentro de projetos (id, name, project_id) |
| `items` | `Item[]` | Tarefas (id, content, project_id, section_id, priority, due) |
| `notes` | `Note[]` | Notas/comentários (id, item_id, content, file_attachment) |

### Mapeamento Seção → Opção Select

| Origem | Destino |
|--------|---------|
| section.name | IPropertyOption.value |
| section.id → GUID | IPropertyOption.id |
| optionColorIndex++ | IPropertyOption.color (cíclico) |
| Todas as seções | Agrupadas em IPropertyTemplate "List" type='select' |

## Fluxo Principal

1. **Parse de argumentos:** minimist lê `-i` e `-o`
2. **Leitura JSON:** fs.readFileSync + JSON.parse → objeto Todoist tipado
3. **Para cada projeto (exceto Inbox):**
   - Cria 1 Board com title = project.name
   - getProjectColumns: busca seções do projeto (ou usa 5 defaults)
   - Cria IPropertyOption para cada seção
   - Cria 1 BoardView do tipo board
   - getProjectCards: filtra items por project.id
   - Para cada item:
     - Cria 1 Card com título = item.content
     - Mapeia section_id para optionId
     - getCardDescription: coleta notas em array de strings
     - Se há notas: cria TextBlock com notas concatenadas
4. **Serialização:** ArchiveUtils.buildBlockArchive(boards, blocks) → NDJSON
5. **Escrita:** fs.writeFileSync(outputFile, outputData)

## Fluxos Alternativos
- **Projeto sem seções:** usa 5 status padrão (No Status, Next Up, In Progress, Completed, Archived)
- **Item sem section_id:** mapeado para noStatusSectionID (primeiro option)
- **Item sem notas:** card criado sem TextBlock filho

## Dependências
- **minimist** (npm), parse de argumentos CLI
- **ArchiveUtils** (`import/util/archive.ts`), serialização .boardarchive
- **webapp/src/blocks/** (board, boardView, card, textBlock, block), tipos e factories Focalboard

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| "Inbox" ignorado na importação | `import/todoist/importTodoist.ts:87` | 🟢 |
| Seções viram coluna "List" (perda de estrutura original) | `import/todoist/importTodoist.ts:137` | 🟢 |
| 5 status padrão para projetos sem seções | `import/todoist/importTodoist.ts:18` | 🟢 |
| Notas concatenadas (sem separação individual) | `import/todoist/importTodoist.ts:173` | 🟢 |
| Labels, prioridades, datas não mapeados | Código não referência estes campos | 🟢 |

## Riscos e Lacunas
- 🟡 Labels, prioridades e datas de vencimento do Todoist não são importados — dado existe no JSON mas não é mapeado
