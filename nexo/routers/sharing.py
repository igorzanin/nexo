from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from nexo.auth.dependencies import get_current_user
from nexo.db.session import get_db
from nexo.models import User
from nexo.repositories.sharing import SharingRepository
from nexo.repositories.board import BoardRepository
from nexo.schemas.sharing import SharingCreate, SharingResponse
from nexo.schemas.board import BoardResponse

router = APIRouter(tags=["sharing"])


@router.get("/api/v1/boards/{board_id}/sharing", response_model=SharingResponse)
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


@router.post("/api/v1/boards/{board_id}/sharing", response_model=SharingResponse)
async def post_sharing(
    board_id: str,
    data: SharingCreate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    repo = SharingRepository(db)
    sharing = repo.upsert(board_id, data, modified_by=user.id)
    return SharingResponse.model_validate(sharing, from_attributes=True)


@router.delete("/api/v1/boards/{board_id}/sharing", status_code=204)
async def delete_sharing(
    board_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    repo = SharingRepository(db)
    repo.delete(board_id)


@router.get("/api/v1/shared/boards/{read_token}", response_model=BoardResponse)
async def get_shared_board(
    read_token: str,
    db: DBSession = Depends(get_db),
):
    """Public board access via readToken — no authentication required (BR-MIGRAR-013)."""
    sharing_repo = SharingRepository(db)
    sharing = sharing_repo.get_by_token(read_token)
    if not sharing or not sharing.enabled:
        raise HTTPException(status_code=404, detail="Shared board not found or sharing disabled")
    board_repo = BoardRepository(db)
    board = board_repo.get(sharing.id)
    if not board or board.delete_at != 0:
        raise HTTPException(status_code=404, detail="Board not found")
    return BoardResponse.model_validate(board, from_attributes=True)
