"""
MySQL Database Adapter

Async MySQL support using aiomysql.
"""

from typing import Any, Dict, List, Optional
import aiomysql


class MySQLAdapter:
    """
    MySQL Database Adapter
    
    Async MySQL database operations.
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 3306,
        user: str = "root",
        password: str = "",
        database: str = "kardocore",
        **kwargs
    ):
        """
        Initialize MySQL adapter
        
        Args:
            host: MySQL host
            port: MySQL port
            user: MySQL user
            password: MySQL password
            database: Database name
            **kwargs: Additional connection options
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.kwargs = kwargs
        self.pool: Optional[aiomysql.Pool] = None
        
    async def connect(self):
        """Establish connection pool"""
        self.pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.database,
            **self.kwargs
        )
        
    async def disconnect(self):
        """Close connection pool"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            
    async def execute(
        self,
        query: str,
        params: Optional[tuple] = None
    ) -> int:
        """
        Execute query
        
        Returns:
            Number of affected rows
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params or ())
                await conn.commit()
                return cursor.rowcount
                
    async def fetch_one(
        self,
        query: str,
        params: Optional[tuple] = None
    ) -> Optional[Dict[str, Any]]:
        """Fetch single row"""
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params or ())
                return await cursor.fetchone()
                
    async def fetch_all(
        self,
        query: str,
        params: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """Fetch all rows"""
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params or ())
                return await cursor.fetchall()
                
    async def transaction(self):
        """Start transaction context"""
        return self.pool.acquire()
