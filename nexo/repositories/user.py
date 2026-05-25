import time

from sqlalchemy import or_, select
from sqlalchemy.orm import Session as DBSession

from nexo.auth.password import hash_password
from nexo.models import User
from nexo.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def get(self, user_id: str) -> User | None:
        return self.db.get(User, user_id)

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username, User.delete_at == 0)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email, User.delete_at == 0)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_login(self, login: str) -> User | None:
        stmt = select(User).where(
            or_(User.username == login, User.email == login),
            User.delete_at == 0,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, data: UserCreate) -> User:
        now = int(time.time() * 1000)
        user = User(
            username=data.username,
            email=data.email,
            password_hash=hash_password(data.password),
            create_at=now,
            update_at=now,
            delete_at=0,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: str, data: UserUpdate) -> User | None:
        user = self.get(user_id)
        if not user:
            return None
        now = int(time.time() * 1000)
        patch = data.model_dump(exclude_unset=True)
        if "password" in patch:
            patch["password_hash"] = hash_password(patch.pop("password"))
        for key, value in patch.items():
            setattr(user, key, value)
        user.update_at = now
        self.db.commit()
        self.db.refresh(user)
        return user

    def soft_delete(self, user_id: str) -> bool:
        user = self.get(user_id)
        if not user:
            return False
        user.delete_at = int(time.time() * 1000)
        self.db.commit()
        return True
