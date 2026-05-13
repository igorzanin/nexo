# API — Membros, Tarefas de Implementação

## Pré-requisitos
- [ ] Modelo BoardMember implementado
- [ ] Sistema de permissões implementado
- [ ] Rota de boards implementada

## Tarefas

- [ ] T-01, Implementar handler GET /boards/{board_id}/members
  - Origem no legado: `server/api/members.go:handleGetMembers`
  - Critério de pronto: Retorna lista de membros do board
  - Confiança: 🟢

- [ ] T-02, Implementar handler POST /boards/{board_id}/members
  - Origem no legado: `server/api/members.go:handleCreateMember`
  - Critério de pronto: Adiciona membro com papel; valida minimumRole
  - Confiança: 🟢

- [ ] T-03, Implementar handler PUT /boards/{board_id}/members/{user_id}
  - Origem no legado: `server/api/members.go:handleUpdateMember`
  - Critério de pronto: Atualiza papel do membro
  - Confiança: 🟢

- [ ] T-04, Implementar handler DELETE /boards/{board_id}/members/{user_id}
  - Origem no legado: `server/api/members.go:handleDeleteMember`
  - Critério de pronto: Remove membro; bloqueia remoção do último admin (403)
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar CRUD de membros
- [ ] TT-02, Testar proteção do último admin
- [ ] TT-03, Testar minimumRole como piso de permissão

## Ordem Sugerida
1. T-01 e T-02
2. T-03 e T-04

## Lacunas Pendentes (🔴)
- 🔴 Lógica exata de minimumRole + papéis explícitos — requer validação
