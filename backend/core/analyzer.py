from typing import Optional

from core.types import Complexity, CostEstimate, ParseResult

DEFAULT_TABLE_SIZE = 1000


def estimate_cost(parse_result: ParseResult, table_sizes: Optional[dict] = None) -> CostEstimate:
    """
    Quick heuristic cost estimate. Not trying to be postgres here,
    just enough to give the user a rough idea.
    """
    if not parse_result.success:
        return CostEstimate(
            rows_scanned_estimate=0,
            complexity=Complexity.LOW,
            details=f"Cannot estimate: {parse_result.error}",
        )

    sizes = table_sizes or {}

    base_rows = sum(sizes.get(t.lower(), DEFAULT_TABLE_SIZE) for t in parse_result.tables)
    if base_rows == 0:
        base_rows = DEFAULT_TABLE_SIZE

    # WHERE cuts it down, no WHERE means full scan
    filter_factor = 0.3 if parse_result.has_where else 1.0

    # joins make things worse
    n_tables = max(len(parse_result.tables), 1)
    join_factor = 1.0 + 0.5 * (n_tables - 1)

    estimated = int(base_rows * filter_factor * join_factor)

    if estimated < 1000:
        complexity = Complexity.LOW
    elif estimated < 10000:
        complexity = Complexity.MEDIUM
    else:
        complexity = Complexity.HIGH

    details = f"base_rows={base_rows}, filter_factor={filter_factor}, join_factor={join_factor}, tables={n_tables}"

    return CostEstimate(rows_scanned_estimate=estimated, complexity=complexity, details=details)
