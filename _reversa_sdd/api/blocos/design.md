# API — Blocos, Design Técnico

## Interface

| Método | Caminho | Entrada | Saída | Status codes |
|--------|---------|---------|-------|--------------|
| GET | `/api/v1/boards/{board_id}/blocks` | `query: {parent_id, type}` | `Block[]` | 200 |
| POST | `/api/v1/boards/{board_id}/blocks` | `Block \| Block[]` | `Block \| Block[]` | 201, 400 |
| PATCH | `/api/v1/boards/{board_id}/blocks/{block_id}` | `BlockPatch` | `Block` | 200, 400 |
| DELETE | `/api/v1/boards/{board_id}/blocks/{block_id}` | - | - | 200 |

## Fluxo Principal

1. Handler extrai board_id da URL e valida 🟢
2. Para GET: aplica filtros opcionais parent_id e type 🟢
3. Para POST: faz unmarshal do body — se array, trata como batch; se objeto, individual 🟢
4. App layer valida board_id, permissão (ManageBoardCards) e constraints do model 🟢
5. Store persiste o(s) block(s) 🟢
6. App layer dispara BroadcastBlockChange via WebSocket 🟢
7. Handler retorna block(s) serializados 🟢

## Fluxos Alternativos

- **Batch com board_id inconsistente:** store rejeita transação 🟢
- **Title excede limite:** model validation retorna erro 🟢
- **Block já deletado ao deletar novamente:** operação idempotente, retorna 200 🟢

## Dependências

- `server/app/blocks.go` — CreateBlocks, PatchBlock, DeleteBlock
- `server/model/block.go` — Block, BlockPatch, validações
- `server/services/store` — Persistência de blocks
- `server/ws` — Broadcast de mudanças

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Suporte a batch insert (POST com array) no mesmo endpoint de criação individual | `server/api/blocks.go:handleCreateBlocks` | 🟢 |
| Soft-delete (delete_at) em vez de hard-delete | `server/model/block.go` | 🟢 |
| Validação de pertencimento ao board em toda operação CRUD | `server/api/blocks.go:139` | 🟢 |

## Riscos e Lacunas
- 🟡 Blocos órfãos (parent_id apontando para block deletado)? Comportamento não documentado
- 🔴 Limite de blocks por requisição batch? Não identificado
