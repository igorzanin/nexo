from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from nexo.auth.dependencies import get_current_user
from nexo.db.session import get_db
from nexo.models import User
from nexo.schemas.board import BoardCreate, BoardUpdate, BoardResponse
from nexo.services.board import BoardService

router = APIRouter(prefix="/api/v1", tags=["boards"])


@router.post("/boards", response_model=BoardResponse)
async def create_board(
    data: BoardCreate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = BoardService(db)
    board = svc.create(data, user.id)
    return BoardResponse.model_validate(board, from_attributes=True)


@router.get("/teams/{team_id}/boards", response_model=list[BoardResponse])
async def get_boards(
    team_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = BoardService(db)
    boards = svc.get_by_team(team_id)
    return [BoardResponse.model_validate(b, from_attributes=True) for b in boards]


@router.get("/boards/{board_id}", response_model=BoardResponse)
async def get_board(
    board_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = BoardService(db)
    board = svc.get(board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return BoardResponse.model_validate(board, from_attributes=True)


@router.patch("/boards/{board_id}", response_model=BoardResponse)
async def patch_board(
    board_id: str,
    data: BoardUpdate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = BoardService(db)
    board = svc.update(board_id, data, user.id)
    return BoardResponse.model_validate(board, from_attributes=True)


@router.delete("/boards/{board_id}", status_code=204)
async def delete_board(
    board_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = BoardService(db)
    svc.delete(board_id, user.id)


@router.post("/boards/{board_id}/duplicate", response_model=BoardResponse)
async def duplicate_board(
    board_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = BoardService(db)
    board = svc.duplicate(board_id, user.id)
    return BoardResponse.model_validate(board, from_attributes=True)


@router.post("/boards/{board_id}/undelete", response_model=BoardResponse)
async def undelete_board(
    board_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    from nexo.repositories.board import BoardRepository
    repo = BoardRepository(db)
    ok = repo.undelete(board_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Board not found or not deleted")
    board = repo.get(board_id)
    return BoardResponse.model_validate(board, from_attributes=True)
