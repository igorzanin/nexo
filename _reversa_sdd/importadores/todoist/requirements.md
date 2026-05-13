# Importador Todoist

## Visão Geral
Ferramenta CLI standalone em TypeScript que converte exportações do Todoist (formato JSON, produzido por darekkay.com/todoist-export/) para o formato .boardarchive do Focalboard. Processa um projeto Todoist por execução, mapeando seções como colunas select e notas como blocos de texto.

## Responsabilidades
- Ler exportação JSON do Todoist a partir de um arquivo local
- Iterar sobre cada projeto Todoist (exceto "Inbox") e converter em um board Focalboard
- Mapear seções do projeto como opções de uma propriedade select "List"
- Usar seções padrão (No Status, Next Up, In Progress, Completed, Archived) quando projeto tem apenas uma seção
- Converter tarefas (items) em cards Focalboard
- Concatenar notas (notes) como TextBlock filho do card
- Anexar links de file_attachment como markdown no texto do card
- Gerar arquivo .boardarchive no formato NDJSON

## Regras de Negócio
- Projeto "Inbox" é ignorado na importação 🟢
- Seções do Todoist são mapeadas como uma única propriedade select chamada "List" 🟢
- Projetos com apenas uma seção recebem 5 status padrão: No Status, Next Up, In Progress, Completed, Archived 🟢
- Cards sem seção (section_id vazio) usam sentinela noStatusSectionID 🟢
- Notas são concatenadas com dupla nova linha (\n\n) em um único TextBlock 🟢
- Labels, prioridades, datas de vencimento e subtarefas NÃO são mapeados 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| TD-RF01 | Aceitar argumento CLI -i com caminho do JSON de export | Must | JSON lido e parseado como Todoist |
| TD-RF02 | Aceitar argumento CLI -o opcional | Should | Output padrão archive.boardarchive |
| TD-RF03 | Ignorar projeto "Inbox" na conversão | Must | Inbox não gera board |
| TD-RF04 | Criar Board + BoardView para cada projeto não-Inbox | Must | Board com título = project.name |
| TD-RF05 | Mapear seções como opções select "List" | Must | Cada section vira IPropertyOption com cor cíclica |
| TD-RF06 | Usar seções padrão quando projeto tem 1 seção | Must | 5 status defaults criados como opções |
| TD-RF07 | Criar card para cada item do projeto | Must | Card com título = item.content, propriedade "List" = section |
| TD-RF08 | Criar TextBlock com notas concatenadas para cada card | Must | Notas unidas com \n\n como conteúdo textual |
| TD-RF09 | Serializar em .boardarchive via ArchiveUtils.buildBlockArchive | Must | Arquivo escrito no caminho de saída |

## Critérios de Aceitação

```gherkin
Dado um JSON de export do Todoist com 2 projetos (excluindo Inbox)
Quando convert() é chamado para cada projeto
Então 2 boards são criados com seus respectivos cards e seções

Dado um projeto com apenas uma seção
Quando convert() é chamado
Então 5 status padrão (No Status, Next Up, In Progress, Completed, Archived) são usados

Dado um item com 3 notas
Quando o card é criado
Então um TextBlock com as 3 notas concatenadas é aninhado como filho
```

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `import/todoist/importTodoist.ts` | main, convert, getProjectColumns, getProjectCards, getCardDescription | 🟢 |
| `import/todoist/todoist.ts` | Todoist, Project, Section, Item, Note, Due | 🟢 |
| `import/todoist/utils.ts` | Utils.createGuid | 🟢 |
| `import/util/archive.ts` | ArchiveUtils.buildBlockArchive | 🟢 |
