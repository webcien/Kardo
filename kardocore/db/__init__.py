"""
Database Module - Core database functionality
"""

from kardocore.db.connection import ConnectionManager
from kardocore.db.protocols import DatabaseProtocol, ColumnType, Column, Table
from kardocore.db.adapters.sqlite import SQLiteAdapter
from kardocore.db.adapters.postgresql import PostgreSQLAdapter
from kardocore.db.adapters.mysql import MySQLAdapter
from kardocore.db.query.builder import QueryBuilder
from kardocore.db.orm import Model, QuerySet
from kardocore.db.migrations.manager import MigrationManager

# Alias for convenience
Database = ConnectionManager

__all__ = [
    "Database",
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
