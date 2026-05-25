from abc import ABC, abstractmethod
from typing import Sequence


class ISubscriptionRepository(ABC):
    @abstractmethod
    def get(
        self,
        block_type: str,
        block_id: str,
        subscriber_type: str,
        subscriber_id: str,
    ) -> object | None: ...

    @abstractmethod
    def create(self, subscription: object) -> object: ...

    @abstractmethod
    def delete(
        self,
        block_type: str,
        block_id: str,
        subscriber_type: str,
        subscriber_id: str,
    ) -> None: ...

    @abstractmethod
    def list_by_block(self, block_type: str, block_id: str) -> Sequence[object]: ...


class INotificationHintRepository(ABC):
    @abstractmethod
    def upsert(self, hint: object) -> object: ...

    @abstractmethod
    def list_pending(self, subscriber_id: str) -> Sequence[object]: ...
