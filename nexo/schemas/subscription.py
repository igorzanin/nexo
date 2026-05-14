from pydantic import BaseModel, ConfigDict

from nexo.models.enums import SubscriberType


class SubscriptionCreate(BaseModel):
    blockId: str
    subscriberId: str
    subscriberType: SubscriberType = SubscriberType.USER


class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    blockId: str
    subscriberId: str
    subscriberType: str
    createAt: int
    notifyAt: int
    updateAt: int
