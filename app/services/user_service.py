from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import User, UserRole


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        result = self.db.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

    def get_user_by_id(self, user_id: int) -> User | None:
        result = self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    def create_user(
        self, telegram_id: int, username: str, role: UserRole = None
    ) -> User:
        # If a role is not specified, determine based on if it's the first user
        if role is None:
            is_first_user = self.is_first_user()
            role = UserRole.ADMIN if is_first_user else UserRole.CLIENT

        user = User(telegram_id=telegram_id, username=username, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def is_first_user(self) -> bool:
        # Check if there are no real users (excluding the placeholder)
        result = self.db.execute(select(User).where(User.telegram_id != -1))
        return len(result.scalars().all()) == 0

    def get_first_user_flag(self) -> User | None:
        # Get the placeholder user that indicates the first user should be admin
        result = self.db.execute(select(User).where(User.telegram_id == -1))
        return result.scalar_one_or_none()

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

    def get_all_users_except(self, exclude_id: int) -> list[User]:
        result = self.db.execute(
            select(User).where(User.telegram_id != exclude_id, User.telegram_id != -1)
        )
        return list(result.scalars().all())

    def update_user_role(self, user_id: int, new_role: UserRole) -> User | None:
        user = self.get_user_by_id(user_id)

        if user:
            user.role = new_role
            user.updated_at = datetime.now(UTC)
            self.db.commit()
            self.db.refresh(user)

        return user
