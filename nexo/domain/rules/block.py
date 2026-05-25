"""Block invariant validators (BR-MIGRAR-002, BR-MIGRAR-007)."""
from __future__ import annotations

import unicodedata

from nexo.domain.exceptions import (
    BlockBatchBoardMismatchError,
    BlockFieldsTooLargeError,
    BlockTitleTooLongError,
    CardIconTooLongError,
)

TITLE_MAX_RUNES = 16_383
FIELDS_MAX_RUNES = 800_000


def _grapheme_count(text: str) -> int:
    """Return the number of user-perceived characters (grapheme clusters).

    Uses NFC normalisation + category check as a lightweight approximation
    sufficient for the 1-grapheme icon constraint.
    """
    normalized = unicodedata.normalize("NFC", text)
    # Count base characters (non-combining)
    return sum(
        1
        for ch in normalized
        if unicodedata.category(ch) not in ("Mn", "Mc", "Me", "Cf")
    )


def validate_block_title(title: str) -> None:
    """Raise BlockTitleTooLongError if title exceeds 16 383 runes."""
    if len(title) > TITLE_MAX_RUNES:
        raise BlockTitleTooLongError(
            f"Block title must be ≤ {TITLE_MAX_RUNES} characters, got {len(title)}."
        )


def validate_block_fields(fields_json: str) -> None:
    """Raise BlockFieldsTooLargeError if fields JSON exceeds 800 000 runes."""
    if len(fields_json) > FIELDS_MAX_RUNES:
        raise BlockFieldsTooLargeError(
            f"Block fields JSON must be ≤ {FIELDS_MAX_RUNES} characters, got {len(fields_json)}."
        )


def validate_card_icon(icon: str) -> None:
    """Raise CardIconTooLongError if icon is more than 1 grapheme."""
    if icon and _grapheme_count(icon) > 1:
        raise CardIconTooLongError(
            f"Card icon must be at most 1 grapheme, got: {icon!r}"
        )


def validate_batch_board_ids(board_ids: list[str]) -> None:
    """Raise BlockBatchBoardMismatchError if blocks span more than one board."""
    unique = set(board_ids)
    if len(unique) > 1:
        raise BlockBatchBoardMismatchError(
            f"Batch insert requires all blocks to belong to the same board; "
            f"found board IDs: {unique}"
        )
