"""
Authentication Module - User authentication and security
"""

from kardocore.auth.user import User, UserRepository, UserRole
from kardocore.auth.password import PasswordHasher, HashAlgorithm
from kardocore.auth.jwt import JWT
from kardocore.auth.session import Session, SessionManager
from kardocore.auth.oauth import OAuth, OAuthProvider
from kardocore.auth.twofa import TwoFactorAuth
from kardocore.auth.email import EmailVerification
from kardocore.auth.reset import PasswordReset
from kardocore.auth.xss import XSSProtection
from kardocore.auth.middleware.csrf import CSRFProtection
from kardocore.auth.middleware.ratelimit import RateLimiter
from kardocore.auth.manager import AuthManager

__all__ = [
    "User",
    "UserRepository",
    "UserRole",
    "PasswordHasher",
    "HashAlgorithm",
    "JWT",
    "Session",
    "SessionManager",
    "OAuth",
    "OAuthProvider",
    "TwoFactorAuth",
    "EmailVerification",
    "PasswordReset",
    "XSSProtection",
    "CSRFProtection",
    "RateLimiter",
    "AuthManager",
]

