# KardoCore Migrations Documentation

Complete guide to the **database migration system** in KardoCore.

---

## Overview

KardoCore provides a powerful migration system for managing database schema changes:

- **Version Control** - Track schema changes over time
- **Up/Down Migrations** - Apply and rollback changes
- **Transaction Support** - Atomic migrations
- **Auto-generation** - Create migration files from templates
- **Status Tracking** - See which migrations are applied
- **CLI Integration** - Manage migrations with `kardo migrate`

---

## Quick Start

### 1. Create a Migration

```bash
kardo migrate create "add users table"
```

This creates a new migration file in `migrations/` directory:

```
migrations/20250124120000_add_users_table.py
```

### 2. Edit the Migration

```python
from kardocore.db.migrations.base import Migration
from kardocore.db import Database


class AddUsersTableMigration(Migration):
    version = "20250124120000"
    description = "add users table"
    
    async def up(self, db: Database):
        """Apply migration"""
        await db.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
    
    async def down(self, db: Database):
        """Rollback migration"""
        await db.execute("DROP TABLE IF EXISTS users")
```

### 3. Apply the Migration

```bash
kardo migrate up
```

### 4. Check Status

```bash
kardo migrate status
```

---

## Migration Files

### File Structure

Migration files are Python modules with a specific structure:

```python
from kardocore.db.migrations.base import Migration
from kardocore.db import Database


class MyMigration(Migration):
    """Migration description"""
    
    # Required: Version (timestamp)
    version = "20250124120000"
    
    # Required: Description
    description = "My migration"
    
    # Required: Apply migration
    async def up(self, db: Database):
        """Apply migration"""
        pass
    
    # Required: Rollback migration
    async def down(self, db: Database):
        """Rollback migration"""
        pass
```

### File Naming

Migration files follow this naming convention:

```
{version}_{description}.py
```

Example:

```
20250124120000_add_users_table.py
20250124130000_add_posts_table.py
20250124140000_add_comments_table.py
```

The version is a timestamp in format `YYYYMMDDHHmmss`.

---

## CLI Commands

### `kardo migrate create` - Create Migration

Create a new migration file:

```bash
kardo migrate create "migration description"
```

**Examples:**

```bash
# Create users table
kardo migrate create "add users table"

# Add column
kardo migrate create "add email column to users"

# Create index
kardo migrate create "add index on users email"
```

**Output:**

```
✅ Migration created: migrations/20250124120000_add_users_table.py

Edit the migration file to implement up() and down() methods
```

---

### `kardo migrate up` - Apply Migrations

Apply pending migrations:

```bash
kardo migrate up [--steps N]
```

**Options:**

- `--steps N` - Apply only N migrations (default: all)

**Examples:**

```bash
# Apply all pending migrations
kardo migrate up

# Apply only next migration
kardo migrate up --steps 1

# Apply next 3 migrations
kardo migrate up --steps 3
```

**Output:**

```
Applying 2 migration(s)...
  Applying 20250124120000: add users table...
  Applying 20250124130000: add posts table...

✅ Applied 2 migration(s) in 0.15s
```

---

### `kardo migrate down` - Rollback Migrations

Rollback applied migrations:

```bash
kardo migrate down [--steps N]
```

**Options:**

- `--steps N` - Rollback N migrations (default: 1)

**Examples:**

```bash
# Rollback last migration
kardo migrate down

# Rollback last 3 migrations
kardo migrate down --steps 3
```

**Output:**

```
Rolling back 1 migration(s)...
  Rolling back 20250124130000: add posts table...

✅ Rolled back 1 migration(s) in 0.08s
```

---

### `kardo migrate status` - Show Status

Show migration status:

```bash
kardo migrate status
```

**Output:**

```
ℹ️  
Migration Status:
  Total: 3
  Applied: 2
  Pending: 1

Migrations:
--------------------------------------------------------------------------------
  [✓] 20250124120000 - add users table
  [✓] 20250124130000 - add posts table
  [ ] 20250124140000 - add comments table
--------------------------------------------------------------------------------
```

