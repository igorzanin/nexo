from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from nexo.models.enums import SubscriberType


class SubscriptionCreate(BaseModel):
    block_id: str
    subscriber_id: str
    subscriber_type: SubscriberType = SubscriberType.USER

    # Accept camelCase from frontend too
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    block_type: str = "block"
    block_id: str
    subscriber_type: str
    subscriber_id: str
    notify_frequency: Optional[str] = None
    create_at: int = 0
    publish_at: int = 0
