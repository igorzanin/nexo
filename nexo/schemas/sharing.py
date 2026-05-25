import secrets
import time

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel


class SharingCreate(BaseModel):
    enabled: bool = False
    token: str = ""

    @field_validator("token")
    @classmethod
    def auto_generate_token(cls, v: str) -> str:
        return v if v else secrets.token_urlsafe(32)


class SharingResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: str
    enabled: bool
    token: str
    modified_by: str | None = None
    update_at: int = 0
    create_at: int = 0
