"""Schemas for BoardView (block type='view') — BC-Views."""
from __future__ import annotations

from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel

from nexo.models.enums import FilterCondition, IViewType


# ---------------------------------------------------------------------------
# Filter tree — BR-MIGRAR-011
# ---------------------------------------------------------------------------

class FilterClause(BaseModel):
    filter_id: str = ""
    property_id: str
    condition: FilterCondition
    values: list[str] = []


class FilterGroup(BaseModel):
    operation: Literal["and", "or"] = "and"
    filters: list[Union["FilterGroup", FilterClause]] = []


FilterGroup.model_rebuild()


# ---------------------------------------------------------------------------
# Sort option
# ---------------------------------------------------------------------------

class SortOption(BaseModel):
    property_id: str
    reversed: bool = False


# ---------------------------------------------------------------------------
# View fields payload stored in blocks.fields JSON
# ---------------------------------------------------------------------------

class ViewFields(BaseModel):
    view_type: IViewType = IViewType.BOARD
    filter: FilterGroup = Field(default_factory=FilterGroup)
    sort_options: list[SortOption] = []
    card_order: list[str] = []
    group_by_id: str = ""
    collapsed_option_ids: dict[str, bool] = {}
    hidden_option_ids: dict[str, bool] = {}
    column_calculations: dict[str, str] = {}

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


# ---------------------------------------------------------------------------
# API request / response schemas
# ---------------------------------------------------------------------------

class BoardViewCreate(BaseModel):
    board_id: str
    title: str = ""
    view_type: IViewType = IViewType.BOARD

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        return v


class BoardViewUpdate(BaseModel):
    title: Optional[str] = None
    fields: Optional[dict[str, Any]] = None


class BoardViewResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: str
    board_id: str
    type: str = "view"
    title: str = ""
    fields: dict = {}
    create_at: int = 0
    update_at: int = 0
    delete_at: int = 0
    created_by: Optional[str] = None
    modified_by: Optional[str] = None
