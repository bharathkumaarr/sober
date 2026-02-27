# dev notes

rules for working on this codebase. mostly for my future self.

## safety stuff (don't break these)

- never execute raw sql from user input — always parse through `core/parser.py` first
- only SELECT allowed — enforce at validator AND safety layers, both need to agree
- core modules stay pure — no flask, no sqlalchemy, no http in `core/`
- all 3 checks (parse, validate, safety) must pass before execution
- EXPLAIN only for simulation, never run anything that modifies data

## code stuff

- add tests when changing parser/validator/analyzer
- keep it simple and readable, not clever
- use pydantic models, not raw dicts, for anything crossing module boundaries
- log every query event — I want to be able to debug issues after the fact

## architecture

- `core/` never imports from `api/` or `db/` — dependencies flow inward
- api layer is thin — calls core functions, handles http, nothing else
- db layer is isolated — engine management separate from business logic
- no `exec()`, no `eval()`, no string-templated sql

## testing

- core tests run without a database
- tests must be deterministic
- test both happy path and rejection cases
