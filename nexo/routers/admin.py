from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession

from nexo.auth.dependencies import get_current_user
from nexo.db.session import get_db
from nexo.models import User
from nexo.config import get_settings

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])
settings = get_settings()


@router.get("/config")
async def get_admin_config(
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    return {
        "enablePublicSharedBoards": settings.enable_public_shared_boards,
        "maxFileSize": settings.max_file_size,
        "sessionExpireTime": settings.access_token_expire_days,
    }
