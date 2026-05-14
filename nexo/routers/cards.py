from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from nexo.auth.dependencies import get_current_user
from nexo.db.session import get_db
from nexo.models import User
from nexo.schemas.block import BlockCreate, BlockUpdate, BlockResponse
from nexo.services.card import CardService

router = APIRouter(prefix="/api/v1", tags=["cards"])


@router.get("/boards/{board_id}/cards", response_model=list[BlockResponse])
async def get_cards(
    board_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = CardService(db)
    cards = svc.get_by_board(board_id)
    return [BlockResponse.model_validate(c, from_attributes=True) for c in cards]


@router.post("/boards/{board_id}/cards", response_model=BlockResponse)
async def create_card(
    board_id: str,
    data: BlockCreate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = CardService(db)
    card = svc.create(data, user.id)
    return BlockResponse.model_validate(card, from_attributes=True)


@router.get("/cards/{card_id}", response_model=BlockResponse)
async def get_card(
    card_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = CardService(db)
    card = svc.get(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return BlockResponse.model_validate(card, from_attributes=True)


@router.patch("/cards/{card_id}/cards", response_model=BlockResponse)
async def patch_card(
    card_id: str,
    data: BlockUpdate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = CardService(db)
    card = svc.update(card_id, data, user.id)
    return BlockResponse.model_validate(card, from_attributes=True)


@router.delete("/cards/{card_id}", status_code=204)
async def delete_card(
    card_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = CardService(db)
    svc.delete(card_id)
