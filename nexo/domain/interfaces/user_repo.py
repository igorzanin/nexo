from abc import ABC, abstractmethod
from typing import Sequence


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> object | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> object | None: ...

    @abstractmethod
    def get_by_username(self, username: str) -> object | None: ...

    @abstractmethod
    def create(self, user: object) -> object: ...

    @abstractmethod
    def update(self, user: object) -> object: ...

    @abstractmethod
    def soft_delete(self, user_id: str, deleted_at_ms: int) -> None: ...


class ISessionRepository(ABC):
    @abstractmethod
    def get_by_token(self, token: str) -> object | None: ...

    @abstractmethod
    def create(self, session: object) -> object: ...

    @abstractmethod
    def delete(self, session_id: str) -> None: ...

    @abstractmethod
    def delete_expired(self, now_ms: int) -> int: ...


class IPreferenceRepository(ABC):
    @abstractmethod
    def get(self, user_id: str, category: str, name: str) -> object | None: ...

    @abstractmethod
    def upsert(self, preference: object) -> object: ...

    @abstractmethod
    def list_by_user(self, user_id: str) -> Sequence[object]: ...
