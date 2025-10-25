"""
Database Module - Core database functionality
"""

from kardocore.db.connection import DatabaseManager
from kardocore.db.protocols import DatabaseProtocol, ColumnType, Column, Table
from kardocore.db.adapters.sqlite import SQLiteAdapter
from kardocore.db.query.builder import QueryBuilder
from kardocore.db.orm import Model, QuerySet
from kardocore.db.migrations.manager import MigrationManager

# Try to import optional adapters
try:
    from kardocore.db.adapters.postgresql import PostgreSQLAdapter
except ImportError:
    PostgreSQLAdapter = None

try:
    from kardocore.db.adapters.mysql import MySQLAdapter
except ImportError:
    MySQLAdapter = None

# Alias for convenience
Database = DatabaseManager
ConnectionManager = DatabaseManager  # Backward compatibility

__all__ = [
    "Database",
    "DatabaseManager",
    "ConnectionManager",
    "DatabaseProtocol",
    "ColumnType",
    "Column",
    "Table",
    "SQLiteAdapter",
    "PostgreSQLAdapter",
    "MySQLAdapter",
    "QueryBuilder",
    "Model",
    "QuerySet",
    "MigrationManager",
]
