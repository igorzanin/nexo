import time

from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from nexo.models import Subscription


class SubscriptionRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def get(self, block_id: str, subscriber_id: str) -> Subscription | None:
        stmt = select(Subscription).where(
            Subscription.block_id == block_id,
            Subscription.subscriber_id == subscriber_id,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_subscriber(self, subscriber_id: str) -> list[Subscription]:
        stmt = select(Subscription).where(Subscription.subscriber_id == subscriber_id)
        return list(self.db.execute(stmt).scalars().all())

    def get_by_block(self, block_id: str) -> list[Subscription]:
        stmt = select(Subscription).where(Subscription.block_id == block_id)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, block_id: str, subscriber_id: str, subscriber_type: str = "user") -> Subscription:
        now = int(time.time() * 1000)
        subscriber_type_value = subscriber_type.value if hasattr(subscriber_type, "value") else subscriber_type
        sub = Subscription(
            block_type="block",
            block_id=block_id,
            subscriber_id=subscriber_id,
            subscriber_type=subscriber_type_value,
            create_at=now,
            publish_at=now,
        )
        self.db.add(sub)
        self.db.commit()
        self.db.refresh(sub)
        return sub

    def delete(self, block_id: str, subscriber_id: str) -> bool:
        sub = self.get(block_id, subscriber_id)
        if not sub:
            return False
        self.db.delete(sub)
        self.db.commit()
        return True
