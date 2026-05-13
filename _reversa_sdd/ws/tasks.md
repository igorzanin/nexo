# WebSocket, Tarefas de Implementação

## Tarefas

- [ ] T-01, Implementar WSConnectionManager (connect, disconnect, broadcast)
  - Fonte legado: `server/ws/server.go`
  - Critério: Gerenciamento concorrente de conexões com asyncio.Lock

- [ ] T-02, Implementar autenticação WebSocket via AUTH com JWT
  - Fonte legado: `server/ws/server.go:authenticateListener`
  - Critério: AUTH com JWT válido autentica sessão

- [ ] T-03, Implementar subscribe/unsubscribe por team
  - Fonte legado: `server/ws/server.go`

- [ ] T-04, Implementar subscribe/unsubscribe por block com read token
  - Fonte legado: `server/ws/server.go`

- [ ] T-05, Implementar broadcast_block_change e broadcast_block_delete
  - Fonte legado: `server/ws/server.go`

- [ ] T-06, Implementar broadcast_board_change e broadcast_board_delete
  - Fonte legado: `server/ws/server.go`

- [ ] T-07, Implementar broadcast_member_change e broadcast_member_delete
  - Fonte legado: `server/ws/server.go`

- [ ] T-08, Implementar broadcast_config_change (todos os listeners)
  - Fonte legado: `server/ws/server.go`

- [ ] T-09, Implementar broadcast_category_change (usuário específico)
  - Fonte legado: `server/ws/server.go`

## Lacunas
- PluginAdapter removido (apenas standalone)
- BroadcastSubscriptionChange: não implementado (decisão do revisor)
- BroadcastCardLimitTimestampChange: não implementado (decisão do revisor)
