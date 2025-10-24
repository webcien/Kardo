"""
PostgreSQL adapter for KardoCore using asyncpg.
"""

from typing import Optional, List, Dict, Any
import asyncpg
from kardocore.db.protocols import DatabaseProtocol, QueryResult, Table


class PostgreSQLAdapter:
    """
    PostgreSQL database adapter.
    
    Features:
    - Connection pooling
    - Prepared statements
    - Type conversion
    - SSL support
    
    Example:
        db = PostgreSQLAdapter("postgresql://user:pass@localhost/dbname")
        await db.connect()
        
        result = await db.execute(
            "INSERT INTO users (name) VALUES (:name)",
            {"name": "John"}
        )
    """
    
    def __init__(
        self,
        dsn: str,
        *,
        min_size: int = 10,
        max_size: int = 20,
        **kwargs
    ):
        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size
        self.kwargs = kwargs
        self.pool: Optional[asyncpg.Pool] = None
    
    @property
    def name(self) -> str:
        return "postgresql"
    
    @property
    def is_connected(self) -> bool:
        return self.pool is not None
    
    async def connect(self) -> None:
        """Create connection pool"""
        self.pool = await asyncpg.create_pool(
            self.dsn,
            min_size=self.min_size,
            max_size=self.max_size,
            **self.kwargs
        )
    
    async def disconnect(self) -> None:
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            self.pool = None
    
    async def execute(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> QueryResult:
        """Execute query"""
        async with self.pool.acquire() as conn:
            # Convert named parameters to positional
            sql, values = self._convert_params(query, params or {})
            
            result = await conn.execute(sql, *values)
            
            # Parse result (e.g., "INSERT 0 1" -> row_count=1)
            row_count = 0
            if result:
                parts = result.split()
                if len(parts) > 1:
                    row_count = int(parts[-1])
            
            return QueryResult(rows=[], row_count=row_count)
    
    async def fetch_one(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Fetch single row"""
        async with self.pool.acquire() as conn:
            sql, values = self._convert_params(query, params or {})
            row = await conn.fetchrow(sql, *values)
            return dict(row) if row else None
    
    async def fetch_all(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Fetch all rows"""
        async with self.pool.acquire() as conn:
            sql, values = self._convert_params(query, params or {})
            rows = await conn.fetch(sql, *values)
            return [dict(row) for row in rows]
    
    async def begin_transaction(self) -> None:
        """Begin transaction"""
        # Transactions are per-connection in asyncpg
        # This is a simplified implementation
        pass
    
    async def commit(self) -> None:
        """Commit transaction"""
        pass
    
    async def rollback(self) -> None:
        """Rollback transaction"""
        pass
    
    async def health_check(self) -> bool:
        """Health check"""
        try:
            async with self.pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception:
            return False
    
    def _convert_params(
        self,
        query: str,
        params: Dict[str, Any]
    ) -> tuple[str, list]:
        """Convert named parameters to positional ($1, $2, ...)"""
        sql = query
        values = []
        
        for i, (key, value) in enumerate(params.items(), 1):
            sql = sql.replace(f":{key}", f"${i}")
            values.append(value)
        
        return sql, values
