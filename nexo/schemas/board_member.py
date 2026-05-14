from pydantic import BaseModel, ConfigDict

from nexo.models.enums import MemberRole


class BoardMemberCreate(BaseModel):
    boardId: str
    userId: str
    minimumRole: MemberRole = MemberRole.NONE
    schemeAdmin: bool = False
    schemeEditor: bool = False
    schemeCommenter: bool = False
    schemeViewer: bool = False


class BoardMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    boardId: str
    userId: str
    minimumRole: str
    schemeAdmin: bool
    schemeEditor: bool
    schemeCommenter: bool
    schemeViewer: bool
