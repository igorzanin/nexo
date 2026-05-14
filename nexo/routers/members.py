from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from nexo.auth.dependencies import get_current_user
from nexo.db.session import get_db
from nexo.models import User
from nexo.schemas.board_member import BoardMemberCreate, BoardMemberResponse
from nexo.services.member import MemberService

router = APIRouter(prefix="/api/v1/boards/{board_id}", tags=["members"])


@router.get("/members", response_model=list[BoardMemberResponse])
async def get_members(
    board_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = MemberService(db)
    members = svc.get_members(board_id)
    return [BoardMemberResponse.model_validate(m, from_attributes=True) for m in members]


@router.post("/members", response_model=BoardMemberResponse)
async def add_member(
    board_id: str,
    data: BoardMemberCreate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = MemberService(db)
    member = svc.add_member(board_id, data, user.id)
    return BoardMemberResponse.model_validate(member, from_attributes=True)


@router.put("/members/{target_user_id}", response_model=BoardMemberResponse)
async def update_member(
    board_id: str,
    target_user_id: str,
    data: BoardMemberCreate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = MemberService(db)
    member = svc.update_member(board_id, target_user_id, data, user.id)
    return BoardMemberResponse.model_validate(member, from_attributes=True)


@router.delete("/members/{target_user_id}", status_code=204)
async def delete_member(
    board_id: str,
    target_user_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = MemberService(db)
    svc.remove_member(board_id, target_user_id, user.id)
