"""Unit tests for auth domain rules (BR-MIGRAR-006)."""
import pytest

from nexo.domain.exceptions import InvalidEmailError, PasswordTooShortError
from nexo.domain.rules.auth import validate_email_format, validate_password_length


class TestValidatePasswordLength:
    def test_8_chars_ok(self):
        validate_password_length("12345678")

    def test_long_password_ok(self):
        validate_password_length("a" * 100)

    def test_7_chars_raises(self):
        with pytest.raises(PasswordTooShortError):
            validate_password_length("1234567")

    def test_empty_raises(self):
        with pytest.raises(PasswordTooShortError):
            validate_password_length("")


class TestValidateEmailFormat:
    def test_valid_email(self):
        result = validate_email_format("Admin@Nexo.Local")
        assert result == "admin@nexo.local"

    def test_strips_whitespace(self):
        result = validate_email_format("  user@example.com  ")
        assert result == "user@example.com"

    @pytest.mark.parametrize("bad", ["notanemail", "@nodomain", "no-at-sign", ""])
    def test_invalid_raises(self, bad):
        with pytest.raises(InvalidEmailError):
            validate_email_format(bad)
