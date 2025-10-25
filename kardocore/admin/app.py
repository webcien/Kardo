"""
KardoAdmin Application

Main admin panel application class.
"""

from typing import Optional, Dict, Any
from pathlib import Path
import asyncio

from ..auth.manager import AuthManager
from ..db.connection import DatabaseManager
from .routes.dashboard import DashboardRoutes
from .routes.users import UserRoutes
from .routes.content import ContentRoutes
from .routes.settings import SettingsRoutes
from .routes.themes import ThemeRoutes
from .routes.files import FileRoutes


class KardoAdmin:
    """
    KardoAdmin - Administrative Panel
    
    Provides a complete admin interface for managing:
    - Users and permissions
    - Content (posts, pages)
    - System settings
    - Themes
    - Files and media
    """
    
    def __init__(
        self,
        db: DatabaseManager,
        auth: AuthManager,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize KardoAdmin
        
        Args:
            db: Database connection
            auth: Authentication manager
            config: Optional configuration dictionary
        """
        self.db = db
        self.auth = auth
        self.config = config or {}
        
        # Set defaults
        self.config.setdefault("admin_path", "/admin")
        self.config.setdefault("items_per_page", 20)
        self.config.setdefault("upload_dir", "uploads")
        self.config.setdefault("max_upload_size", 10 * 1024 * 1024)  # 10MB
        
        # Initialize routes
        self.dashboard = DashboardRoutes(self)
        self.users = UserRoutes(self)
        self.content = ContentRoutes(self)
        self.settings = SettingsRoutes(self)
        self.themes = ThemeRoutes(self)
        self.files = FileRoutes(self)
        
    def get_template_path(self) -> Path:
        """Get templates directory path"""
        return Path(__file__).parent / "templates"
        
    def get_static_path(self) -> Path:
        """Get static files directory path"""
        return Path(__file__).parent / "static"
        
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get dashboard statistics
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            "users": await self._count_users(),
            "posts": await self._count_posts(),
            "pages": await self._count_pages(),
            "files": await self._count_files(),
        }
        return stats
        
    async def _count_users(self) -> int:
        """Count total users"""
        result = await self.db.fetch_one(
            "SELECT COUNT(*) as count FROM users"
        )
        return result["count"] if result else 0
        
    async def _count_posts(self) -> int:
        """Count total posts"""
        result = await self.db.fetch_one(
            "SELECT COUNT(*) as count FROM posts WHERE type = 'post'"
        )
        return result["count"] if result else 0
        
    async def _count_pages(self) -> int:
        """Count total pages"""
        result = await self.db.fetch_one(
            "SELECT COUNT(*) as count FROM posts WHERE type = 'page'"
        )
        return result["count"] if result else 0
        
    async def _count_files(self) -> int:
        """Count total uploaded files"""
        result = await self.db.fetch_one(
            "SELECT COUNT(*) as count FROM files"
        )
        return result["count"] if result else 0
