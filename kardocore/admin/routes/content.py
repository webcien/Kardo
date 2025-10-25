"""Content management routes"""
from typing import Dict, Any

class ContentRoutes:
    def __init__(self, admin):
        self.admin = admin
        
    async def list(self, content_type: str = "post", page: int = 1) -> Dict[str, Any]:
        """List content"""
        per_page = self.admin.config["items_per_page"]
        offset = (page - 1) * per_page
        
        items = await self.admin.db.query("posts")\
            .select("id", "title", "slug", "status", "created_at")\
            .where("type", "=", content_type)\
            .order_by("created_at", "DESC")\
            .limit(per_page)\
            .offset(offset)\
            .fetch_all()
            
        return {
            "template": "content/list.html",
            "context": {"items": items, "type": content_type, "page": page}
        }
        
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create content"""
        await self.admin.db.query("posts").insert(data)
        return {"success": True}
        
    async def update(self, post_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update content"""
        await self.admin.db.query("posts")\
            .where("id", "=", post_id)\
            .update(data)
        return {"success": True}
        
    async def delete(self, post_id: int) -> Dict[str, Any]:
        """Delete content"""
        await self.admin.db.query("posts")\
            .where("id", "=", post_id)\
            .delete()
        return {"success": True}
