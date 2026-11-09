"""
PlacementPilot Repositories Package
"""

from app.repositories.base import BaseRepository
from app.repositories.user import UserRepository, user_repository
from app.repositories.profile import StudentProfileRepository, profile_repository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "user_repository",
    "StudentProfileRepository",
    "profile_repository",
]
