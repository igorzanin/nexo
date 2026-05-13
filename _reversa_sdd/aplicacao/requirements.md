# Aplicação — Lógica de Negócio (Services)

## Visão Geral
Camada de serviços Python que implementa toda a lógica de domínio: criação e manipulação de boards, blocks, cards, categorias, membros, permissões, notificações e importação/exportação. Chamada pelos routers FastAPI e chama os repositórios SQLAlchemy.

## Responsabilidades
- CRUD de boards com validação de regras de negócio
- CRUD de blocks/cards com validação de constraints
- Gerenciamento de permissões RBAC
- Gerenciamento de categorias e reordenação
- Gerenciamento de membros de board
- Notificações via subscription
- Importação e exportação de boards (.boardarchive)
- Tour de onboarding

## Stack

| Componente | Tecnologia |
|------------|-----------|
| Framework | Python 3.12+ |
| ORM | SQLAlchemy 2.0 |
| Serialização | Pydantic v2 |
| Background | FastAPI BackgroundTasks |

## Regras de Negócio
- Board type (O/P) imutável após criação, exceto por PermissionManageBoardType 🟢
- Último admin de board não pode ser removido/rebaixado 🟢
- Block deve pertencer ao board em toda operação 🟢
- Todos os blocks em batch insert devem pertencer ao mesmo board 🟢
- Convidados não podem criar boards 🟢
- Board não-template adicionado à categoria padrão automaticamente 🟢
- Duplicação de board reverte se cópia de arquivos falhar 🟢
- Rate limiting ativo para operações sensíveis 🟢

## Rastreabilidade

| Serviço | Fonte legado | Confiança |
|---------|-------------|-----------|
| BoardService | `server/app/boards.go` | 🟢 |
| BlockService | `server/app/blocks.go` | 🟢 |
| CardService | `server/app/cards.go` | 🟢 |
| CategoryService | `server/app/categories.go` | 🟢 |
| MemberService | `server/app/members.go` | 🟢 |
| PermissionService | `server/app/permissions.go` | 🟢 |
| ImportService | `server/app/import.go` | 🟢 |
| OnboardingService | `server/app/onboarding.go` | 🟢 |
| NotificationService | `server/app/notifications.go` | 🟢 |
