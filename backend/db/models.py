from datetime import datetime, timezone
import json

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    query_text = Column(Text, nullable=False)
    parsed_tree = Column(Text, nullable=True)
    safe = Column(Boolean, default=False)
    warnings = Column(Text, default="[]")  # stored as json
    cost_estimate = Column(Float, nullable=True)
    execution_time = Column(Float, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "query_text": self.query_text,
            "parsed_tree": self.parsed_tree,
            "safe": self.safe,
            "warnings": json.loads(self.warnings) if self.warnings else [],
            "cost_estimate": self.cost_estimate,
            "execution_time": self.execution_time,
            "error": self.error,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
