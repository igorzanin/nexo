from abc import ABC, abstractmethod
from typing import Sequence


class IBoardRepository(ABC):
    @abstractmethod
    def get_by_id(self, board_id: str) -> object | None: ...

    @abstractmethod
    def list_by_team(self, team_id: str, include_deleted: bool = False) -> Sequence[object]: ...

    @abstractmethod
    def create(self, board: object) -> object: ...

    @abstractmethod
    def update(self, board: object) -> object: ...

    @abstractmethod
    def soft_delete(self, board_id: str, deleted_at_ms: int) -> None: ...

    @abstractmethod
    def count_admins(self, board_id: str) -> int: ...
