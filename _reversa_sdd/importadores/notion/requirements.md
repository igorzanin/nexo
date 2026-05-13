# Importador Notion

## Visão Geral
Ferramenta CLI standalone em TypeScript que converte exportações do Notion (formato CSV + markdown) para o formato .boardarchive do Focalboard. Processa um board do Notion por execução, mapeando colunas do CSV como propriedades select e conteúdos markdown como blocos de texto.

## Responsabilidades
- Ler exportação CSV do Notion a partir de uma pasta local
- Extrair nome do board a partir do nome do arquivo CSV
- Converter cada linha do CSV em um card Focalboard
- Mapear colunas do CSV como propriedades do tipo select com opções dinâmicas
- Associar arquivos markdown como conteúdo textual dos cards
- Gerar arquivo .boardarchive no formato NDJSON compatível com Focalboard

## Regras de Negócio
- Todas as propriedades do CSV são convertidas como tipo 'select' (formato de export do Notion não preserva tipos originais) 🟢
- O nome do arquivo CSV (sem extensão) é parseado para extrair o título do board — tokens numéricos no final são removidos 🟢
- Valores vazios em colunas são ignorados (cards podem ter propriedades sem valor) 🟢
- Opções select ganham cores do array optionColors em ciclo (gray, brown, orange, yellow, green, blue, purple, pink, red) 🟢
- Apenas um board por execução 🟢
- HACK: global.window = {} é definido para compatibilidade com Utils.createGuid 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| NI-RF01 | Aceitar argumento CLI -i com caminho da pasta de export | Must | Pasta lida, CSV encontrado, erro se não existir |
| NI-RF02 | Aceitar argumento CLI -o opcional para output | Should | Output padrão archive.boardarchive se omitido |
| NI-RF03 | Converter CSV em array de objetos JSON | Must | csvtojson lê e parseia o CSV corretamente |
| NI-RF04 | Extrair título do board do nome do arquivo CSV | Must | "Project Tasks 123.csv" → título "Project Tasks" |
| NI-RF05 | Criar board Focalboard com cardProperties select para cada coluna | Must | Cada coluna (exceto a primeira) vira IPropertyTemplate type='select' |
| NI-RF06 | Criar BoardView do tipo board vinculada ao board | Must | viewType='board', boardId e parentId apontam para o board |
| NI-RF07 | Criar card para cada linha do CSV | Must | Card com título = primeiro campo, propriedades mapeadas |
| NI-RF08 | Buscar arquivo markdown correspondente para cada card | Must | Subpasta Nome-do-Board/ escaneada por .md com nome correspondente ao título |
| NI-RF09 | Criar TextBlock com conteúdo markdown como filho do card | Must | contentOrder do card inclui ID do TextBlock |
| NI-RF10 | Serializar boards + blocks em NDJSON via ArchiveUtils.buildBlockArchive | Must | Arquivo .boardarchive escrito no caminho de saída |

## Critérios de Aceitação

```gherkin
Dado uma pasta com export.csv e subpasta com arquivos .md
Quando o script é executado com -i <pasta>
Então um arquivo .boardarchive é gerado com board, view, cards e textBlocks

Dado um CSV com colunas "Title", "Status", "Priority"
Quando a conversão ocorre
Então Status e Priority são propriedades select com opções extraídas dos valores únicos

Dado um card cujo título corresponde a um arquivo .md
Quando o card é criado
Então um TextBlock com o conteúdo markdown é aninhado como filho
```

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `import/notion/importNotion.ts` | main, convert, getCsvFilePath, getMarkdown, getColumns | 🟢 |
| `import/notion/utils.ts` | Utils.createGuid | 🟢 |
| `import/util/archive.ts` | ArchiveUtils.buildBlockArchive | 🟢 |
