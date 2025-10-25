"""User management routes"""
from typing import Dict, Any, List, Optional

class UserRoutes:
    def __init__(self, admin):
        self.admin = admin
        
    async def list(self, page: int = 1) -> Dict[str, Any]:
        """List users"""
        per_page = self.admin.config["items_per_page"]
        offset = (page - 1) * per_page
        
        users = await self.admin.db.query("users")\
            .select("id", "email", "name", "role", "created_at")\
            .limit(per_page)\
            .offset(offset)\
            .fetch_all()
            
        return {
            "template": "users/list.html",
            "context": {"users": users, "page": page}
        }
        
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new user"""
        user = await self.admin.auth.register(
            email=data["email"],
            password=data["password"],
            name=data.get("name"),
            role=data.get("role", "user")
        )
        return {"success": True, "user": user}
        
    async def update(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user"""
        await self.admin.db.query("users")\
            .where("id", "=", user_id)\
            .update(data)
        return {"success": True}
        
    async def delete(self, user_id: int) -> Dict[str, Any]:
        """Delete user"""
        await self.admin.db.query("users")\
            .where("id", "=", user_id)\
            .delete()
        return {"success": True}
