# API — Blocos (Blocks)

## Visão Geral
Handlers REST para CRUD de blocks. Block é a entidade base polimórfica do Nexo — boards, cards, views, comments, text, images etc. são todos subtipos de Block.

## Responsabilidades
- Listar blocks por board com filtros (parent_id, type)
- Criar blocks (individual ou batch)
- Atualizar blocks via patch parcial
- Deletar blocks (soft-delete)

## Regras de Negócio
- Block deve ter BoardID não-vazio 🟢
- Block deve pertencer ao board da rota 🟢
- Batch insert: todos os blocks devem pertencer ao mesmo board 🟢
- Block title máximo: 16383 runes 🟢
- Block fields JSON máximo: 800000 runes 🟢
- Deletar bloco inexistente NÃO é erro (idempotente) 🟢
- Comentários requerem PermissionCommentBoardCards 🟢
- Modificar conteúdo requer PermissionManageBoardCards 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| BL-RF01 | Listar blocks de um board | Must | GET retorna blocks filtrados por parent_id e/ou type |
| BL-RF02 | Criar block individual | Must | POST cria block vinculado ao board |
| BL-RF03 | Criar blocks em batch | Must | POST com array cria múltiplos blocks de uma vez |
| BL-RF04 | Atualizar block | Must | PATCH atualiza campos do block |
| BL-RF05 | Deletar block | Must | DELETE marca block com delete_at |
| BL-RF06 | Validar tamanho do title | Should | Title > 16383 runes é rejeitado |

## Critérios de Aceitação

```gherkin
Dado um board existente
Quando cria um block com board_id, type e title válidos
Então block é criado e retorna 201

Dado um board existente
Quando envia POST com array de 3 blocks
Então todos os 3 blocks são criados no board (201)

Dado um block que não existe
Quando tenta deletá-lo
Então retorna 200 (idempotente, sem erro)

Dado um board
Quando cria um block sem board_id
Então retorna 400 Bad Request
```

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `server/api/blocks.go` | handleGetBlocks, handleCreateBlocks, handlePatchBlock, handleDeleteBlock | 🟢 |
| `server/app/blocks.go` | CreateBlocks, PatchBlock, DeleteBlock, UndeleteBlock | 🟢 |
| `server/model/block.go` | Block, BlockPatch structs e validações | 🟢 |
