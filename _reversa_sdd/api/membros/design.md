# API — Membros, Design Técnico

## Interface

| Método | Caminho | Entrada | Saída | Status codes |
|--------|---------|---------|-------|--------------|
| GET | `/api/v1/boards/{board_id}/members` | - | `BoardMember[]` | 200 |
| POST | `/api/v1/boards/{board_id}/members` | `BoardMember` | `BoardMember` | 201, 400 |
| PUT | `/api/v1/boards/{board_id}/members/{user_id}` | `BoardMember` | `BoardMember` | 200, 403 |
| DELETE | `/api/v1/boards/{board_id}/members/{user_id}` | - | - | 200, 403 |

## Fluxo Principal

1. Handler extrai board_id da URL 🟢
2. Para adicionar: App layer valida permissão do solicitante 🟢
3. Para remover: verifica se é o último admin (se sim, bloqueia) 🟢
4. Store persiste a associação 🟢
5. WebSocket broadcast de BroadcastMemberChange/BroadcastMemberDelete 🟢

## Dependências

- `server/app/permissions.go` — Verificação de permissões
- `server/app/boards.go` — Validação de último admin
- `server/model/board.go` — BoardMember struct

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Proteção do último admin | `server/app/boards.go:575` | 🟢 |
| minimumRole como piso de permissão | `server/mmpermissions.go:98-107` | 🟢 |
| Esquema de permissão com 4 papéis mutuamente exclusivos | Modelo BoardMember | 🟡 |

## Riscos e Lacunas
- 🔴 Como minimumRole interage com papéis explícitos? Lógica parcialmente inferida
