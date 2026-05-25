"""Subscription invariant validators (BR-MIGRAR-005)."""
from __future__ import annotations

from nexo.domain.enums import SubscriberType
from nexo.domain.exceptions import (
    InvalidSubscriberTypeError,
    SubscriptionMissingFieldError,
)


def validate_subscription_fields(
    block_id: str,
    block_type: str,
    subscriber_id: str,
    subscriber_type: str,
) -> None:
    """Raise SubscriptionMissingFieldError if any required field is empty."""
    missing = [
        name
        for name, value in [
            ("block_id", block_id),
            ("block_type", block_type),
            ("subscriber_id", subscriber_id),
            ("subscriber_type", subscriber_type),
        ]
        if not value
    ]
    if missing:
        raise SubscriptionMissingFieldError(
            f"Required subscription fields missing: {missing}"
        )


def validate_subscriber_type(value: str) -> SubscriberType:
    """Raise InvalidSubscriberTypeError if value is not 'user'."""
    if value != SubscriberType.USER.value:
        raise InvalidSubscriberTypeError(
            f"subscriberType must be 'user', got: {value!r}"
        )
    return SubscriberType.USER
