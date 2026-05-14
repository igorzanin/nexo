from typing import Optional

from pydantic import BaseModel, ConfigDict

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
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    userID: str
    teamID: str
    type: str
    collapsed: bool
    sortOrder: int
    createAt: int
    updateAt: int
    deleteAt: int
