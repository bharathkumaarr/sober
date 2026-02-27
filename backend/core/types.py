from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class QueryType(str, Enum):
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    DROP = "DROP"
    ALTER = "ALTER"
    CREATE = "CREATE"
    UNKNOWN = "UNKNOWN"


class Complexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ParseResult(BaseModel):
    success: bool
    normalized_sql: Optional[str] = None
    query_type: Optional[QueryType] = None
    tables: list[str] = Field(default_factory=list)
    columns: list[str] = Field(default_factory=list)
    has_where: bool = False
    has_star: bool = False
    error: Optional[str] = None


class ValidationResult(BaseModel):
    valid: bool
    is_select: bool = False
    unknown_tables: list[str] = Field(default_factory=list)
    unknown_columns: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class SafetyResult(BaseModel):
    safe: bool
    warnings: list[str] = Field(default_factory=list)
    block_reason: Optional[str] = None


class CostEstimate(BaseModel):
    rows_scanned_estimate: int = 0
    complexity: Complexity = Complexity.LOW
    details: str = ""


class SimulationResult(BaseModel):
    explain_plan: list[dict[str, Any]] = Field(default_factory=list)
    rows_estimate: int = 0
    cost_estimate: float = 0.0
    error: Optional[str] = None


class ExecutionResult(BaseModel):
    rows: list[dict[str, Any]] = Field(default_factory=list)
    row_count: int = 0
    execution_time_ms: float = 0.0
    error: Optional[str] = None


class AnalysisResult(BaseModel):
    parsed: Optional[ParseResult] = None
    validation: Optional[ValidationResult] = None
    safety: Optional[SafetyResult] = None
    safe: bool = False
    warnings: list[str] = Field(default_factory=list)
    block_reason: Optional[str] = None
    schema_valid: bool = False


class QueryLogEntry(BaseModel):
    id: Optional[int] = None
    query_text: str
    parsed_tree: Optional[str] = None
    safe: bool = False
    warnings: list[str] = Field(default_factory=list)
    cost_estimate: Optional[float] = None
    execution_time_ms: Optional[float] = None
    error: Optional[str] = None
    created_at: Optional[datetime] = None


class DBConnectionParams(BaseModel):
    db_type: str = "sqlite"
    host: str = ""
    port: int = 5432
    user: str = ""
    password: str = ""
    database: str = ""
