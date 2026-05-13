# API — Arquivos, Design Técnico

## Interface

| Método | Caminho | Entrada | Saída | Status codes |
|--------|---------|---------|-------|--------------|
| POST | `/api/v1/files/{team_id}/{board_id}` | `multipart/form-data` | `{file_id, name}` | 201, 413 |
| GET | `/api/v1/files/{team_id}/{board_id}/{file_id}` | - | `binary` | 200, 404 |

## Fluxo Principal

1. Handler lê multipart form e extrai arquivo 🟢
2. Valida tamanho (limite de 100KB) 🟢
3. App layer salva arquivo no backend de armazenamento 🟢
4. Retorna file_id e nome do arquivo 🟢
5. Download: handler busca file_id, retorna binário com content-type apropriado 🟢

## Dependências

- `server/app/files.go` — UploadFile, GetFile
- Backend de armazenamento (filesystem local ou S3-compatible)

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Limite de 100KB por arquivo | `server/api/files.go:45` | 🟢 |
| Upload via multipart/form-data | `server/api/files.go` | 🟢 |

## Riscos e Lacunas
- 🔴 Backend de armazenamento: filesystem local ou S3? Não confirmado
- 🔴 Proteção antimalware no upload? Não identificado
