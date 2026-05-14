import time

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session as DBSession
from slowapi import Limiter
from slowapi.util import get_remote_address

from nexo.auth.dependencies import get_current_user
from nexo.auth.jwt import create_access_token, create_refresh_token, decode_token
from nexo.auth.password import hash_password, verify_password
from nexo.auth.schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    ChangePasswordRequest,
    RefreshRequest,
)
from nexo.db.session import get_db
from nexo.models import User, Board
from nexo.config import get_settings

router = APIRouter(prefix="/api/v1", tags=["auth"])
limiter = Limiter(key_func=get_remote_address)
settings = get_settings()


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
async def login(request: Request, body: LoginRequest, db: DBSession = Depends(get_db)):
    user = db.query(User).filter(
        (User.username == body.username) | (User.email == body.username),
        User.deleteAt == 0,
    ).first()
    if not user or not verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(current_user: User = Depends(get_current_user)):
    pass


@router.post("/register", response_model=TokenResponse)
@limiter.limit("5/minute")
async def register(request: Request, body: RegisterRequest, db: DBSession = Depends(get_db)):
    existing = db.query(User).filter(
        (User.username == body.username) | (User.email == body.email),
        User.deleteAt == 0,
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")
    user = User(
        username=body.username,
        email=body.email,
        password=hash_password(body.password),
        createAt=int(time.time() * 1000),
        updateAt=int(time.time() * 1000),
        deleteAt=0,
    )
    db.add(user)
    db.flush()

    from nexo.models import Team, Category
    existing_teams = db.query(Team).count()
    if existing_teams == 0:
        now = int(time.time() * 1000)
        team = Team(title="My Workspace", signupToken="", modifiedBy=user.id, updateAt=now)
        db.add(team)
        db.flush()

        board = Board(teamId=team.id, channelId="", type="P", title="Welcome Board",
                      description="", icon="🎉", showDescription=False,
                      isTemplate=False, templateVersion=0, minimumRole="",
                      createAt=now, updateAt=now, deleteAt=0)
        db.add(board)
        db.flush()

        from nexo.models import Category
        cat = Category(name="Boards", userID=user.id, teamID=team.id,
                       type="system", collapsed=False, sortOrder=0,
                       createAt=now, updateAt=now, deleteAt=0)
        db.add(cat)
        db.flush()

        from nexo.models import BoardMember, CategoryBoard
        db.add(BoardMember(boardId=board.id, userId=user.id, minimumRole="",
                           schemeAdmin=True, schemeEditor=False,
                           schemeCommenter=False, schemeViewer=False))
        db.add(CategoryBoard(categoryId=cat.id, boardId=board.id, sortOrder=0, hidden=False))

    db.commit()
    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/users/{user_id}/changepassword", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user_id: str,
    body: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot change another user's password")
    if not verify_password(body.old_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid current password")
    current_user.password = hash_password(body.new_password)
    current_user.updateAt = int(time.time() * 1000)
    db.commit()


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest):
    payload = decode_token(body.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    return TokenResponse(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )
