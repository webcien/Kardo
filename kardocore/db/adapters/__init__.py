"""
Database Adapters

Note: PostgreSQL and MySQL adapters require optional dependencies.
Install with: pip install kardocore[postgresql] or kardocore[mysql]
"""

# SQLite is always available (no external dependencies)
from kardocore.db.adapters.sqlite import SQLiteAdapter

# Try to import optional adapters, but don't fail if dependencies are missing
try:
    from kardocore.db.adapters.postgresql import PostgreSQLAdapter
except ImportError:
    PostgreSQLAdapter = None

try:
    from kardocore.db.adapters.mysql import MySQLAdapter
except ImportError:
    MySQLAdapter = None

__all__ = [
    "SQLiteAdapter",
    "PostgreSQLAdapter",
    "MySQLAdapter",
]
