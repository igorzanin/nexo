import warnings
from typing import Optional, Any

from pydantic import BaseModel, ConfigDict, field_validator

from nexo.models.enums import BlockType

warnings.filterwarnings("ignore", message="Field name \"schema\"", category=UserWarning)

MAX_TITLE_RUNES = 16383
MAX_FIELDS_RUNES = 800000


class BlockCreate(BaseModel):
    board_id: str
    parent_id: str = ""
    type: BlockType
    title: str = ""
    fields: dict[str, Any] = {}
    schema: int = 1

    @field_validator("title")
    @classmethod
    def title_length(cls, v: str) -> str:
        if len(v) > MAX_TITLE_RUNES:
            raise ValueError(f"title exceeds {MAX_TITLE_RUNES} runes")
        return v

    @field_validator("fields")
    @classmethod
    def fields_size(cls, v: dict) -> dict:
        text = str(v)
        if len(text) > MAX_FIELDS_RUNES:
            raise ValueError(f"fields exceeds {MAX_FIELDS_RUNES} runes")
        return v


class BlockUpdate(BaseModel):
    parent_id: Optional[str] = None
    title: Optional[str] = None
    fields: Optional[dict[str, Any]] = None
    schema: Optional[int] = None

    @field_validator("title")
    @classmethod
    def title_length(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > MAX_TITLE_RUNES:
            raise ValueError(f"title exceeds {MAX_TITLE_RUNES} runes")
        return v

    @field_validator("fields")
    @classmethod
    def fields_size(cls, v: Optional[dict]) -> Optional[dict]:
        if v is not None:
            text = str(v)
            if len(text) > MAX_FIELDS_RUNES:
                raise ValueError(f"fields exceeds {MAX_FIELDS_RUNES} runes")
        return v


class BlockResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    boardId: str
    parentId: str
    createdBy: str
    modifiedBy: str
    type: str
    title: str
    fields: dict
    schema: int
    createAt: int
    updateAt: int
    deleteAt: int

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, v):
        if isinstance(v, BlockType):
            return v.value
        return v
