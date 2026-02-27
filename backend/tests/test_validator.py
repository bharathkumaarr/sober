import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.parser import parse_sql
from core.validator import validate_query

SCHEMA = {
    "users": ["id", "name", "email", "created_at"],
    "orders": ["id", "user_id", "total", "status"],
    "products": ["id", "name", "price"],
}


class TestValidQueries:
    def test_valid_select(self):
        r = validate_query(parse_sql("SELECT id, name FROM users"), SCHEMA)
        assert r.valid
        assert r.is_select
        assert r.unknown_tables == []
        assert r.unknown_columns == []

    def test_valid_select_star(self):
        r = validate_query(parse_sql("SELECT * FROM users"), SCHEMA)
        assert r.valid

    def test_valid_join(self):
        r = validate_query(
            parse_sql("SELECT u.id, o.total FROM users u JOIN orders o ON u.id = o.user_id"),
            SCHEMA,
        )
        assert r.valid


class TestUnknownTables:
    def test_unknown_table(self):
        r = validate_query(parse_sql("SELECT id FROM nonexistent_table"), SCHEMA)
        assert not r.valid
        assert "nonexistent_table" in r.unknown_tables

    def test_one_known_one_unknown(self):
        r = validate_query(
            parse_sql("SELECT u.id FROM users u JOIN fake_table f ON u.id = f.id"),
            SCHEMA,
        )
        assert not r.valid
        assert "fake_table" in r.unknown_tables


class TestUnknownColumns:
    def test_unknown_column(self):
        r = validate_query(parse_sql("SELECT nonexistent_column FROM users"), SCHEMA)
        assert not r.valid
        assert "nonexistent_column" in r.unknown_columns

    def test_mixed_known_unknown(self):
        r = validate_query(parse_sql("SELECT id, fake_col FROM users"), SCHEMA)
        assert not r.valid
        assert "fake_col" in r.unknown_columns
        assert "id" not in r.unknown_columns


class TestNonSelectRejection:
    def test_insert_rejected(self):
        r = validate_query(parse_sql("INSERT INTO users (name) VALUES ('test')"), SCHEMA)
        assert not r.valid
        assert not r.is_select

    def test_delete_rejected(self):
        r = validate_query(parse_sql("DELETE FROM users WHERE id = 1"), SCHEMA)
        assert not r.valid
        assert not r.is_select
