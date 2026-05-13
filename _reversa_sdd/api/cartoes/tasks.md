# API — Cartões, Tarefas de Implementação

## Pré-requisitos
- [ ] Modelo Card implementado
- [ ] Store com operações de card implementada
- [ ] Rota de boards implementada

## Tarefas

- [ ] T-01, Implementar handler GET /boards/{board_id}/cards
  - Origem no legado: `server/api/cards.go:handleGetCards`
  - Critério de pronto: Retorna todos os cards do board ordenados
  - Confiança: 🟢

- [ ] T-02, Implementar handler POST /boards/{board_id}/cards
  - Origem no legado: `server/api/cards.go:handleCreateCard`
  - Critério de pronto: Cria card com properties, contentOrder, icon; valida icon <= 1 grafema
  - Confiança: 🟢

- [ ] T-03, Implementar handler PATCH /boards/{board_id}/cards/{card_id}
  - Origem no legado: `server/api/cards.go:handlePatchCard`
  - Critério de pronto: Atualiza campos do CardPatch
  - Confiança: 🟢

- [ ] T-04, Implementar handler DELETE /boards/{board_id}/cards/{card_id}
  - Origem no legado: `server/api/cards.go:handleDeleteCard`
  - Critério de pronto: Card marcado como deletado
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar CRUD completo de card
- [ ] TT-02, Testar validação de icon com múltiplos grafemas
- [ ] TT-03, Testar criação de card com properties variadas

## Ordem Sugerida
1. T-01 (GET) e T-02 (POST) — criação e leitura
2. T-03 (PATCH) e T-04 (DELETE) — atualização e remoção

## Lacunas Pendentes (🔴)
- 🔴 Limite de cards por board (feature cloud desabilitada, confirmar se deve ser implementada)
