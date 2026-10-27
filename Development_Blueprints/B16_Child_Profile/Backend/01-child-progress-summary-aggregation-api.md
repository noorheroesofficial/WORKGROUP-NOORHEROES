# B-01 — Child Progress Summary Aggregation API

## 1. Feature Context
The Child Profile (Bottom Tab) screen needs a lightweight, glanceable stats card (level, XP, streak, badges). This endpoint is a thin, read-mostly aggregator composed from the **existing** `learning` context (mastery/progress) and `rewards` context (wallet/badges) — it introduces no new business logic, mastery computation, or reward computation of its own.

## 2. Parent Feature
Feature B.16 — Child Profile (Bottom Tab)

## 3. Sub-feature
1.1 Child Progress Summary Aggregation API (ID: **B-01**)

## 4. Objective
Implement `GET /v1/children/{id}/progress` as a condensed, strictly per-child-scoped aggregation of existing `LearningService`/mastery data and `RewardService.get_balance()` data, with zero-tolerance sibling-mismatch rejection and a deliberately narrow response contract that cannot become an unintended full-data-access path into A.9/A.11's domains.

## 5. Business Requirements
- FR-4: A child cannot see sibling stats from this screen — no UI path, query parameter, or route may expose another child's data.
- FR-5: Learning stats summary is sourced from `GET /v1/children/{id}/progress`, the same underlying progress data A.9 (Mastery) and A.11 (Rewards) already compute, presented as a condensed summary — not recomputed independently.
- NFR: Profile screen load p95 < 600ms; cached progress summary preferred over blocking live computation.
- Data Isolation: strict per-child scoping on every call, consistent with the platform-wide "No Lateral Sibling Access" rule.
- Acceptance Criteria: any attempt (normal navigation, crafted deep link, stale cache) to view another child's stats is rejected server-side, never merely omitted client-side.

