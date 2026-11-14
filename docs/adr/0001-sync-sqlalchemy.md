# 1. Use synchronous SQLAlchemy

- Status: proposed
- Date: 2026-11-14
- Issue: #13

## Context

The backend needs database access via SQLAlchemy 2.x. SQLAlchemy offers a synchronous API
(`Session`, `create_engine`) and an asynchronous one (`AsyncSession`, `create_async_engine`).
FastAPI supports both: plain `def` endpoints run in a thread pool, `async def` endpoints run on
the event loop.

We are two students learning the stack. The app is an internal inventory tool with low
concurrency.

## Decision

We use the synchronous API: `create_engine`, `sessionmaker`, `Session`, and `def` endpoints.

## Consequences

- Simpler code and tests: no `await`, no async test plugin, no lazy-loading pitfalls
  (implicit IO on attribute access raises errors in async sessions).
- Each request occupies a thread from FastAPI's pool while it waits on the database. That limits
  throughput under high concurrency, which this app does not have.
- Switching later is possible but touches every repository, service and endpoint signature.
  If we ever need it, we write a new ADR.
