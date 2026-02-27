# Sober

Safe query simulation & analysis engine. Accepts SQL queries, checks them against a connected database, simulates execution with EXPLAIN, estimates cost, flags dangerous patterns, and only runs them if everything looks safe.

## how it works

```
user query -> parser (sqlglot) -> validator -> safety rules -> analyzer
                                                               |
                                                          simulator (EXPLAIN)
```

All the important logic lives in `core/` — pure python, no flask, no database imports. This makes it easy to test and reuse outside the web app.

The flask API is just a thin layer that wires everything together.

## safety

- only SELECT queries get through, everything else is blocked
- tables and columns are checked against the real schema
- SELECT * and missing WHERE clauses get flagged as warnings
- simulation uses EXPLAIN, never modifies data
- queries only execute after passing validation AND safety checks

## cost estimation

rough heuristic — not trying to replace postgres's query planner, just enough to give users a heads up:

```
estimated_rows = base_rows * filter_factor * join_factor

base_rows     = sum of table sizes (default 1000 if unknown)
filter_factor = 0.3 with WHERE, 1.0 without
join_factor   = 1.0 + 0.5 per additional table
```

complexity: LOW (<1k rows), MEDIUM (1k-10k), HIGH (>10k)

## logging

every query event goes into `sober_logs.db` — the raw sql, whether it was safe, warnings, execution time, errors, timestamps. accessible via `GET /logs`.

## getting started

```bash
# backend
cd backend
pip3 install -r requirements.txt
python3 app.py  # runs on port 5001

# frontend (separate terminal)
cd frontend
npm install
npm run dev  # runs on port 5173
```

open http://localhost:5173, connect to a sqlite db, and start querying.

## tests

```bash
cd backend
python3 -m pytest tests/ -v
```

## stack

- **backend**: python, flask, sqlalchemy, sqlglot, pydantic
- **frontend**: react, vite
- **databases**: sqlite (dev + logs), postgresql (supported)

## tradeoffs

| choice | why |
|---|---|
| sqlglot over sqlparse | much better AST, but heavier dep |
| heuristic cost | works without pg_stats, less accurate though |
| in-memory connection state | simple for now, doesn't survive restarts |
| sqlite for logs | zero config, good enough for single-user |
| single-file react | quick to build, would split up if it grows |
