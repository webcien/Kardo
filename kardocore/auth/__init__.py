"""
KardoCore Authentication & Security Module.

Complete authentication system with:
- User management
- Password hashing (bcrypt/argon2)
- JWT tokens
- Session management
- CSRF protection
- Rate limiting
- OAuth support (planned)

Example:
    from kardocore.auth import Auth
    from kardocore.db import Database
    from kardocore.db.adapters import SQLiteAdapter
    
    # Setup
    db = Database(SQLiteAdapter("app.db"))
    await db.connect()
    
    auth = Auth(db, secret="your-secret-key")
    await auth.setup()
    
    # Register user
    user = await auth.register(
        email="john@example.com",
        username="john",
        password="SecurePass123!"
    )
    
    # Login
    result = await auth.login("john@example.com", "SecurePass123!")
    if result:
        token = result["token"]
        user = result["user"]
    
    # Verify token
    user = await auth.verify_token(token)
"""

from .user import User, UserRole, UserRepository
from .password import PasswordHasher, HashAlgorithm
from .jwt import JWT
from .session import Session, SessionManager
from .middleware.csrf import CSRFProtection
from .middleware.ratelimit import RateLimiter

__all__ = [
    "Auth",
    "User",
    "UserRole",
    "UserRepository",
    "PasswordHasher",
    "HashAlgorithm",
    "JWT",
    "Session",
    "SessionManager",
    "CSRFProtection",
    "RateLimiter",
]


class Auth:
    """
    Main authentication class.
    
    Integrates all authentication components.
    
    Example:
        auth = Auth(db, secret="your-secret-key")
        await auth.setup()
        
        # Register
        user = await auth.register("john@example.com", "john", "password123")
        
        # Login
        result = await auth.login("john@example.com", "password123")
        
        # Verify token
        user = await auth.verify_token(result["token"])
    """
    
    def __init__(
        self,
        db,
        secret: str,
        jwt_expires_in: int = 3600,
        session_expires_in: int = 86400,
        max_login_attempts: int = 5,
        login_window: int = 300
    ):
        self.db = db
        self.secret = secret
        self.jwt_expires_in = jwt_expires_in
        self.session_expires_in = session_expires_in
        
        # Components
        self.users = UserRepository(db)
        self.sessions = SessionManager(db)
        self.jwt = JWT(secret)
        self.csrf = CSRFProtection(secret)
        self.rate_limiter = RateLimiter(
            max_attempts=max_login_attempts,
            window=login_window
        )
    
    async def setup(self):
        """Setup database tables"""
        await self.users.create_table()
        await self.sessions.create_table()
    
    async def register(
        self,
        email: str,
        username: str,
        password: str,
        role: UserRole = UserRole.USER
    ) -> User:
        """
        Register new user.
        
        Args:
            email: User email
            username: Username
            password: Plain text password
            role: User role
            
        Returns:
            Created user
            
        Raises:
            ValueError: If validation fails
        """
        # Validate password strength
        is_valid, errors = PasswordHasher.validate_strength(password)
        if not is_valid:
            raise ValueError(f"Weak password: {', '.join(errors)}")
        
        # Check if user exists
        existing = await self.users.find_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        
        existing = await self.users.find_by_username(username)
        if existing:
            raise ValueError("Username already taken")
        
        # Create user
        user = User(email=email, username=username, role=role)
        user = await self.users.create(user, password)
        
        return user
    
    async def login(
        self,
        email: str,
        password: str,
        ip_address: str = None,
        user_agent: str = None
    ) -> dict:
        """
        Login user.
        
        Args:
            email: User email
            password: Plain text password
            ip_address: Client IP
            user_agent: Client user agent
            
        Returns:
            Dict with token, session_id, and user
            
        Raises:
            ValueError: If login fails
        """
        # Check rate limit
        is_allowed, retry_after = self.rate_limiter.is_allowed(ip_address or email)
        if not is_allowed:
            raise ValueError(f"Too many login attempts. Retry after {retry_after} seconds")
        
        # Verify credentials
        user = await self.users.verify_password(email, password)
        if not user:
            self.rate_limiter.record_attempt(ip_address or email)
            raise ValueError("Invalid email or password")
        
        # Check if user is active
        if not user.is_active:
            raise ValueError("Account is disabled")
        
        # Reset rate limiter on successful login
        self.rate_limiter.reset(ip_address or email)
        
        # Create JWT token
        token = self.jwt.encode({
            "user_id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role.value
        }, expires_in=self.jwt_expires_in)
        
        # Create session
        session = await self.sessions.create(
            user_id=user.id,
            expires_in=self.session_expires_in,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return {
            "token": token,
            "session_id": session.session_id,
            "user": user.to_dict()
        }
    
    async def verify_token(self, token: str) -> User:
        """
        Verify JWT token and get user.
        
        Args:
            token: JWT token
            
        Returns:
            User if valid
            
        Raises:
            ValueError: If token is invalid
        """
        payload = self.jwt.decode(token)
        if not payload:
            raise ValueError("Invalid or expired token")
        
        user_id = payload.get("user_id")
        if not user_id:
            raise ValueError("Invalid token payload")
        
        user = await self.users.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        if not user.is_active:
            raise ValueError("Account is disabled")
        
        return user
    
    async def logout(self, session_id: str):
        """Logout user (destroy session)"""
        await self.sessions.destroy(session_id)
    
    async def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str
    ):
        """
        Change user password.
        
        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password
            
        Raises:
            ValueError: If validation fails
        """
        user = await self.users.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Verify old password
        hasher = PasswordHasher()
        if not hasher.verify(old_password, user.password_hash):
            raise ValueError("Invalid current password")
        
        # Validate new password
        is_valid, errors = PasswordHasher.validate_strength(new_password)
        if not is_valid:
            raise ValueError(f"Weak password: {', '.join(errors)}")
        
        # Update password
        user.password_hash = hasher.hash(new_password)
        await self.users.update(user)
        
        # Destroy all sessions
        await self.sessions.destroy_user_sessions(user_id)
