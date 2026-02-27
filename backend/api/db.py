from flask import Blueprint, jsonify, request
from core.types import DBConnectionParams

db_bp = Blueprint("db", __name__)


@db_bp.route("/connect-db", methods=["POST"])
def connect_db():
    from flask import current_app

    try:
        data = request.get_json(force=True)
        params = DBConnectionParams(**data)
    except Exception as e:
        return jsonify({"error": f"Invalid parameters: {e}"}), 400

    db_manager = current_app.config["DB_MANAGER"]

    try:
        url = db_manager.connect_user_db(
            db_type=params.db_type,
            host=params.host,
            port=params.port,
            user=params.user,
            password=params.password,
            database=params.database,
        )
        schema = db_manager.get_schema()
        return jsonify({"connected": True, "url": url, "schema": schema})
    except Exception as e:
        return jsonify({"error": f"Connection failed: {e}"}), 500
