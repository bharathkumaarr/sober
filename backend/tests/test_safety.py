import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.parser import parse_sql
from core.safety_rules import check_safety


class TestBlockedQueries:
    def test_delete_blocked(self):
        r = check_safety(parse_sql("DELETE FROM users WHERE id = 1"))
        assert not r.safe
        assert r.block_reason
        assert "SELECT" in r.block_reason

    def test_insert_blocked(self):
        r = check_safety(parse_sql("INSERT INTO users (name) VALUES ('x')"))
        assert not r.safe
        assert r.block_reason

    def test_update_blocked(self):
        r = check_safety(parse_sql("UPDATE users SET name = 'x' WHERE id = 1"))
        assert not r.safe

    def test_drop_blocked(self):
        r = check_safety(parse_sql("DROP TABLE users"))
        assert not r.safe


class TestWarnings:
    def test_select_star_warning(self):
        r = check_safety(parse_sql("SELECT * FROM users"))
        assert r.safe
        assert any("SELECT *" in w for w in r.warnings)

    def test_full_table_scan_warning(self):
        r = check_safety(parse_sql("SELECT id FROM users"))
        assert r.safe
        assert any("WHERE" in w for w in r.warnings)

    def test_select_star_and_no_where(self):
        r = check_safety(parse_sql("SELECT * FROM users"))
        assert r.safe
        assert len(r.warnings) >= 2  # should get both warnings

    def test_no_warnings_with_where(self):
        r = check_safety(parse_sql("SELECT id, name FROM users WHERE id = 1"))
        assert r.safe
        assert len(r.warnings) == 0


class TestSafeQueries:
    def test_clean_select(self):
        r = check_safety(parse_sql("SELECT id, name FROM users WHERE id = 1"))
        assert r.safe
        assert r.block_reason is None
        assert len(r.warnings) == 0
