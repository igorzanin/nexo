"""Domain exception hierarchy for nexo.

All domain violations raise a subclass of DomainError so callers can
catch the hierarchy or handle specific errors as needed.
"""


class DomainError(Exception):
    """Base class for all domain-layer errors."""


# ── Board ──────────────────────────────────────────────────────────────────────

class BoardNotFoundError(DomainError):
    """Board with given ID does not exist."""


class InvalidBoardTypeError(DomainError):
    """Board type must be 'O' (Open) or 'P' (Private)."""


class BoardTypeImmutableError(DomainError):
    """Board type cannot be changed without PermissionManageBoardType."""


class InvalidMinimumRoleError(DomainError):
    """minimumRole must be one of: '', viewer, commenter, editor, admin."""


class LastAdminError(DomainError):
    """Cannot remove or demote the last admin of a board."""


class DuplicateBoardError(DomainError):
    """Board duplication failed; transactional rollback required."""


# ── Block ──────────────────────────────────────────────────────────────────────

class BlockTitleTooLongError(DomainError):
    """Block title exceeds 16 383 runes."""


class BlockFieldsTooLargeError(DomainError):
    """Block fields JSON exceeds 800 000 runes."""


class CardIconTooLongError(DomainError):
    """Card icon must be at most 1 grapheme."""


class BlockBatchBoardMismatchError(DomainError):
    """All blocks in a batch must belong to the same board."""


class BlockNotFoundError(DomainError):
    """Block with given ID does not exist (non-fatal for delete operations)."""


# ── Auth / User ────────────────────────────────────────────────────────────────

class PasswordTooShortError(DomainError):
    """Password must have at least 8 characters."""


class DuplicateUsernameError(DomainError):
    """Username is already taken."""


class DuplicateEmailError(DomainError):
    """Email address is already registered."""


class UserNotFoundError(DomainError):
    """User with given ID does not exist."""


class InvalidEmailError(DomainError):
    """Email address format is invalid."""


class TokenExpiredError(DomainError):
    """JWT or refresh token has expired."""


class InvalidTokenError(DomainError):
    """Token is malformed or its signature is invalid."""


class InvalidCredentialsError(DomainError):
    """Username/password combination is incorrect."""


# ── Category ───────────────────────────────────────────────────────────────────

class InvalidCategoryTypeError(DomainError):
    """Category type must be 'system' or 'custom'."""


class CategoryNotFoundError(DomainError):
    """Category with given ID does not exist."""


# ── Sharing ────────────────────────────────────────────────────────────────────

class SharingDisabledError(DomainError):
    """Public sharing is disabled on this server (enablePublicSharedBoards=false)."""


class InvalidReadTokenError(DomainError):
    """Read token is invalid or does not match the board."""


# ── Subscription ───────────────────────────────────────────────────────────────

class InvalidSubscriberTypeError(DomainError):
    """subscriberType must be 'user'."""


class SubscriptionMissingFieldError(DomainError):
    """blockId, blockType, subscriberId, and subscriberType are all required."""


# ── Permission ─────────────────────────────────────────────────────────────────

class PermissionDeniedError(DomainError):
    """Caller does not have the required permission for this action."""
