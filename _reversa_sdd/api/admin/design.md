# API — Administração, Design Técnico

## Interface

| Método | Caminho | Entrada | Saída | Status codes |
|--------|---------|---------|-------|--------------|
| GET | `/api/v1/admin/config` | - | `Configuration` | 200, 403 |
| PUT | `/api/v1/admin/config` | `Configuration` | `Configuration` | 200, 403 |

## Fluxo Principal

1. Middleware verifica se usuário é admin do sistema 🟢
2. GET: app layer lê configuração atual do store 🟢
3. PUT: app layer valida e persiste nova configuração 🟢
4. WebSocket broadcast de BroadcastConfigChange 🟢
5. Retorna configuração serializada 🟢

## Dependências

- `server/services/config` — Gerenciamento de configuração
- `server/services/store` — Persistência

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Config gerenciada via viper | Dependência go.mod | 🟡 |
| WebSocket broadcast notifica todos os listeners | `server/api/admin.go` | 🟢 |

## Riscos e Lacunas
- 🔴 Campos exatos da Configuration expostos via API? Não detalhado
