from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

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


class BoardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    teamId: str
    channelId: str
    type: str
    title: str
    description: str
    icon: str
    showDescription: bool
    isTemplate: bool
    templateVersion: int
    minimumRole: str
    createAt: int
    updateAt: int
    deleteAt: int

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, v):
        if isinstance(v, BoardType):
            return v.value
        return v

    @field_validator("minimumRole", mode="before")
    @classmethod
    def validate_minimum_role(cls, v):
        if isinstance(v, MemberRole):
            return v.value
        return v
