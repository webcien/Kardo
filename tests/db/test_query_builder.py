"""
Tests for Query Builder
"""

import pytest
from kardocore.db.query.builder import QueryBuilder


def test_select_all():
    query = QueryBuilder("users").select()
    assert query.sql() == "SELECT * FROM users"
    assert query.params() == {}


def test_select_columns():
    query = QueryBuilder("users").select("id", "name", "email")
    assert query.sql() == "SELECT id, name, email FROM users"


def test_where():
    query = QueryBuilder("users").select().where("active", "=", True)
    assert "WHERE active = :where_0" in query.sql()
    assert query.params() == {"where_0": True}


def test_multiple_where():
    query = (
        QueryBuilder("users")
        .select()
        .where("active", "=", True)
        .where("age", ">", 18)
    )
    sql = query.sql()
    assert "WHERE active = :where_0 AND age > :where_1" in sql
    assert query.params() == {"where_0": True, "where_1": 18}


def test_where_in():
    query = QueryBuilder("users").select().where_in("id", [1, 2, 3])
    sql = query.sql()
    assert "WHERE id IN (:where_0_0, :where_0_1, :where_0_2)" in sql
    params = query.params()
    assert params == {"where_0_0": 1, "where_0_1": 2, "where_0_2": 3}


def test_order_by():
    query = QueryBuilder("users").select().order_by("created_at", "DESC")
    assert "ORDER BY created_at DESC" in query.sql()


def test_limit():
    query = QueryBuilder("users").select().limit(10)
    assert "LIMIT 10" in query.sql()


def test_offset():
    query = QueryBuilder("users").select().limit(10).offset(20)
    sql = query.sql()
    assert "LIMIT 10" in sql
    assert "OFFSET 20" in sql


def test_insert():
    query = QueryBuilder("users").insert({"name": "John", "email": "john@example.com"})
    sql = query.sql()
    assert "INSERT INTO users" in sql
    assert "name, email" in sql or "email, name" in sql
    params = query.params()
    assert params["name"] == "John"
    assert params["email"] == "john@example.com"


def test_update():
    query = (
        QueryBuilder("users")
        .update({"active": False})
        .where("email", "=", "john@example.com")
    )
    sql = query.sql()
    assert "UPDATE users SET active = :active" in sql
    assert "WHERE email = :where_0" in sql
    params = query.params()
    assert params["active"] == False
    assert params["where_0"] == "john@example.com"


def test_delete():
    query = QueryBuilder("users").delete().where("active", "=", False)
    sql = query.sql()
    assert "DELETE FROM users" in sql
    assert "WHERE active = :where_0" in sql


def test_complex_query():
    query = (
        QueryBuilder("users")
        .select("id", "name", "email")
        .where("active", "=", True)
        .where("age", ">=", 18)
        .order_by("created_at", "DESC")
        .limit(10)
        .offset(0)
    )
    sql = query.sql()
    assert "SELECT id, name, email FROM users" in sql
    assert "WHERE active = :where_0 AND age >= :where_1" in sql
    assert "ORDER BY created_at DESC" in sql
    assert "LIMIT 10" in sql
    assert "OFFSET 0" in sql
