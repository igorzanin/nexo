# Repositories, Design Técnico

## Estrutura de Pacotes

```
nexo/
├── repositories/
│   ├── __init__.py
│   ├── board.py        # BoardRepository
│   ├── block.py        # BlockRepository
│   ├── card.py         # CardRepository
│   ├── user.py         # UserRepository
│   ├── session.py      # SessionRepository
│   ├── team.py         # TeamRepository
│   ├── category.py     # CategoryRepository
│   ├── subscription.py # SubscriptionRepository
│   └── sharing.py      # SharingRepository
├── services/
│   ├── __init__.py
│   ├── file.py         # FileService
│   ├── permissions.py  # PermissionsService
│   └── notification.py # NotificationService
└── database.py          # Engine, SessionLocal, Base
```

## Repository Pattern

```python
class BoardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, board_id: str) -> Board | None:
        return self.db.get(Board, board_id)

    def get_by_team(self, team_id: str) -> list[Board]:
        return self.db.exec(
            select(Board).where(Board.team_id == team_id, Board.delete_at == 0)
        ).all()

    def create(self, data: BoardCreate) -> Board:
        board = Board(**data.model_dump())
        self.db.add(board)
        self.db.commit()
        self.db.refresh(board)
        return board

    def patch(self, board_id: str, data: BoardPatch) -> Board | None:
        board = self.get(board_id)
        if not board:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(board, key, value)
        self.db.commit()
        self.db.refresh(board)
        return board

    def soft_delete(self, board_id: str) -> bool:
        board = self.get(board_id)
        if not board:
            return False
        board.delete_at = int(time() * 1000)
        self.db.commit()
        return True
```

## Alembic Migrations

```python
# migrations/versions/000001_init.py
def upgrade():
    op.create_table("teams", ...)
    op.create_table("boards", ...)
    op.create_table("blocks", ...)
    # ...

def downgrade():
    op.drop_table("blocks")
    op.drop_table("boards")
    op.drop_table("teams")
```

## Dependências
- `sqlalchemy`, `alembic`
- `python-multipart` (file upload)
- `aiofiles` (async file operations)
