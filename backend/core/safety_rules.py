from core.types import ParseResult, QueryType, SafetyResult


def check_safety(parse_result: ParseResult) -> SafetyResult:
    if not parse_result.success:
        return SafetyResult(safe=False, block_reason=f"Cannot evaluate safety: {parse_result.error}")

    warnings = []

    # hard block anything that isn't SELECT
    if parse_result.query_type != QueryType.SELECT:
        return SafetyResult(
            safe=False,
            block_reason=f"Only SELECT queries are allowed. Detected: {parse_result.query_type.value}",
        )

    if parse_result.has_star:
        warnings.append("SELECT * detected — consider specifying explicit columns")

    if not parse_result.has_where and parse_result.tables:
        warnings.append("No WHERE clause — this may perform a full table scan")

    return SafetyResult(safe=True, warnings=warnings)
