from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession

from nexo.auth.dependencies import get_current_user
from nexo.db.session import get_db
from nexo.models import User
from nexo.repositories.subscription import SubscriptionRepository
from nexo.schemas.subscription import SubscriptionCreate, SubscriptionResponse

router = APIRouter(prefix="/api/v1", tags=["subscriptions"])


@router.post("/subscriptions", response_model=SubscriptionResponse)
async def create_subscription(
    data: SubscriptionCreate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    repo = SubscriptionRepository(db)
    sub = repo.create(data.blockId, data.subscriberId, data.subscriberType)
    return SubscriptionResponse.model_validate(sub, from_attributes=True)


@router.get("/subscriptions/{subscriber_id}", response_model=list[SubscriptionResponse])
async def get_subscriptions(
    subscriber_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    repo = SubscriptionRepository(db)
    subs = repo.get_by_subscriber(subscriber_id)
    return [SubscriptionResponse.model_validate(s, from_attributes=True) for s in subs]


@router.delete("/subscriptions/{block_id}/{subscriber_id}", status_code=204)
async def delete_subscription(
    block_id: str,
    subscriber_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    repo = SubscriptionRepository(db)
    repo.delete(block_id, subscriber_id)