## 6. Existing Architecture
Reuses `modules/learning/service.py::LearningService.get_child_learning_progress()` and `modules/rewards/service.py::RewardService.get_balance()` (both already exist per `FAST-API-INSTRUCTIONS.md` §5.5/§5.9). This sub-feature adds a new thin aggregation endpoint in the `identity` context (path-consistent with `/v1/identity/family/children`'s existing child-scoped routes) that composes calls to both, rather than duplicating their schemas or logic.

## 7. Existing Code to Reuse
- `modules/learning/service.py::LearningService.get_child_learning_progress()` (read-only call)
- `modules/rewards/service.py::RewardService.get_balance()` (read-only call)
- `core/deps.py::get_current_child` → `ChildSessionContext` (session-derived `child_id`)
- `core/exceptions.py::AuthorizationError`, `ChildScopeViolationError` (existing exception classes — reuse `ChildScopeViolationError` for the sibling-mismatch case rather than inventing a new exception type)
- `infrastructure/redis.py::get_redis_pool()` (short-TTL cache)

## 8. Files to Create
- `src/noorheroes/modules/identity/profile_summary_service.py` — `ProgressSummaryAggregator` class
- `src/noorheroes/modules/identity/profile_summary_schemas.py` — `ChildProgressSummaryResponse`
- `tests/modules/identity/test_progress_summary_aggregation.py`

## 9. Files to Modify
- `src/noorheroes/modules/identity/api.py` — add `GET /v1/children/{id}/progress` route
- `src/noorheroes/modules/identity/deps.py` (or `core/deps.py` factory section) — add `get_progress_summary_aggregator` factory

## 10. Backend Requirements
- `ProgressSummaryAggregator.get_summary(child_ctx: ChildSessionContext, path_child_id: str)` first compares `path_child_id` to `child_ctx.child_id`; on mismatch, raise `ChildScopeViolationError` immediately, **before** any call to `LearningService`/`RewardService` — no partial data must ever be fetched for a mismatched id.
- Compose `level`, `xp`, `xp_to_next_level` from `LearningService.get_child_learning_progress()`; compose `streak_current` from the same call (existing streak field) or `common/utils/streak.py::StreakCalculator` if not already exposed; compose `badges_count` from `RewardService.get_balance()`'s existing badge count field.
- Response schema is a **closed, condensed set** — `ChildProgressSummaryResponse` must not include the full skill-list or full transaction ledger, enforced by the Pydantic model only declaring the five documented fields.
- Cache the composed result in Redis with a short TTL (e.g., 60s), keyed by `child_id`; on a mutating event from `learning`/`rewards` (quiz completion, reward grant) no explicit invalidation is required given the acceptable staleness for a glance-summary.
- On a downstream service failure (`learning` or `rewards` unreachable/erroring), return a distinct `503 PROGRESS_SUMMARY_UNAVAILABLE` rather than a partial or zeroed response, so the client can render its graceful "may be unavailable right now" state.
- Detect an invalid/disabled child session (session references a `child_id` no longer active) and return `409 SESSION_INVALID` distinctly from `403 CHILD_MISMATCH`, so the client can distinguish "wrong child" from "your own session is stale" and route accordingly.

## 11. API Contract

### `GET /v1/children/{id}/progress`
- **Auth:** Bearer, child-mode session (`get_current_child`)
- **Authorization:** path `id` must equal `child_ctx.child_id`
- **Response 200:** `{ "level": 6, "xp": 1240, "xp_to_next_level": 260, "streak_current": 5, "badges_count": 8 }`
- **Errors:** `401` unauthenticated · `403 CHILD_MISMATCH` (path `id` is a different, even valid, child — zero data in body) · `409 SESSION_INVALID` (own session no longer active) · `503 PROGRESS_SUMMARY_UNAVAILABLE` (downstream failure)
- **Caching:** Redis, 60s TTL, keyed `progress_summary:{child_id}`
- **Rate limit:** standard authenticated-read tier (no elevated risk beyond normal read endpoints)

## 12. Database Requirements
No new tables. Reads existing mastery/skill-state tables (via `LearningService`) and `reward_wallets`/`child_badges` (via `RewardService`) exclusively through their existing service methods — no direct cross-module repository access.

## 13. Validation
`id` path parameter is a UUID; malformed UUID → `422`. No request body.

## 14. Authentication
Bearer token via existing `get_current_child`.

## 15. Authorization
Strict `id == child_ctx.child_id` check performed as the very first statement in `ProgressSummaryAggregator.get_summary()`, before any downstream service call — this ordering is itself a requirement, not just the check's existence.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Path `id` matches a sibling's valid child_id | `403 CHILD_MISMATCH`, empty body (no hint the id is valid) |
| Path `id` malformed | `422` |
| No active child session | `401` |
| Own session stale/disabled | `409 SESSION_INVALID` |
| `learning` or `rewards` service failure | `503 PROGRESS_SUMMARY_UNAVAILABLE` |

## 17. Analytics
No server-side analytics event required for this read endpoint beyond standard structured request logging (`request_id`, `child_id` hash, latency, cache hit/miss) — client-side events (`child_profile_viewed`, `child_profile_stats_load_failed`) are emitted by K-01/K-02.

## 18. Performance
p95 < 600ms target per PRD NFR; Redis cache is the primary lever. Avoid N+1 by calling `LearningService`/`RewardService` concurrently (`asyncio.gather`) rather than sequentially, since both are independent read calls.

## 19. Security
Sibling-mismatch rejection (§16) is this endpoint's defining security control — an IDOR-class vulnerability if omitted. No PII beyond `child_id`/`family_id` is logged. The condensed-response-only contract (§10) prevents this aggregator from becoming an unintended alternate full-data-access path into A.9/A.11.

## 20. Library Requirements
No new dependencies — reuses existing FastAPI/Pydantic/Redis stack.

## 21. Testing
- Unit: `ProgressSummaryAggregator.get_summary()` mismatch-check runs before any downstream call (mock `LearningService`/`RewardService` and assert zero calls on mismatch).
- Integration: two sibling fixture children, child A's session requests child B's `id` → `403`, response body contains no data about child B whatsoever, not even an error message confirming child B's existence (treated as the single most important test in this deliverable, per PRD §5).
- Contract test: response schema does NOT include full mastery-skill-list or full reward-ledger fields (schema introspection test, not just a runtime response check).
- Integration: downstream `learning` failure → `503 PROGRESS_SUMMARY_UNAVAILABLE`, not a partial/zeroed `200`.
- Integration: disabled/stale session → `409 SESSION_INVALID`, distinct from `403`.
- Cache test: second request within TTL does not re-call `LearningService`/`RewardService`.

## 22. Documentation
Add OpenAPI description explicitly noting the condensed-contract-by-design rationale (so future maintainers don't "helpfully" widen the response and reintroduce the very risk §10 guards against).

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `ChildProgressSummaryResponse` Schema**
Objective: Closed, five-field Pydantic response schema. Why: prevents accidental full-data exposure. Follow: `common/schemas.py::NoorHeroesBaseModel` camelCase base convention. Files to Create: `profile_summary_schemas.py`. Tests: schema introspection test asserting exactly five fields. Definition of Done: schema cannot serialize any field beyond the five documented ones.

**Task 02 — Implement `ProgressSummaryAggregator`**
Objective: Compose the condensed summary from `LearningService`/`RewardService`. Why: single-responsibility aggregator per PRD §3.1 ("no new business-logic service of its own"). Follow: `BaseService` pattern is not required here since this performs no writes/outbox emission — a plain composed-dependency class is sufficient, but must still raise typed `DomainError` subclasses only. Files to Create: `profile_summary_service.py`. Business Rules: mismatch-check first, concurrent downstream calls via `asyncio.gather`, Redis short-TTL cache. Reuse: `ChildScopeViolationError`. Do Not Change: do not modify `LearningService`/`RewardService` internals — call their existing public methods only. Tests: mismatch-check-runs-first unit test; cache-hit/miss test. Definition of Done: zero downstream calls occur on a mismatched `id`.

**Task 03 — Add Route & Dependency Factory**
Objective: Wire `GET /v1/children/{id}/progress` into `identity/api.py`. Follow: existing router `Depends()` conventions (§10 of core FastAPI doc). Files to Modify: `api.py`, `deps.py`. Dependencies: Task 02. Definition of Done: route registered, OpenAPI spec includes `403`/`409`/`503` response models.

**Task 04 — Sibling-Mismatch Zero-Leakage Test Suite**
Objective: The PRD-mandated "single most important test." Follow: two-sibling fixture pattern already used elsewhere in the identity test suite (mirror B-06's fixture style). Files to Create: `test_progress_summary_aggregation.py`. Tests: full matrix per §21. Definition of Done: this test is CI-blocking on any PR touching `profile_summary_service.py` or `identity/api.py`'s progress route.

**Task 05 — Add Redis Caching Layer**
Objective: 60s TTL cache keyed by `child_id`. Follow: existing `infrastructure/redis.py::get_redis_pool()` usage pattern (mirrors `TranslationCacheManager`'s style). Tests: cache-hit avoids downstream calls. Definition of Done: TTL configurable via `Settings`, not hardcoded magic number in the service body.

**Task 06 — Update OpenAPI Documentation**
Objective: Document the condensed-contract rationale and all error codes. Definition of Done: `/docs` shows `403 CHILD_MISMATCH`, `409 SESSION_INVALID`, `503 PROGRESS_SUMMARY_UNAVAILABLE` with example bodies.

**Task 07 — Final Code Review**
Objective: Confirm mismatch-check ordering, concurrent downstream calls, closed schema, CI-blocking test wired. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [x] `id`-matches-session check executes before any downstream service call
- [x] Sibling-mismatch response body contains zero data, not even existence confirmation
- [x] Response schema is closed to exactly five documented fields
- [x] Downstream failure returns `503`, never a partial/zeroed `200`
- [x] Disabled/stale own-session returns `409 SESSION_INVALID`, distinct from `403`
- [x] Redis cache TTL configurable, not hardcoded
- [x] Sibling-mismatch test is CI-blocking
- [x] No PostgreSQL or Redis credentials modified

## 25. Definition of Done
`GET /v1/children/{id}/progress` is live, strictly per-child-scoped with zero-leakage sibling-mismatch rejection, composing existing `LearningService`/`RewardService` data into a closed condensed contract, cached for performance, and ready for K-02 (Learning Stats Summary Widget) to consume.

**Status:** ✅ **Implemented & Verified** (12 unit & API integration tests passing in `tests/modules/identity/test_progress_summary_aggregation.py`).
