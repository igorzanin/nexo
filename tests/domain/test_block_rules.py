"""Unit tests for block domain rules (BR-MIGRAR-002)."""
import pytest

from nexo.domain.exceptions import (
    BlockBatchBoardMismatchError,
    BlockFieldsTooLargeError,
    BlockTitleTooLongError,
    CardIconTooLongError,
)
from nexo.domain.rules.block import (
    FIELDS_MAX_RUNES,
    TITLE_MAX_RUNES,
    validate_batch_board_ids,
    validate_block_fields,
    validate_block_title,
    validate_card_icon,
)


class TestValidateBlockTitle:
    def test_valid_title(self):
        validate_block_title("Hello World")

    def test_empty_title_ok(self):
        validate_block_title("")

    def test_max_length_ok(self):
        validate_block_title("a" * TITLE_MAX_RUNES)

    def test_over_limit_raises(self):
        with pytest.raises(BlockTitleTooLongError):
            validate_block_title("a" * (TITLE_MAX_RUNES + 1))


class TestValidateBlockFields:
    def test_valid_fields(self):
        validate_block_fields('{"viewType": "board"}')

    def test_max_length_ok(self):
        validate_block_fields("x" * FIELDS_MAX_RUNES)

    def test_over_limit_raises(self):
        with pytest.raises(BlockFieldsTooLargeError):
            validate_block_fields("x" * (FIELDS_MAX_RUNES + 1))


class TestValidateCardIcon:
    def test_empty_ok(self):
        validate_card_icon("")

    def test_single_ascii_char_ok(self):
        validate_card_icon("A")

    def test_single_emoji_ok(self):
        validate_card_icon("🎯")

    def test_two_chars_raises(self):
        with pytest.raises(CardIconTooLongError):
            validate_card_icon("AB")


class TestValidateBatchBoardIds:
    def test_single_board_ok(self):
        validate_batch_board_ids(["board-1", "board-1", "board-1"])

    def test_empty_list_ok(self):
        validate_batch_board_ids([])

    def test_multiple_boards_raises(self):
        with pytest.raises(BlockBatchBoardMismatchError):
            validate_batch_board_ids(["board-1", "board-2"])
