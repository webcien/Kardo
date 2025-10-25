"""File management routes"""
from typing import Dict, Any
from pathlib import Path
import os

class FileRoutes:
    def __init__(self, admin):
        self.admin = admin
        self.upload_dir = Path(admin.config["upload_dir"])
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
    async def list(self, page: int = 1) -> Dict[str, Any]:
        """List uploaded files"""
        per_page = self.admin.config["items_per_page"]
        offset = (page - 1) * per_page
        
        files = await self.admin.db.query("files")\
            .select("id", "filename", "size", "mime_type", "created_at")\
            .order_by("created_at", "DESC")\
            .limit(per_page)\
            .offset(offset)\
            .fetch_all()
            
        return {
            "template": "files/list.html",
            "context": {"files": files, "page": page}
        }
        
    async def upload(self, file_data: bytes, filename: str, mime_type: str) -> Dict[str, Any]:
        """Upload file"""
        # Save file
        file_path = self.upload_dir / filename
        file_path.write_bytes(file_data)
        
        # Save to database
        await self.admin.db.query("files").insert({
            "filename": filename,
            "path": str(file_path),
            "size": len(file_data),
            "mime_type": mime_type
        })
        
        return {"success": True, "filename": filename}
        
    async def delete(self, file_id: int) -> Dict[str, Any]:
        """Delete file"""
        # Get file info
        file = await self.admin.db.query("files")\
            .where("id", "=", file_id)\
            .fetch_one()
            
        if file:
            # Delete physical file
            file_path = Path(file["path"])
            if file_path.exists():
                file_path.unlink()
                
            # Delete from database
            await self.admin.db.query("files")\
                .where("id", "=", file_id)\
                .delete()
                
        return {"success": True}
