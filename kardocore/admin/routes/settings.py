"""Settings routes"""
from typing import Dict, Any

class SettingsRoutes:
    def __init__(self, admin):
        self.admin = admin
        
    async def index(self) -> Dict[str, Any]:
        """Settings page"""
        settings = await self._get_all_settings()
        return {
            "template": "settings/index.html",
            "context": {"settings": settings}
        }
        
    async def update(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update settings"""
        for key, value in data.items():
            await self._save_setting(key, value)
        return {"success": True}
        
    async def _get_all_settings(self) -> Dict[str, Any]:
        """Get all settings"""
        rows = await self.admin.db.fetch_all("SELECT key, value FROM settings")
        return {row["key"]: row["value"] for row in rows}
        
    async def _save_setting(self, key: str, value: str):
        """Save a setting"""
        await self.admin.db.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, value)
        )
