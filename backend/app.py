import os

from flask import Flask
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker

from api.db import db_bp
from api.query import query_bp
from db.engine import DatabaseManager
from db.models import Base


def create_app():
    app = Flask(__name__)
    CORS(app)

    db_manager = DatabaseManager()
    app.config["DB_MANAGER"] = db_manager

    # set up the logs database
    log_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sober_logs.db")
    app_engine = db_manager.init_app_db(log_db_path)
    Base.metadata.create_all(app_engine)
    app.config["SESSION_FACTORY"] = sessionmaker(bind=app_engine)

    app.register_blueprint(db_bp)
    app.register_blueprint(query_bp)

    @app.route("/health")
    def health():
        return {"status": "ok", "connected": db_manager.is_connected}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
