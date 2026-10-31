from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User, StudentProfile
from app.repositories.base import BaseRepository
from app.schemas.auth import UserRegisterRequest, UserUpdateRequest

class UserRepository(BaseRepository[User, UserRegisterRequest, UserUpdateRequest]):
    """Specialized repository for User and StudentProfile operations."""
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Fetch a single user by exact normalized email address."""
        stmt = select(User).where(User.email == email.strip().lower())
        return db.scalar(stmt)

    def email_exists(self, db: Session, email: str) -> bool:
        """Check if an email address is already registered."""
        stmt = select(User.id).where(User.email == email.strip().lower())
        return db.scalar(stmt) is not None

    def create_user_with_profile(
        self,
        db: Session,
        *,
        user: User,
        profile: Optional[StudentProfile] = None
    ) -> User:
        """Persists a new user and links their initial student profile within one transaction."""
        db.add(user)
        db.flush()  # Generate user.id for profile foreign key
        if profile:
            profile.user_id = user.id
            db.add(profile)
        db.commit()
        db.refresh(user)
        return user

    def update_password_hash(self, db: Session, user: User, password_hash: str) -> User:
        """Updates user password hash and commits."""
        user.password_hash = password_hash
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

user_repository = UserRepository()

