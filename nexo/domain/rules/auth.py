"""Authentication and user invariant validators (BR-MIGRAR-006)."""
from __future__ import annotations

import re

from nexo.domain.exceptions import InvalidEmailError, PasswordTooShortError

PASSWORD_MIN_LENGTH = 8
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_password_length(password: str) -> None:
    """Raise PasswordTooShortError if password has fewer than 8 characters."""
    if len(password) < PASSWORD_MIN_LENGTH:
        raise PasswordTooShortError(
            f"Password must have at least {PASSWORD_MIN_LENGTH} characters."
        )


def validate_email_format(email: str) -> str:
    """Normalize and validate email format. Raise InvalidEmailError if invalid.

    Returns the lower-cased, stripped email.
    """
    normalized = email.strip().lower()
    if not _EMAIL_RE.match(normalized):
        raise InvalidEmailError(f"Invalid email address: {email!r}")
    return normalized
