from nexo.domain.enums import (
    BoardType,
    BlockType,
    CategoryType,
    MinimumRole,
    Permission,
    SubscriberType,
)
from nexo.domain.exceptions import (
    BoardNotFoundError,
    BlockNotFoundError,
    BlockBatchBoardMismatchError,
    BlockFieldsTooLargeError,
    BlockTitleTooLongError,
    CardIconTooLongError,
    BoardTypeImmutableError,
    CategoryNotFoundError,
    DomainError,
    DuplicateBoardError,
    DuplicateEmailError,
    DuplicateUsernameError,
    InvalidBoardTypeError,
    InvalidCategoryTypeError,
    InvalidCredentialsError,
    InvalidEmailError,
    InvalidMinimumRoleError,
    InvalidReadTokenError,
    InvalidSubscriberTypeError,
    InvalidTokenError,
    LastAdminError,
    PasswordTooShortError,
    PermissionDeniedError,
    SharingDisabledError,
    SubscriptionMissingFieldError,
    TokenExpiredError,
)
from nexo.domain.rules import (
    assert_not_last_admin,
    validate_batch_board_ids,
    validate_block_fields,
    validate_block_title,
    validate_board_type,
    validate_card_icon,
    validate_category_type,
    validate_email_format,
    validate_minimum_role,
    validate_password_length,
    validate_subscriber_type,
    validate_subscription_fields,
)
from nexo.domain.services.permission import PermissionService
from nexo.domain.interfaces import (
    IBoardRepository,
    IBlockRepository,
    ICategoryBoardRepository,
    ICategoryRepository,
    INotificationHintRepository,
    IPreferenceRepository,
    ISessionRepository,
    ISharingRepository,
    ISubscriptionRepository,
    IUserRepository,
)

__all__ = [
    # enums
    "BoardType", "BlockType", "CategoryType", "MinimumRole", "Permission", "SubscriberType",
    # exceptions
    "DomainError", "BoardNotFoundError", "BlockNotFoundError",
    "BlockBatchBoardMismatchError", "BlockFieldsTooLargeError", "BlockTitleTooLongError",
    "CardIconTooLongError", "BoardTypeImmutableError", "CategoryNotFoundError",
    "DuplicateBoardError", "DuplicateEmailError", "DuplicateUsernameError",
    "InvalidBoardTypeError", "InvalidCategoryTypeError", "InvalidCredentialsError",
    "InvalidEmailError", "InvalidMinimumRoleError", "InvalidReadTokenError",
    "InvalidSubscriberTypeError", "InvalidTokenError", "LastAdminError",
    "PasswordTooShortError", "PermissionDeniedError", "SharingDisabledError",
    "SubscriptionMissingFieldError", "TokenExpiredError",
    # rules
    "assert_not_last_admin", "validate_batch_board_ids", "validate_block_fields",
    "validate_block_title", "validate_board_type", "validate_card_icon",
    "validate_category_type", "validate_email_format", "validate_minimum_role",
    "validate_password_length", "validate_subscriber_type", "validate_subscription_fields",
    # services
    "PermissionService",
    # interfaces
    "IBoardRepository", "IBlockRepository", "ICategoryBoardRepository", "ICategoryRepository",
    "INotificationHintRepository", "IPreferenceRepository", "ISessionRepository",
    "ISharingRepository", "ISubscriptionRepository", "IUserRepository",
]
