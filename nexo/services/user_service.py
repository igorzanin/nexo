"""UserService — BC-Identity.

Wraps UserRepository with domain validation from nexo.domain.rules.auth.
"""
from __future__ import annotations

import time

from sqlalchemy.orm import Session as DBSession

from nexo.auth.password import verify_password, hash_password
from nexo.domain.exceptions import (
    DuplicateEmailError,
    DuplicateUsernameError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from nexo.domain.rules.auth import validate_email_format, validate_password_length
from nexo.models import User
from nexo.repositories.user import UserRepository
from nexo.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: DBSession):
        self._repo = UserRepository(db)
        self._db = db

    def get_by_id(self, user_id: str) -> User:
        user = self._repo.get(user_id)
        if not user or user.delete_at != 0:
            raise UserNotFoundError(user_id)
        return user

    def get_by_login(self, login: str) -> User | None:
        return self._repo.get_by_login(login)

    def create(self, data: UserCreate) -> User:
        validate_password_length(data.password)
        validate_email_format(data.email)
        if self._repo.get_by_email(data.email):
            raise DuplicateEmailError(data.email)
        if self._repo.get_by_username(data.username):
            raise DuplicateUsernameError(data.username)
        return self._repo.create(data)

    def update(self, user_id: str, data: UserUpdate) -> User:
        if data.email is not None:
            validate_email_format(data.email)
        if data.password is not None:
            validate_password_length(data.password)
        updated = self._repo.update(user_id, data)
        if not updated:
            raise UserNotFoundError(user_id)
        return updated

    def change_password(self, user: User, old_password: str, new_password: str) -> None:
        if not verify_password(old_password, user.password_hash):
            raise InvalidCredentialsError()
        validate_password_length(new_password)
        user.password_hash = hash_password(new_password)
        user.update_at = int(time.time() * 1000)
        self._db.commit()
