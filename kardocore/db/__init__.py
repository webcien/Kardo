"""
KardoCore Database Module.

Universal, protocol-based database layer.

Example:
    from kardocore.db import Database
    from kardocore.db.adapters import SQLiteAdapter
    
    db = Database(SQLiteAdapter("app.db"))
    await db.connect()
    
    users = await db.fetch_all("SELECT * FROM users")
"""

from .protocols import (
    DatabaseProtocol,
    ColumnType,
    Column,
    Table,
    QueryResult
)
from .connection import DatabaseManager
from .query.builder import QueryBuilder

__all__ = [
    "Database",
    "DatabaseManager",
    "DatabaseProtocol",
    "ColumnType",
    "Column",
    "Table",
    "QueryResult",
    "QueryBuilder",
]

# Import Database class
"""
Main database interface for KardoCore.
"""

from typing import Optional, List, Dict, Any
from .protocols import DatabaseProtocol, QueryResult
from .query.builder import QueryBuilder


class Database:
    """
    Main database interface.
    
    Wraps a database adapter and provides a clean API.
    
    Example:
        from kardocore.db import Database
        from kardocore.db.adapters import SQLiteAdapter
        
        db = Database(SQLiteAdapter("app.db"))
        await db.connect()
        
        # Execute
        await db.execute("INSERT INTO users (name) VALUES (:name)", {"name": "John"})
        
        # Fetch
        user = await db.fetch_one("SELECT * FROM users WHERE id = :id", {"id": 1})
        users = await db.fetch_all("SELECT * FROM users WHERE active = :active", {"active": True})
        
        # Query builder
        query = db.table("users").select("id", "name").where("active", "=", True)
        users = await db.fetch_all(query.sql(), query.params())
    """
    
    def __init__(self, adapter: DatabaseProtocol):
        self.adapter = adapter
    
    @property
    def name(self) -> str:
        """Database adapter name"""
        return self.adapter.name
    
    @property
    def is_connected(self) -> bool:
        """Check if connected"""
        return self.adapter.is_connected
    
    async def connect(self) -> None:
        """Connect to database"""
        await self.adapter.connect()
    
    async def disconnect(self) -> None:
        """Disconnect from database"""
        if hasattr(self.adapter, 'disconnect'):
            await self.adapter.disconnect()
    
    async def execute(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> QueryResult:
        """Execute a query"""
        return await self.adapter.execute(query, params)
    
    async def fetch_one(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Fetch single row"""
        return await self.adapter.fetch_one(query, params)
    
    async def fetch_all(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Fetch all rows"""
        return await self.adapter.fetch_all(query, params)
    
    def table(self, name: str) -> QueryBuilder:
        """Get query builder for table"""
        return QueryBuilder(name)
    
    async def begin_transaction(self) -> None:
        """Begin transaction"""
        await self.adapter.begin_transaction()
    
    async def commit(self) -> None:
        """Commit transaction"""
        await self.adapter.commit()
    
    async def rollback(self) -> None:
        """Rollback transaction"""
        await self.adapter.rollback()
    
    async def health_check(self) -> bool:
        """Health check"""
        if hasattr(self.adapter, 'health_check'):
            return await self.adapter.health_check()
        return self.is_connected
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()
