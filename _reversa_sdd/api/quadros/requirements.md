# API — Quadros (Boards)

## Visão Geral
Handlers REST para CRUD de boards, duplicação e vínculo com canais. Board é a entidade central de organização do Nexo, que agrupa cards e define permissões de acesso.

## Responsabilidades
- Criar, ler, atualizar e deletar boards
- Duplicar board com todos os blocks
- Gerenciar tipo do board (Open/Private) e minimumRole
- Vincular/desvincular board a canal do Mattermost

## Regras de Negócio
- Board deve ter TeamID e Type (`O`/`P`) válido 🟢
- Board Type é imutável após criação (apenas por quem tem PermissionManageBoardType) 🟢
- Convidados (guests) não podem criar boards 🟢
- Board público requer PermissionCreatePublicChannel 🟢
- Board privado requer PermissionCreatePrivateChannel 🟢
- Boards não-template são automaticamente adicionados à categoria padrão do usuário 🟢
- Board não pode ser criado com ID pré-definido 🟢
- Duplicação reverte criação se cópia de arquivos falhar 🟢
- Desvincular board de canal posta mensagem no canal 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| QB-RF01 | Listar boards de uma equipe | Must | GET /teams/{id}/boards retorna boards do time |
| QB-RF02 | Criar board | Must | POST /boards cria board com tipo e time válidos |
| QB-RF03 | Ler board por ID | Must | GET /boards/{id} retorna board |
| QB-RF04 | Atualizar board | Must | PATCH /boards/{id} atualiza campos permitidos |
| QB-RF05 | Deletar board | Must | DELETE /boards/{id} remove board |
| QB-RF06 | Duplicar board | Should | POST /boards/{id}/duplicate cria cópia fiel |
| QB-RF07 | Vincular board a canal | Should | Board linkado a canal do Mattermost |

## Critérios de Aceitação

```gherkin
Dado um usuário autenticado
Quando cria um board com type="O" e team_id válido
Então o board é criado com sucesso (201)

Dado um usuário guest
Quando tenta criar um board
Então retorna 403 Forbidden

Dado um board com um único admin
Quando tenta alterar o type do board
Então retorna 200 se tem PermissionManageBoardType, senão 403

Dado um board existente
Quando duplica o board
Então um novo board é criado com os mesmos blocks e properties
```

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `server/api/boards.go` | handleGetBoards, handleCreateBoard, handlePatchBoard, handleDeleteBoard, handleDuplicateBoard | 🟢 |
| `server/app/boards.go` | CreateBoard, PatchBoard, DeleteBoard, DuplicateBoard | 🟢 |
| `server/api/boards.go:138` | Validação de permissão para board público | 🟢 |
| `server/api/boards.go:144` | Validação de permissão para board privado | 🟢 |
