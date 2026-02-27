import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.analyzer import estimate_cost
from core.parser import parse_sql
from core.types import Complexity


class TestDeterminism:
    def test_same_query_same_result(self):
        pr = parse_sql("SELECT id FROM users WHERE id = 1")
        sizes = {"users": 5000}
        r1 = estimate_cost(pr, sizes)
        r2 = estimate_cost(pr, sizes)
        assert r1.rows_scanned_estimate == r2.rows_scanned_estimate
        assert r1.complexity == r2.complexity

    def test_deterministic_across_calls(self):
        sql = "SELECT u.id, o.total FROM users u JOIN orders o ON u.id = o.user_id"
        sizes = {"users": 1000, "orders": 5000}
        results = [estimate_cost(parse_sql(sql), sizes) for _ in range(10)]
        assert all(r.rows_scanned_estimate == results[0].rows_scanned_estimate for r in results)


class TestComplexity:
    def test_low(self):
        r = estimate_cost(parse_sql("SELECT id FROM users WHERE id = 1"), {"users": 100})
        assert r.complexity == Complexity.LOW

    def test_medium(self):
        r = estimate_cost(parse_sql("SELECT id FROM users"), {"users": 5000})
        assert r.complexity == Complexity.MEDIUM

    def test_high(self):
        r = estimate_cost(parse_sql("SELECT id FROM users"), {"users": 50000})
        assert r.complexity == Complexity.HIGH


class TestHeuristics:
    def test_where_reduces_cost(self):
        sizes = {"users": 10000}
        no_where = estimate_cost(parse_sql("SELECT id FROM users"), sizes)
        with_where = estimate_cost(parse_sql("SELECT id FROM users WHERE id = 1"), sizes)
        assert with_where.rows_scanned_estimate < no_where.rows_scanned_estimate

    def test_join_increases_cost(self):
        sizes = {"users": 1000, "orders": 1000}
        single = estimate_cost(parse_sql("SELECT id FROM users"), sizes)
        joined = estimate_cost(
            parse_sql("SELECT u.id FROM users u JOIN orders o ON u.id = o.user_id"),
            sizes,
        )
        assert joined.rows_scanned_estimate > single.rows_scanned_estimate

    def test_default_table_size(self):
        r = estimate_cost(parse_sql("SELECT id FROM unknown_table"))
        assert r.rows_scanned_estimate > 0
