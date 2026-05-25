from nexo.domain.interfaces.board_repo import IBoardRepository
from nexo.domain.interfaces.block_repo import IBlockRepository
from nexo.domain.interfaces.user_repo import (
    IPreferenceRepository,
    ISessionRepository,
    IUserRepository,
)
from nexo.domain.interfaces.category_repo import (
    ICategoryBoardRepository,
    ICategoryRepository,
)
from nexo.domain.interfaces.sharing_repo import ISharingRepository
from nexo.domain.interfaces.subscription_repo import (
    INotificationHintRepository,
    ISubscriptionRepository,
)

__all__ = [
    "IBoardRepository",
    "IBlockRepository",
    "IUserRepository",
    "ISessionRepository",
    "IPreferenceRepository",
    "ICategoryRepository",
    "ICategoryBoardRepository",
    "ISharingRepository",
    "ISubscriptionRepository",
    "INotificationHintRepository",
]
