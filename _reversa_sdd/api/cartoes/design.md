# API — Cartões, Design Técnico

## Interface

| Método | Caminho | Entrada | Saída | Status codes |
|--------|---------|---------|-------|--------------|
| GET | `/api/v1/boards/{board_id}/cards` | - | `Card[]` | 200 |
| POST | `/api/v1/boards/{board_id}/cards` | `Card` | `Card` | 201, 400 |
| PATCH | `/api/v1/boards/{board_id}/cards/{card_id}` | `CardPatch` | `Card` | 200, 400 |
| DELETE | `/api/v1/boards/{board_id}/cards/{card_id}` | - | - | 200 |

## Fluxo Principal

1. Handler extrai board_id e card_id da URL 🟢
2. Handler faz unmarshal do body JSON 🟢
3. App layer valida Card (properties, contentOrder, icon) 🟢
4. Store persiste o card 🟢
5. WebSocket broadcast de BlockChange é disparado 🟢
6. Handler retorna card serializado 🟢

## Dependências

- `server/app/blocks.go` — Cards são armazenados como blocks
- `server/model/card.go` — Card, CardPatch
- `server/services/store` — Persistência

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Card é armazenado como Block com type específico de card | `server/model/card.go` | 🟢 |
| Properties é um map[string]interface{} para suportar schemas dinâmicos | `server/model/card.go` | 🟢 |

## Riscos e Lacunas
- 🔴 Limite de cards por board? Feature de cloud limits existe mas está desabilitada
- 🟡 Como properties são validadas contra o schema do board? Não confirmado
