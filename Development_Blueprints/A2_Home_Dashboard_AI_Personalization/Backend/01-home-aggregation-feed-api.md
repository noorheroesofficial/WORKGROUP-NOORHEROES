# B-01 — Home Aggregation & Personalized Feed API

## 1. Feature Context
NoorHeroes Child App, Feature A.2 (Child Home Dashboard & AI Personalization). This is the single highest-traffic backend endpoint in the app — every app open/foreground hits it. It is the orchestration root that all other Home sub-features (B-02 through B-08) plug into.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization (`PRD_Documents/Child App (1-12)/Feature_A2_Home_Dashboard_AI_Personalization.md`)

## 3. Sub-feature
1.1 Home Aggregation & Personalized Feed API (ID: B-01)

## 4. Objective
Build a `Home Aggregation Service` exposing `GET /v1/home` that fans out concurrently to seven upstream services, assembles a fixed 10-section response contract in strict priority order, degrades gracefully per-section on partial upstream failure, and architecturally guarantees zero billing/subscription content can ever reach a child session.

## 5. Business Requirements
Derived from PRD §1.7 (FR-1 through FR-18), §1.9 Acceptance Criteria, §1.10 Edge Cases, §1.11 Error Handling, §3:
- Sections render in the fixed order defined in FR-1; order is not client- or user-configurable.
- `bedtime_corner` key is always present in the JSON payload; its value is `null` outside the parent-configured window (not an omitted key) — window evaluation must correctly handle spans crossing midnight.
- Home must never query or return subscription/billing/paywall fields, enforced architecturally (response-shaping allowlist), not just by omission convention (FR-9).
- Partial upstream failures degrade only the affected section; the endpoint still returns `200` (never a `503 PARTIAL_DEGRADATION`).
- First-day / zero-activity children receive `is_first_day: true` so the client can swap in the guided empty state.
- Response must support `ETag`-based conditional caching (`If-None-Match`).

## 6. Existing Architecture
Follow `FAST-API-INSTRUCTIONS.md` for: project layout (routers/services/repositories/schemas/dependencies), async SQLAlchemy 2.0 session handling, Pydantic v2 schema conventions, structured logging, and existing exception-handling middleware. Reuse the same auth/session dependency pattern already implemented for Feature A.1 (child-mode Bearer session scoping to `family_id` + `child_id`) — do not create a parallel auth mechanism.

## 7. Existing Code to Reuse
- Child-mode session auth dependency (from A.1 Identity & Family Service — `POST /v1/auth/otp/verify` issues the token this endpoint consumes).
- Redis client/connection pool already configured for the platform (do not create a second Redis client instance).
- Analytics Event Bus publisher utility used by A.1 endpoints.
- Existing FastAPI exception-handling middleware / standard error-envelope format.

## 8. Files to Create
- `app/routers/home.py` — `GET /v1/home` route
- `app/services/home_aggregation_service.py` — fan-out orchestration + degradation logic
- `app/schemas/home.py` — strict Pydantic response models (allowlist)
- `app/services/clients/` — thin async httpx clients for Recommendation, Progress, Habit, Challenge, Achievement, Content Catalog, Islamic Calendar services (only if not already present from other in-flight sub-features; coordinate with B-02/B-05/B-06/B-07 to avoid duplicate client creation)
- `app/cache/home_cache.py` — Redis cache read/write/partial-invalidate helpers, key pattern `home:{child_id}`
- `tests/unit/test_home_aggregation_service.py`
- `tests/integration/test_home_endpoint_degradation.py`
- `tests/integration/test_home_content_safety_audit.py` (co-owned with B-08; this file establishes the harness, B-08 extends the blocklist matrix)

## 9. Files to Modify
- `app/main.py` — register `home` router
- `app/core/config.py` — add per-upstream timeout config (400ms default) and cache TTL (5 min) as named settings, not magic numbers
- OpenAPI tags/docs index

