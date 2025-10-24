"""
Database protocols for KardoCore.
"""

from typing import Protocol, Any, Optional, List, Dict
from dataclasses import dataclass
from enum import Enum

class ColumnType(Enum):
    INTEGER = "INTEGER"
    TEXT = "TEXT"
    BOOLEAN = "BOOLEAN"
    DATETIME = "DATETIME"
    JSON = "JSON"

@dataclass
class Column:
    name: str
    type: ColumnType
    nullable: bool = True
    primary_key: bool = False

@dataclass
class Table:
    name: str
    columns: List[Column]

@dataclass
class QueryResult:
    rows: List[Dict[str, Any]]
    row_count: int

class DatabaseProtocol(Protocol):
    @property
    def name(self) -> str: ...
    async def connect(self) -> None: ...
    async def execute(self, query: str, params: Optional[Dict] = None) -> QueryResult: ...
    async def fetch_one(self, query: str, params: Optional[Dict] = None) -> Optional[Dict]: ...
    async def fetch_all(self, query: str, params: Optional[Dict] = None) -> List[Dict]: ...
