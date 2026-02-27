import json

from flask import Blueprint, jsonify, request

from core.analyzer import estimate_cost
from core.parser import parse_sql
from core.safety_rules import check_safety
from core.simulator import build_explain_query, parse_explain_output
from core.validator import validate_query

query_bp = Blueprint("query", __name__)


@query_bp.route("/analyze-query", methods=["POST"])
def analyze_query():
    from flask import current_app

    data = request.get_json(force=True)
    sql = data.get("query", "").strip()
    if not sql:
        return jsonify({"error": "No query provided"}), 400

    db_manager = current_app.config["DB_MANAGER"]
    if not db_manager.is_connected:
        return jsonify({"error": "No database connected"}), 400

    schema = db_manager.get_schema()

    parse_result = parse_sql(sql)
    validation = validate_query(parse_result, schema)
    safety = check_safety(parse_result)

    safe = validation.valid and safety.safe
    warnings = safety.warnings.copy()
    block_reason = None

    if not validation.valid:
        block_reason = "; ".join(validation.errors)
    elif not safety.safe:
        block_reason = safety.block_reason

    _log_query(current_app, sql, parse_result, safe, warnings, block_reason=block_reason)

    return jsonify({
        "parsed": parse_result.model_dump() if parse_result else None,
        "safe": safe,
        "warnings": warnings,
        "block_reason": block_reason,
        "schema_valid": validation.valid,
        "validation_errors": validation.errors,
    })


@query_bp.route("/simulate-query", methods=["POST"])
def simulate_query():
    from flask import current_app

    data = request.get_json(force=True)
    sql = data.get("query", "").strip()
    if not sql:
        return jsonify({"error": "No query provided"}), 400

    db_manager = current_app.config["DB_MANAGER"]
    if not db_manager.is_connected:
        return jsonify({"error": "No database connected"}), 400

    schema = db_manager.get_schema()

    parse_result = parse_sql(sql)
    validation = validate_query(parse_result, schema)
    safety = check_safety(parse_result)

    if not validation.valid:
        return jsonify({"error": "Query validation failed", "validation_errors": validation.errors}), 400

    if not safety.safe:
        return jsonify({"error": "Query blocked by safety rules", "block_reason": safety.block_reason}), 400

    # run EXPLAIN
    try:
        explain_sql = build_explain_query(parse_result.normalized_sql, db_manager.db_type)
        explain_rows = db_manager.run_explain(explain_sql)
        simulation = parse_explain_output(explain_rows, db_manager.db_type)
    except Exception as e:
        simulation = None
        explain_error = str(e)

    table_sizes = db_manager.get_table_sizes()
    cost = estimate_cost(parse_result, table_sizes)

    result = {
        "cost_estimate": cost.model_dump(),
        "rows_estimate": simulation.rows_estimate if simulation else 0,
        "explain_plan": simulation.explain_plan if simulation else [],
        "warnings": safety.warnings,
    }
    if simulation is None:
        result["explain_error"] = explain_error

    return jsonify(result)


@query_bp.route("/execute-query", methods=["POST"])
def execute_query():
    from flask import current_app

    data = request.get_json(force=True)
    sql = data.get("query", "").strip()
    if not sql:
        return jsonify({"error": "No query provided"}), 400

    db_manager = current_app.config["DB_MANAGER"]
    if not db_manager.is_connected:
        return jsonify({"error": "No database connected"}), 400

    schema = db_manager.get_schema()

    # full pipeline: parse -> validate -> safety check
    parse_result = parse_sql(sql)
    validation = validate_query(parse_result, schema)
    safety = check_safety(parse_result)

    if not validation.valid:
        _log_query(current_app, sql, parse_result, False, safety.warnings, block_reason="; ".join(validation.errors))
        return jsonify({"error": "Query validation failed", "validation_errors": validation.errors}), 400

    if not safety.safe:
        _log_query(current_app, sql, parse_result, False, safety.warnings, block_reason=safety.block_reason)
        return jsonify({"error": "Query blocked by safety rules", "block_reason": safety.block_reason}), 400

    try:
        rows, exec_time = db_manager.run_select(parse_result.normalized_sql)
        _log_query(current_app, sql, parse_result, True, safety.warnings, execution_time=exec_time)
        return jsonify({
            "rows": rows,
            "row_count": len(rows),
            "execution_time_ms": round(exec_time, 2),
            "warnings": safety.warnings,
        })
    except Exception as e:
        _log_query(current_app, sql, parse_result, True, safety.warnings, error=str(e))
        return jsonify({"error": f"Execution failed: {e}"}), 500


@query_bp.route("/logs", methods=["GET"])
def get_logs():
    from flask import current_app

    session_factory = current_app.config.get("SESSION_FACTORY")
    if not session_factory:
        return jsonify({"logs": []})

    from db.models import QueryLog

    session = session_factory()
    try:
        logs = session.query(QueryLog).order_by(QueryLog.created_at.desc()).all()
        return jsonify({"logs": [log.to_dict() for log in logs]})
    finally:
        session.close()


def _log_query(app, sql, parse_result, safe, warnings, **kwargs):
    session_factory = app.config.get("SESSION_FACTORY")
    if not session_factory:
        return

    from db.models import QueryLog

    session = session_factory()
    try:
        log = QueryLog(
            query_text=sql,
            parsed_tree=parse_result.normalized_sql if parse_result else None,
            safe=safe,
            warnings=json.dumps(warnings),
            cost_estimate=kwargs.get("cost_estimate"),
            execution_time=kwargs.get("execution_time"),
            error=kwargs.get("error") or kwargs.get("block_reason"),
        )
        session.add(log)
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()
