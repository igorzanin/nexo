# API — Categorias, Tarefas de Implementação

## Pré-requisitos
- [ ] Modelo Category implementado
- [ ] Store com operações de categoria implementada
- [ ] Rota de boards implementada

## Tarefas

- [ ] T-01, Implementar handler GET /boards/{board_id}/categories
  - Origem no legado: `server/api/categories.go:handleGetCategories`
  - Critério de pronto: Retorna categorias do board
  - Confiança: 🟢

- [ ] T-02, Implementar handler POST /boards/{board_id}/categories
  - Origem no legado: `server/api/categories.go:handleCreateCategory`
  - Critério de pronto: Cria categoria custom; valida campos obrigatórios
  - Confiança: 🟢

- [ ] T-03, Implementar handler PATCH /boards/{board_id}/categories/{category_id}
  - Origem no legado: `server/api/categories.go:handlePatchCategory`
  - Critério de pronto: Atualiza nome da categoria
  - Confiança: 🟢

- [ ] T-04, Implementar handler DELETE /boards/{board_id}/categories/{category_id}
  - Origem no legado: `server/api/categories.go:handleDeleteCategory`
  - Critério de pronto: Soft-delete com delete_at > 0
  - Confiança: 🟢

- [ ] T-05, Implementar handler POST /categories/reorder
  - Origem no legado: `server/api/categories.go:handleReorderCategories`
  - Critério de pronto: Reordena categorias do usuário
  - Confiança: 🟢

- [ ] T-06, Implementar handler POST /categories/{category_id}/reorder
  - Origem no legado: `server/api/categories.go:handleReorderCategoryBoards`
  - Critério de pronto: Reordena boards dentro de uma categoria
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar CRUD de categoria
- [ ] TT-02, Testar soft-delete de categoria
- [ ] TT-03, Testar reorder de categorias e boards

## Ordem Sugerida
1. T-01 (GET) e T-02 (POST)
2. T-03 (PATCH) e T-04 (DELETE)
3. T-05 e T-06 (reorder)

## Lacunas Pendentes (🔴)
- 🔴 Comportamento de criação automática de categorias system — depende de trigger na criação de usuário/team
