from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from nexo.models.enums import CategoryType


class CategoryCreate(BaseModel):
    name: str
    userID: str
    teamID: str
    type: CategoryType = CategoryType.CUSTOM
    collapsed: bool = False
    sortOrder: int = 0


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    collapsed: Optional[bool] = None
    sortOrder: Optional[int] = None


class CategoryResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: str
    name: str
    user_id: str = Field(serialization_alias="userID")
    team_id: str = Field(serialization_alias="teamID")
    type: str
    sort_order: int = Field(0, serialization_alias="sortOrder")
    collapsed: bool = False
    create_at: int = Field(serialization_alias="createAt")
    update_at: int = Field(serialization_alias="updateAt")
    delete_at: int = Field(serialization_alias="deleteAt")
