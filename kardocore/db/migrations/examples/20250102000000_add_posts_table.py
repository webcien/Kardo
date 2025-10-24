"""
Migration: Add Posts Table

Created: 2025-01-02T00:00:00
"""

from kardocore.db.migrations.base import Migration
from kardocore.db import Database


class AddPostsTableMigration(Migration):
    """Add posts table for blog functionality"""
    
    version = "20250102000000"
    description = "Add posts table"
    
    async def up(self, db: Database):
        """Create posts table"""
        await db.execute("""
            CREATE TABLE posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                slug TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                excerpt TEXT,
                author_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'draft',
                published_at TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Create indexes
        await db.execute("CREATE INDEX idx_posts_slug ON posts(slug)")
        await db.execute("CREATE INDEX idx_posts_author ON posts(author_id)")
        await db.execute("CREATE INDEX idx_posts_status ON posts(status)")
    
    async def down(self, db: Database):
        """Drop posts table"""
        await db.execute("DROP INDEX IF EXISTS idx_posts_slug")
        await db.execute("DROP INDEX IF EXISTS idx_posts_author")
        await db.execute("DROP INDEX IF EXISTS idx_posts_status")
        await db.execute("DROP TABLE IF EXISTS posts")
