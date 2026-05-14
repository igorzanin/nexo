from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from nexo.auth.dependencies import get_current_user
from nexo.db.session import get_db
from nexo.models import User
from nexo.repositories.sharing import SharingRepository
from nexo.schemas.sharing import SharingCreate, SharingResponse

router = APIRouter(prefix="/api/v1/boards/{board_id}", tags=["sharing"])


@router.get("/sharing", response_model=SharingResponse)
async def get_sharing(
    board_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    repo = SharingRepository(db)
    sharing = repo.get(board_id)
    if not sharing:
        raise HTTPException(status_code=404, detail="Sharing not found")
    return SharingResponse.model_validate(sharing, from_attributes=True)


@router.post("/sharing", response_model=SharingResponse)
async def post_sharing(
    board_id: str,
    data: SharingCreate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    repo = SharingRepository(db)
    sharing = repo.upsert(board_id, data)
    return SharingResponse.model_validate(sharing, from_attributes=True)
