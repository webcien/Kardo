# KardoCore Authentication & Security Module

**Version**: 0.2.0  
**Status**: Production Ready  
**Philosophy**: Secure by default, Fast, Typed, Modular

---

## 🎯 Overview

Complete authentication and security system for KardoCore with industry-standard practices.

### Key Features

- ✅ **User Management** - Complete user CRUD with roles
- ✅ **Password Hashing** - Bcrypt, Argon2, PBKDF2 support
- ✅ **JWT Tokens** - Stateless authentication
- ✅ **Session Management** - Stateful sessions with expiration
- ✅ **CSRF Protection** - Double submit cookie pattern
- ✅ **Rate Limiting** - Brute force protection
- ✅ **Password Validation** - Strength requirements
- ✅ **Role-Based Access** - Admin, Author, User, Guest roles

---

## 📦 Installation

```bash
# Core module (included in KardoCore)
pip install kardocore

# Optional: Bcrypt for password hashing
pip install bcrypt

# Optional: Argon2 for maximum security
pip install argon2-cffi
```

---

## 🚀 Quick Start

### Basic Setup

```python
from kardocore.auth import Auth
from kardocore.db import Database
from kardocore.db.adapters import SQLiteAdapter

# Create database
db = Database(SQLiteAdapter("app.db"))
await db.connect()

# Create auth instance
auth = Auth(db, secret="your-secret-key-change-this")
await auth.setup()  # Creates tables
```

### Register User

```python
# Register new user
user = await auth.register(
    email="john@example.com",
    username="john",
    password="SecurePass123!"
)

print(f"User created: {user.id}")
```

### Login

```python
# Login user
result = await auth.login(
    email="john@example.com",
    password="SecurePass123!",
    ip_address="192.168.1.1",
    user_agent="Mozilla/5.0..."
)

token = result["token"]
session_id = result["session_id"]
user = result["user"]

print(f"Logged in: {user['username']}")
print(f"Token: {token}")
```

### Verify Token

```python
# Verify JWT token
try:
    user = await auth.verify_token(token)
    print(f"Authenticated as: {user.username}")
except ValueError as e:
    print(f"Authentication failed: {e}")
```

### Logout

```python
# Logout (destroy session)
await auth.logout(session_id)
```

---

## 👤 User Management

### User Model

```python
from kardocore.auth import User, UserRole

user = User(
    email="john@example.com",
    username="john",
    role=UserRole.ADMIN,
    is_active=True,
    is_verified=False
)
```

### User Roles

```python
from kardocore.auth import UserRole

# Available roles
UserRole.ADMIN   # Full access
UserRole.AUTHOR  # Can read, write, edit own content
UserRole.USER    # Can read only
UserRole.GUEST   # No permissions
```

### Check Permissions

```python
if user.has_permission("write"):
    # Allow writing
    pass
```

### User Repository

```python
from kardocore.auth import UserRepository

repo = UserRepository(db)

# Find user
user = await repo.find_by_email("john@example.com")
user = await repo.find_by_username("john")
user = await repo.find_by_id(1)

# Update user
user.is_verified = True
await repo.update(user)

# Delete user
await repo.delete(user.id)
```

---

## 🔐 Password Hashing

### Supported Algorithms

```python
from kardocore.auth import PasswordHasher, HashAlgorithm

# Bcrypt (recommended)
hasher = PasswordHasher(HashAlgorithm.BCRYPT)

# Argon2 (most secure)
hasher = PasswordHasher(HashAlgorithm.ARGON2)

# PBKDF2 (fallback)
hasher = PasswordHasher(HashAlgorithm.PBKDF2)
```

### Hash Password

```python
hashed = hasher.hash("my_password")
```

### Verify Password

```python
is_valid = hasher.verify("my_password", hashed)
```

### Password Strength Validation

```python
is_valid, errors = PasswordHasher.validate_strength(
    "weak",
    min_length=8,
    require_uppercase=True,
    require_lowercase=True,
    require_digit=True,
    require_special=True
)

if not is_valid:
    print("Password errors:", errors)
    # ['Password must be at least 8 characters',
    #  'Password must contain at least one uppercase letter', ...]
```

---

## 🎫 JWT Tokens

