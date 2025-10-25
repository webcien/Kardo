"""
ORM (Object-Relational Mapping) Layer

Simple ORM for model-database mapping.
"""

from typing import Any, Dict, List, Optional, Type, TypeVar
from dataclasses import dataclass, fields
import inspect


T = TypeVar('T')


@dataclass
class Field:
    """Database field definition"""
    name: str
    type: str
    primary_key: bool = False
    nullable: bool = True
    default: Any = None
    unique: bool = False
    index: bool = False


class Model:
    """
    Base Model Class
    
    Inherit from this to create ORM models.
    """
    
    __table_name__: str = ""
    __primary_key__: str = "id"
    
    def __init_subclass__(cls):
        """Auto-set table name"""
        if not cls.__table_name__:
            cls.__table_name__ = cls.__name__.lower() + 's'
            
    @classmethod
    def get_fields(cls) -> List[Field]:
        """Get model fields"""
        if hasattr(cls, '__dataclass_fields__'):
            return [
                Field(
                    name=f.name,
                    type=f.type.__name__,
                    nullable=f.default is not None
                )
                for f in fields(cls)
            ]
        return []
        
    @classmethod
    async def create(cls: Type[T], db, **kwargs) -> T:
        """
        Create new record
        
        Args:
            db: Database instance
            **kwargs: Field values
            
        Returns:
            Created model instance
        """
        # Build INSERT query
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs])
        query = f"INSERT INTO {cls.__table_name__} ({columns}) VALUES ({placeholders})"
        
        # Execute
        await db.execute(query, tuple(kwargs.values()))
        
        # Return instance
        return cls(**kwargs)
        
    @classmethod
    async def get(cls: Type[T], db, id: Any) -> Optional[T]:
        """
        Get record by ID
        
        Args:
            db: Database instance
            id: Primary key value
            
        Returns:
            Model instance or None
        """
        query = f"SELECT * FROM {cls.__table_name__} WHERE {cls.__primary_key__} = ?"
        result = await db.fetch_one(query, (id,))
        
        if result:
            return cls(**result)
        return None
        
    @classmethod
    async def all(cls: Type[T], db) -> List[T]:
        """
        Get all records
        
        Args:
            db: Database instance
            
        Returns:
            List of model instances
        """
        query = f"SELECT * FROM {cls.__table_name__}"
        results = await db.fetch_all(query)
        
        return [cls(**row) for row in results]
        
    @classmethod
    async def filter(cls: Type[T], db, **kwargs) -> List[T]:
        """
        Filter records
        
        Args:
            db: Database instance
            **kwargs: Filter conditions
            
        Returns:
            List of matching model instances
        """
        conditions = ' AND '.join(f"{k} = ?" for k in kwargs.keys())
        query = f"SELECT * FROM {cls.__table_name__} WHERE {conditions}"
        results = await db.fetch_all(query, tuple(kwargs.values()))
        
        return [cls(**row) for row in results]
        
    async def save(self, db):
        """
        Save (update) record
        
        Args:
            db: Database instance
        """
        # Get all fields except primary key
        data = {
            k: v for k, v in self.__dict__.items()
            if k != self.__primary_key__
        }
        
        # Build UPDATE query
        set_clause = ', '.join(f"{k} = ?" for k in data.keys())
        query = f"""
            UPDATE {self.__table_name__}
            SET {set_clause}
            WHERE {self.__primary_key__} = ?
        """
        
        # Execute
        pk_value = getattr(self, self.__primary_key__)
        await db.execute(query, (*data.values(), pk_value))
        
    async def delete(self, db):
        """
        Delete record
        
        Args:
            db: Database instance
        """
        pk_value = getattr(self, self.__primary_key__)
        query = f"DELETE FROM {self.__table_name__} WHERE {self.__primary_key__} = ?"
        await db.execute(query, (pk_value,))


class QuerySet:
    """
    QuerySet for chaining queries
    
    Similar to Django ORM.
    """
    
    def __init__(self, model: Type[Model], db):
        self.model = model
        self.db = db
        self._filters = []
        self._order_by = []
        self._limit = None
        self._offset = None
        
    def filter(self, **kwargs):
        """Add filter conditions"""
        self._filters.extend(kwargs.items())
        return self
        
    def order_by(self, *fields):
        """Add ordering"""
        self._order_by.extend(fields)
        return self
        
    def limit(self, n: int):
        """Add limit"""
        self._limit = n
        return self
        
    def offset(self, n: int):
        """Add offset"""
        self._offset = n
        return self
        
    async def all(self) -> List[Model]:
        """Execute query and return all results"""
        query = f"SELECT * FROM {self.model.__table_name__}"
        params = []
        
        # Add WHERE clause
        if self._filters:
            conditions = ' AND '.join(f"{k} = ?" for k, v in self._filters)
            query += f" WHERE {conditions}"
            params.extend(v for k, v in self._filters)
            
        # Add ORDER BY
        if self._order_by:
            query += f" ORDER BY {', '.join(self._order_by)}"
            
        # Add LIMIT/OFFSET
        if self._limit:
            query += f" LIMIT {self._limit}"
        if self._offset:
            query += f" OFFSET {self._offset}"
            
        # Execute
        results = await self.db.fetch_all(query, tuple(params))
        return [self.model(**row) for row in results]
        
    async def first(self) -> Optional[Model]:
        """Get first result"""
        self._limit = 1
        results = await self.all()
        return results[0] if results else None
        
    async def count(self) -> int:
        """Count results"""
        query = f"SELECT COUNT(*) as count FROM {self.model.__table_name__}"
        params = []
        
        if self._filters:
            conditions = ' AND '.join(f"{k} = ?" for k, v in self._filters)
            query += f" WHERE {conditions}"
            params.extend(v for k, v in self._filters)
            
        result = await self.db.fetch_one(query, tuple(params))
        return result['count'] if result else 0
