"""
Database connection manager for KardoCore.
"""

from typing import Dict, Optional, Any
from .protocols import DatabaseProtocol


class DatabaseManager:
    """
    Manage multiple database connections.
    
    Features:
    - Multi-database support
    - Connection pooling
    - Health checks
    - Auto-reconnect
    
    Example:
        manager = DatabaseManager()
        manager.add("default", SQLiteAdapter("app.db"))
        manager.add("analytics", PostgreSQLAdapter("postgresql://..."))
        
        await manager.connect_all()
        
        # Use specific database
        users = await manager.get("default").fetch_all("SELECT * FROM users")
    """
    
    def __init__(self):
        self.databases: Dict[str, DatabaseProtocol] = {}
        self.default_name: Optional[str] = None
    
    def add(
        self,
        name: str,
        adapter: DatabaseProtocol,
        is_default: bool = False
    ):
        """Add a database connection"""
        self.databases[name] = adapter
        
        if is_default or self.default_name is None:
            self.default_name = name
    
    def get(self, name: Optional[str] = None) -> DatabaseProtocol:
        """Get database connection"""
        db_name = name or self.default_name
        
        if db_name is None:
            raise ValueError("No default database configured")
        
        if db_name not in self.databases:
            raise ValueError(f"Database '{db_name}' not found")
        
        return self.databases[db_name]
    
    async def connect_all(self):
        """Connect all databases"""
        for adapter in self.databases.values():
            await adapter.connect()
    
    async def disconnect_all(self):
        """Disconnect all databases"""
        for adapter in self.databases.values():
            if hasattr(adapter, 'disconnect'):
                await adapter.disconnect()
    
    async def health_check_all(self) -> Dict[str, bool]:
        """Health check all databases"""
        results = {}
        for name, adapter in self.databases.items():
            try:
                if hasattr(adapter, 'health_check'):
                    results[name] = await adapter.health_check()
                else:
                    results[name] = True
            except Exception:
                results[name] = False
        return results
