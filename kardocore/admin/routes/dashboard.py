"""Dashboard routes"""
from typing import Dict, Any

class DashboardRoutes:
    def __init__(self, admin):
        self.admin = admin
        
    async def index(self) -> Dict[str, Any]:
        """Dashboard home page"""
        stats = await self.admin.get_stats()
        return {
            "template": "dashboard/index.html",
            "context": {"stats": stats}
        }
