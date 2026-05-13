# API — Equipes (Teams)

## Visão Geral
Handlers REST para gerenciamento de equipes. Team é o agrupamento de usuários no Nexo — todo board pertence a um team.

## Responsabilidades
- Listar equipes do usuário
- Criar equipe

## Regras de Negócio
- Team agrupa usuários e boards 🟢
- Usuário pode pertencer a múltiplos teams 🟢
- Criação de team verifica permissão do usuário 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| EQ-RF01 | Listar equipes do usuário | Must | GET /teams?user_id={id} retorna equipes |
| EQ-RF02 | Criar equipe | Must | POST /teams cria equipe |

## Critérios de Aceitação

```gherkin
Dado um usuário autenticado
Quando lista equipes
Então retorna as equipes às quais o usuário pertence (200)

Dado um usuário autenticado
Quando cria uma equipe com nome válido
Então a equipe é criada (201)
```

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `server/api/teams.go` | handleGetTeams, handleCreateTeam | 🟢 |
