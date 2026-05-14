from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from nexo.models import Subscription


class SubscriptionRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def get(self, block_id: str, subscriber_id: str) -> Subscription | None:
        return self.db.get(Subscription, (block_id, subscriber_id))

    def get_by_subscriber(self, subscriber_id: str) -> list[Subscription]:
        stmt = select(Subscription).where(Subscription.subscriberId == subscriber_id)
        return list(self.db.execute(stmt).scalars().all())

    def get_by_block(self, block_id: str) -> list[Subscription]:
        stmt = select(Subscription).where(Subscription.blockId == block_id)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, block_id: str, subscriber_id: str, subscriber_type: str = "user") -> Subscription:
        import time

        now = int(time.time() * 1000)
        sub = Subscription(
            blockId=block_id,
            subscriberId=subscriber_id,
            subscriberType=subscriber_type,
            createAt=now,
            notifyAt=now,
            updateAt=now,
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