### Create Token

```python
from kardocore.auth import JWT

jwt = JWT("your-secret-key")

token = jwt.encode(
    payload={"user_id": 1, "email": "john@example.com"},
    expires_in=3600  # 1 hour
)
```

### Verify Token

```python
payload = jwt.decode(token)
if payload:
    user_id = payload["user_id"]
    print(f"Valid token for user {user_id}")
else:
    print("Invalid or expired token")
```

### Token Claims

Tokens automatically include:
- `iat` - Issued at timestamp
- `exp` - Expiration timestamp
- Custom claims (user_id, email, etc.)

---

## 📝 Session Management

### Create Session

```python
from kardocore.auth import SessionManager

manager = SessionManager(db)
await manager.create_table()

session = await manager.create(
    user_id=1,
    expires_in=86400,  # 24 hours
    ip_address="192.168.1.1",
    user_agent="Mozilla/5.0..."
)

print(f"Session ID: {session.session_id}")
```

### Get Session

```python
session = await manager.get(session_id)
if session:
    print(f"User ID: {session.user_id}")
    print(f"Data: {session.data}")
else:
    print("Session expired or not found")
```

### Update Session Data

```python
await manager.update(session_id, {
    "cart": [1, 2, 3],
    "preferences": {"theme": "dark"}
})
```

### Destroy Session

```python
# Single session
await manager.destroy(session_id)

# All user sessions
await manager.destroy_user_sessions(user_id)

# Cleanup expired sessions
count = await manager.cleanup_expired()
print(f"Removed {count} expired sessions")
```

---

## 🛡️ CSRF Protection

### Generate Token

```python
from kardocore.auth import CSRFProtection

csrf = CSRFProtection("your-secret-key")

# Generate token
token = csrf.generate_token(session_id="abc123")

# Include in form
# <input type="hidden" name="csrf_token" value="{token}">
```

### Validate Token

```python
# From form submission
csrf_token = request.form.get("csrf_token")
is_valid = csrf.validate_token(csrf_token, session_id="abc123")

if not is_valid:
    raise ValueError("CSRF validation failed")
```

---

## ⏱️ Rate Limiting

### Basic Usage

```python
from kardocore.auth import RateLimiter

# 5 attempts per 5 minutes
limiter = RateLimiter(max_attempts=5, window=300)

# Check if allowed
is_allowed, retry_after = limiter.is_allowed("192.168.1.1")

if not is_allowed:
    raise ValueError(f"Rate limited. Retry after {retry_after} seconds")

# Record attempt
limiter.record_attempt("192.168.1.1")
```

### Reset Attempts

```python
# On successful login
limiter.reset("192.168.1.1")
```

---

## 🔒 Security Best Practices

### 1. Secret Key

```python
# ❌ DON'T: Hardcode secrets
auth = Auth(db, secret="my-secret")

# ✅ DO: Use environment variables
import os
auth = Auth(db, secret=os.getenv("SECRET_KEY"))
```

### 2. Password Requirements

```python
# Enforce strong passwords
is_valid, errors = PasswordHasher.validate_strength(
    password,
    min_length=12,  # Longer is better
    require_uppercase=True,
    require_lowercase=True,
    require_digit=True,
    require_special=True
)
```

### 3. Rate Limiting

```python
# Protect login endpoints
auth = Auth(
    db,
    secret=secret,
    max_login_attempts=5,  # Max attempts
    login_window=300  # Per 5 minutes
)
```

### 4. Session Expiration

```python
# Short-lived sessions
auth = Auth(
    db,
    secret=secret,
    jwt_expires_in=3600,  # 1 hour
    session_expires_in=86400  # 24 hours
)
```

### 5. HTTPS Only

```python
# Always use HTTPS in production
# Set secure cookie flags
# session_cookie_secure=True
# session_cookie_httponly=True
# session_cookie_samesite='Lax'
```

---

## 📊 Complete Example

