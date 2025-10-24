"""
Type-safe query builder for KardoCore.

Philosophy: Fast, Typed, Secure, Modular
"""

from typing import Any, Dict, List, Optional, Union
from enum import Enum


class QueryType(Enum):
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class QueryBuilder:
    """
    Type-safe SQL query builder with method chaining.
    
    Features:
    - SQL injection prevention (parameterized queries)
    - Method chaining for readable code
    - Type-safe operations
    - Support for complex queries
    
    Example:
        query = (
            QueryBuilder("users")
            .select("id", "name", "email")
            .where("active", "=", True)
            .order_by("created_at", "DESC")
            .limit(10)
        )
        
        sql = query.sql()
        params = query.params()
    """
    
    def __init__(self, table: str):
        self.table = table
        self._type = QueryType.SELECT
        self._columns: List[str] = ["*"]
        self._where_clauses: List[tuple] = []
        self._joins: List[str] = []
        self._order_by: List[tuple] = []
        self._group_by: List[str] = []
        self._limit_value: Optional[int] = None
        self._offset_value: Optional[int] = None
        self._values: Dict[str, Any] = {}
        self._param_counter = 0
    
    def select(self, *columns: str) -> "QueryBuilder":
        """Select specific columns"""
        self._type = QueryType.SELECT
        self._columns = list(columns) if columns else ["*"]
        return self
    
    def insert(self, values: Dict[str, Any]) -> "QueryBuilder":
        """Insert values"""
        self._type = QueryType.INSERT
        self._values = values
        return self
    
    def update(self, values: Dict[str, Any]) -> "QueryBuilder":
        """Update values"""
        self._type = QueryType.UPDATE
        self._values = values
        return self
    
    def delete(self) -> "QueryBuilder":
        """Delete query"""
        self._type = QueryType.DELETE
        return self
    
    def where(
        self,
        column: str,
        operator: str,
        value: Any
    ) -> "QueryBuilder":
        """Add WHERE clause"""
        self._where_clauses.append((column, operator, value))
        return self
    
    def where_in(self, column: str, values: List[Any]) -> "QueryBuilder":
        """WHERE column IN (values)"""
        self._where_clauses.append((column, "IN", values))
        return self
    
    def where_null(self, column: str) -> "QueryBuilder":
        """WHERE column IS NULL"""
        self._where_clauses.append((column, "IS NULL", None))
        return self
    
    def where_not_null(self, column: str) -> "QueryBuilder":
        """WHERE column IS NOT NULL"""
        self._where_clauses.append((column, "IS NOT NULL", None))
        return self
    
    def join(
        self,
        table: str,
        on_left: str,
        on_right: str,
        join_type: str = "INNER"
    ) -> "QueryBuilder":
        """Add JOIN clause"""
        self._joins.append(f"{join_type} JOIN {table} ON {on_left} = {on_right}")
        return self
    
    def left_join(self, table: str, on_left: str, on_right: str) -> "QueryBuilder":
        """Add LEFT JOIN"""
        return self.join(table, on_left, on_right, "LEFT")
    
    def order_by(self, column: str, direction: str = "ASC") -> "QueryBuilder":
        """Add ORDER BY clause"""
        self._order_by.append((column, direction.upper()))
        return self
    
    def group_by(self, *columns: str) -> "QueryBuilder":
        """Add GROUP BY clause"""
        self._group_by.extend(columns)
        return self
    
    def limit(self, limit: int) -> "QueryBuilder":
        """Add LIMIT clause"""
        self._limit_value = limit
        return self
    
    def offset(self, offset: int) -> "QueryBuilder":
        """Add OFFSET clause"""
        self._offset_value = offset
        return self
    
    def sql(self) -> str:
        """Generate SQL query"""
        if self._type == QueryType.SELECT:
            return self._build_select()
        elif self._type == QueryType.INSERT:
            return self._build_insert()
        elif self._type == QueryType.UPDATE:
            return self._build_update()
        elif self._type == QueryType.DELETE:
            return self._build_delete()
    
    def params(self) -> Dict[str, Any]:
        """Get query parameters"""
        params = {}
        
        # WHERE clause parameters
        for i, (column, operator, value) in enumerate(self._where_clauses):
            if operator in ("IS NULL", "IS NOT NULL"):
                continue
            elif operator == "IN":
                for j, v in enumerate(value):
                    params[f"where_{i}_{j}"] = v
            else:
                params[f"where_{i}"] = value
        
        # INSERT/UPDATE parameters
        if self._type in (QueryType.INSERT, QueryType.UPDATE):
            for key, value in self._values.items():
                params[key] = value
        
        return params
    
    def _build_select(self) -> str:
        """Build SELECT query"""
        columns = ", ".join(self._columns)
        sql = f"SELECT {columns} FROM {self.table}"
        
        # JOINs
        if self._joins:
            sql += " " + " ".join(self._joins)
        
        # WHERE
        where_sql = self._build_where()
        if where_sql:
            sql += f" WHERE {where_sql}"
        
        # GROUP BY
        if self._group_by:
            sql += f" GROUP BY {', '.join(self._group_by)}"
        
        # ORDER BY
        if self._order_by:
            order_parts = [f"{col} {dir}" for col, dir in self._order_by]
            sql += f" ORDER BY {', '.join(order_parts)}"
        
        # LIMIT
        if self._limit_value is not None:
            sql += f" LIMIT {self._limit_value}"
        
        # OFFSET
        if self._offset_value is not None:
            sql += f" OFFSET {self._offset_value}"
        
        return sql
    
    def _build_insert(self) -> str:
        """Build INSERT query"""
        columns = ", ".join(self._values.keys())
        placeholders = ", ".join(f":{key}" for key in self._values.keys())
        return f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
    
    def _build_update(self) -> str:
        """Build UPDATE query"""
        set_parts = [f"{key} = :{key}" for key in self._values.keys()]
        sql = f"UPDATE {self.table} SET {', '.join(set_parts)}"
        
        where_sql = self._build_where()
        if where_sql:
            sql += f" WHERE {where_sql}"
        
        return sql
    
    def _build_delete(self) -> str:
        """Build DELETE query"""
        sql = f"DELETE FROM {self.table}"
        
        where_sql = self._build_where()
        if where_sql:
            sql += f" WHERE {where_sql}"
        
        return sql
    
    def _build_where(self) -> str:
        """Build WHERE clause"""
        if not self._where_clauses:
            return ""
        
        parts = []
        for i, (column, operator, value) in enumerate(self._where_clauses):
            if operator == "IS NULL":
                parts.append(f"{column} IS NULL")
            elif operator == "IS NOT NULL":
                parts.append(f"{column} IS NOT NULL")
            elif operator == "IN":
                placeholders = ", ".join(f":where_{i}_{j}" for j in range(len(value)))
                parts.append(f"{column} IN ({placeholders})")
            else:
                parts.append(f"{column} {operator} :where_{i}")
        
        return " AND ".join(parts)
    
    def __str__(self) -> str:
        """String representation"""
        return self.sql()
