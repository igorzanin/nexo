"""Category invariant validators (BR-MIGRAR-004)."""
from __future__ import annotations

from nexo.domain.enums import CategoryType
from nexo.domain.exceptions import InvalidCategoryTypeError


def validate_category_type(value: str) -> CategoryType:
    """Raise InvalidCategoryTypeError if value is not 'system' or 'custom'."""
    try:
        return CategoryType(value)
    except ValueError:
        raise InvalidCategoryTypeError(
            f"Category type must be 'system' or 'custom', got: {value!r}"
        )
