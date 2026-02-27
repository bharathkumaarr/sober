from typing import Any

from core.types import SimulationResult


def build_explain_query(sql: str, db_type: str = "sqlite") -> str:
    """Turn a SELECT into an EXPLAIN. Doesn't execute anything."""
    stripped = sql.strip().rstrip(";")
    if db_type.lower() == "postgresql":
        return f"EXPLAIN (FORMAT JSON) {stripped}"
    return f"EXPLAIN QUERY PLAN {stripped}"


def parse_explain_output(rows: list[dict[str, Any]], db_type: str = "sqlite") -> SimulationResult:
    if not rows:
        return SimulationResult(explain_plan=[], rows_estimate=0, cost_estimate=0.0)

    if db_type.lower() == "postgresql":
        return _parse_pg(rows)
    return _parse_sqlite(rows)


def _parse_pg(rows):
    try:
        plan_data = rows[0] if rows else {}
        if "QUERY PLAN" in plan_data:
            plan_json = plan_data["QUERY PLAN"]
            if isinstance(plan_json, list) and plan_json:
                plan = plan_json[0].get("Plan", {})
                return SimulationResult(
                    explain_plan=plan_json,
                    rows_estimate=plan.get("Plan Rows", 0),
                    cost_estimate=plan.get("Total Cost", 0.0),
                )
        return SimulationResult(explain_plan=rows, rows_estimate=0, cost_estimate=0.0)
    except (KeyError, IndexError, TypeError):
        return SimulationResult(explain_plan=rows, rows_estimate=0, cost_estimate=0.0)


def _parse_sqlite(rows):
    entries = []
    for row in rows:
        entries.append({
            "id": row.get("id", 0),
            "parent": row.get("parent", 0),
            "detail": row.get("detail", str(row)),
        })

    # sqlite explain doesn't give row estimates unfortunately
    return SimulationResult(explain_plan=entries, rows_estimate=0, cost_estimate=0.0)
