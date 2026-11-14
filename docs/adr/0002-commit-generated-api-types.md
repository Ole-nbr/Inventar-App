# 2. Commit generated API types

- Status: proposed
- Date: 2026-11-14
- Issue: #15

## Context

The frontend's API types are generated from the backend's OpenAPI spec with
`openapi-typescript` (`npm run generate:api`), so they are never written by hand.
Our rules also say generated files are not committed.

If `frontend/src/api/types.ts` is not committed, the frontend cannot type check or build
without a running backend, neither locally nor in CI.

## Decision

`frontend/src/api/types.ts` is committed, as a deliberate exception to the rule.
Whoever changes an endpoint or schema in the backend runs `npm run generate:api` against the
running backend and commits the updated file in the same PR.

## Consequences

- The frontend builds and type checks on its own; the frontend workflow needs no backend.
- The file can drift from the backend if someone forgets to regenerate it. A CI check that
  exports the spec from the backend and compares the generated output can close that gap later.
- The file is never edited by hand; changes always come from the generator.
