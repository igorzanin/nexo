# Importador Trello

## Visão Geral
Ferramenta CLI standalone em TypeScript que converte exportações JSON do Trello para o formato .boardarchive do Focalboard. Processa um board do Trello por execução, mapeando listas como colunas select, cards como cards Focalboard, descrições como text blocks e checklists como checkbox blocks.

## Responsabilidades
- Ler exportação JSON do Trello a partir de um arquivo local
- Criar board Focalboard com título e descrição do board Trello
- Mapear listas Trello como opções de uma propriedade select "List"
- Converter cada card Trello em card Focalboard com associação à lista
- Converter descrição do card em TextBlock filho
- Converter checklists em CheckboxBlocks filhos (checked/unchecked)
- Gerar arquivo .boardarchive no formato NDJSON

## Regras de Negócio
- Listas do Trello são mapeadas como uma única propriedade select chamada "List" 🟢
- Cada lista vira um IPropertyOption com cor cíclica do array optionColors 🟢
- Cards com descrição (card.desc) geram TextBlock filho via contentOrder 🟢
- Checklists são convertidos em CheckboxBlocks individuais com value=true se "complete" 🟢
- Labels, anexos, comentários, datas de vencimento, membros e custom fields NÃO são mapeados 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| TL-RF01 | Aceitar argumento CLI -i com caminho do JSON de export | Must | JSON lido e parseado como Trello |
| TL-RF02 | Aceitar argumento CLI -o opcional | Should | Output padrão archive.boardarchive |
| TL-RF03 | Criar Board com título e descrição do Trello board | Must | createBoard() com title e description setados |
| TL-RF04 | Mapear listas Trello como opções select "List" | Must | Cada lista vira IPropertyOption com cor |
| TL-RF05 | Criar BoardView do tipo board | Must | viewType='board' vinculada ao board |
| TL-RF06 | Criar Card para cada card Trello | Must | Card com título = card.name, List = optionId da lista |
| TL-RF07 | Criar TextBlock com descrição do card se presente | Must | card.desc não vazio → TextBlock filho |
| TL-RF08 | Criar CheckboxBlocks para checklists do card | Must | Cada checkitem vira CheckboxBlock com value true/false |
| TL-RF09 | Serializar em .boardarchive via ArchiveUtils.buildBlockArchive | Must | Arquivo escrito no caminho de saída |

## Critérios de Aceitação

```gherkin
Dado um JSON de export do Trello com 3 listas e 5 cards
Quando convert() é chamado
Então 1 board, 3 opções select, 1 boardView, 5 cards são criados

Dado um card com descrição e 2 checklists (3 itens completos, 1 incompleto)
Quando o card é convertido
Então 1 TextBlock (descrição) e 4 CheckboxBlocks (3 true, 1 false) são criados como filhos

Dado um card sem descrição e sem checklists
Quando o card é convertido
Então apenas o Card é criado (sem filhos)
```

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `import/trello/importTrello.ts` | main, convert | 🟢 |
| `import/trello/trello.ts` | Trello, CardElement, List, ChecklistElement, CheckItemElement | 🟢 |
| `import/trello/utils.ts` | Utils.createGuid | 🟢 |
| `import/util/archive.ts` | ArchiveUtils.buildBlockArchive | 🟢 |
