"""
Authentication Manager

Central authentication manager that integrates all auth components.
"""

from typing import Optional, Dict, Any
from kardocore.auth.user import User, UserRepository
from kardocore.auth.password import PasswordHasher
from kardocore.auth.jwt import JWT
from kardocore.auth.session import SessionManager


class AuthManager:
    """
    Authentication Manager
    
    Central manager for all authentication operations.
    Integrates user management, password hashing, JWT, and sessions.
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        secret_key: str,
        session_manager: Optional[SessionManager] = None
    ):
        """
        Initialize AuthManager
        
        Args:
            user_repository: User repository for database operations
            secret_key: Secret key for JWT signing
            session_manager: Optional session manager
        """
        self.users = user_repository
        self.password_hasher = PasswordHasher()
        self.jwt = JWT(secret=secret_key)
        self.sessions = session_manager
    
    async def authenticate(
        self,
        username: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate user with username and password
        
        Args:
            username: Username or email
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        user = await self.users.get_by_username(username)
        if not user:
            user = await self.users.get_by_email(username)
        
        if not user:
            return None
        
        if not self.password_hasher.verify(password, user.password_hash):
            return None
        
        return user
    
    def create_token(self, user: User, expires_in: int = 3600) -> str:
        """
        Create JWT token for user
        
        Args:
            user: User object
            expires_in: Token expiration in seconds
            
        Returns:
            JWT token string
        """
        payload = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return self.jwt.encode(payload, expires_in=expires_in)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            Token payload if valid, None otherwise
        """
        return self.jwt.decode(token)
    
    async def get_user_by_token(self, token: str) -> Optional[User]:
        """
        Get user from JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            User object if token is valid, None otherwise
        """
        payload = self.verify_token(token)
        if not payload:
            return None
        
        user_id = payload.get("user_id")
        if not user_id:
            return None
        
        return await self.users.get_by_id(user_id)

