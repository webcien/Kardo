"""
Blog CMS Example Application

Demonstrates KardoCore with Database and Authentication.
"""

import asyncio
from datetime import datetime
from kardocore.db import Database
from kardocore.db.adapters import SQLiteAdapter
from kardocore.auth import Auth, UserRole


class BlogPost:
    """Blog post model"""
    
    def __init__(
        self,
        id=None,
        title="",
        content="",
        author_id=None,
        author_name="",
        published=False,
        created_at=None,
        updated_at=None
    ):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.author_name = author_name
        self.published = published
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author_id": self.author_id,
            "author_name": self.author_name,
            "published": self.published,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class BlogCMS:
    """Main Blog CMS application"""
    
    def __init__(self, db_path="blog.db", secret="change-this-secret-key"):
        self.db = Database(SQLiteAdapter(db_path))
        self.auth = Auth(self.db, secret=secret)
    
    async def setup(self):
        """Initialize database and auth"""
        await self.db.connect()
        await self.auth.setup()
        await self._create_posts_table()
        print("✅ Blog CMS initialized")
    
    async def _create_posts_table(self):
        """Create posts table"""
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                author_name TEXT NOT NULL,
                published BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (author_id) REFERENCES users(id)
            )
        """)
        await self.db.execute("CREATE INDEX IF NOT EXISTS idx_posts_author ON posts(author_id)")
        await self.db.execute("CREATE INDEX IF NOT EXISTS idx_posts_published ON posts(published)")
    
    async def register_user(self, email, username, password, role=UserRole.USER):
        """Register new user"""
        try:
            user = await self.auth.register(email, username, password, role)
            print(f"✅ User registered: {user.username} ({user.role.value})")
            return user
        except ValueError as e:
            print(f"❌ Registration failed: {e}")
            return None
    
    async def login(self, email, password):
        """Login user"""
        try:
            result = await self.auth.login(email, password, ip_address="127.0.0.1")
            print(f"✅ Logged in as: {result['user']['username']}")
            print(f"   Token: {result['token'][:30]}...")
            return result
        except ValueError as e:
            print(f"❌ Login failed: {e}")
            return None
    
    async def create_post(self, token, title, content, published=False):
        """Create new blog post"""
        try:
            # Verify user
            user = await self.auth.verify_token(token)
            
            # Check permission
            if not user.has_permission("write"):
                print("❌ Permission denied: User cannot write posts")
                return None
            
            # Create post
            query = self.db.table("posts").insert({
                "title": title,
                "content": content,
                "author_id": user.id,
                "author_name": user.username,
                "published": published,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            })
            
            result = await self.db.execute(query.sql(), query.params())
            post_id = result.last_insert_id
            
            print(f"✅ Post created: #{post_id} - {title}")
            return post_id
            
        except ValueError as e:
            print(f"❌ Create post failed: {e}")
            return None
    
    async def list_posts(self, published_only=False):
        """List all posts"""
        query = self.db.table("posts").select()
        
        if published_only:
            query = query.where("published", "=", True)
        
        query = query.order_by("created_at", "DESC")
        
        posts = await self.db.fetch_all(query.sql(), query.params())
        
        print(f"\n📝 Posts ({len(posts)}):")
        for post in posts:
            status = "✓" if post["published"] else "✗"
            print(f"  [{status}] #{post['id']} - {post['title']}")
            print(f"      By: {post['author_name']} | {post['created_at']}")
        
        return posts
    
    async def get_post(self, post_id):
        """Get post by ID"""
        query = self.db.table("posts").select().where("id", "=", post_id)
        post = await self.db.fetch_one(query.sql(), query.params())
        
        if post:
            print(f"\n📄 Post #{post['id']}")
            print(f"Title: {post['title']}")
            print(f"Author: {post['author_name']}")
            print(f"Published: {post['published']}")
            print(f"Created: {post['created_at']}")
            print(f"\nContent:\n{post['content']}")
        else:
            print(f"❌ Post #{post_id} not found")
        
        return post
    
    async def update_post(self, token, post_id, title=None, content=None, published=None):
        """Update post"""
        try:
            # Verify user
            user = await self.auth.verify_token(token)
            
            # Get post
            query = self.db.table("posts").select().where("id", "=", post_id)
            post = await self.db.fetch_one(query.sql(), query.params())
            
            if not post:
                print(f"❌ Post #{post_id} not found")
                return False
            
            # Check ownership (unless admin)
            if user.role != UserRole.ADMIN and post["author_id"] != user.id:
                print("❌ Permission denied: You can only edit your own posts")
                return False
            
            # Update post
            updates = {"updated_at": datetime.now().isoformat()}
            if title:
                updates["title"] = title
            if content:
                updates["content"] = content
            if published is not None:
                updates["published"] = published
            
            query = self.db.table("posts").update(updates).where("id", "=", post_id)
            await self.db.execute(query.sql(), query.params())
            
            print(f"✅ Post #{post_id} updated")
            return True
            
        except ValueError as e:
            print(f"❌ Update failed: {e}")
            return False
    
    async def delete_post(self, token, post_id):
        """Delete post"""
        try:
            # Verify user
            user = await self.auth.verify_token(token)
            
            # Get post
            query = self.db.table("posts").select().where("id", "=", post_id)
            post = await self.db.fetch_one(query.sql(), query.params())
            
            if not post:
                print(f"❌ Post #{post_id} not found")
                return False
            
            # Check ownership (unless admin)
            if user.role != UserRole.ADMIN and post["author_id"] != user.id:
                print("❌ Permission denied: You can only delete your own posts")
                return False
            
            # Delete post
            query = self.db.table("posts").delete().where("id", "=", post_id)
            await self.db.execute(query.sql(), query.params())
            
            print(f"✅ Post #{post_id} deleted")
            return True
            
        except ValueError as e:
            print(f"❌ Delete failed: {e}")
            return False
    
    async def close(self):
        """Close database connection"""
        await self.db.disconnect()


async def demo():
    """Run demo"""
    print("=" * 60)
    print("Blog CMS Example - KardoCore Database + Authentication")
    print("=" * 60)
    
    # Initialize
    cms = BlogCMS()
    await cms.setup()
    
    # Register users
    print("\n1. Registering users...")
    admin = await cms.register_user(
        "admin@example.com",
        "admin",
        "AdminPass123!",
        UserRole.ADMIN
    )
    
    author = await cms.register_user(
        "author@example.com",
        "author",
        "AuthorPass123!",
        UserRole.AUTHOR
    )
    
    user = await cms.register_user(
        "user@example.com",
        "user",
        "UserPass123!",
        UserRole.USER
    )
    
    # Login as admin
    print("\n2. Logging in as admin...")
    admin_login = await cms.login("admin@example.com", "AdminPass123!")
    admin_token = admin_login["token"] if admin_login else None
    
    # Login as author
    print("\n3. Logging in as author...")
    author_login = await cms.login("author@example.com", "AuthorPass123!")
    author_token = author_login["token"] if author_login else None
    
    # Create posts
    print("\n4. Creating posts...")
    if admin_token:
        await cms.create_post(
            admin_token,
            "Welcome to Our Blog",
            "This is the first post on our new blog platform!",
            published=True
        )
    
    if author_token:
        await cms.create_post(
            author_token,
            "Getting Started with KardoCore",
            "Learn how to build modern web applications with KardoCore...",
            published=True
        )
        
        await cms.create_post(
            author_token,
            "Draft: Upcoming Features",
            "This is a draft post about upcoming features...",
            published=False
        )
    
    # List posts
    print("\n5. Listing all posts...")
    await cms.list_posts()
    
    # Get specific post
    print("\n6. Getting post #1...")
    await cms.get_post(1)
    
    # Update post
    print("\n7. Updating post #3...")
    if author_token:
        await cms.update_post(
            author_token,
            3,
            title="Upcoming Features in KardoCore",
            published=True
        )
    
    # List published posts only
    print("\n8. Listing published posts...")
    await cms.list_posts(published_only=True)
    
    # Try to delete post as wrong user (should fail)
    print("\n9. Testing permissions (author trying to delete admin's post)...")
    if author_token:
        await cms.delete_post(author_token, 1)
    
    # Delete post as admin (should succeed)
    print("\n10. Deleting post as admin...")
    if admin_token:
        await cms.delete_post(admin_token, 3)
    
    # Final list
    print("\n11. Final post list...")
    await cms.list_posts()
    
    # Close
    await cms.close()
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(demo())
