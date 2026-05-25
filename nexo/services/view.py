"""ViewService — orchestrates BoardView CRUD and card filtering (BR-MIGRAR-010, BR-MIGRAR-011)."""
from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from nexo.models import Block
from nexo.models.enums import FilterCondition
from nexo.repositories.view import ViewRepository
from nexo.schemas.view import BoardViewCreate, BoardViewUpdate, FilterClause, FilterGroup, SortOption


class ViewService:
    def __init__(self, db: DBSession):
        self.db = db
        self.view_repo = ViewRepository(db)

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def create(self, data: BoardViewCreate, user_id: str) -> Block:
        return self.view_repo.create(data, user_id)

    def list_views(self, board_id: str) -> list[Block]:
        return self.view_repo.list_for_board(board_id)

    def get(self, view_id: str) -> Block | None:
        return self.view_repo.get(view_id)

    def update(self, view_id: str, data: BoardViewUpdate, user_id: str) -> Block | None:
        return self.view_repo.update(view_id, data, user_id)

    def delete(self, view_id: str) -> bool:
        return self.view_repo.soft_delete(view_id)

    # ------------------------------------------------------------------
    # Filtered card query — BR-MIGRAR-010 / BR-MIGRAR-011
    # ------------------------------------------------------------------

    def get_filtered_cards(self, board_id: str, view_id: str) -> list[Block]:
        """Return active cards for the board filtered and sorted by the view's settings."""
        view = self.view_repo.get(view_id)
        if not view:
            return []

        stmt = select(Block).where(
            Block.board_id == board_id,
            Block.type == "card",
            Block.delete_at == 0,
        )
        cards: list[Block] = list(self.db.execute(stmt).scalars().all())

        fields: dict = view.fields or {}

        # Apply filter tree
        filter_group = fields.get("filter") or fields.get("filterGroup")
        if filter_group:
            fg = _parse_filter_group(filter_group)
            if fg:
                cards = [c for c in cards if _apply_filter_group(fg, c)]

        # Apply sort options
        sort_options_raw: list[dict] = fields.get("sort_options") or fields.get("sortOptions", [])
        if sort_options_raw:
            sort_opts = [SortOption(**s) if isinstance(s, dict) else s for s in sort_options_raw]
            cards = _sort_cards(cards, sort_opts)

        # Apply card order (position in view)
        card_order: list[str] = fields.get("card_order") or fields.get("cardOrder", [])
        if card_order:
            order_index = {cid: i for i, cid in enumerate(card_order)}
            cards.sort(key=lambda c: order_index.get(c.id, len(card_order)))

        return cards


# ---------------------------------------------------------------------------
# Filter helpers
# ---------------------------------------------------------------------------

def _parse_filter_group(raw: dict) -> FilterGroup | None:
    try:
        return FilterGroup(**raw)
    except Exception:
        return None


def _apply_filter_group(fg: FilterGroup, card: Block) -> bool:
    results = []
    for f in fg.filters:
        if isinstance(f, FilterGroup):
            results.append(_apply_filter_group(f, card))
        elif isinstance(f, FilterClause):
            results.append(_apply_clause(f, card))
        elif isinstance(f, dict):
            if "operation" in f:
                sub = _parse_filter_group(f)
                if sub:
                    results.append(_apply_filter_group(sub, card))
            else:
                try:
                    results.append(_apply_clause(FilterClause(**f), card))
                except Exception:
                    pass

    if not results:
        return True
    if fg.operation == "and":
        return all(results)
    return any(results)


def _get_card_prop_values(card: Block, property_id: str) -> list[str]:
    """Extract property values from card fields JSON."""
    fields: dict = card.fields or {}
    props: dict = fields.get("properties") or fields.get("property_values") or {}
    val = props.get(property_id)
    if val is None:
        return []
    if isinstance(val, list):
        return [str(v) for v in val]
    return [str(val)]


def _apply_clause(clause: FilterClause, card: Block) -> bool:
    cond = clause.condition
    values = clause.values
    prop_vals = _get_card_prop_values(card, clause.property_id)

    if cond == FilterCondition.IS_EMPTY or cond == FilterCondition.IS_NOT_SET:
        return len(prop_vals) == 0 or all(v == "" for v in prop_vals)
    if cond == FilterCondition.IS_NOT_EMPTY or cond == FilterCondition.IS_SET:
        return bool(prop_vals) and any(v != "" for v in prop_vals)
    if cond == FilterCondition.INCLUDES:
        return any(v in values for v in prop_vals)
    if cond == FilterCondition.NOT_INCLUDES:
        return not any(v in values for v in prop_vals)
    if cond == FilterCondition.IS:
        return prop_vals == values or (len(prop_vals) == 1 and len(values) == 1 and prop_vals[0] == values[0])
    if cond == FilterCondition.CONTAINS:
        return any(values[0].lower() in v.lower() for v in prop_vals) if values else False
    if cond == FilterCondition.NOT_CONTAINS:
        return not any(values[0].lower() in v.lower() for v in prop_vals) if values else True
    if cond == FilterCondition.STARTS_WITH:
        return any(v.lower().startswith(values[0].lower()) for v in prop_vals) if values else False
    if cond == FilterCondition.NOT_STARTS_WITH:
        return not any(v.lower().startswith(values[0].lower()) for v in prop_vals) if values else True
    if cond == FilterCondition.ENDS_WITH:
        return any(v.lower().endswith(values[0].lower()) for v in prop_vals) if values else False
    if cond == FilterCondition.NOT_ENDS_WITH:
        return not any(v.lower().endswith(values[0].lower()) for v in prop_vals) if values else True
    if cond == FilterCondition.IS_BEFORE:
        try:
            return bool(prop_vals) and int(prop_vals[0]) < int(values[0])
        except (ValueError, IndexError):
            return False
    if cond == FilterCondition.IS_AFTER:
        try:
            return bool(prop_vals) and int(prop_vals[0]) > int(values[0])
        except (ValueError, IndexError):
            return False
    return True


def _sort_cards(cards: list[Block], sort_opts: list[SortOption]) -> list[Block]:
    for opt in reversed(sort_opts):
        reverse = opt.reversed
        pid = opt.property_id
        cards.sort(
            key=lambda c: _sort_key(c, pid),
            reverse=reverse,
        )
    return cards


def _sort_key(card: Block, property_id: str) -> Any:
    vals = _get_card_prop_values(card, property_id)
    if not vals:
        return ""
    v = vals[0]
    try:
        return int(v)
    except (ValueError, TypeError):
        return v.lower()
