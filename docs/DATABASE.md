# KardoCore Database Module

**Version**: 0.2.0  
**Status**: Production Ready  
**Philosophy**: Fast, Typed, Secure, Modular, Intelligent, Modern

---

## 🎯 Overview

Universal, protocol-based database layer for KardoCore that supports **any database** through a clean, type-safe interface.

### Key Features

- ✅ **Protocol-based** - Any database can be added via plugins
- ✅ **Type-safe** - Full type hints with IDE support
- ✅ **Async-first** - Non-blocking I/O for maximum performance
- ✅ **Secure** - Parameterized queries prevent SQL injection
- ✅ **Zero dependencies** - SQLite works out of the box
- ✅ **Query Builder** - Fluent, chainable API
- ✅ **Multi-database** - Use multiple databases simultaneously

---

## 📦 Installation

```bash
# Core module (included in KardoCore)
pip install kardocore

# Optional: PostgreSQL support
pip install asyncpg

# Optional: MySQL support  
pip install aiomysql
```

---

## 🚀 Quick Start

### Basic Usage

```python
from kardocore.db import Database
from kardocore.db.adapters import SQLiteAdapter

# Create database
db = Database(SQLiteAdapter("app.db"))
await db.connect()

# Execute query
result = await db.execute(
    "INSERT INTO users (name, email) VALUES (:name, :email)",
    {"name": "John", "email": "john@example.com"}
)

# Fetch single row
user = await db.fetch_one(
    "SELECT * FROM users WHERE email = :email",
    {"email": "john@example.com"}
)

# Fetch all rows
users = await db.fetch_all("SELECT * FROM users WHERE active = :active", {"active": True})

# Disconnect
await db.disconnect()
```

### Context Manager

```python
async with Database(SQLiteAdapter("app.db")) as db:
    users = await db.fetch_all("SELECT * FROM users")
    # Auto-disconnect on exit
```

---

## 🔨 Query Builder

Type-safe query construction with method chaining.

### SELECT

```python
query = (
    db.table("users")
    .select("id", "name", "email")
    .where("active", "=", True)
    .where("age", ">=", 18)
    .order_by("created_at", "DESC")
    .limit(10)
    .offset(0)
)

users = await db.fetch_all(query.sql(), query.params())
```

### INSERT

```python
query = db.table("users").insert({
    "name": "Jane",
    "email": "jane@example.com",
    "active": True
})

result = await db.execute(query.sql(), query.params())
```

### UPDATE

```python
query = (
    db.table("users")
    .update({"active": False})
    .where("email", "=", "jane@example.com")
)

result = await db.execute(query.sql(), query.params())
```

### DELETE

```python
query = (
    db.table("users")
    .delete()
    .where("active", "=", False)
)

result = await db.execute(query.sql(), query.params())
```

### Advanced Queries

```python
# WHERE IN
query = db.table("users").select().where_in("id", [1, 2, 3, 4, 5])

# WHERE NULL
query = db.table("users").select().where_null("deleted_at")

# WHERE NOT NULL
query = db.table("users").select().where_not_null("email")

# JOIN
query = (
    db.table("users")
    .select("users.name", "posts.title")
    .join("posts", "users.id", "posts.user_id")
)

# LEFT JOIN
query = (
    db.table("users")
    .select("users.name", "posts.title")
    .left_join("posts", "users.id", "posts.user_id")
)

# GROUP BY
query = (
    db.table("orders")
    .select("user_id", "COUNT(*) as total")
    .group_by("user_id")
)
```

---

## 🗄️ Database Adapters

### SQLite (Built-in)

```python
from kardocore.db.adapters import SQLiteAdapter

# In-memory database
db = Database(SQLiteAdapter(":memory:"))

# File-based database
db = Database(SQLiteAdapter("app.db"))

# Custom path
db = Database(SQLiteAdapter("/var/data/app.db"))
```

**Features**:
- ✅ No external dependencies
- ✅ Perfect for development
- ✅ Async support via aiosqlite
- ✅ Full SQL support

### PostgreSQL