## 10. Backend Requirements
- FastAPI async endpoint; `asyncio.gather(..., return_exceptions=True)` for concurrent fan-out with per-call timeout wrapped via `asyncio.wait_for`.
- Strict Pydantic response model (`model_config = ConfigDict(extra="forbid")` equivalent behavior enforced by explicitly constructing the response object field-by-field from validated upstream data — never `**upstream_dict` spread into the response model).
- Section order encoded as literal ordered fields in the Pydantic model / response dict construction, covered by a snapshot test.
- Redis cache keyed `home:{child_id}`, 5-minute TTL for ranking-derived sections; deterministic sections (habits, challenges) invalidated immediately on mutation by the owning service (B-03, B-06), not time-based.
- Rate limiting: 30 req/min/child_session (reuse existing rate-limit middleware/dependency if present in the codebase; otherwise implement via Redis sliding window consistent with A.1's rate-limiting pattern).

## 11. KMP Requirements
Not implemented in this sub-feature. Consumed by KMP sub-feature K-01 (`HomeRepository.getHome()`) and K-07 (offline cache fallback). No KMP code is written here — this section documents the contract KMP depends on.

## 12. NextJS Requirements
Not directly applicable. The Home Composition Health Monitor (N-01) consumes *aggregated metrics derived from* this service's per-section outcomes, not this endpoint itself — ensure the aggregation service emits a lightweight internal metrics event (section outcome: content/hidden/error) to the metrics pipeline N-01 reads from.

## 13. API Contract

**Endpoint:** `GET /v1/home`
**Auth:** Bearer (child-mode session, scoped to `family_id` + `child_id`)
**Request Headers:** `X-Child-Session-Id`, `X-Timezone`, `X-App-Version`, `If-None-Match`

**Response 200:**
```json
{
  "child_id": "child_...",
  "generated_at": "2026-06-22T10:00:00Z",
  "greeting": { "text": "Good morning, Amina!", "occasion": "Jummah Mubarak" },
  "streak": { "current": 5, "mercy_day_active": false, "xp": 1240, "xp_to_next_level": 260 },
  "sections": {
    "today_mission": { "items": [ { "content_id": "...", "type": "quiz", "title": "...", "progress": 0 } ] },
    "continue_learning": { "items": [] },
    "continue_watching": { "items": [] },
    "recommended": { "items": [ { "content_id": "...", "reason_tag": "because_you_liked_prophet_stories" } ] },
    "daily_quiz": { "quiz_id": "...", "question_count": 5, "completed_today": false },
    "habits": { "items": [ { "habit_id": "...", "label": "Fajr", "checked_today": false } ] },
    "weekly_challenge": { "challenge_id": "...", "percent_complete": 40, "days_remaining": 3 },
    "milestones": { "recent": [], "next_teaser": {} },
    "bedtime_corner": null,
    "islamic_fact": { "fact_id": "...", "text": "..." }
  },
  "is_first_day": false
}
```

**Error Responses:** `401 INVALID_SESSION`, `403 CHILD_LOCKED`. No top-level `503` for partial degradation — degraded sections are represented as `null`/empty within a `200` response.

## 14. Database Requirements
This endpoint is read-heavy across tables owned by other sub-features (`progress_record`, `habit_definition`, `habit_checkin`, `challenge_participation`, `achievement_unlock`, `daily_mission_assignment`, `home_fact_history`). No new tables are created by B-01 itself; ensure indexes listed in the PRD §4.2 exist before this service goes live (coordinate with B-03/B-04/B-05/B-06/B-07 migrations landing first, or stub upstream calls in early integration testing).

## 15. Validation
- `X-Timezone` header required for correct bedtime-window evaluation; falls back to family's stored timezone if header absent/invalid, logged as a data-quality warning.
- Response object validated against the strict Pydantic model before serialization; any upstream field not in the model is silently dropped (this is a validation step, not just documentation).

## 16. Authentication
Bearer JWT (child-mode session) issued by A.1's Identity & Family Service; token must carry both `family_id` and `child_id` claims. Standard JWT verification middleware already established in A.1 is reused unmodified.

## 17. Authorization
Endpoint strictly scoped to the authenticated token's own `child_id` — a request cannot pass another child's ID (via path, query, or header tampering) and receive that child's data, even within the same family. Enforced at the service layer by ignoring any client-supplied `child_id` and using only the token claim.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Recommendation Service timeout/failure | Serve rule-based fallback feed (deterministic, scholar-curated); no error surfaced |
| Progress Service failure | `continue_learning`/`continue_watching` sections null; rest of response unaffected |
| Full payload fetch failure, no cache | Client-facing concern (handled by K-07); server returns standard 5xx only for true infrastructure failure, not partial degradation |
| Islamic Calendar Service failure | `greeting.occasion` omitted silently |
| Any single upstream failure | Section-level null/empty; overall response remains `200` |

## 19. Offline First
Not applicable server-side (server has no offline mode). This endpoint is the source of truth that KMP's offline cache (K-07) is built from — ensure the response is fully self-contained and cacheable client-side without requiring supplementary calls for basic rendering.

## 20. Local Data
Not applicable (backend). See K-07 for the corresponding Room-based local cache.

## 21. Localization
`greeting.text`, `greeting.occasion`, and any AI-generated greeting variant are resolved server-side based on the child's `preferred_language` (stored on the `child` record from A.1) — client receives already-localized strings, not locale keys requiring further client-side lookup, except where a shared string-resource key is the established pattern elsewhere in the codebase (follow existing convention; do not introduce a new localization mechanism).

## 22. RTL
Text content itself is language-appropriate (Arabic/Urdu); layout RTL mirroring is a client-side (KMP) concern, not a backend concern for this endpoint.

## 23. Analytics
This service does not itself emit user-facing analytics events (those are client-fired per PRD §1.19: `home_viewed`, `home_section_rendered`, etc.). It does emit **internal** operational telemetry per section (content/hidden/error outcome, per-call latency) to the metrics pipeline consumed by N-01's Home Composition Health Monitor.

## 24. Performance
- Cold load p95 < 1.2s, warm/cached p95 < 300ms (PRD §1.8) — validate via load test before rollout.
- Per-upstream-call timeout: 400ms, enforced via `asyncio.wait_for` per call inside the `asyncio.gather` fan-out.
- N+1 avoidance: batch any per-item lookups (e.g., content metadata for recommended items) rather than looping individual calls.
- Redis cache (5 min TTL, partial invalidation) to keep warm-path latency low under DAU peak (regional evening/Maghrib spike, per PRD §1.8 Scalability).

## 25. Security
- Response-shaping allowlist is the primary defense against billing-content leakage (FR-9) — this is the architectural core of this sub-feature; see B-08 for the dedicated CI audit that continuously verifies it.
- Redis cache keys are UUID-based (`child_id`), never sequential/guessable.
- No PII beyond `child_id` reference is logged.

## 26. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 (async), httpx (async client for internal service calls), Redis (`redis.asyncio`), pytest + pytest-asyncio for tests. Do not introduce a new HTTP client library if httpx is already the established internal-service-call pattern elsewhere in the codebase.

## 27. Testing
- Unit: response-shaping allowlist strips unexpected fields; section-order literal structure; bedtime-window null-vs-omitted-key behavior including midnight-crossing.
- Integration: simulate each of the 7 upstream dependencies failing independently — assert `200` with only the affected section degraded.
- Integration: cache hit/miss/partial-invalidation behavior.
- Content-safety audit harness (shared with B-08): recursive blocklist scan across a fixture matrix (age, tier, locale).
- Load test: p95 latency targets under simulated DAU peak.

## 28. Documentation
Update OpenAPI schema/docs for `GET /v1/home` including the explicit note that `bedtime_corner` is always a present key. Add an internal architecture doc note (or update the existing Core-Architecture FastAPI doc) describing the response-shaping-allowlist pattern as a reusable defense-in-depth technique, since B-08 and future features may reference it.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Strict Response Schema**
- Objective: Create the Pydantic response models enforcing the allowlist.
- Why Required: This is the primary architectural defense against billing-content leakage (FR-9); must exist before any service logic is written.
- Existing Architecture to Follow: `FAST-API-INSTRUCTIONS.md` schema conventions.
- Existing Files to Reuse: none new; base `BaseModel` conventions from existing schemas.
- Files to Create: `app/schemas/home.py`
- Files to Modify: none
- Implementation Details: Define `HomeResponse`, `GreetingModel`, `StreakModel`, `SectionsModel` (fields in fixed literal order matching FR-1), and per-section item models. `bedtime_corner: Optional[BedtimeCornerModel] = None`.
- Business Rules: No field outside this contract may ever be added without an explicit spec change.
- Validation: Models must reject/ignore unknown upstream fields by construction (explicit field-by-field assignment in the service layer, not `**kwargs`).
- Error Handling: N/A at schema level.
- Security: This task IS the security control (FR-9 enforcement).
- Performance: N/A.
- Localization: `greeting.text`/`occasion` typed as plain localized strings.
- RTL: N/A (backend).
- Analytics: N/A.
- Tests: Unit test constructing a model from a dict containing an extraneous `"subscription_upsell"` field and asserting it is absent from `.model_dump()`.
- Documentation: Docstring on `HomeResponse` explaining the allowlist guarantee.
- Dependencies: None (first task).
- Do Not Change: Do not make any field `Optional[Any]` or use permissive `dict` typing for `sections` — every section must be an explicit typed model.
- Expected Result: `app/schemas/home.py` exists with full model tree.
- Definition of Done: Schema file compiles, unit test above passes.

**Task 02 — Build Upstream Service Clients**
- Objective: Thin async httpx clients for the 7 fan-out dependencies.
- Why Required: Aggregation logic needs a consistent, timeout-capable interface to each upstream service.
- Existing Architecture to Follow: Existing internal-service-call pattern (httpx + shared base client class, if one exists in the codebase — reuse it).
- Existing Files to Reuse: Any existing `BaseServiceClient` from A.1's OTP/Google-auth service clients.
- Files to Create: `app/services/clients/recommendation_client.py`, `progress_client.py`, `habit_client.py`, `challenge_client.py`, `achievement_client.py`, `content_catalog_client.py`, `islamic_calendar_client.py`
- Files to Modify: none
- Implementation Details: Each client exposes one async method returning a typed result or raising a client-specific exception on failure/timeout; timeout defaulted from `app/core/config.py` setting (400ms).
- Business Rules: Clients must not retry internally beyond a single attempt (the aggregation service owns the fail-fast/degrade decision, not the client).
- Validation: Response payload from each upstream validated against a minimal internal schema before being handed to the aggregation service.
- Error Handling: Raise a typed exception (e.g., `UpstreamTimeoutError`, `UpstreamUnavailableError`) rather than propagating raw httpx exceptions.
- Security: No credentials/secrets hardcoded; read from existing config/secrets mechanism.
- Performance: Connection pooling reused across requests (module-level httpx.AsyncClient, not per-call instantiation).
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Unit tests per client with mocked httpx responses (success, timeout, 5xx).
- Documentation: Docstring per client noting the service it wraps and its SLA/timeout.
- Dependencies: Task 01.
- Do Not Change: Do not modify PostgreSQL/Redis credentials while wiring config.
- Expected Result: 7 client modules under `app/services/clients/`.
- Definition of Done: All client unit tests pass; no shared mutable state between clients.

**Task 03 — Implement Home Aggregation Service (Fan-Out + Degradation)**
- Objective: Orchestrate concurrent calls and assemble the response with per-section graceful degradation.
- Why Required: Core business logic of this sub-feature.
- Existing Architecture to Follow: FastAPI service-layer pattern (business logic outside the router).
- Existing Files to Reuse: Clients from Task 02, schema from Task 01.
- Files to Create: `app/services/home_aggregation_service.py`
- Files to Modify: none
- Implementation Details: `asyncio.gather(*calls, return_exceptions=True)`; for each result, if it's an exception or timeout, set that section to `None`/empty per contract; assemble `HomeResponse` explicitly field-by-field (never spread).
- Business Rules: `bedtime_corner` evaluated via a pure function taking `(now, timezone, bedtime_window_start, bedtime_window_end)` handling midnight-crossing (`start > end` case). `is_first_day` computed from absence of any `progress_record`/`habit_checkin`/`daily_mission_assignment` rows for the child.
- Validation: Final assembled object validated against `HomeResponse` before return.
- Error Handling: Per PRD §1.11 table — implement exactly as specified per upstream.
- Security: No unfiltered upstream dict ever touches the response object.
- Performance: All calls issued concurrently, not sequentially; per-call `asyncio.wait_for(call, timeout=0.4)`.
- Localization: Pass-through of already-localized upstream strings.
- RTL: N/A.
- Analytics: Emit internal per-section outcome metric (content/hidden/error) after assembly.
- Tests: Unit tests for the midnight-crossing bedtime function (explicit edge case: 20:00–06:00 window at 23:00 and at 03:00 and at 12:00); unit tests for `is_first_day` computation; integration tests simulating each upstream failing independently.
- Documentation: Docstring explaining the fail-open-per-section / fail-closed-for-AI-content distinction (this section is fail-open for infra failures, but AI Safety Filter per B-02 is fail-closed for content-safety failures — do not conflate the two).
- Dependencies: Tasks 01, 02.
- Do Not Change: Do not let a single upstream exception propagate to a 500 for the whole response.
- Expected Result: `home_aggregation_service.get_home(child_id, timezone) -> HomeResponse`.
- Definition of Done: All degradation integration tests pass; p95 latency measured in test harness within target on mocked-fast upstreams.

**Task 04 — Implement Redis Caching Layer**
- Objective: `home:{child_id}` cache with 5-min TTL and partial-section invalidation hooks.
- Why Required: Meets warm-path p95 < 300ms target and reduces upstream load under DAU peak.
- Existing Architecture to Follow: Existing Redis client/connection pool from the platform's core Redis setup.
- Existing Files to Reuse: Existing `redis.asyncio` client instance (do not create a second pool).
- Files to Create: `app/cache/home_cache.py`
- Files to Modify: `app/services/home_aggregation_service.py` (read-through cache wrapper)
- Implementation Details: `get_cached_home(child_id)`, `set_cached_home(child_id, response, ttl=300)`, `invalidate_section(child_id, section_name)` (partial invalidation storing sections as separate hash fields, not one monolithic blob, so a habit check-in can invalidate only `habits`).
- Business Rules: Deterministic sections (habits, challenges, missions) invalidated immediately by their owning mutation endpoints (B-03/B-04/B-06), not by TTL alone.
- Validation: Cache read result validated against schema before being trusted (defensive deserialization).
- Error Handling: Cache failure (Redis down) must not fail the request — fall through to live fan-out.
- Security: Cache keys UUID-based, never guessable/sequential.
- Performance: This is the primary performance lever for this sub-feature.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Unit tests for cache hit/miss/partial-invalidate; integration test confirming Redis outage doesn't break the endpoint (fail-open for cache, fail-closed for content-safety — distinct failure modes).
- Documentation: Note the hash-field-per-section storage design rationale.
- Dependencies: Task 03.
- Do Not Change: Do not modify Redis credentials/connection settings.
- Expected Result: Cache-wrapped aggregation service.
- Definition of Done: Cache tests pass; Redis-outage fallback verified.

**Task 05 — Implement `GET /v1/home` Router + Auth/Rate-Limit Wiring**
- Objective: Expose the endpoint with auth, rate limiting, and ETag support.
- Why Required: Client-facing entry point.
- Existing Architecture to Follow: Existing router registration pattern in `app/main.py`; existing auth dependency from A.1.
- Existing Files to Reuse: A.1's Bearer/child-session auth dependency; existing rate-limit dependency/middleware if present.
- Files to Create: `app/routers/home.py`
- Files to Modify: `app/main.py`
- Implementation Details: Route depends on auth dependency (extracts `child_id`/`family_id` from token, ignoring any client-supplied ID), rate-limit dependency (30/min/child_session), and `If-None-Match` handling for `304 Not Modified` short-circuit.
- Business Rules: Never trust a client-supplied `child_id`.
- Validation: `X-Timezone` header parsed/validated; invalid values fall back to stored family timezone with a logged warning.
- Error Handling: `401 INVALID_SESSION`, `403 CHILD_LOCKED` per contract.
- Security: Authorization enforced at this layer (Task/Section 17).
- Performance: ETag short-circuit avoids full response body transfer on unchanged data.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Integration tests for 401/403 paths, ETag 304 behavior, cross-child access attempt (tampered token) returning 403 with zero data leakage.
- Documentation: OpenAPI route docstring.
- Dependencies: Tasks 03, 04.
- Do Not Change: N/A.
- Expected Result: Working `GET /v1/home` endpoint.
- Definition of Done: All integration tests in this task and Task 03/04 pass.

**Task 06 — Content-Safety Audit Test Harness**
- Objective: Establish the recursive blocklist-scan test harness (shared foundation for B-08).
- Why Required: FR-9 is the feature's defining non-negotiable guarantee; must be automated, not manually verified.
- Existing Architecture to Follow: pytest conventions already used in the repo.
- Existing Files to Reuse: Fixture factories for child profiles (free/premium/trial-expired/various locales) if they exist from A.1's testing setup.
- Files to Create: `tests/integration/test_home_content_safety_audit.py`
- Files to Modify: none
- Implementation Details: Parametrized test issuing `GET /v1/home` across a fixture matrix, recursively stringifying the JSON response and asserting none of `["subscribe","upgrade","$","price","billing","trial","renew"]` (case-insensitive) appear anywhere.
- Business Rules: This test must be CI-blocking (wired in Task 07/B-08).
- Validation: N/A.
- Error Handling: N/A.
- Security: This IS the security control verification.
- Performance: N/A.
- Localization: Run matrix across at least English and Arabic fixture locales to ensure translated billing terms aren't missed (flag as a known limitation if translated-term blocklist isn't yet available — coordinate with B-08 for full localization of the blocklist).
- RTL: N/A.
- Analytics: N/A.
- Tests: This task is itself the test suite.
- Documentation: Comment block explaining why this test exists and its zero-tolerance policy.
- Dependencies: Task 05.
- Do Not Change: Do not weaken the blocklist without Trust & Safety sign-off (per PRD §15.1).
- Expected Result: Passing safety-audit test suite.
- Definition of Done: Suite runs green against the full fixture matrix; wired into CI (finalized in B-08).

## 30. Definition of Done
- `GET /v1/home` returns the exact fixed-order contract, `200` under all single-upstream-failure scenarios, and never leaks billing content across the fixture matrix.
- All unit and integration tests (Tasks 01–06) pass in CI.
- p95 latency targets met in load test (cold < 1.2s, warm < 300ms).
- OpenAPI docs updated.

## 31. Final Verification Checklist
- [x] Fixed section order verified via snapshot test
- [x] `bedtime_corner` is a present key with `null` value outside window, including midnight-crossing windows
- [x] Response-shaping allowlist strips any unexpected upstream field
- [x] Per-section graceful degradation confirmed for all 7 upstream dependencies independently
- [x] Cross-child data isolation verified (tampered/foreign `child_id` rejected with zero leakage)
- [x] Redis cache hit/miss/partial-invalidation verified; Redis outage does not break the endpoint
- [x] Content-safety audit suite passes across the full fixture matrix
- [x] Rate limiting (30/min/child_session) enforced
- [x] p95 latency targets met under simulated load
- [x] PostgreSQL and Redis credentials unmodified
- [x] OpenAPI documentation updated
