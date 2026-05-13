# API — Administração (Admin)

## Visão Geral
Handlers REST para administração do servidor. Permite ler e alterar configuração global, visualizar métricas e gerenciar logs. Acesso restrito a administradores do sistema.

## Responsabilidades
- Ler configuração do servidor
- Alterar configuração do servidor
- Coleta de métricas (Prometheus)

## Regras de Negócio
- Apenas admin do sistema pode acessar endpoints admin 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| AD-RF01 | Ler configuração | Must | GET /admin/config retorna config atual; 403 se não admin |
| AD-RF02 | Alterar configuração | Must | PUT /admin/config atualiza config; 403 se não admin |

## Critérios de Aceitação

```gherkin
Dado um admin do sistema autenticado
Quando acessa GET /admin/config
Então a configuração do servidor é retornada (200)

Dado um admin do sistema autenticado
Quando altera PUT /admin/config com campos válidos
Então a configuração é atualizada (200)

Dado um usuário não-admin autenticado
Quando acessa GET /admin/config
Então retorna 403 Forbidden
```

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `server/api/admin.go` | handleGetConfig, handleSetConfig | 🟢 |
