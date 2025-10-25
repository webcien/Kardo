"""Theme management routes"""
from typing import Dict, Any, List

class ThemeRoutes:
    def __init__(self, admin):
        self.admin = admin
        
    async def list(self) -> Dict[str, Any]:
        """List installed themes"""
        # TODO: Integrate with PackageManager
        themes = []
        return {
            "template": "themes/list.html",
            "context": {"themes": themes}
        }
        
    async def install(self, theme_name: str) -> Dict[str, Any]:
        """Install theme"""
        # TODO: Integrate with PackageManager
        return {"success": True, "message": f"Theme {theme_name} installed"}
        
    async def activate(self, theme_name: str) -> Dict[str, Any]:
        """Activate theme"""
        await self._save_setting("active_theme", theme_name)
        return {"success": True}
        
    async def _save_setting(self, key: str, value: str):
        """Save setting"""
        await self.admin.db.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, value)
        )
