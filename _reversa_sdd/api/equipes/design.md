# API — Equipes, Design Técnico

## Interface

| Método | Caminho | Entrada | Saída | Status codes |
|--------|---------|---------|-------|--------------|
| GET | `/api/v1/teams` | `query: {user_id}` | `Team[]` | 200 |
| POST | `/api/v1/teams` | `Team` | `Team` | 201, 400 |

## Fluxo Principal

1. GET /teams: filtra equipes pelo user_id do query param 🟢
2. POST /teams: valida dados da equipe e persiste 🟢

## Dependências

- `server/services/store` — Persistência

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Listagem de equipes filtrando por user_id | `server/api/teams.go` | 🟢 |

## Riscos e Lacunas
- 🔴 Regras de permissão para criação de team? Não detalhado
