"""
User model for KardoCore authentication.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class UserRole(Enum):
    """User roles"""
    ADMIN = "admin"
    AUTHOR = "author"
    USER = "user"
    GUEST = "guest"


@dataclass
class User:
    """
    User model.
    
    Attributes:
        id: User ID
        email: User email (unique)
        username: Username (unique)
        password_hash: Hashed password
        role: User role
        is_active: Whether user is active
        is_verified: Whether email is verified
        created_at: Creation timestamp
        updated_at: Last update timestamp
        last_login: Last login timestamp
        metadata: Additional user data
    """
    id: Optional[int] = None
    email: str = ""
    username: str = ""
    password_hash: str = ""
    role: UserRole = UserRole.USER
    is_active: bool = True
    is_verified: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    metadata: dict = field(default_factory=dict)
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has permission"""
        # Admin has all permissions
        if self.role == UserRole.ADMIN:
            return True
        
        # Define role permissions
        role_permissions = {
            UserRole.ADMIN: ["*"],
            UserRole.AUTHOR: ["read", "write", "edit_own"],
            UserRole.USER: ["read"],
            UserRole.GUEST: []
        }
        
        perms = role_permissions.get(self.role, [])
        return "*" in perms or permission in perms
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """Convert to dictionary"""
        data = {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "role": self.role.value,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "metadata": self.metadata
        }
        
        if include_sensitive:
            data["password_hash"] = self.password_hash
        
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Create from dictionary"""
        role = UserRole(data.get("role", "user"))
        
        return cls(
            id=data.get("id"),
            email=data.get("email", ""),
            username=data.get("username", ""),
            password_hash=data.get("password_hash", ""),
            role=role,
            is_active=data.get("is_active", True),
            is_verified=data.get("is_verified", False),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None,
            last_login=datetime.fromisoformat(data["last_login"]) if data.get("last_login") else None,
            metadata=data.get("metadata", {})
        )


class UserRepository:
    """
    User repository for database operations.
    
    Example:
        from kardocore.db import Database
        from kardocore.db.adapters import SQLiteAdapter
        
        db = Database(SQLiteAdapter("app.db"))
        await db.connect()
        
        repo = UserRepository(db)
        await repo.create_table()
        
        # Create user
        user = User(email="john@example.com", username="john")
        user = await repo.create(user, password="secret123")
        
        # Find user
        user = await repo.find_by_email("john@example.com")
        
        # Update user
        user.is_verified = True
        await repo.update(user)
    """
    
    def __init__(self, db):
        self.db = db
    
    async def create_table(self):
        """Create users table"""
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                is_active BOOLEAN DEFAULT TRUE,
                is_verified BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                metadata TEXT DEFAULT '{}'
            )
        """)
        
        # Create indexes
        await self.db.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        await self.db.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
    
    async def create(self, user: User, password: str) -> User:
        """Create new user"""
        from .password import PasswordHasher
        
        hasher = PasswordHasher()
        user.password_hash = hasher.hash(password)
        user.created_at = datetime.now()
        user.updated_at = datetime.now()
        
        query = self.db.table("users").insert({
            "email": user.email,
            "username": user.username,
            "password_hash": user.password_hash,
            "role": user.role.value,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
            "metadata": str(user.metadata)
        })
        
        result = await self.db.execute(query.sql(), query.params())
        user.id = result.last_insert_id
        
        return user
    
    async def find_by_id(self, user_id: int) -> Optional[User]:
        """Find user by ID"""
        query = self.db.table("users").select().where("id", "=", user_id)
        row = await self.db.fetch_one(query.sql(), query.params())
        
        return User.from_dict(row) if row else None
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email"""
        query = self.db.table("users").select().where("email", "=", email)
        row = await self.db.fetch_one(query.sql(), query.params())
        
        return User.from_dict(row) if row else None
    
    async def find_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        query = self.db.table("users").select().where("username", "=", username)
        row = await self.db.fetch_one(query.sql(), query.params())
        
        return User.from_dict(row) if row else None
    
    async def update(self, user: User) -> User:
        """Update user"""
        user.updated_at = datetime.now()
        
        query = self.db.table("users").update({
            "email": user.email,
            "username": user.username,
            "password_hash": user.password_hash,
            "role": user.role.value,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "updated_at": user.updated_at.isoformat(),
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "metadata": str(user.metadata)
        }).where("id", "=", user.id)
        
        await self.db.execute(query.sql(), query.params())
        
        return user
    
    async def delete(self, user_id: int) -> bool:
        """Delete user"""
        query = self.db.table("users").delete().where("id", "=", user_id)
        result = await self.db.execute(query.sql(), query.params())
        
        return result.row_count > 0
    
    async def verify_password(self, email: str, password: str) -> Optional[User]:
        """Verify user password"""
        from .password import PasswordHasher
        
        user = await self.find_by_email(email)
        if not user:
            return None
        
        hasher = PasswordHasher()
        if not hasher.verify(password, user.password_hash):
            return None
        
        # Update last login
        user.last_login = datetime.now()
        await self.update(user)
        
        return user
