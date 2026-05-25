import time

import time

from sqlalchemy.orm import Session as DBSession

from nexo.models import CategoryBoard
from nexo.repositories.category import CategoryRepository
from nexo.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, db: DBSession):
        self.db = db
        self.category_repo = CategoryRepository(db)

    def create(self, data: CategoryCreate) -> object:
        return self.category_repo.create(data)

    def get_by_team(self, team_id: str) -> list:
        return self.category_repo.get_by_team(team_id)

    def update(self, category_id: str, data: CategoryUpdate) -> object:
        updated = self.category_repo.update(category_id, data)
        if updated is None:
            raise ValueError("Category not found")
        return updated

    def delete(self, category_id: str) -> bool:
        return self.category_repo.soft_delete(category_id)

    def reorder_categories(self, category_ids: list[str]) -> None:
        self.category_repo.reorder_categories(category_ids)

    def reorder_category_boards(self, category_id: str, board_ids: list[str]) -> None:
        self.category_repo.reorder_category_boards(category_id, board_ids)

    def add_board_to_default_category(self, user_id: str, board_id: str) -> None:
        categories = self.category_repo.get_by_user(user_id)
        default = next((c for c in categories if c.type == "system"), None)
        if default:
            existing = self.db.query(CategoryBoard).filter(
                CategoryBoard.category_id == default.id,
                CategoryBoard.board_id == board_id,
            ).first()
            if not existing:
                now = int(time.time() * 1000)
                self.db.add(
                    CategoryBoard(
                        user_id=default.user_id,
                        team_id=default.team_id,
                        category_id=default.id,
                        board_id=board_id,
                        sort_order=0,
                        hide=False,
                        create_at=now,
                        update_at=now,
                        delete_at=0,
                    )
                )
                self.db.commit()

    def add_board_to_category(self, category_id: str, board_id: str, sort_order: int = 0) -> None:
        existing = self.db.query(CategoryBoard).filter(
            CategoryBoard.category_id == category_id,
            CategoryBoard.board_id == board_id,
        ).first()
        if not existing:
            category = self.category_repo.get(category_id)
            if category is None:
                raise ValueError("Category not found")
            now = int(time.time() * 1000)
            self.db.add(
                CategoryBoard(
                    user_id=category.user_id,
                    team_id=category.team_id,
                    category_id=category_id,
                    board_id=board_id,
                    sort_order=sort_order,
                    hide=False,
                    create_at=now,
                    update_at=now,
                    delete_at=0,
                )
            )
            self.db.commit()

    def remove_board_from_category(self, category_id: str, board_id: str) -> None:
        self.db.query(CategoryBoard).filter(
            CategoryBoard.category_id == category_id,
            CategoryBoard.board_id == board_id,
        ).delete()
        self.db.commit()
