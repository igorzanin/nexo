# API — Quadros, Design Técnico

## Interface

| Método | Caminho | Entrada | Saída | Status codes |
|--------|---------|---------|-------|--------------|
| GET | `/api/v1/teams/{team_id}/boards` | `team_id: string` | `Board[]` | 200 |
| POST | `/api/v1/boards` | `Board` | `Board` | 201, 400, 403 |
| GET | `/api/v1/boards/{board_id}` | `board_id: string` | `Board` | 200, 404 |
| PATCH | `/api/v1/boards/{board_id}` | `BoardPatch` | `Board` | 200, 400, 403 |
| DELETE | `/api/v1/boards/{board_id}` | `board_id: string` | - | 200, 403 |
| POST | `/api/v1/boards/{board_id}/duplicate` | `board_id: string` | `Board` | 201 |

## Fluxo Principal

1. Handler recebe requisição HTTP com parâmetros validados pelo router 🟢
2. Handler extrai session do contexto (setado pelo middleware requireAuth) 🟢
3. Handler chamando método correspondente em `server/app` 🟢
4. App layer valida permissões (PermissionCreatePublicChannel, PermissionManageBoardType, etc.) 🟢
5. App layer persiste via store e retorna resultado 🟢
6. Handler serializa resposta JSON 🟢
7. App layer dispara BroadcastBoardChange via WebSocket em escrita 🟢

## Fluxos Alternativos

- **Board não encontrado:** store retorna ErrNotFound → handler retorna 404 🟢
- **Sem permissão:** app layer retorna erro de permissão → handler retorna 403 🟢
- **Board duplicado com arquivos:** se cópia de arquivos falha, board criado é deletado (rollback) 🟢

## Dependências

- `server/app/boards.go` — CreateBoard, PatchBoard, DeleteBoard, DuplicateBoard
- `server/app/permissions.go` — Verificação de permissões
- `server/services/store` — Persistência
- `server/model/board.go` — Tipos Board, BoardPatch, BoardMember

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| ID do board gerado pelo servidor, não aceito do cliente | `server/app/boards.go:234` | 🟢 |
| Duplicação com rollback em caso de falha | `server/app/boards.go:190` | 🟢 |
| Boards não-template adicionados à categoria padrão automaticamente | `server/app/boards.go:269` | 🟢 |

## Riscos e Lacunas
- 🔴 Limite de boards por equipe? Não identificado no código
- 🟡 Ordenação padrão de boards na listagem? Não confirmado
