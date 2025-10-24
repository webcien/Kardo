"""
Migration Manager

Manages database migrations: apply, rollback, status tracking.
"""

import os
import importlib.util
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from kardocore.db import Database
from kardocore.db.migrations.base import Migration


class MigrationManager:
    """Manage database migrations"""
    
    def __init__(self, db: Database, migrations_dir: str = "migrations"):
        self.db = db
        self.migrations_dir = Path(migrations_dir)
        self.migrations_table = "schema_migrations"
    
    async def setup(self):
        """Setup migrations table"""
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.migrations_table} (
            version TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            applied_at TEXT NOT NULL,
            execution_time_ms INTEGER
        )
        """
        await self.db.execute(sql)
    
    async def get_applied_migrations(self) -> List[str]:
        """Get list of applied migration versions"""
        await self.setup()
        
        query = self.db.table(self.migrations_table).select("version").order_by("version")
        results = await self.db.fetch_all(query.sql(), query.params())
        
        return [row["version"] for row in results]
    
    async def get_pending_migrations(self) -> List[Path]:
        """Get list of pending migration files"""
        if not self.migrations_dir.exists():
            return []
        
        applied = await self.get_applied_migrations()
        
        # Find all migration files
        migration_files = sorted(self.migrations_dir.glob("*.py"))
        migration_files = [f for f in migration_files if not f.name.startswith("_")]
        
        # Filter out applied migrations
        pending = []
        for file in migration_files:
            version = file.stem.split("_")[0]
            if version not in applied:
                pending.append(file)
        
        return pending
    
    def load_migration(self, file_path: Path) -> Migration:
        """Load migration from file"""
        spec = importlib.util.spec_from_file_location("migration", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find Migration class in module
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and 
                issubclass(attr, Migration) and 
                attr is not Migration):
                return attr()
        
        raise ValueError(f"No Migration class found in {file_path}")
    
    async def apply_migration(self, file_path: Path) -> float:
        """Apply a single migration"""
        migration = self.load_migration(file_path)
        
        print(f"  Applying {migration.version}: {migration.description}...")
        
        start_time = datetime.now()
        
        # Run migration in transaction
        async with self.db.transaction():
            await migration.up(self.db)
            
            # Record migration
            await self.db.execute(
                f"""
                INSERT INTO {self.migrations_table} 
                (version, description, applied_at, execution_time_ms)
                VALUES (?, ?, ?, ?)
                """,
                (
                    migration.version,
                    migration.description,
                    datetime.now().isoformat(),
                    int((datetime.now() - start_time).total_seconds() * 1000)
                )
            )
        
        execution_time = (datetime.now() - start_time).total_seconds()
        return execution_time
    
    async def rollback_migration(self, version: str) -> float:
        """Rollback a single migration"""
        # Find migration file
        migration_files = list(self.migrations_dir.glob(f"{version}_*.py"))
        
        if not migration_files:
            raise ValueError(f"Migration file not found for version {version}")
        
        migration = self.load_migration(migration_files[0])
        
        print(f"  Rolling back {migration.version}: {migration.description}...")
        
        start_time = datetime.now()
        
        # Run rollback in transaction
        async with self.db.transaction():
            await migration.down(self.db)
            
            # Remove migration record
            await self.db.execute(
                f"DELETE FROM {self.migrations_table} WHERE version = ?",
                (version,)
            )
        
        execution_time = (datetime.now() - start_time).total_seconds()
        return execution_time
    
    async def migrate_up(self, steps: Optional[int] = None) -> int:
        """Apply pending migrations"""
        await self.setup()
        
        pending = await self.get_pending_migrations()
        
        if not pending:
            print("✅ No pending migrations")
            return 0
        
        if steps:
            pending = pending[:steps]
        
        print(f"\nApplying {len(pending)} migration(s)...")
        
        total_time = 0.0
        for file_path in pending:
            execution_time = await self.apply_migration(file_path)
            total_time += execution_time
        
        print(f"\n✅ Applied {len(pending)} migration(s) in {total_time:.2f}s")
        return len(pending)
    
    async def migrate_down(self, steps: int = 1) -> int:
        """Rollback migrations"""
        await self.setup()
        
        applied = await self.get_applied_migrations()
        
        if not applied:
            print("✅ No migrations to rollback")
            return 0
        
        # Get last N migrations
        to_rollback = list(reversed(applied[-steps:]))
        
        print(f"\nRolling back {len(to_rollback)} migration(s)...")
        
        total_time = 0.0
        for version in to_rollback:
            execution_time = await self.rollback_migration(version)
            total_time += execution_time
        
        print(f"\n✅ Rolled back {len(to_rollback)} migration(s) in {total_time:.2f}s")
        return len(to_rollback)
    
    async def status(self) -> Dict[str, Any]:
        """Get migration status"""
        await self.setup()
        
        applied = await self.get_applied_migrations()
        pending = await self.get_pending_migrations()
        
        # Get all migration files
        all_files = sorted(self.migrations_dir.glob("*.py")) if self.migrations_dir.exists() else []
        all_files = [f for f in all_files if not f.name.startswith("_")]
        
        migrations_status = []
        
        for file_path in all_files:
            version = file_path.stem.split("_")[0]
            migration = self.load_migration(file_path)
            
            is_applied = version in applied
            
            migrations_status.append({
                "version": version,
                "description": migration.description,
                "applied": is_applied,
                "file": file_path.name
            })
        
        return {
            "total": len(all_files),
            "applied": len(applied),
            "pending": len(pending),
            "migrations": migrations_status
        }
    
    def create_migration(self, description: str) -> Path:
        """Create a new migration file"""
        # Create migrations directory if it doesn't exist
        self.migrations_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate version (timestamp)
        version = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Generate filename
        safe_description = description.lower().replace(" ", "_").replace("-", "_")
        filename = f"{version}_{safe_description}.py"
        file_path = self.migrations_dir / filename
        
        # Create migration template
        template = f'''"""
Migration: {description}

Created: {datetime.now().isoformat()}
"""

from kardocore.db.migrations.base import Migration
from kardocore.db import Database


class {self._to_class_name(description)}Migration(Migration):
    """Migration: {description}"""
    
    version = "{version}"
    description = "{description}"
    
    async def up(self, db: Database):
        """Apply migration"""
        # TODO: Implement migration
        # Example:
        # await db.execute("""
        #     CREATE TABLE example (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         name TEXT NOT NULL,
        #         created_at TEXT NOT NULL
        #     )
        # """)
        pass
    
    async def down(self, db: Database):
        """Rollback migration"""
        # TODO: Implement rollback
        # Example:
        # await db.execute("DROP TABLE IF EXISTS example")
        pass
'''
        
        file_path.write_text(template)
        
        return file_path
    
    def _to_class_name(self, description: str) -> str:
        """Convert description to class name"""
        words = description.replace("_", " ").replace("-", " ").split()
        return "".join(word.capitalize() for word in words)