---

## Python API

### Using MigrationManager

```python
import asyncio
from kardocore.db import Database
from kardocore.db.adapters import SQLiteAdapter
from kardocore.db.migrations import MigrationManager


async def main():
    # Setup database
    db = Database(SQLiteAdapter("app.db"))
    await db.connect()
    
    # Create migration manager
    manager = MigrationManager(db, "migrations")
    
    # Apply all pending migrations
    count = await manager.migrate_up()
    print(f"Applied {count} migrations")
    
    # Get status
    status = await manager.status()
    print(f"Total: {status['total']}, Applied: {status['applied']}")
    
    # Rollback last migration
    count = await manager.migrate_down(steps=1)
    print(f"Rolled back {count} migrations")
    
    await db.disconnect()


asyncio.run(main())
```

---

## Migration Examples

### Example 1: Create Table

```python
from kardocore.db.migrations.base import Migration
from kardocore.db import Database


class CreateUsersTableMigration(Migration):
    version = "20250124120000"
    description = "create users table"
    
    async def up(self, db: Database):
        await db.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # Create indexes
        await db.execute("CREATE INDEX idx_users_email ON users(email)")
        await db.execute("CREATE INDEX idx_users_username ON users(username)")
    
    async def down(self, db: Database):
        await db.execute("DROP INDEX IF EXISTS idx_users_email")
        await db.execute("DROP INDEX IF EXISTS idx_users_username")
        await db.execute("DROP TABLE IF EXISTS users")
```

---

### Example 2: Add Column

```python
from kardocore.db.migrations.base import Migration
from kardocore.db import Database


class AddEmailVerifiedColumnMigration(Migration):
    version = "20250124130000"
    description = "add email_verified column to users"
    
    async def up(self, db: Database):
        await db.execute("""
            ALTER TABLE users 
            ADD COLUMN email_verified INTEGER NOT NULL DEFAULT 0
        """)
    
    async def down(self, db: Database):
        # SQLite doesn't support DROP COLUMN, so we need to recreate the table
        await db.execute("""
            CREATE TABLE users_new AS 
            SELECT id, email, username, password_hash, role, is_active, created_at, updated_at
            FROM users
        """)
        
        await db.execute("DROP TABLE users")
        await db.execute("ALTER TABLE users_new RENAME TO users")
```

---

### Example 3: Create Index

```python
from kardocore.db.migrations.base import Migration
from kardocore.db import Database


class AddPostsSlugIndexMigration(Migration):
    version = "20250124140000"
    description = "add index on posts slug"
    
    async def up(self, db: Database):
        await db.execute("CREATE INDEX idx_posts_slug ON posts(slug)")
    
    async def down(self, db: Database):
        await db.execute("DROP INDEX IF EXISTS idx_posts_slug")
```

---

### Example 4: Data Migration

```python
from kardocore.db.migrations.base import Migration
from kardocore.db import Database


class MigrateUserRolesMigration(Migration):
    version = "20250124150000"
    description = "migrate user roles to new format"
    
    async def up(self, db: Database):
        # Update old role values to new format
        await db.execute("""
            UPDATE users 
            SET role = 'admin' 
            WHERE role = '1'
        """)
        
        await db.execute("""
            UPDATE users 
            SET role = 'user' 
            WHERE role = '0'
        """)
    
    async def down(self, db: Database):
        # Revert to old format
        await db.execute("""
            UPDATE users 
            SET role = '1' 
            WHERE role = 'admin'
        """)
        
        await db.execute("""
            UPDATE users 
            SET role = '0' 
            WHERE role = 'user'
        """)
```

---

### Example 5: Foreign Key

