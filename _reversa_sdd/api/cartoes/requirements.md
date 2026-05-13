# API — Cartões (Cards)

## Visão Geral
Handlers REST para CRUD de cards. Card é a unidade atômica de trabalho no Nexo — contém properties customizáveis, conteúdo ordenado (contentOrder), comentários e anexos.

## Responsabilidades
- Listar cards de um board
- Criar, atualizar e deletar cards
- Gerenciar properties, contentOrder e icon

## Regras de Negócio
- Card deve ter ID, BoardID, ContentOrder, Properties não-nulo, CreateAt e UpdateAt > 0 🟢
- Card icon deve ter no máximo 1 grafema 🟢
- ContentOrder gerencia a ordem dos blocos de conteúdo do card 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| CA-RF01 | Listar cards de um board | Must | GET /boards/{id}/cards retorna todos os cards |
| CA-RF02 | Criar card | Must | POST /boards/{id}/cards cria card com properties e contentOrder |
| CA-RF03 | Atualizar card | Must | PATCH /boards/{id}/cards/{id} atualiza campos |
| CA-RF04 | Deletar card | Must | DELETE /boards/{id}/cards/{id} remove card |
| CA-RF05 | Validar icon | Should | Icon com >1 grafema é rejeitado |

## Critérios de Aceitação

```gherkin
Dado um board existente
Quando cria um card com properties e content_order válidos
Então o card é criado e retorna 201

Dado um card existente
Quando tenta definir um icon com 2 emojis
Então retorna 400 Bad Request

Dado um card existente
Quando atualiza suas properties
Então as properties são atualizadas e retorna 200
```

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `server/api/cards.go` | handleGetCards, handleCreateCard, handlePatchCard, handleDeleteCard | 🟢 |
| `server/model/card.go` | Card, CardPatch structs e validações | 🟢 |
