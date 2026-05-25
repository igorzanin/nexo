from abc import ABC, abstractmethod
from typing import Sequence


class ICategoryRepository(ABC):
    @abstractmethod
    def get_by_id(self, category_id: str) -> object | None: ...

    @abstractmethod
    def list_by_user_team(self, user_id: str, team_id: str) -> Sequence[object]: ...

    @abstractmethod
    def create(self, category: object) -> object: ...

    @abstractmethod
    def update(self, category: object) -> object: ...

    @abstractmethod
    def soft_delete(self, category_id: str, deleted_at_ms: int) -> None: ...

    @abstractmethod
    def get_default_for_user(self, user_id: str, team_id: str) -> object | None: ...


class ICategoryBoardRepository(ABC):
    @abstractmethod
    def attach(self, category_board: object) -> object: ...

    @abstractmethod
    def detach(self, category_id: str, board_id: str) -> None: ...

    @abstractmethod
    def list_by_category(self, category_id: str) -> Sequence[object]: ...

    @abstractmethod
    def reorder(self, category_id: str, board_ids_ordered: list[str]) -> None: ...
