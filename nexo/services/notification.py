from sqlalchemy.orm import Session as DBSession

from nexo.repositories.subscription import SubscriptionRepository


class NotificationService:
    def __init__(self, db: DBSession):
        self.db = db
        self.subscription_repo = SubscriptionRepository(db)

    def notify_block_change(self, block_id: str, board_id: str) -> list[str]:
        subscriptions = self.subscription_repo.get_by_block(block_id)
        subscriber_ids = [s.subscriber_id for s in subscriptions if s.subscriber_type == "user"]
        return subscriber_ids

    def notify_board_change(self, board_id: str) -> list[str]:
        from sqlalchemy import select

        from nexo.models import BoardMember

        stmt = select(BoardMember).where(BoardMember.board_id == board_id)
        members = list(self.db.execute(stmt).scalars().all())
        return [m.user_id for m in members]
