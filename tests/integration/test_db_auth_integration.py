"""
Integration tests for Database + Authentication modules.

Tests the interaction between kardocore.db and kardocore.auth.
"""

import pytest
import asyncio
from datetime import datetime
from kardocore.db import Database
from kardocore.db.adapters import SQLiteAdapter
from kardocore.auth import Auth, UserRole


@pytest.fixture
async def db():
    """Create test database"""
    database = Database(SQLiteAdapter(":memory:"))
    await database.connect()
    yield database
    await database.disconnect()


@pytest.fixture
async def auth(db):
    """Create auth instance"""
    auth_instance = Auth(db, secret="test-secret-key")
    await auth_instance.setup()
    return auth_instance


@pytest.mark.asyncio
async def test_user_registration_and_login(auth):
    """Test complete user registration and login flow"""
    # Register user
    user = await auth.register(
        email="test@example.com",
        username="testuser",
        password="TestPass123!",
        role=UserRole.USER
    )
    
    assert user is not None
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.role == UserRole.USER
    assert user.is_active is True
    assert user.is_verified is False
    
    # Login
    result = await auth.login(
        email="test@example.com",
        password="TestPass123!",
        ip_address="127.0.0.1"
    )
    
    assert result is not None
    assert "token" in result
    assert "session_id" in result
    assert "user" in result
    assert result["user"]["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_token_verification(auth):
    """Test JWT token verification"""
    # Register and login
    await auth.register("test@example.com", "testuser", "TestPass123!")
    result = await auth.login("test@example.com", "TestPass123!")
    
    token = result["token"]
    
    # Verify token
    user = await auth.verify_token(token)
    
    assert user is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"


@pytest.mark.asyncio
async def test_session_management(auth):
    """Test session creation and retrieval"""
    # Register and login
    await auth.register("test@example.com", "testuser", "TestPass123!")
    result = await auth.login("test@example.com", "TestPass123!")
    
    session_id = result["session_id"]
    
    # Get session
    session = await auth.sessions.get(session_id)
    
    assert session is not None
    assert session.user_id == result["user"]["id"]
    assert session.ip_address == "127.0.0.1"
    
    # Logout
    await auth.logout(session_id)
    
    # Session should be gone
    session = await auth.sessions.get(session_id)
    assert session is None


@pytest.mark.asyncio
async def test_role_based_permissions(auth):
    """Test role-based access control"""
    # Register users with different roles
    admin = await auth.register(
        "admin@example.com",
        "admin",
        "AdminPass123!",
        UserRole.ADMIN
    )
    
    author = await auth.register(
        "author@example.com",
        "author",
        "AuthorPass123!",
        UserRole.AUTHOR
    )
    
    user = await auth.register(
        "user@example.com",
        "user",
        "UserPass123!",
        UserRole.USER
    )
    
    # Check permissions
    assert admin.has_permission("write") is True
    assert admin.has_permission("delete") is True
    assert admin.has_permission("anything") is True  # Admin has all
    
    assert author.has_permission("write") is True
    assert author.has_permission("read") is True
    
    assert user.has_permission("read") is True
    assert user.has_permission("write") is False


@pytest.mark.asyncio
async def test_password_change(auth):
    """Test password change functionality"""
    # Register user
    user = await auth.register("test@example.com", "testuser", "OldPass123!")
    
    # Login with old password
    result = await auth.login("test@example.com", "OldPass123!")
    assert result is not None
    
    # Change password
    await auth.change_password(user.id, "OldPass123!", "NewPass456!")
    
    # Old password should not work
    with pytest.raises(ValueError):
        await auth.login("test@example.com", "OldPass123!")
    
    # New password should work
    result = await auth.login("test@example.com", "NewPass456!")
    assert result is not None


@pytest.mark.asyncio
async def test_rate_limiting(auth):
    """Test rate limiting on login attempts"""
    # Register user
    await auth.register("test@example.com", "testuser", "TestPass123!")
    
    # Make multiple failed login attempts
    for i in range(5):
        try:
            await auth.login("test@example.com", "WrongPassword!", ip_address="192.168.1.1")
        except ValueError:
            pass
    
    # Next attempt should be rate limited
    with pytest.raises(ValueError) as exc_info:
        await auth.login("test@example.com", "TestPass123!", ip_address="192.168.1.1")
    
    assert "Too many login attempts" in str(exc_info.value)


@pytest.mark.asyncio
async def test_database_query_builder_with_auth(db, auth):
    """Test database query builder with authentication data"""
    # Register users
    await auth.register("user1@example.com", "user1", "Pass123!")
    await auth.register("user2@example.com", "user2", "Pass123!")
    await auth.register("user3@example.com", "user3", "Pass123!")
    
    # Query users using query builder
    query = db.table("users").select("email", "username").where("is_active", "=", True)
    users = await db.fetch_all(query.sql(), query.params())
    
    assert len(users) == 3
    assert all("email" in user for user in users)
    assert all("username" in user for user in users)
    
    # Query specific user
    query = db.table("users").select().where("email", "=", "user2@example.com")
    user = await db.fetch_one(query.sql(), query.params())
    
    assert user is not None
    assert user["username"] == "user2"


@pytest.mark.asyncio
async def test_transaction_with_user_creation(db, auth):
    """Test database transactions with user creation"""
    # Begin transaction
    await db.begin_transaction()
    
    try:
        # Register user
        user = await auth.register("test@example.com", "testuser", "TestPass123!")
        
        # Create related data (e.g., profile)
        query = db.table("users").update({"is_verified": True}).where("id", "=", user.id)
        await db.execute(query.sql(), query.params())
        
        # Commit
        await db.commit()
        
        # Verify user is verified
        updated_user = await auth.users.find_by_id(user.id)
        assert updated_user.is_verified is True
        
    except Exception as e:
        await db.rollback()
        raise e


@pytest.mark.asyncio
async def test_concurrent_user_operations(auth):
    """Test concurrent user operations"""
    # Create multiple users concurrently
    tasks = [
        auth.register(f"user{i}@example.com", f"user{i}", "Pass123!")
        for i in range(10)
    ]
    
    users = await asyncio.gather(*tasks)
    
    assert len(users) == 10
    assert all(user.id is not None for user in users)
    
    # Login all users concurrently
    login_tasks = [
        auth.login(f"user{i}@example.com", "Pass123!")
        for i in range(10)
    ]
    
    results = await asyncio.gather(*login_tasks)
    
    assert len(results) == 10
    assert all("token" in result for result in results)


@pytest.mark.asyncio
async def test_user_search_and_filtering(db, auth):
    """Test user search and filtering with query builder"""
    # Register users
    await auth.register("admin@example.com", "admin", "Pass123!", UserRole.ADMIN)
    await auth.register("author1@example.com", "author1", "Pass123!", UserRole.AUTHOR)
    await auth.register("author2@example.com", "author2", "Pass123!", UserRole.AUTHOR)
    await auth.register("user1@example.com", "user1", "Pass123!", UserRole.USER)
    await auth.register("user2@example.com", "user2", "Pass123!", UserRole.USER)
    
    # Find all authors
    query = db.table("users").select().where("role", "=", "author")
    authors = await db.fetch_all(query.sql(), query.params())
    
    assert len(authors) == 2
    
    # Find admin
    query = db.table("users").select().where("role", "=", "admin")
    admins = await db.fetch_all(query.sql(), query.params())
    
    assert len(admins) == 1
    assert admins[0]["username"] == "admin"


@pytest.mark.asyncio
async def test_password_strength_validation(auth):
    """Test password strength validation"""
    # Weak password should fail
    with pytest.raises(ValueError) as exc_info:
        await auth.register("test@example.com", "testuser", "weak")
    
    assert "Weak password" in str(exc_info.value)
    
    # Strong password should succeed
    user = await auth.register("test@example.com", "testuser", "StrongPass123!")
    assert user is not None


@pytest.mark.asyncio
async def test_duplicate_email_prevention(auth):
    """Test duplicate email prevention"""
    # Register first user
    await auth.register("test@example.com", "user1", "Pass123!")
    
    # Try to register with same email
    with pytest.raises(ValueError) as exc_info:
        await auth.register("test@example.com", "user2", "Pass123!")
    
    assert "Email already registered" in str(exc_info.value)


@pytest.mark.asyncio
async def test_duplicate_username_prevention(auth):
    """Test duplicate username prevention"""
    # Register first user
    await auth.register("user1@example.com", "testuser", "Pass123!")
    
    # Try to register with same username
    with pytest.raises(ValueError) as exc_info:
        await auth.register("user2@example.com", "testuser", "Pass123!")
    
    assert "Username already taken" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
