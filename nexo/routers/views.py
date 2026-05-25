"""REST endpoints for BoardViews (BC-Views)."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from nexo.auth.dependencies import get_current_user
from nexo.db.session import get_db
from nexo.models import User
from nexo.schemas.block import BlockResponse
from nexo.schemas.view import BoardViewCreate, BoardViewResponse, BoardViewUpdate
from nexo.services.view import ViewService

router = APIRouter(prefix="/api/v1/boards/{board_id}", tags=["views"])


@router.get("/views", response_model=list[BoardViewResponse])
async def list_views(
    board_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = ViewService(db)
    views = svc.list_views(board_id)
    return [BoardViewResponse.model_validate(v, from_attributes=True) for v in views]


@router.post("/views", response_model=BoardViewResponse)
async def create_view(
    board_id: str,
    data: BoardViewCreate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = ViewService(db)
    view = svc.create(data, user.id)
    return BoardViewResponse.model_validate(view, from_attributes=True)


@router.patch("/views/{view_id}", response_model=BoardViewResponse)
async def update_view(
    board_id: str,
    view_id: str,
    data: BoardViewUpdate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = ViewService(db)
    view = svc.update(view_id, data, user.id)
    if not view:
        raise HTTPException(status_code=404, detail="View not found")
    return BoardViewResponse.model_validate(view, from_attributes=True)


@router.delete("/views/{view_id}", status_code=204)
async def delete_view(
    board_id: str,
    view_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = ViewService(db)
    svc.delete(view_id)


@router.get("/views/{view_id}/cards", response_model=list[BlockResponse])
async def get_filtered_cards(
    board_id: str,
    view_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = ViewService(db)
    cards = svc.get_filtered_cards(board_id, view_id)
    return [BlockResponse.model_validate(c, from_attributes=True) for c in cards]
