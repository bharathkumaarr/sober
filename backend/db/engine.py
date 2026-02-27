import time
from typing import Any

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine


class DatabaseManager:
    def __init__(self):
        self._user_engine = None
        self._app_engine = None
        self._db_type = "sqlite"

    def connect_user_db(self, db_type="sqlite", host="", port=5432, user="", password="", database=""):
        self._db_type = db_type.lower()

        if self._db_type == "sqlite":
            path = database if database else ":memory:"
            url = f"sqlite:///{path}"
        elif self._db_type == "postgresql":
            url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        else:
            raise ValueError(f"Unsupported db type: {db_type}")

        self._user_engine = create_engine(url)

        # make sure it actually works
        with self._user_engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        # don't leak passwords in the response
        safe_url = url.replace(password, "****") if password else url
        return safe_url

    @property
    def user_engine(self):
        return self._user_engine

    @property
    def db_type(self):
        return self._db_type

    @property
    def is_connected(self):
        return self._user_engine is not None

    def get_schema(self):
        """Returns {table_name: [col_names]} for all tables"""
        if not self._user_engine:
            return {}

        insp = inspect(self._user_engine)
        schema = {}
        for table in insp.get_table_names():
            cols = [c["name"].lower() for c in insp.get_columns(table)]
            schema[table.lower()] = cols
        return schema

    def get_table_sizes(self):
        if not self._user_engine:
            return {}

        sizes = {}
        with self._user_engine.connect() as conn:
            for table in self.get_schema():
                try:
                    result = conn.execute(text(f'SELECT COUNT(*) FROM "{table}"'))
                    sizes[table] = result.scalar() or 0
                except Exception:
                    sizes[table] = 0
        return sizes

    def run_explain(self, explain_sql):
        if not self._user_engine:
            raise RuntimeError("No database connected")

        with self._user_engine.connect() as conn:
            result = conn.execute(text(explain_sql))
            cols = list(result.keys())
            return [dict(zip(cols, row)) for row in result.fetchall()]

    def run_select(self, sql):
        if not self._user_engine:
            raise RuntimeError("No database connected")

        start = time.perf_counter()
        with self._user_engine.connect() as conn:
            result = conn.execute(text(sql))
            cols = list(result.keys())
            rows = [dict(zip(cols, row)) for row in result.fetchall()]
        elapsed = (time.perf_counter() - start) * 1000
        return rows, elapsed

    # app's own log database

    def init_app_db(self, db_path="sober_logs.db"):
        url = f"sqlite:///{db_path}"
        self._app_engine = create_engine(url)
        return self._app_engine

    @property
    def app_engine(self):
        return self._app_engine
