# Importador Nextcloud Deck, Design Técnico

## Interface

### CLI

| Parâmetro | Descrição | Obrigatório | Padrão |
|-----------|-----------|-------------|--------|
| `--url` | URL do servidor Nextcloud | Não (prompt) | — |
| `-u` | Usuário Nextcloud | Não (prompt) | — |
| `-p` | Senha Nextcloud | Não (prompt oculto) | — |
| `-b` | ID do board | Não (lista interativa) | — |
| `-o` | Caminho do arquivo de saída | Não | `archive.boardarchive` |
| `-h` / `--help` | Exibir ajuda | Não | — |

### API (NextcloudDeckClient)

| Método | Retorno | Descrição |
|--------|---------|-----------|
| `getBoards()` | `Board[]` | Lista boards disponíveis |
| `getBoardDetails(id)` | `Board` | Board com labels, owners, etc. |
| `getStacks(boardId)` | `Stack[]` | Stacks com cards (sem comentários) |
| `getComments(cardId)` | `Comment[]` | Comentários de um card específico |

## Fluxo Principal

1. Parsear argumentos CLI 🟢 — `importDeck.ts:36`
2. Coletar credenciais (flags ou prompts interativos) 🟢 — `importDeck.ts:45-48`
3. Criar `NextcloudDeckClient` 🟢 — `importDeck.ts:53`
4. Selecionar board (flag `-b` ou `selectBoard` interativo) 🟢 — `importDeck.ts:56`
5. Buscar detalhes do board com `getBoardDetails` 🟢 — `importDeck.ts:59`
6. Buscar stacks com cards; para cada card com comentários, buscar comments 🟢 — `importDeck.ts:60-70`
7. Converter stacks em Select "List", labels em MultiSelect "Label", due date em Date 🟢 — `importDeck.ts:98-149`
8. Criar BoardView 🟢 — `importDeck.ts:153-158`
9. Para cada card: criar CardBlock, mapear stack/label/due date, anexar descrição como TextBlock, comentários como CommentBlock 🟢 — `importDeck.ts:161-209`
10. Serializar com `ArchiveUtils.buildBlockArchive` 🟢 — `importDeck.ts:76`

## Fluxos Alternativos

- **Board ID não fornecido:** `selectBoard` lista boards com ID e título, aguarda input numérico 🟢 — `importDeck.ts:82-87`
- **Card sem stackId mapeável:** Exibe warn, card criado sem propriedade List 🟢 — `importDeck.ts:175-177`
- **Card sem descrição:** Criado sem TextBlock filho 🟢 — `importDeck.ts:190`
- **Card sem comentários:** Nenhuma chamada a getComments (otimização) 🟢 — `importDeck.ts:64`

## Dependências

- `import/nextcloud-deck/deck.ts` — NextcloudDeckClient e tipos
- `readline-sync` — Input interativo
- `import/util/archive.ts` — ArchiveUtils.buildBlockArchive
- `import/nextcloud-deck/utils.ts` — Utils.createGuid
- `webapp/src/blocks/commentBlock.ts` — CommentBlock (exclusivo deste importador)

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Comentários buscados sob demanda (só se commentsCount > 0) | `importDeck.ts:64` | 🟢 |
| Labels como MultiSelect (único importador com este tipo) | `importDeck.ts:136-141` | 🟢 |
| Comentários como CommentBlock (único importador) | `importDeck.ts:201-207` | 🟢 |
| Input interativo via readline-sync para credenciais | `importDeck.ts:45-47` | 🟢 |
| Stacks e cards em paralelo via Promise.all | `importDeck.ts:60` | 🟢 |
| Autor do comentário não preservado | `importDeck.ts:201` | 🟢 |

## Estado Interno

Nenhum — script one-shot. `optionColorIndex` global é resetado a cada execução.

## Observabilidade

- `console.log` para progresso (URL, boards disponíveis, cards, total de blocks)
- `console.warn` para card sem stackId mapeável
