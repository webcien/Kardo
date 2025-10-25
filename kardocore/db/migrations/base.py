"""
Migration Base Class

Base class for all database migrations.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from kardocore.db.connection import DatabaseManager


class Migration(ABC):
    """Base class for migrations"""
    
    # Migration metadata
    version: str = ""
    description: str = ""
    
    @abstractmethod
    async def up(self, db: 'DatabaseManager'):
        """Apply migration"""
        pass
    
    @abstractmethod
    async def down(self, db: 'DatabaseManager'):
        """Rollback migration"""
        pass
    
    def __repr__(self):
        return f"<Migration {self.version}: {self.description}>"


class TableMigration(Migration):
    """Helper for table creation migrations"""
    
    def __init__(self, table_name: str, columns: List[Dict[str, Any]]):
        self.table_name = table_name
        self.columns = columns
    
    async def up(self, db: 'DatabaseManager'):
        """Create table"""
        # Build CREATE TABLE SQL
        column_defs = []
        for col in self.columns:
            col_def = f"{col['name']} {col['type']}"
            
            if col.get('primary_key'):
                col_def += " PRIMARY KEY"
            if col.get('auto_increment'):
                col_def += " AUTOINCREMENT"
            if col.get('not_null'):
                col_def += " NOT NULL"
            if col.get('unique'):
                col_def += " UNIQUE"
            if 'default' in col:
                col_def += f" DEFAULT {col['default']}"
            
            column_defs.append(col_def)
        
        sql = f"CREATE TABLE {self.table_name} ({', '.join(column_defs)})"
        await db.execute(sql)
    
    async def down(self, db: 'DatabaseManager'):
        """Drop table"""
        await db.execute(f"DROP TABLE IF EXISTS {self.table_name}")
