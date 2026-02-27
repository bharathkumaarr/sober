import sqlglot
from sqlglot import exp

from core.types import ParseResult, QueryType

# sqlglot expression -> our QueryType
_TYPE_MAP = {
    exp.Select: QueryType.SELECT,
    exp.Insert: QueryType.INSERT,
    exp.Update: QueryType.UPDATE,
    exp.Delete: QueryType.DELETE,
    exp.Drop: QueryType.DROP,
    exp.Alter: QueryType.ALTER,
    exp.Create: QueryType.CREATE,
}


def parse_sql(sql: str) -> ParseResult:
    if not sql or not sql.strip():
        return ParseResult(success=False, error="Empty SQL query")

    try:
        expressions = sqlglot.parse(sql)
    except sqlglot.errors.ParseError as e:
        return ParseResult(success=False, error=f"SQL parse error: {e}")

    if not expressions or expressions[0] is None:
        return ParseResult(success=False, error="Could not parse SQL")

    if len(expressions) > 1:
        return ParseResult(success=False, error="Multiple statements not allowed")

    ast = expressions[0]

    # figure out what kind of statement this is
    query_type = QueryType.UNKNOWN
    for expr_type, qt in _TYPE_MAP.items():
        if isinstance(ast, expr_type):
            query_type = qt
            break

    tables = _extract_tables(ast)
    columns = _extract_columns(ast)
    has_star = _check_star(ast)
    has_where = _check_where(ast)

    return ParseResult(
        success=True,
        normalized_sql=ast.sql(pretty=False),
        query_type=query_type,
        tables=tables,
        columns=columns,
        has_where=has_where,
        has_star=has_star,
    )


def _extract_tables(ast):
    tables = []
    for table in ast.find_all(exp.Table):
        if table.name:
            tables.append(table.name.lower())
    # dedupe but keep order
    return list(dict.fromkeys(tables))


def _extract_columns(ast):
    cols = []
    for col in ast.find_all(exp.Column):
        if col.name:
            cols.append(col.name.lower())
    return list(dict.fromkeys(cols))


def _check_star(ast):
    if not isinstance(ast, exp.Select):
        return False
    for _ in ast.find_all(exp.Star):
        return True
    return False


def _check_where(ast):
    if not isinstance(ast, exp.Select):
        return False
    return ast.find(exp.Where) is not None
