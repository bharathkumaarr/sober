from core.types import ParseResult, QueryType, ValidationResult


def validate_query(parse_result: ParseResult, schema: dict[str, list[str]]) -> ValidationResult:
    """Check parsed query against actual db schema."""
    if not parse_result.success:
        return ValidationResult(valid=False, errors=[f"Parse failed: {parse_result.error}"])

    errors = []

    is_select = parse_result.query_type == QueryType.SELECT
    if not is_select:
        errors.append(f"Only SELECT queries are allowed, got {parse_result.query_type}")

    # normalize everything to lowercase for comparison
    norm_schema = {k.lower(): [c.lower() for c in v] for k, v in schema.items()}

    unknown_tables = [t for t in parse_result.tables if t.lower() not in norm_schema]
    if unknown_tables:
        errors.append(f"Unknown tables: {', '.join(unknown_tables)}")

    # only bother checking columns if we know all the tables
    all_cols = set()
    for table in parse_result.tables:
        if table.lower() in norm_schema:
            all_cols.update(norm_schema[table.lower()])

    unknown_columns = []
    if parse_result.columns and not unknown_tables:
        for col in parse_result.columns:
            if col.lower() not in all_cols:
                unknown_columns.append(col)
        if unknown_columns:
            errors.append(f"Unknown columns: {', '.join(unknown_columns)}")

    valid = is_select and not unknown_tables and not unknown_columns

    return ValidationResult(
        valid=valid,
        is_select=is_select,
        unknown_tables=unknown_tables,
        unknown_columns=unknown_columns,
        errors=errors,
    )
