from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel

from nexo.models.enums import BoardType, MemberRole


class BoardCreate(BaseModel):
    team_id: str
    type: BoardType = BoardType.PRIVATE
    title: str = ""
    description: str = ""
    icon: str = ""
    show_description: bool = False
    is_template: bool = False
    template_version: int = 0
    minimum_role: MemberRole = MemberRole.NONE
    channel_id: str = ""


class BoardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    show_description: Optional[bool] = None
    is_template: Optional[bool] = None
    template_version: Optional[int] = None
    minimum_role: Optional[MemberRole] = None
    channel_id: Optional[str] = None
    card_properties: Optional[Any] = None


class BoardResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: str
    team_id: str
    channel_id: str = ""
    type: str
    title: str = ""
    description: str = ""
    icon: str = ""
    show_description: bool = False
    is_template: bool = False
    template_version: int = 0
    minimum_role: str = ""
    create_at: int = 0
    update_at: int = 0
    delete_at: int = 0

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, v):
        if isinstance(v, BoardType):
            return v.value
        return v

    @field_validator("minimum_role", mode="before")
    @classmethod
    def validate_minimum_role(cls, v):
        if isinstance(v, MemberRole):
            return v.value
        return v
