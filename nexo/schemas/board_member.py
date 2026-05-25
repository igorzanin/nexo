from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

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
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    board_id: str
    user_id: str
    roles: str = ""
    scheme_admin: bool = False
    scheme_editor: bool = False
    scheme_commenter: bool = False
    scheme_viewer: bool = False
    create_at: int = 0
    update_at: int = 0
    delete_at: int = 0
