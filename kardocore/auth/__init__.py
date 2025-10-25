"""
Authentication Module - User authentication and security
"""

from kardocore.auth.user import User, UserRepository
from kardocore.auth.password import PasswordHasher
from kardocore.auth.jwt import JWTManager
from kardocore.auth.session import SessionManager
from kardocore.auth.oauth import OAuth
from kardocore.auth.twofa import TwoFactorAuth
from kardocore.auth.email import EmailVerification
from kardocore.auth.reset import PasswordReset
from kardocore.auth.xss import XSSPrevention
from kardocore.auth.middleware.csrf import CSRFProtection
from kardocore.auth.middleware.ratelimit import RateLimiter

__all__ = [
    "User",
    "UserRepository",
    "PasswordHasher",
    "JWTManager",
    "SessionManager",
    "OAuth",
    "TwoFactorAuth",
    "EmailVerification",
    "PasswordReset",
    "XSSPrevention",
    "CSRFProtection",
    "RateLimiter",
]
