# Aplicação, Tarefas de Implementação

## Tarefas

- [ ] T-01, Implementar BoardService (CRUD + duplicate + link channel)
  - Fonte legado: `server/app/boards.go`
  - Critério: Board criado com validação de tipo e permissões; duplicação com rollback

- [ ] T-02, Implementar BlockService (CRUD + batch + undelete)
  - Fonte legado: `server/app/blocks.go`
  - Critério: Block criado com validações; batch insert atômico

- [ ] T-03, Implementar CardService (CRUD)
  - Fonte legado: `server/app/cards.go`

- [ ] T-04, Implementar CategoryService (CRUD + reorder)
  - Fonte legado: `server/app/categories.go`

- [ ] T-05, Implementar MemberService (CRUD + proteção último admin)
  - Fonte legado: `server/app/members.go`

- [ ] T-06, Implementar PermissionService RBAC
  - Fonte legado: `server/app/permissions.go`
  - Critério: Verificação por papel do membro + minimumRole

- [ ] T-07, Implementar ImportService (.boardarchive)
  - Fonte legado: `server/app/import.go`

- [ ] T-08, Implementar OnboardingService
  - Fonte legado: `server/app/onboarding.go`

- [ ] T-09, Implementar NotificationService (subscriptions)
  - Fonte legado: `server/app/notifications.go`

## Lacunas
- BroadcastSubscriptionChange: não implementado (decisão do revisor)
