# Importador Asana

## Visão Geral
Script autônomo em TypeScript que converte exportação JSON do Asana para formato `.boardarchive` do Nexo. Cada projeto Asana vira um board, seções viram propriedade Select "Section", e tarefas viram cards.

## Responsabilidades
- Ler exportação JSON do Asana (`-i`)
- Mapear projetos, seções e tarefas para Block/Board do Nexo
- Preservar notas como text blocks filhos do card
- Gerar saída `.boardarchive` consumível pelo Nexo

## Regras de Negócio
- Apenas o primeiro projeto da exportação é processado (TODO: múltiplos projetos) 🟢
- Seções viram opções da propriedade Select "Section" com cores cíclicas 🟢
- Cards sem membership em seção geram warn, não erro 🟢
- Notas do card viram `TextBlock` filho com `contentOrder` 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| AS-RF01 | Ler JSON export do Asana via -i | Must | Arquivo JSON válido é parseado; arquivo inexistente retorna erro código 2 |
| AS-RF02 | Converter seções em Select "Section" | Must | Cada seção vira uma opção colorida na propriedade "Section" do board |
| AS-RF03 | Criar board view do tipo "board" | Must | BoardView com viewType=board é gerada para o board |
| AS-RF04 | Preservar notas como TextBlock | Must | Card com notes tem TextBlock filho com title = notes e contentOrder atualizado |
| AS-RF05 | Gerar .boardarchive via ArchiveUtils | Must | Saída válida consumível pelo Nexo |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Performance | Leitura completa em memória (readFileSync) | `importAsana.ts:49` | 🟢 |
| Tratamento de erros | Valida existência do arquivo antes de ler | `importAsana.ts:43-45` | 🟢 |

## Critérios de Aceitação

```gherkin
Dado um arquivo JSON export do Asana com 1 projeto, 3 seções e 5 tarefas
Quando executado importAsana.ts -i <arquivo>
Então um .boardarchive é gerado com 1 board, 1 view, 5 cards e 5 text blocks

Dado um arquivo JSON com 2 projetos
Quando executado importAsana.ts
Então apenas o primeiro projeto é convertido (TODO)

Dado um caminho de arquivo inexistente
Quando executado importAsana.ts -i inexistente.json
Então exibe "File not found:" e encerra com código 2
```

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `import/asana/importAsana.ts` | `main`, `convert`, `getProjects`, `getSections`, `showHelp` | 🟢 |
| `import/asana/asana.ts` | Tipos Asana, Workspace, Datum, Membership | 🟢 |
| `import/asana/utils.ts` | `Utils.createGuid` | 🟢 |