```python
from kardocore.db.adapters import PostgreSQLAdapter

db = Database(PostgreSQLAdapter(
    "postgresql://user:password@localhost:5432/dbname",
    min_size=10,  # Min pool size
    max_size=20   # Max pool size
))
```

**Features**:
- ✅ Connection pooling
- ✅ Prepared statements
- ✅ SSL/TLS support
- ✅ Advanced PostgreSQL features
- ✅ High performance via asyncpg

### Custom Adapter

Create your own adapter by implementing `DatabaseProtocol`:

```python
from kardocore.db.protocols import DatabaseProtocol, QueryResult
from typing import Optional, List, Dict, Any

class MyDatabaseAdapter:
    """Custom database adapter"""
    
    @property
    def name(self) -> str:
        return "mydatabase"
    
    @property
    def is_connected(self) -> bool:
        return self._connected
    
    async def connect(self) -> None:
        # Your connection logic
        pass
    
    async def execute(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> QueryResult:
        # Your execution logic
        pass
    
    async def fetch_one(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        # Your fetch logic
        pass
    
    async def fetch_all(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        # Your fetch all logic
        pass
    
    # Implement other required methods...
```

---

## 🔄 Multi-Database Support

Use multiple databases simultaneously:

```python
from kardocore.db import DatabaseManager
from kardocore.db.adapters import SQLiteAdapter, PostgreSQLAdapter

# Create manager
manager = DatabaseManager()

# Add databases
manager.add("default", SQLiteAdapter("app.db"), is_default=True)
manager.add("analytics", PostgreSQLAdapter("postgresql://localhost/analytics"))
manager.add("cache", SQLiteAdapter(":memory:"))

# Connect all
await manager.connect_all()

# Use specific database
users = await manager.get("default").fetch_all("SELECT * FROM users")
stats = await manager.get("analytics").fetch_all("SELECT * FROM page_views")

# Health check all
health = await manager.health_check_all()
# {'default': True, 'analytics': True, 'cache': True}

# Disconnect all
await manager.disconnect_all()
```

---

## 🔒 Security

### SQL Injection Prevention

All queries use **parameterized queries** by default:

```python
# ✅ SAFE - Parameterized query
user = await db.fetch_one(
    "SELECT * FROM users WHERE email = :email",
    {"email": user_input}
)

# ❌ UNSAFE - String concatenation (DON'T DO THIS)
user = await db.fetch_one(
    f"SELECT * FROM users WHERE email = '{user_input}'"
)
```

The query builder automatically uses parameterized queries:

```python
# ✅ SAFE - Automatic parameterization
query = db.table("users").select().where("email", "=", user_input)
```

### Best Practices

1. **Always use parameterized queries**
2. **Validate input data** before queries
3. **Use transactions** for critical operations
4. **Limit query results** with `.limit()`
5. **Use connection pooling** in production

---

## ⚡ Performance

### Connection Pooling

PostgreSQL adapter includes built-in connection pooling:

```python
db = Database(PostgreSQLAdapter(
    "postgresql://localhost/db",
    min_size=10,  # Keep 10 connections ready
    max_size=50   # Max 50 concurrent connections
))
```

### Transactions

```python
# Begin transaction
await db.begin_transaction()

try:
    # Multiple operations
    await db.execute("INSERT INTO users ...")
    await db.execute("INSERT INTO profiles ...")
    
    # Commit if all succeed
    await db.commit()
except Exception:
    # Rollback on error
    await db.rollback()
    raise
```

### Batch Operations

```python
# Batch insert
users = [
    {"name": "John", "email": "john@example.com"},
    {"name": "Jane", "email": "jane@example.com"},
    # ... more users
]

await db.begin_transaction()
for user in users:
    query = db.table("users").insert(user)
    await db.execute(query.sql(), query.params())
await db.commit()
```

---

## 📊 Examples

### User Management

