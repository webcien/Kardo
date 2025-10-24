"""
Migrate Command - Run database migrations
"""

from pathlib import Path
from kardocore.cli.commands.base import BaseCommand
from kardocore.db import Database
from kardocore.db.adapters import SQLiteAdapter
from kardocore.db.migrations import MigrationManager


class MigrateCommand(BaseCommand):
    """Run database migrations"""
    
    name = "migrate"
    description = "Run database migrations"
    
    def _add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="subcommand", help="Migration subcommands")
        
        # Up
        up_parser = subparsers.add_parser("up", help="Run pending migrations")
        up_parser.add_argument("--steps", type=int, help="Number of migrations to apply")
        
        # Down
        down_parser = subparsers.add_parser("down", help="Rollback last migration")
        down_parser.add_argument("--steps", type=int, default=1, help="Number of migrations to rollback")
        
        # Status
        subparsers.add_parser("status", help="Show migration status")
        
        # Create
        create_parser = subparsers.add_parser("create", help="Create a new migration")
        create_parser.add_argument("description", help="Migration description")
    
    async def _get_manager(self):
        """Get migration manager instance"""
        db_path = Path.cwd() / "app.db"
        
        if not db_path.exists():
            raise FileNotFoundError(
                "Database not found. Make sure you're in a KardoCore project directory."
            )
        
        db = Database(SQLiteAdapter(str(db_path)))
        await db.connect()
        
        migrations_dir = Path.cwd() / "migrations"
        manager = MigrationManager(db, str(migrations_dir))
        
        return db, manager
    
    async def execute(self, args):
        """Execute migrate command"""
        parsed = self.parse_args(args)
        
        if not parsed.subcommand:
            self.parser.print_help()
            return 1
        
        if parsed.subcommand == "create":
            return await self._create_migration(parsed)
        
        try:
            db, manager = await self._get_manager()
        except FileNotFoundError as e:
            self.print_error(str(e))
            return 1
        
        try:
            if parsed.subcommand == "up":
                return await self._migrate_up(manager, parsed)
            elif parsed.subcommand == "down":
                return await self._migrate_down(manager, parsed)
            elif parsed.subcommand == "status":
                return await self._show_status(manager)
        finally:
            await db.disconnect()
        
        return 1
    
    async def _migrate_up(self, manager, parsed):
        """Run pending migrations"""
        try:
            count = await manager.migrate_up(steps=parsed.steps)
            if count == 0:
                self.print_info("No pending migrations")
            return 0
        except Exception as e:
            self.print_error(f"Migration failed: {e}")
            return 1
    
    async def _migrate_down(self, manager, parsed):
        """Rollback migrations"""
        try:
            count = await manager.migrate_down(steps=parsed.steps)
            if count == 0:
                self.print_info("No migrations to rollback")
            return 0
        except Exception as e:
            self.print_error(f"Rollback failed: {e}")
            return 1
    
    async def _show_status(self, manager):
        """Show migration status"""
        try:
            status = await manager.status()
            self.print_info(f"\nMigration Status:")
            self.print_info(f"  Total: {status['total']}")
            self.print_info(f"  Applied: {status['applied']}")
            self.print_info(f"  Pending: {status['pending']}")
            
            if status['migrations']:
                self.print_info("\nMigrations:")
                self.print_info("-" * 80)
                for migration in status['migrations']:
                    status_icon = "✓" if migration['applied'] else " "
                    print(f"  [{status_icon}] {migration['version']} - {migration['description']}")
                self.print_info("-" * 80)
            return 0
        except Exception as e:
            self.print_error(f"Failed to get status: {e}")
            return 1
    
    async def _create_migration(self, parsed):
        """Create a new migration"""
        migrations_dir = Path.cwd() / "migrations"
        manager = MigrationManager(None, str(migrations_dir))
        
        try:
            file_path = manager.create_migration(parsed.description)
            self.print_success(f"Migration created: {file_path.relative_to(Path.cwd())}")
            self.print_info(f"\nEdit the migration file to implement up() and down() methods")
            return 0
        except Exception as e:
            self.print_error(f"Failed to create migration: {e}")
            return 1
