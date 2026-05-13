# API — Blocos, Tarefas de Implementação

## Pré-requisitos
- [ ] Modelo Block implementado com validações
- [ ] Store com operações de block implementada
- [ ] Middleware de autenticação e permissão implementados
- [ ] Rota de boards implementada

## Tarefas

- [ ] T-01, Implementar handler GET /boards/{board_id}/blocks com filtros
  - Origem no legado: `server/api/blocks.go:handleGetBlocks`
  - Critério de pronto: Retorna blocks filtrados por parent_id e type; ordenados por update_at
  - Confiança: 🟢

- [ ] T-02, Implementar handler POST /boards/{board_id}/blocks (individual e batch)
  - Origem no legado: `server/api/blocks.go:handleCreateBlocks`
  - Critério de pronto: Aceita Block ou Block[]; valida board_id e constraints; retorna 201
  - Confiança: 🟢

- [ ] T-03, Implementar handler PATCH /boards/{board_id}/blocks/{block_id}
  - Origem no legado: `server/api/blocks.go:handlePatchBlock`
  - Critério de pronto: Atualiza campos parciais do block
  - Confiança: 🟢

- [ ] T-04, Implementar handler DELETE /boards/{board_id}/blocks/{block_id}
  - Origem no legado: `server/api/blocks.go:handleDeleteBlock`
  - Critério de pronto: Block marcado com delete_at; block inexistente não gera erro
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar CRUD individual de block
- [ ] TT-02, Testar batch insert de blocks
- [ ] TT-03, Testar deleção idempotente de block inexistente
- [ ] TT-04, Testar rejeição de title > 16383 runes
- [ ] TT-05, Testar criação de block sem permissão ManageBoardCards

## Ordem Sugerida
1. T-01 (GET) e T-02 (POST) — funcionalidades principais
2. T-03 (PATCH) e T-04 (DELETE) — complementares

## Lacunas Pendentes (🔴)
- 🔴 Tamanho máximo do payload batch? Não identificado
