"""Users router — BC-Identity.

GET  /api/v1/users/me          → perfil do usuário autenticado
GET  /api/v1/users/{user_id}   → perfil por ID
PUT  /api/v1/users/{user_id}   → atualizar próprio perfil
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DBSession

from nexo.auth.dependencies import get_current_user
from nexo.db.session import get_db
from nexo.domain.exceptions import (
    DuplicateEmailError,
    DuplicateUsernameError,
    InvalidEmailError,
    PasswordTooShortError,
    UserNotFoundError,
)
from nexo.models import User
from nexo.schemas.user import UserResponse, UserUpdate
from nexo.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["users"])


def _svc(db: DBSession = Depends(get_db)) -> UserService:
    return UserService(db)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    svc: UserService = Depends(_svc),
):
    try:
        return svc.get_by_id(user_id)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    body: UserUpdate,
    current_user: User = Depends(get_current_user),
    svc: UserService = Depends(_svc),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot update another user's profile")
    try:
        return svc.update(user_id, body)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except (DuplicateEmailError, DuplicateUsernameError) as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except (InvalidEmailError, PasswordTooShortError) as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
