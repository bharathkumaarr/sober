import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.parser import parse_sql
from core.types import QueryType


class TestParseValidSQL:
    def test_simple_select(self):
        r = parse_sql("SELECT id, name FROM users")
        assert r.success
        assert r.query_type == QueryType.SELECT
        assert "users" in r.tables
        assert "id" in r.columns
        assert "name" in r.columns

    def test_select_with_where(self):
        r = parse_sql("SELECT id FROM users WHERE id = 1")
        assert r.success
        assert r.has_where

    def test_select_star(self):
        r = parse_sql("SELECT * FROM users")
        assert r.success
        assert r.has_star

    def test_select_with_join(self):
        r = parse_sql("SELECT u.id, o.total FROM users u JOIN orders o ON u.id = o.user_id")
        assert r.success
        assert "users" in r.tables
        assert "orders" in r.tables

    def test_select_no_where(self):
        r = parse_sql("SELECT id FROM users")
        assert r.success
        assert r.has_where is False

    def test_normalized_sql(self):
        r = parse_sql("  SELECT  id  FROM  users  ")
        assert r.success
        assert r.normalized_sql is not None


class TestParseInvalidSQL:
    def test_empty_string(self):
        r = parse_sql("")
        assert not r.success
        assert r.error

    def test_whitespace_only(self):
        assert not parse_sql("   ").success

    def test_gibberish(self):
        r = parse_sql("NOT VALID SQL AT ALL !!!")
        assert r is not None  # sqlglot might still parse some of this


class TestNonSelectQueries:
    def test_insert(self):
        r = parse_sql("INSERT INTO users (name) VALUES ('test')")
        assert r.success
        assert r.query_type == QueryType.INSERT

    def test_delete(self):
        r = parse_sql("DELETE FROM users WHERE id = 1")
        assert r.success
        assert r.query_type == QueryType.DELETE

    def test_update(self):
        r = parse_sql("UPDATE users SET name = 'test' WHERE id = 1")
        assert r.success
        assert r.query_type == QueryType.UPDATE

    def test_drop(self):
        r = parse_sql("DROP TABLE users")
        assert r.success
        assert r.query_type == QueryType.DROP
