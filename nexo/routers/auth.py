import time

from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session as DBSession

from nexo.auth.dependencies import get_current_user
from nexo.auth.jwt import create_access_token, create_refresh_token, decode_token
from nexo.auth.password import hash_password, verify_password
from nexo.auth.schemas import (
    ChangePasswordRequest,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from nexo.config import get_settings
from nexo.db.session import get_db
from nexo.models import User
from nexo.services.session_service import SessionService

router = APIRouter(prefix="/api/v1", tags=["auth"])
limiter = Limiter(key_func=get_remote_address)
settings = get_settings()


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
async def login(request: Request, body: LoginRequest, db: DBSession = Depends(get_db)):
    user = db.query(User).filter(
        (User.username == body.username) | (User.email == body.username),
        User.delete_at == 0,
    ).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    SessionService(db).create(user.id, access_token, settings.access_token_expire_days)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    auth = request.headers.get("authorization", "")
    token = auth.split(" ", 1)[-1] if " " in auth else ""
    if token:
        SessionService(db).revoke(token)


@router.post("/register", response_model=TokenResponse)
@limiter.limit("5/minute")
async def register(request: Request, body: RegisterRequest, db: DBSession = Depends(get_db)):
    existing = db.query(User).filter(
        (User.username == body.username) | (User.email == body.email),
        User.delete_at == 0,
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")

    now = int(time.time() * 1000)
    user = User(
        username=body.username,
        email=body.email,
        password_hash=hash_password(body.password),
        create_at=now,
        update_at=now,
        delete_at=0,
    )
    db.add(user)
    db.flush()

    from nexo.models import BoardMember, Category, CategoryBoard, Team, Board

    existing_teams = db.query(Team).count()
    if existing_teams == 0:
        team = Team(
            display_name="My Workspace",
            create_at=now,
            update_at=now,
            delete_at=0,
        )
        db.add(team)
        db.flush()

        board = Board(
            team_id=team.id,
            type="P",
            title="Welcome Board",
            description="",
            icon="🎉",
            show_description=False,
            is_template=False,
            template_version=0,
            minimum_role="",
            create_at=now,
            update_at=now,
            delete_at=0,
        )
        db.add(board)
        db.flush()

        cat = Category(
            name="Boards",
            user_id=user.id,
            team_id=team.id,
            type="system",
            sort_order=0,
            create_at=now,
            update_at=now,
            delete_at=0,
        )
        db.add(cat)
        db.flush()

        db.add(
            BoardMember(
                board_id=board.id,
                user_id=user.id,
                roles="",
                scheme_admin=True,
                scheme_editor=False,
                scheme_commenter=False,
                scheme_viewer=False,
                create_at=now,
                update_at=now,
                delete_at=0,
            )
        )
        db.add(
            CategoryBoard(
                user_id=user.id,
                team_id=team.id,
                category_id=cat.id,
                board_id=board.id,
                sort_order=0,
                hide=False,
                create_at=now,
                update_at=now,
                delete_at=0,
            )
        )

    db.commit()

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    SessionService(db).create(user.id, access_token, settings.access_token_expire_days)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/users/{user_id}/changepassword", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user_id: str,
    body: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot change another user's password")
    if not verify_password(body.old_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid current password")
    current_user.password_hash = hash_password(body.new_password)
    current_user.update_at = int(time.time() * 1000)
    db.commit()


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest, db: DBSession = Depends(get_db)):
    payload = decode_token(body.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    SessionService(db).create(user_id, access_token, settings.access_token_expire_days)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
