# API — Quadros, Tarefas de Implementação

## Pré-requisitos
- [ ] Modelo Board implementado (server/model)
- [ ] Store com operações de board implementada
- [ ] Middleware de autenticação implementado
- [ ] Sistema de permissões implementado

## Tarefas

- [ ] T-01, Implementar handler GET /teams/{team_id}/boards
  - Origem no legado: `server/api/boards.go:handleGetBoards`
  - Critério de pronto: Lista boards da equipe; ordenados por update_at (decrescente)
  - Confiança: 🟢

- [ ] T-02, Implementar handler POST /boards (criação)
  - Origem no legado: `server/api/boards.go:handleCreateBoard`
  - Critério de pronto: Valida team_id, type (O/P), permissões; board é criado e adicionado à categoria padrão
  - Confiança: 🟢

- [ ] T-03, Implementar handler GET /boards/{board_id}
  - Origem no legado: `server/api/boards.go:handleGetBoard`
  - Critério de pronto: Retorna board por ID; 404 se não encontrado
  - Confiança: 🟢

- [ ] T-04, Implementar handler PATCH /boards/{board_id}
  - Origem no legado: `server/api/boards.go:handlePatchBoard`
  - Critério de pronto: Atualiza campos do BoardPatch; valida permissão ManageBoardType se type mudar
  - Confiança: 🟢

- [ ] T-05, Implementar handler DELETE /boards/{board_id}
  - Origem no legado: `server/api/boards.go:handleDeleteBoard`
  - Critério de pronto: Board marcado como deletado; deleta todos os blocks associados
  - Confiança: 🟢

- [ ] T-06, Implementar handler POST /boards/{board_id}/duplicate
  - Origem no legado: `server/api/boards.go:handleDuplicateBoard`
  - Critério de pronto: Board duplicado com blocks; rollback em caso de falha de arquivos
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar criação de board com tipo O e P
- [ ] TT-02, Testar criação de board por guest (deve falhar)
- [ ] TT-03, Testar duplicação de board com blocks
- [ ] TT-04, Testar remoção de board e verificar blocks deletados

## Ordem Sugerida
1. T-01 (listagem) — mais simples, bom ponto de partida
2. T-02 (criação) — dependência para os demais
3. T-03, T-04, T-05 (CRUD restante)
4. T-06 (duplicação) — mais complexo, requer blocks e files funcionando

## Lacunas Pendentes (🔴)
- 🔴 Limite de boards por equipe? Verificar se deve ser implementado