```python
from kardocore.auth import Auth, UserRole
from kardocore.db import Database
from kardocore.db.adapters import SQLiteAdapter

async def main():
    # Setup
    db = Database(SQLiteAdapter("app.db"))
    await db.connect()
    
    auth = Auth(db, secret="your-secret-key")
    await auth.setup()
    
    # Register admin user
    try:
        admin = await auth.register(
            email="admin@example.com",
            username="admin",
            password="AdminPass123!",
            role=UserRole.ADMIN
        )
        print(f"✅ Admin created: {admin.username}")
    except ValueError as e:
        print(f"❌ Registration failed: {e}")
    
    # Login
    try:
        result = await auth.login(
            email="admin@example.com",
            password="AdminPass123!",
            ip_address="127.0.0.1"
        )
        
        token = result["token"]
        session_id = result["session_id"]
        
        print(f"✅ Logged in")
        print(f"   Token: {token[:20]}...")
        print(f"   Session: {session_id[:20]}...")
        
        # Verify token
        user = await auth.verify_token(token)
        print(f"✅ Token valid for: {user.username}")
        
        # Check permissions
        if user.has_permission("write"):
            print("✅ User has write permission")
        
        # Change password
        await auth.change_password(
            user_id=user.id,
            old_password="AdminPass123!",
            new_password="NewAdminPass456!"
        )
        print("✅ Password changed")
        
        # Logout
        await auth.logout(session_id)
        print("✅ Logged out")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
    
    await db.disconnect()

# Run
import asyncio
asyncio.run(main())
```

---

## 🧪 Testing

```python
import pytest
from kardocore.auth import Auth, UserRole
from kardocore.db import Database
from kardocore.db.adapters import SQLiteAdapter

@pytest.mark.asyncio
async def test_auth_flow():
    # Setup
    db = Database(SQLiteAdapter(":memory:"))
    await db.connect()
    
    auth = Auth(db, secret="test-secret")
    await auth.setup()
    
    # Register
    user = await auth.register(
        email="test@example.com",
        username="test",
        password="TestPass123!"
    )
    assert user.id is not None
    
    # Login
    result = await auth.login("test@example.com", "TestPass123!")
    assert "token" in result
    assert "session_id" in result
    
    # Verify token
    verified_user = await auth.verify_token(result["token"])
    assert verified_user.id == user.id
    
    # Logout
    await auth.logout(result["session_id"])
    
    await db.disconnect()
```

---

## 📚 API Reference

### Auth Class

- `Auth(db, secret, jwt_expires_in, session_expires_in, max_login_attempts, login_window)`
- `await auth.setup()` - Create database tables
- `await auth.register(email, username, password, role)` - Register user
- `await auth.login(email, password, ip_address, user_agent)` - Login user
- `await auth.verify_token(token)` - Verify JWT token
- `await auth.logout(session_id)` - Logout user
- `await auth.change_password(user_id, old_password, new_password)` - Change password

### User Model

- `User(email, username, password_hash, role, is_active, is_verified)`
- `user.has_permission(permission)` - Check permission
- `user.to_dict(include_sensitive)` - Convert to dict
- `User.from_dict(data)` - Create from dict

### PasswordHasher

- `PasswordHasher(algorithm)` - Create hasher
- `hasher.hash(password)` - Hash password
- `hasher.verify(password, hashed)` - Verify password
- `PasswordHasher.validate_strength(password, ...)` - Validate strength

### JWT

- `JWT(secret, algorithm)` - Create JWT handler
- `jwt.encode(payload, expires_in)` - Create token
- `jwt.decode(token)` - Verify and decode token

### SessionManager

- `SessionManager(db)` - Create session manager
- `await manager.create(user_id, expires_in, ...)` - Create session
- `await manager.get(session_id)` - Get session
- `await manager.update(session_id, data)` - Update session
- `await manager.destroy(session_id)` - Destroy session

---

## 🎯 Roadmap

- ✅ User management
- ✅ Password hashing
- ✅ JWT tokens
- ✅ Session management
- ✅ CSRF protection
- ✅ Rate limiting
- ⏳ OAuth providers (Google, GitHub, etc.)
- ⏳ Two-factor authentication (2FA)
- ⏳ Email verification
- ⏳ Password reset
- ⏳ Account lockout
- ⏳ Audit logging

---

## 📄 License

MIT License - See LICENSE file for details

---

**KardoCore Authentication Module** - Secure by default, Fast, Typed, Modular