```python
from kardocore.db.migrations.base import Migration
from kardocore.db import Database


class CreatePostsTableMigration(Migration):
    version = "20250124160000"
    description = "create posts table with foreign key"
    
    async def up(self, db: Database):
        await db.execute("""
            CREATE TABLE posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        await db.execute("CREATE INDEX idx_posts_author ON posts(author_id)")
    
    async def down(self, db: Database):
        await db.execute("DROP INDEX IF EXISTS idx_posts_author")
        await db.execute("DROP TABLE IF EXISTS posts")
```

---

## Best Practices

### 1. **Always Write Down Migrations**

Every `up()` migration should have a corresponding `down()` migration:

```python
async def up(self, db: Database):
    await db.execute("CREATE TABLE users (...)")

async def down(self, db: Database):
    await db.execute("DROP TABLE IF EXISTS users")
```

### 2. **Use Transactions**

Migrations are automatically wrapped in transactions by MigrationManager, but you can also use explicit transactions:

```python
async def up(self, db: Database):
    async with db.transaction():
        await db.execute("CREATE TABLE users (...)")
        await db.execute("CREATE INDEX idx_users_email ON users(email)")
```

### 3. **Test Migrations**

Always test both `up()` and `down()` migrations:

```bash
# Apply migration
kardo migrate up

# Test rollback
kardo migrate down

# Re-apply
kardo migrate up
```

### 4. **Keep Migrations Small**

Create focused migrations that do one thing:

✅ Good:
- `add_users_table`
- `add_email_index`
- `add_posts_table`

❌ Bad:
- `add_all_tables`
- `update_schema`

### 5. **Never Modify Applied Migrations**

Once a migration is applied (especially in production), never modify it. Create a new migration instead.

### 6. **Use Descriptive Names**

Use clear, descriptive names for migrations:

✅ Good:
- `add_email_verified_column_to_users`
- `create_posts_table`
- `add_index_on_users_email`

❌ Bad:
- `update1`
- `fix_db`
- `changes`

### 7. **Handle SQLite Limitations**

SQLite has limitations (e.g., no DROP COLUMN). Handle them properly:

```python
# Instead of DROP COLUMN, recreate table
async def down(self, db: Database):
    await db.execute("CREATE TABLE users_new AS SELECT id, email FROM users")
    await db.execute("DROP TABLE users")
    await db.execute("ALTER TABLE users_new RENAME TO users")
```

---

## Troubleshooting

### Migration Failed

**Error:**

```
❌ Migration failed: table users already exists
```

**Solution:**

Check if the table already exists. Either:
1. Drop the table manually
2. Modify the migration to use `CREATE TABLE IF NOT EXISTS`
3. Rollback and re-apply

### Rollback Failed

**Error:**

```
❌ Rollback failed: no such table: users
```

**Solution:**

The `down()` migration may be incorrect. Check the migration file and ensure the rollback logic is correct.

### Migration File Not Found

**Error:**

```
❌ Migration file not found for version 20250124120000
```

**Solution:**

Ensure the migration file exists in the `migrations/` directory with the correct naming format.

### Database Not Found

**Error:**

```
❌ Database not found. Make sure you're in a KardoCore project directory.
```

**Solution:**

Run migrations from a KardoCore project directory that contains `app.db`.

---

## Advanced Usage

### Custom Migrations Directory

```python
manager = MigrationManager(db, "custom/migrations/path")
```

### Programmatic Migration Creation

```python
file_path = manager.create_migration("add users table")
print(f"Created: {file_path}")
```

### Get Migration Status

```python
status = await manager.status()

print(f"Total: {status['total']}")
print(f"Applied: {status['applied']}")
print(f"Pending: {status['pending']}")

for migration in status['migrations']:
    print(f"{migration['version']}: {migration['description']} - {'✓' if migration['applied'] else ' '}")
```

---

## See Also

- [Database Documentation](DATABASE.md)
- [CLI Documentation](CLI.md)
- [Authentication Documentation](AUTHENTICATION.md)

---

## Support

- **Documentation**: https://github.com/webcien/Kardo
- **Issues**: https://github.com/webcien/Kardo/issues
- **Discussions**: https://github.com/webcien/Kardo/discussions

