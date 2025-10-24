"""
Tests for Database class
"""

import pytest
from kardocore.db import Database
from kardocore.db.adapters.sqlite import SQLiteAdapter


@pytest.mark.asyncio
async def test_database_context_manager():
    async with Database(SQLiteAdapter(":memory:")) as db:
        assert db.is_connected
        assert db.name == "sqlite"


@pytest.mark.asyncio
async def test_database_query_builder():
    db = Database(SQLiteAdapter(":memory:"))
    await db.connect()
    
    # Create table
    await db.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            active BOOLEAN
        )
    """)
    
    # Insert using query builder
    query = db.table("users").insert({"name": "John", "active": True})
    await db.execute(query.sql(), query.params())
    
    # Select using query builder
    query = db.table("users").select().where("active", "=", True)
    users = await db.fetch_all(query.sql(), query.params())
    
    assert len(users) == 1
    assert users[0]["name"] == "John"
    
    await db.disconnect()
