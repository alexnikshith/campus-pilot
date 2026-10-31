"""
PlacementPilot Services Package
"""

from app.services.base import BaseService
from app.services.auth_service import AuthService, auth_service

__all__ = ["BaseService", "AuthService", "auth_service"]
