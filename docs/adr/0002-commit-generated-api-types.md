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
Whoever changes an endpoint or schema in the backend runs `npm run generate:api` and commits
the updated file in the same PR. The script exports the spec with `backend/scripts/export_openapi.py`,
so no running backend is needed.

## Consequences

- The frontend builds and type checks on its own; the frontend workflow needs no backend.
- The file could drift from the backend if someone forgets to regenerate it. The
  `api-types.yml` workflow regenerates it and fails if it differs from the committed file (#20).
- The file is never edited by hand; changes always come from the generator.
