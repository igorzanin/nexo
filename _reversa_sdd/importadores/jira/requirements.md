# Importador Jira

## Visão Geral
Script autônomo em TypeScript que converte exportação XML do Jira para formato `.boardarchive` do Nexo. Issues viram cards com 8 propriedades mapeadas e descrições HTML convertidas para Markdown.

## Responsabilidades
- Ler exportação XML do Jira via `-i`
- Mapear 8 propriedades padrão (Priority, Status, Resolution, Type, Assignee, Reporter, Original URL, Created Date)
- Converter descrições HTML para Markdown via TurndownService
- Gerar saída `.boardarchive`

## Regras de Negócio
- Entrada é XML (RSS feed) — não JSON 🟢
- 8 propriedades de card: 6 Select, 1 URL, 1 Date 🟢
- Propriedades Select com opções deduplicadas e coloridas 🟢
- Descrições HTML convertidas para Markdown via TurndownService 🟢
- Propriedades custom do Jira NÃO são mapeadas (TODO aberto) 🟢
- Board único com título fixo "Jira import" 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| JR-RF01 | Ler XML export do Jira via -i | Must | Arquivo XML RSS é parseado com xml2js; sem channel retorna erro |
| JR-RF02 | Mapear propriedades Priority, Status, Resolution, Type, Assignee, Reporter | Must | Cada propriedade vira Select com opções únicas e coloridas |
| JR-RF03 | Mapear Original URL como propriedade URL | Must | Link do issue mapeado como propriedade tipo url |
| JR-RF04 | Mapear Created Date como propriedade Date | Must | Data de criação parseada e armazenada como timestamp |
| JR-RF05 | Converter descrição HTML para Markdown | Must | Descrições HTML passam por TurndownService; resultado vai para TextBlock |
| JR-RF06 | Gerar .boardarchive | Must | Saída válida consumível pelo Nexo |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Performance | Leitura completa em memória | `jiraImporter.ts:49` | 🟢 |
| Dependência | xml2js para parsing XML | `jiraImporter.ts:13` | 🟢 |
| Dependência | TurndownService para HTML→MD | `jiraImporter.ts:14,32` | 🟢 |

## Critérios de Aceitação

```gherkin
Dado um XML export do Jira com 10 issues de tipos variados
Quando executado jiraImporter.ts -i <arquivo>
Então um .boardarchive é gerado com 1 board, 1 view, 10 cards com 8 propriedades cada

Dado um XML sem channel
Quando executado jiraImporter.ts
Então exibe "No channels in xml" e encerra com código 2

Dado um XML com issue contendo descrição HTML
Quando executado jiraImporter.ts
Então a descrição é convertida para Markdown no TextBlock do card
```

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `import/jira/jiraImporter.ts` | `run`, `convert`, `buildCardPropertyFromValues`, `setSelectProperty`, `optionForPropertyValue` | 🟢 |
| `import/jira/utils.ts` | `Utils.createGuid` | 🟢 |
