# API — Membros (Board Members)

## Visão Geral
Handlers REST para gerenciamento de membros de boards. Controla quem tem acesso a cada board e com qual papel (admin, editor, commenter, viewer).

## Responsabilidades
- Listar membros de um board
- Adicionar, atualizar e remover membros
- Garantir que o último admin não seja removido ou rebaixado

## Regras de Negócio
- Último admin de um board não pode ser removido nem ter seu papel rebaixado 🟢
- BoardMember.schemeAdmin/Editor/Commenter/Viewer são mutuamente exclusivos 🟡
- BoardMember.minimumRole atua como piso: se minimumRole="editor", todo membro ganha SchemeEditor 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| MB-RF01 | Listar membros de um board | Must | GET /boards/{id}/members retorna membros |
| MB-RF02 | Adicionar membro ao board | Must | POST /boards/{id}/members adiciona com papel |
| MB-RF03 | Atualizar papel do membro | Must | PUT /boards/{id}/members/{userId} altera papel |
| MB-RF04 | Remover membro do board | Must | DELETE /boards/{id}/members/{userId} remove |
| MB-RF05 | Impedir remoção do último admin | Must | DELETE /boards/{id}/members/{userId} do último admin retorna 403 |

## Critérios de Aceitação

```gherkin
Dado um board com 2 admins
Quando remove um dos admins
Então o admin é removido (200)

Dado um board com 1 admin
Quando tenta remover o único admin
Então retorna 403 Forbidden

Dado um board com minimumRole="editor"
Quando adiciona um novo membro sem papel explícito
Então o membro ganha SchemeEditor automaticamente
```

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `server/api/members.go` | handleGetMembers, handleCreateMember, handleUpdateMember, handleDeleteMember | 🟢 |
| `server/app/boards.go:575` | Validação de último admin | 🟢 |
| `server/mmpermissions.go:98-107` | Lógica de minimumRole | 🟢 |
