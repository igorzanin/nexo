# Importador Nextcloud Deck

## Visão Geral
Script autônomo em TypeScript que se conecta à API REST do Nextcloud Deck e converte boards, stacks e cards para formato `.boardarchive` do Nexo. Único importador que opera via API ao vivo (não arquivo local). Preserva labels como MultiSelect e comentários como CommentBlock.

## Responsabilidades
- Conectar via API REST Nextcloud Deck com credenciais
- Listar boards disponíveis e permitir seleção interativa
- Buscar stacks, cards, labels e comentários
- Converter para modelo Block/Board do Nexo
- Preservar labels, datas de vencimento, descrições e comentários

## Regras de Negócio
- Stacks viram propriedade Select "List" 🟢
- Labels viram propriedade MultiSelect "Label" 🟢
- Due date viram propriedade Date "Due Date" 🟢
- Comentários viram CommentBlock filho do card (autor não preservado) 🟢
- Descrição do card viram TextBlock filho 🟢
- Input interativo via readline-sync quando flags omitidas 🟢
- Comentários são buscados condicionalmente (apenas se commentsCount > 0) 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| ND-RF01 | Conectar à API Nextcloud Deck com URL + usuário + senha | Must | Cliente NextcloudDeckClient criado com credenciais; prompts interativos se omitidos |
| ND-RF02 | Selecionar board por ID (-b) ou interativamente | Must | boardIdString via CLI ou selectBoard() lista boards e aguarda input |
| ND-RF03 | Buscar stacks e cards com detalhes | Must | getBoardDetails + getStacks retornam dados completos com cards aninhados |
| ND-RF04 | Buscar comentários de cards (quando existirem) | Must | Apenas cards com commentsCount > 0 disparam getComments |
| ND-RF05 | Converter labels em MultiSelect | Must | Labels do board viram opções da propriedade MultiSelect "Label" |
| ND-RF06 | Preservar comentários como CommentBlock | Must | Cada comentário vira CommentBlock filho do card |
| ND-RF07 | Gerar .boardarchive via ArchiveUtils | Must | Saída válida consumível pelo Nexo |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Dependência | API Nextcloud Deck ativa | `importDeck.ts:13` | 🟢 |
| Dependência | readline-sync para input interativo | `importDeck.ts:15` | 🟢 |
| Performance | Chamadas em paralelo via Promise.all | `importDeck.ts:60` | 🟢 |

## Critérios de Aceitação

```gherkin
Dado um Nextcloud Deck com board, 3 stacks, 5 cards com labels e comentários
Quando executado importDeck.ts --url <url> -u <user> -p <pass> -b <boardId>
Então um .boardarchive é gerado com 1 board, propriedades List/Label/Due Date, cards com CommentBlocks

Dado flags de credenciais omitidas
Quando executado importDeck.ts
Então readline-sync solicita URL, usuário e senha interativamente

Dado boardId omitido
Quando executado importDeck.ts
Então selectBoard lista boards disponíveis e aguarda input do ID
```

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `import/nextcloud-deck/importDeck.ts` | `main`, `selectBoard`, `convert` | 🟢 |
| `import/nextcloud-deck/deck.ts` | NextcloudDeckClient, tipos Board, Stack, Card | 🟢 |
| `import/nextcloud-deck/utils.ts` | Utils.createGuid | 🟢 |
