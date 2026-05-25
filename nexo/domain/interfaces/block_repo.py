from abc import ABC, abstractmethod
from typing import Sequence


class IBlockRepository(ABC):
    @abstractmethod
    def get_by_id(self, block_id: str) -> object | None: ...

    @abstractmethod
    def list_by_board(self, board_id: str, include_deleted: bool = False) -> Sequence[object]: ...

    @abstractmethod
    def create(self, block: object) -> object: ...

    @abstractmethod
    def update(self, block: object) -> object: ...

    @abstractmethod
    def soft_delete(self, block_id: str, deleted_at_ms: int) -> None: ...

    @abstractmethod
    def archive_to_history(self, block_id: str, insert_at_ms: int) -> None: ...

    @abstractmethod
    def restore_from_history(self, block_id: str, insert_at_ms: int) -> object: ...

    @abstractmethod
    def insert_batch(self, blocks: Sequence[object]) -> Sequence[object]: ...
