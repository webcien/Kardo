"""
Session management for KardoCore.
"""

import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class Session:
    """
    User session.
    
    Attributes:
        session_id: Unique session ID
        user_id: User ID
        data: Session data
        created_at: Creation timestamp
        expires_at: Expiration timestamp
        ip_address: Client IP address
        user_agent: Client user agent
    """
    session_id: str
    user_id: int
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    def is_expired(self) -> bool:
        """Check if session is expired"""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "data": self.data,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent
        }


class SessionManager:
    """
    Session manager.
    
    Features:
    - Secure session ID generation
    - Session expiration
    - Session data storage
    - IP and user agent tracking
    
    Example:
        manager = SessionManager(db)
        await manager.create_table()
        
        # Create session
        session = await manager.create(user_id=1, expires_in=3600)
        
        # Get session
        session = await manager.get(session_id)
        
        # Update session data
        await manager.update(session_id, {"cart": [1, 2, 3]})
        
        # Destroy session
        await manager.destroy(session_id)
    """
    
    def __init__(self, db):
        self.db = db
    
    async def create_table(self):
        """Create sessions table"""
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                data TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT
            )
        """)
        
        await self.db.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id)")
        await self.db.execute("CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at)")
    
    async def create(
        self,
        user_id: int,
        expires_in: int = 3600,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Session:
        """Create new session"""
        session_id = secrets.token_urlsafe(32)
        created_at = datetime.now()
        expires_at = created_at + timedelta(seconds=expires_in)
        
        query = self.db.table("sessions").insert({
            "session_id": session_id,
            "user_id": user_id,
            "data": "{}",
            "created_at": created_at.isoformat(),
            "expires_at": expires_at.isoformat(),
            "ip_address": ip_address,
            "user_agent": user_agent
        })
        
        await self.db.execute(query.sql(), query.params())
        
        return Session(
            session_id=session_id,
            user_id=user_id,
            created_at=created_at,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    async def get(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        query = self.db.table("sessions").select().where("session_id", "=", session_id)
        row = await self.db.fetch_one(query.sql(), query.params())
        
        if not row:
            return None
        
        import json
        
        session = Session(
            session_id=row["session_id"],
            user_id=row["user_id"],
            data=json.loads(row["data"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            expires_at=datetime.fromisoformat(row["expires_at"]) if row["expires_at"] else None,
            ip_address=row.get("ip_address"),
            user_agent=row.get("user_agent")
        )
        
        # Check expiration
        if session.is_expired():
            await self.destroy(session_id)
            return None
        
        return session
    
    async def update(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Update session data"""
        import json
        
        query = self.db.table("sessions").update({
            "data": json.dumps(data)
        }).where("session_id", "=", session_id)
        
        result = await self.db.execute(query.sql(), query.params())
        return result.row_count > 0
    
    async def destroy(self, session_id: str) -> bool:
        """Destroy session"""
        query = self.db.table("sessions").delete().where("session_id", "=", session_id)
        result = await self.db.execute(query.sql(), query.params())
        return result.row_count > 0
    
    async def destroy_user_sessions(self, user_id: int) -> int:
        """Destroy all sessions for a user"""
        query = self.db.table("sessions").delete().where("user_id", "=", user_id)
        result = await self.db.execute(query.sql(), query.params())
        return result.row_count
    
    async def cleanup_expired(self) -> int:
        """Remove expired sessions"""
        now = datetime.now().isoformat()
        query = self.db.table("sessions").delete().where("expires_at", "<", now)
        result = await self.db.execute(query.sql(), query.params())
        return result.row_count
