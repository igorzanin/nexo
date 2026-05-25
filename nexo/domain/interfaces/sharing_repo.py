from abc import ABC, abstractmethod


class ISharingRepository(ABC):
    @abstractmethod
    def get_by_board_id(self, board_id: str) -> object | None: ...

    @abstractmethod
    def upsert(self, sharing: object) -> object: ...

    @abstractmethod
    def validate_token(self, board_id: str, token: str) -> bool: ...
