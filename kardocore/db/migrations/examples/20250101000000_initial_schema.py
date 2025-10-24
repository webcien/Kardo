"""
Migration: Initial Schema

Created: 2025-01-01T00:00:00
"""

from kardocore.db.migrations.base import Migration
from kardocore.db import Database


class InitialSchemaMigration(Migration):
    """Create initial database schema"""
    
    version = "20250101000000"
    description = "Initial schema"
    
    async def up(self, db: Database):
        """Create users table"""
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
        
        # Create index
        await db.execute("""
            CREATE INDEX idx_users_email ON users(email)
        """)
    
    async def down(self, db: Database):
        """Drop users table"""
        await db.execute("DROP INDEX IF EXISTS idx_users_email")
        await db.execute("DROP TABLE IF EXISTS users")
