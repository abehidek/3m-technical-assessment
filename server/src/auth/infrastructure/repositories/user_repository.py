from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
from src.auth.application.ports.repositories import UserRepositoryInterface
from src.auth.domain.models.user import User


class UserRepository(UserRepositoryInterface):
    """
    Implementation of UserRepositoryInterface
    """

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, email: str, hashed_password: str) -> User:
        """Create a new user in the database"""
        user = User(email=email, hashed_password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Find user by email"""
        result = self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Find user by ID"""
        result = self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
