# Aplicação, Design Técnico

## Estrutura

```
nexo/services/
├── __init__.py
├── board.py         # BoardService
├── block.py         # BlockService
├── card.py          # CardService
├── category.py      # CategoryService
├── member.py        # MemberService
├── permission.py    # PermissionService
├── import_export.py  # ImportService
├── notification.py  # NotificationService
└── onboarding.py    # OnboardingService
```

## Service Pattern

```python
class BoardService:
    def __init__(self, board_repo: BoardRepository, permission_svc: PermissionService):
        self.board_repo = board_repo
        self.permission_svc = permission_svc

    def create(self, db: Session, data: BoardCreate, user: User) -> Board:
        # Valida permissão
        if not self.permission_svc.can_create_board(user, data.type):
            raise PermissionError("Cannot create board")
        # Cria board
        board = self.board_repo.create(db, data)
        # Adiciona à categoria padrão
        category_service.add_board_to_default_category(db, user, board)
        # Broadcast WebSocket
        ws_broadcast.board_change(board.team_id, board)
        return board

    def patch(self, db: Session, board_id: str, data: BoardPatch, user: User) -> Board:
        board = self.board_repo.get(db, board_id)
        if not board:
            raise NotFoundError("Board not found")
        # Valida permissão
        if not self.permission_svc.has_permission(user, board, Permission.MANAGE_BOARD_TYPE):
            raise PermissionError()
        # Aplica patch
        board = self.board_repo.patch(db, board_id, data)
        # Broadcast
        ws_broadcast.board_change(board.team_id, board)
        return board
```

## Dependências
- `nexo/repositories/` — acesso a dados
- `nexo/models/` — SQLAlchemy models
- `nexo/ws/` — WebSocket broadcast
