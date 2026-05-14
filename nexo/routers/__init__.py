from nexo.routers.auth import router as auth_router
from nexo.routers.ws import router as ws_router
from nexo.routers.boards import router as boards_router
from nexo.routers.blocks import router as blocks_router
from nexo.routers.cards import router as cards_router
from nexo.routers.categories import router as categories_router
from nexo.routers.members import router as members_router
from nexo.routers.files import router as files_router
from nexo.routers.teams import router as teams_router
from nexo.routers.admin import router as admin_router
from nexo.routers.subscriptions import router as subscriptions_router
from nexo.routers.sharing import router as sharing_router

__all__ = [
    "auth_router", "ws_router", "boards_router", "blocks_router",
    "cards_router", "categories_router", "members_router",
    "files_router", "teams_router", "admin_router",
    "subscriptions_router", "sharing_router",
]
