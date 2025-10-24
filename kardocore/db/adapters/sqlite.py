"""SQLite adapter for KardoCore"""
import aiosqlite
from typing import Optional, List, Dict, Any
from kardocore.db.protocols import DatabaseProtocol, QueryResult, Table, Column

class SQLiteAdapter:
    def __init__(self, database: str = ":memory:"):
        self.database = database
        self.conn = None
    
    @property
    def name(self) -> str:
        return "sqlite"
    
    async def connect(self) -> None:
        self.conn = await aiosqlite.connect(self.database)
        self.conn.row_factory = aiosqlite.Row
    
    async def execute(self, query: str, params: Optional[Dict] = None) -> QueryResult:
        cursor = await self.conn.execute(query, params or {})
        await self.conn.commit()
        return QueryResult(rows=[], row_count=cursor.rowcount)
    
    async def fetch_one(self, query: str, params: Optional[Dict] = None) -> Optional[Dict]:
        cursor = await self.conn.execute(query, params or {})
        row = await cursor.fetchone()
        return dict(row) if row else None
    
    async def fetch_all(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        cursor = await self.conn.execute(query, params or {})
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
