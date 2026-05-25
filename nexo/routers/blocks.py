from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from nexo.auth.dependencies import get_current_user
from nexo.db.session import get_db
from nexo.models import User, Block
from nexo.schemas.block import BlockCreate, BlockUpdate, BlockResponse
from nexo.services.block import BlockService

router = APIRouter(prefix="/api/v1/boards/{board_id}", tags=["blocks"])


@router.get("/blocks", response_model=list[BlockResponse])
async def get_blocks(
    board_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = BlockService(db)
    blocks = svc.get_blocks_for_board(board_id)
    return [BlockResponse.model_validate(b, from_attributes=True) for b in blocks]


@router.post("/blocks", response_model=BlockResponse)
async def create_block(
    board_id: str,
    data: BlockCreate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = BlockService(db)
    block = svc.create(data, user.id)
    return BlockResponse.model_validate(block, from_attributes=True)


@router.post("/blocks/batch", response_model=list[BlockResponse])
async def batch_create_blocks(
    board_id: str,
    items: list[BlockCreate],
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = BlockService(db)
    try:
        blocks = svc.batch_create(items, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return [BlockResponse.model_validate(b, from_attributes=True) for b in blocks]


@router.patch("/blocks/{block_id}", response_model=BlockResponse)
async def patch_block(
    board_id: str,
    block_id: str,
    data: BlockUpdate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = BlockService(db)
    block = svc.update(block_id, data, user.id)
    return BlockResponse.model_validate(block, from_attributes=True)


@router.delete("/blocks/{block_id}", status_code=204)
async def delete_block(
    board_id: str,
    block_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = BlockService(db)
    svc.delete(block_id)


@router.post("/blocks/{block_id}/undelete", response_model=BlockResponse)
async def undelete_block(
    board_id: str,
    block_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = BlockService(db)
    ok = svc.undelete(block_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Block not found or not deleted")
    block = svc.block_repo.get(block_id)
    return BlockResponse.model_validate(block, from_attributes=True)
