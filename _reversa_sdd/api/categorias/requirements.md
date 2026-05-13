# API — Categorias

## Visão Geral
Handlers REST para CRUD de categorias. Categoria é uma pasta na sidebar que agrupa boards. Suporta dois tipos: `system` (criada automaticamente pelo sistema) e `custom` (criada pelo usuário).

## Responsabilidades
- Listar categorias de um board
- Criar, atualizar e deletar categorias
- Reordenar categorias e boards dentro de categorias

## Regras de Negócio
- Categoria deve ter ID, Name, UserID, TeamID não-vazios 🟢
- Tipo de categoria: `"system"` ou `"custom"` 🟢
- Sistema cria categorias do tipo `"system"` automaticamente 🟡
- Categoria deletada via soft-delete (deleteAt > 0) 🟢
- Board não-template é adicionado à categoria padrão automaticamente 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| CA-RF01 | Listar categorias de um board | Must | GET retorna categorias do board |
| CA-RF02 | Criar categoria | Must | POST cria categoria type=custom |
| CA-RF03 | Atualizar categoria | Must | PATCH atualiza nome da categoria |
| CA-RF04 | Deletar categoria | Must | DELETE marca soft-delete |
| CA-RF05 | Reordenar categorias | Should | POST reordena lista de categorias do usuário |
| CA-RF06 | Reordenar boards na categoria | Should | POST reordena boards dentro de uma categoria |

## Critérios de Aceitação

```gherkin
Dado um usuário autenticado
Quando cria uma categoria com name, user_id e team_id
Então a categoria é criada com type="custom" (201)

Dado uma categoria existente
Quando a deleta
Então a categoria é marcada com delete_at > 0

Dado um board criado (não-template)
Quando verifica as categorias do usuário
Então o board aparece na categoria padrão automática
```

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `server/api/categories.go` | handleGetCategories, handleCreateCategory, handlePatchCategory, handleDeleteCategory, handleReorderCategories, handleReorderCategoryBoards | 🟢 |
| `server/app/categories.go` | CreateCategory, PatchCategory, DeleteCategory, ReorderCategories, ReorderCategoryBoards | 🟢 |
| `server/model/category.go` | Category struct e validações | 🟢 |
