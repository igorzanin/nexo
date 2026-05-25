import time

from sqlalchemy import select, update
from sqlalchemy.orm import Session as DBSession

from nexo.models import Category, CategoryBoard
from nexo.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def get(self, category_id: str) -> Category | None:
        return self.db.get(Category, category_id)

    def get_by_team(self, team_id: str) -> list[Category]:
        stmt = select(Category).where(Category.team_id == team_id, Category.delete_at == 0)
        return list(self.db.execute(stmt).scalars().all())

    def get_by_user(self, user_id: str) -> list[Category]:
        stmt = select(Category).where(Category.user_id == user_id, Category.delete_at == 0)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, data: CategoryCreate) -> Category:
        now = int(time.time() * 1000)
        cat = Category(
            name=data.name,
            user_id=data.userID,
            team_id=data.teamID,
            type=data.type.value if hasattr(data.type, "value") else data.type,
            sort_order=data.sortOrder,
            create_at=now,
            update_at=now,
            delete_at=0,
        )
        self.db.add(cat)
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def update(self, category_id: str, data: CategoryUpdate) -> Category | None:
        cat = self.get(category_id)
        if not cat:
            return None
        patch = data.model_dump(exclude_unset=True)
        patch.pop("collapsed", None)
        if "sortOrder" in patch:
            patch["sort_order"] = patch.pop("sortOrder")
        for key, value in patch.items():
            setattr(cat, key, value)
        cat.update_at = int(time.time() * 1000)
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def soft_delete(self, category_id: str) -> bool:
        cat = self.get(category_id)
        if not cat:
            return False
        cat.delete_at = int(time.time() * 1000)
        self.db.commit()
        return True

    def reorder_categories(self, category_ids: list[str]) -> None:
        for i, cid in enumerate(category_ids):
            self.db.execute(update(Category).where(Category.id == cid).values(sort_order=i))
        self.db.commit()

    def reorder_category_boards(self, category_id: str, board_ids: list[str]) -> None:
        for i, bid in enumerate(board_ids):
            self.db.execute(
                update(CategoryBoard).where(
                    CategoryBoard.category_id == category_id,
                    CategoryBoard.board_id == bid,
                ).values(sort_order=i)
            )
        self.db.commit()
