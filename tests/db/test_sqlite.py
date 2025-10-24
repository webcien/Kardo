"""
Tests for SQLite Adapter
"""

import pytest
import asyncio
from kardocore.db.adapters.sqlite import SQLiteAdapter


@pytest.mark.asyncio
async def test_connect():
    db = SQLiteAdapter(":memory:")
    await db.connect()
    assert db.is_connected
    assert db.name == "sqlite"


@pytest.mark.asyncio
async def test_create_and_query():
    db = SQLiteAdapter(":memory:")
    await db.connect()
    
    # Create table
    await db.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE
        )
    """)
    
    # Insert
    result = await db.execute(
        "INSERT INTO users (name, email) VALUES (:name, :email)",
        {"name": "John", "email": "john@example.com"}
    )
    assert result.row_count == 1
    
    # Fetch one
    user = await db.fetch_one(
        "SELECT * FROM users WHERE email = :email",
        {"email": "john@example.com"}
    )
    assert user is not None
    assert user["name"] == "John"
    assert user["email"] == "john@example.com"
    
    # Fetch all
    users = await db.fetch_all("SELECT * FROM users")
    assert len(users) == 1
