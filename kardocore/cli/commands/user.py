"""
User Command - Manage users
"""

import asyncio
from pathlib import Path
from kardocore.cli.commands.base import BaseCommand
from kardocore.db import Database
from kardocore.db.adapters import SQLiteAdapter
from kardocore.auth import AuthManager, UserRole


class UserCommand(BaseCommand):
    """Manage users"""
    
    name = "user"
    description = "Manage users (create, list, delete, etc.)"
    
    def _add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="subcommand", help="User subcommands")
        
        # Create
        create_parser = subparsers.add_parser("create", help="Create a new user")
        create_parser.add_argument("email", help="User email")
        create_parser.add_argument("username", help="Username")
        create_parser.add_argument("--password", help="Password (will prompt if not provided)")
        create_parser.add_argument("--role", default="user", choices=["admin", "author", "user", "guest"], help="User role")
        
        # List
        list_parser = subparsers.add_parser("list", help="List all users")
        list_parser.add_argument("--role", help="Filter by role")
        
        # Delete
        delete_parser = subparsers.add_parser("delete", help="Delete a user")
        delete_parser.add_argument("email", help="User email")
        
        # Change password
        passwd_parser = subparsers.add_parser("passwd", help="Change user password")
        passwd_parser.add_argument("email", help="User email")
        passwd_parser.add_argument("--password", help="New password (will prompt if not provided)")
    
    async def _get_auth(self):
        """Get auth instance"""
        # Look for database in current directory
        db_path = Path.cwd() / "app.db"
        
        if not db_path.exists():
            raise FileNotFoundError(
                "Database not found. Make sure you're in a KardoCore project directory."
            )
        
        db = Database(SQLiteAdapter(str(db_path)))
        await db.connect()
        
        # TODO: Get secret from config
        from kardocore.auth import UserRepository
        user_repo = UserRepository(db)
        auth = AuthManager(user_repo, secret_key="change-this-secret-key")
        
        return db, auth
    
    async def execute(self, args):
        """Execute user command"""
        parsed = self.parse_args(args)
        
        if not parsed.subcommand:
            self.parser.print_help()
            return 1
        
        try:
            db, auth = await self._get_auth()
        except FileNotFoundError as e:
            self.print_error(str(e))
            return 1
        
        try:
            if parsed.subcommand == "create":
                return await self._create_user(auth, parsed)
            
            elif parsed.subcommand == "list":
                return await self._list_users(db, parsed)
            
            elif parsed.subcommand == "delete":
                return await self._delete_user(auth, parsed)
            
            elif parsed.subcommand == "passwd":
                return await self._change_password(auth, parsed)
        
        finally:
            await db.disconnect()
        
        return 1
    
    async def _create_user(self, auth, parsed):
        """Create new user"""
        import getpass
        
        email = parsed.email
        username = parsed.username
        password = parsed.password
        role_str = parsed.role
        
        # Map role string to UserRole
        role_map = {
            "admin": UserRole.ADMIN,
            "author": UserRole.AUTHOR,
            "user": UserRole.USER,
            "guest": UserRole.GUEST
        }
        role = role_map[role_str]
        
        # Prompt for password if not provided
        if not password:
            password = getpass.getpass("Password: ")
            password_confirm = getpass.getpass("Confirm password: ")
            
            if password != password_confirm:
                self.print_error("Passwords do not match")
                return 1
        
        try:
            user = await auth.register(email, username, password, role)
            self.print_success(f"User created: {user.username} ({user.role.value})")
            self.print_info(f"  ID: {user.id}")
            self.print_info(f"  Email: {user.email}")
            return 0
        except ValueError as e:
            self.print_error(f"Failed to create user: {e}")
            return 1
    
    async def _list_users(self, db, parsed):
        """List users"""
        query = db.table("users").select("id", "email", "username", "role", "is_active")
        
        if parsed.role:
            query = query.where("role", "=", parsed.role)
        
        users = await db.fetch_all(query.sql(), query.params())
        
        if not users:
            self.print_info("No users found")
            return 0
        
        self.print_info(f"\nUsers ({len(users)}):")
        self.print_info("-" * 70)
        self.print_info(f"{'ID':<5} {'Email':<30} {'Username':<20} {'Role':<10} {'Active'}")
        self.print_info("-" * 70)
        
        for user in users:
            active = "✓" if user["is_active"] else "✗"
            print(f"{user['id']:<5} {user['email']:<30} {user['username']:<20} {user['role']:<10} {active}")
        
        return 0
    
    async def _delete_user(self, auth, parsed):
        """Delete user"""
        email = parsed.email
        
        # Find user
        user = await auth.users.find_by_email(email)
        
        if not user:
            self.print_error(f"User not found: {email}")
            return 1
        
        # Confirm deletion
        import sys
        print(f"⚠️  Are you sure you want to delete user '{user.username}' ({email})? [y/N] ", end="")
        confirm = input().lower()
        
        if confirm != "y":
            self.print_info("Deletion cancelled")
            return 0
        
        # Delete user
        await auth.users.delete(user.id)
        self.print_success(f"User deleted: {email}")
        return 0
    
    async def _change_password(self, auth, parsed):
        """Change user password"""
        import getpass
        
        email = parsed.email
        new_password = parsed.password
        
        # Find user
        user = await auth.users.find_by_email(email)
        
        if not user:
            self.print_error(f"User not found: {email}")
            return 1
        
        # Prompt for passwords if not provided
        if not new_password:
            old_password = getpass.getpass("Current password: ")
            new_password = getpass.getpass("New password: ")
            password_confirm = getpass.getpass("Confirm new password: ")
            
            if new_password != password_confirm:
                self.print_error("Passwords do not match")
                return 1
        else:
            old_password = getpass.getpass("Current password: ")
        
        try:
            await auth.change_password(user.id, old_password, new_password)
            self.print_success(f"Password changed for: {email}")
            return 0
        except ValueError as e:
            self.print_error(f"Failed to change password: {e}")
            return 1
