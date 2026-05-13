# API — Categorias, Design Técnico

## Interface

| Método | Caminho | Entrada | Saída | Status codes |
|--------|---------|---------|-------|--------------|
| GET | `/api/v1/boards/{board_id}/categories` | - | `Category[]` | 200 |
| POST | `/api/v1/boards/{board_id}/categories` | `Category` | `Category` | 201, 400 |
| PATCH | `/api/v1/boards/{board_id}/categories/{category_id}` | `CategoryPatch` | `Category` | 200, 400 |
| DELETE | `/api/v1/boards/{board_id}/categories/{category_id}` | - | - | 200 |
| POST | `/api/v1/categories/reorder` | `{order: string[]}` | - | 200 |
| POST | `/api/v1/categories/{category_id}/reorder` | `{board_order: string[]}` | - | 200 |

## Fluxo Principal

1. Handler extrai parâmetros da URL 🟢
2. Para criação: valida name, user_id, team_id 🟢
3. App layer persiste categoria com delete_at=0 e type=("system"|"custom") 🟢
4. WebSocket broadcast dispara BroadcastCategoryChange 🟢
5. Reorder: app layer atualiza order fields na store e broadcast 🟢

## Dependências

- `server/app/categories.go` — CreateCategory, PatchCategory, DeleteCategory, ReorderCategories, ReorderCategoryBoards
- `server/model/category.go` — Category, CategoryPatch
- `server/services/store` — Persistência

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Soft-delete com delete_at em vez de hard-delete | `server/model/category.go:46` | 🟢 |
| Categorias system vs custom para diferenciar automáticas de manuais | `server/model/category.go:104` | 🟢 |
| Reorder armazena ordem como array de IDs | `server/app/categories.go` | 🟢 |

## Riscos e Lacunas
- 🔴 Como são criadas as categorias system automáticas? Não detalhado
- 🟡 Limite de categorias por usuário? Não identificado