```python
# Create users table
await db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Insert user
query = db.table("users").insert({
    "name": "John Doe",
    "email": "john@example.com",
    "active": True
})
result = await db.execute(query.sql(), query.params())

# Get user by email
query = db.table("users").select().where("email", "=", "john@example.com")
user = await db.fetch_one(query.sql(), query.params())

# Update user
query = (
    db.table("users")
    .update({"name": "John Smith"})
    .where("email", "=", "john@example.com")
)
await db.execute(query.sql(), query.params())

# Delete inactive users
query = db.table("users").delete().where("active", "=", False)
await db.execute(query.sql(), query.params())

# Get active users, ordered by creation date
query = (
    db.table("users")
    .select()
    .where("active", "=", True)
    .order_by("created_at", "DESC")
    .limit(10)
)
users = await db.fetch_all(query.sql(), query.params())
```

### Blog Posts with Pagination

```python
# Get posts with pagination
page = 1
per_page = 10
offset = (page - 1) * per_page

query = (
    db.table("posts")
    .select("id", "title", "created_at")
    .where("published", "=", True)
    .order_by("created_at", "DESC")
    .limit(per_page)
    .offset(offset)
)

posts = await db.fetch_all(query.sql(), query.params())
```

### Analytics

```python
# Count users by status
query = (
    db.table("users")
    .select("active", "COUNT(*) as count")
    .group_by("active")
)
stats = await db.fetch_all(query.sql(), query.params())
# [{'active': True, 'count': 150}, {'active': False, 'count': 25}]
```

---

## 🧪 Testing

```python
import pytest
from kardocore.db import Database
from kardocore.db.adapters import SQLiteAdapter

@pytest.mark.asyncio
async def test_database():
    # Use in-memory database for tests
    async with Database(SQLiteAdapter(":memory:")) as db:
        # Create table
        await db.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """)
        
        # Insert
        query = db.table("users").insert({"name": "Test User"})
        await db.execute(query.sql(), query.params())
        
        # Fetch
        query = db.table("users").select()
        users = await db.fetch_all(query.sql(), query.params())
        
        assert len(users) == 1
        assert users[0]["name"] == "Test User"
```

---

## 📚 API Reference

### Database Class

- `Database(adapter: DatabaseProtocol)` - Create database instance
- `await db.connect()` - Connect to database
- `await db.disconnect()` - Disconnect from database
- `await db.execute(query, params)` - Execute query
- `await db.fetch_one(query, params)` - Fetch single row
- `await db.fetch_all(query, params)` - Fetch all rows
- `db.table(name)` - Get query builder for table
- `await db.begin_transaction()` - Begin transaction
- `await db.commit()` - Commit transaction
- `await db.rollback()` - Rollback transaction
- `await db.health_check()` - Check database health

### QueryBuilder Class

- `QueryBuilder(table)` - Create query builder
- `.select(*columns)` - Select columns
- `.insert(values)` - Insert values
- `.update(values)` - Update values
- `.delete()` - Delete query
- `.where(column, operator, value)` - Add WHERE clause
- `.where_in(column, values)` - WHERE IN clause
- `.where_null(column)` - WHERE NULL clause
- `.where_not_null(column)` - WHERE NOT NULL clause
- `.join(table, on_left, on_right, type)` - Add JOIN
- `.left_join(table, on_left, on_right)` - Add LEFT JOIN
- `.order_by(column, direction)` - Add ORDER BY
- `.group_by(*columns)` - Add GROUP BY
- `.limit(limit)` - Add LIMIT
- `.offset(offset)` - Add OFFSET
- `.sql()` - Generate SQL query
- `.params()` - Get query parameters

---

## 🎯 Roadmap

- ✅ SQLite adapter
- ✅ PostgreSQL adapter
- ✅ Query Builder
- ✅ Connection Manager
- ⏳ MySQL adapter
- ⏳ MongoDB adapter
- ⏳ Migration system
- ⏳ ORM layer
- ⏳ Query caching
- ⏳ Replication support

---

## 🤝 Contributing

Contributions are welcome! To add a new database adapter:

1. Implement `DatabaseProtocol`
2. Add tests
3. Update documentation
4. Submit pull request

---

## 📄 License

MIT License - See LICENSE file for details

---

**KardoCore Database Module** - Fast, Typed, Secure, Modular, Intelligent, Modern

