# B-02 — Child Fact-of-the-Day Selection API

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). This is the primary child-facing (User API) surface — the endpoint Home's Fact of the Day card and any spaced-repetition resurfacing prompt ultimately resolve to. It is the canonical successor to A.2/B-07's legacy `GET /v1/facts/daily`, to be cut over via B-08.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
1.2 Child Fact-of-the-Day Selection API (ID: B-02) — **User API**

## 4. Objective
Implement `GET /v1/facts/daily` selecting an age-band/locale-appropriate, scholar-approved, deduplicated, seasonally-weighted fact for the requesting child, with graceful fallback at every failure point rather than ever returning "no fact."

## 5. Business Requirements
- FR-1, FR-8, FR-10, FR-11 (see PRD §1.7).
- Acceptance Criteria: fact appropriate to age band/locale, not previously seen within the recent dedup window; excludes any fact whose approval is revoked.
- Edge Case 1: age-band rollover resolves correctly on next selection without special migration.
- Edge Case 2: small catalog → dedup window gracefully relaxes rather than returning nothing.
- Edge Case 4: same fact instance not shown twice across surfaces (Home card vs. resurfacing prompt) on the same day for one child.
- Edge Case 7: exhausted seasonal pool → fall back to general pool.
- NFR: Fact-of-the-Day selection p95 < 300ms (cacheable, low-churn data).
- Error Handling table: selection service failure → cached/default evergreen fact, never "no fact."

## 6. Existing Architecture
New service within the existing `content` bounded context, `FactSelectionService`, layered Router → Service → Repository per `FAST-API-INSTRUCTIONS.md` §1. Uses B-01's `FactVersionRepository.get_published_version()` and `FactSeenLogRepository`. Redis (`infrastructure/redis.py`) used for the daily-stable response cache — no new caching infrastructure.

## 7. Existing Code to Reuse
- B-01: `FactVersionRepository`, `FactSeenLogRepository`, `ScholarApprovalRepository`.
- `core/deps.py` → `get_current_child`, `ChildSessionContext` (age band derived exclusively server-side, never from a client parameter).
- `common/utils/age_band.py` → `AgeBand` enum.
- `infrastructure/redis.py` → `get_redis_pool()`.
- Existing seasonal-mode resolver (Ramadan/Eid detection) — confirm exact existing service before assuming a new one is needed (cross-ref A.2's occasion resolver retained under B-08).

## 8. Files to Create
- `src/noorheroes/modules/content/services/fact_selection_service.py` — `FactSelectionService(BaseService)`.
- `src/noorheroes/modules/content/api/facts_router.py` — `GET /v1/facts/daily`.
- `src/noorheroes/modules/content/deps.py` (extend) — `get_fact_selection_service` factory.
- `tests/modules/content/test_fact_daily_selection.py`.
- `tests/modules/content/test_fact_dedup_relaxation.py`.
- `tests/modules/content/test_fact_seasonal_fallback.py`.

## 9. Files to Modify
- `src/noorheroes/api/router.py` — register `facts_router` (or extend existing `content` router aggregator).

## 10. Backend Requirements
- `GET /v1/facts/daily?child_id=`, auth `Depends(get_current_child)`.
- Resolve age-band/locale text variant via `FactVersionRepository.get_published_version()` (approval-gated).
- Dedup: exclude facts present in `FactSeenLogRepository.get_recent_seen_ids(child_id, window_days=30)`; relax window progressively (e.g., 30 → 14 → 7 → 0 days) if the eligible candidate set is empty at each step, rather than returning zero candidates (Edge Case 2).
- Seasonal weighting: when a seasonal mode is active, bias candidate selection toward seasonally-tagged facts; if that pool is exhausted for the child this season, fall back to the general eligible pool (Edge Case 7).
- Same-day cross-surface distinctness: track today's already-selected fact_id in the daily cache key so a resurfacing prompt elsewhere doesn't independently select the identical fact instance the same day (Edge Case 4).
- Cache response in Redis keyed `(child_age_band, locale, local_date)`, TTL to end of local day.
- On selection-service failure (DB error, timeout): fall back to a configured evergreen/default fact rather than an error response.
- Record the selected fact in `fact_seen_log` upon successful selection (not upon mere card render — confirm exact "seen" semantics against A.2's original B-07 definition before finalizing, since B-08's migration depends on consistent semantics).

## 11. KMP Requirements
Consumed by K-01 (`FactsRepository.getDailyFact()`). No KMP code produced here; interface contract only.

## 12. NextJS Requirements
N/A — child-facing endpoint only.

## 13. API Contract
**Endpoint:** `GET /v1/facts/daily`
**Method:** GET
**Auth:** Bearer, child-mode (`Depends(get_current_child)`)
**Query Params:** `child_id` (implicit from session; not client-suppliable as an override)
**Request:** none
**Response 200:**
```json
{ "fact_id": "...", "text": "...", "topic": "...", "scholar_approved": true, "approval_version": "v3" }
```
**Authorization:** Age band derived exclusively from `ChildSessionContext`; never trusts a client-suppliable age-band parameter.
**Validation:** Approval-gated (B-01), dedup-applied, seasonally-weighted.
**Error Responses:** `401` (invalid/missing child session). No error for zero-candidate scenarios — always resolves to a fact via graceful degradation (§10).

## 14. Database Requirements
Reads: `fact`, `fact_version`, `scholar_approval` (via B-01's gated join), `fact_seen_log`. Writes: `fact_seen_log` (append-only insert on selection).

## 15. Validation
`child_id` resolved server-side only; any client-supplied age-band-shaped parameter is parsed but structurally ignored, never read into the filter-building code path (mirroring B.13's search age-band enforcement pattern).

## 16. Authentication
`Depends(get_current_child)`; `401 AuthenticationError` on invalid/missing token.

## 17. Authorization
Implicit — a child session can only ever request their own daily fact; no child_id override parameter exists.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Selection service DB failure | Cached/default evergreen fact returned |
| Eligible pool empty even after full dedup relaxation | Falls back to evergreen default fact (documented last-resort path) |
| Seasonal pool exhausted | Falls back to general pool (Edge Case 7) |
| Invalid/missing child session | `401` |

## 19. Offline First
N/A — backend endpoint. Offline caching of the response is K-03's concern.

## 20. Local Data
N/A — backend.

## 21. Localization
Text variant resolved per `child`'s locale (English, Hindi, Arabic, Urdu) via `FactVersionRepository`.

## 22. RTL
N/A at API layer — plain text response, RTL rendering is a KMP concern.

## 23. Analytics
Emits internal signal `fact_selection_fallback_used` (Edge Case 2/7 telemetry) and `fact_scholar_approval_revoked_excluded` when a candidate is excluded due to revocation — both consumed by the Analytics Event Bus, not returned in the API response.

## 24. Performance
p95 < 300ms target; Redis cache keyed per `(age_band, locale, local_date)` since "today's fact" is stable per child per day; dedup query uses the `(child_id, seen_at DESC)` index from B-01.

## 25. Security
No new attack surface; age-band derivation is exclusively server-side (§15), consistent with the platform's established pattern (cross-ref B.13's identical child-session-derived-eligibility approach).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Redis client — all existing platform dependencies.

## 27. Testing
- Unit: normal-pool-size dedup strictly enforced.
- Unit: small-pool-size graceful relaxation (progressive window shrink) rather than empty result.
- Unit: seasonal-pool-exhausted fallback to general pool.
- Unit: age-band rollover resolves correctly without special migration (Edge Case 1).
- Unit: revoked-approval fact excluded from candidate set.
- Integration: full daily-selection flow against fixture multi-age-band/locale catalogs.

## 28. Documentation
OpenAPI docstring for `GET /v1/facts/daily` including the graceful-degradation behavior (so consumers know a `200` is always returned, never an error, for this endpoint).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `FactSelectionService.select_daily_fact()`**
Objective: Core selection algorithm (dedup → seasonal weighting → fallback).
Why Required: Central business logic for this endpoint.
Existing Architecture to Follow: `BaseService` pattern, B-01 repositories.
Files to Create: `services/fact_selection_service.py`.
Implementation Details: Progressive dedup-window relaxation loop; seasonal-pool-then-general-pool candidate resolution; evergreen fallback on any failure.
Business Rules: Edge Cases 1, 2, 4, 7.
Error Handling: Never raises for "no candidates" — always resolves via fallback chain.
Performance: Single query per relaxation step, capped iteration count.
Dependencies: B-01 complete.
Expected Result: Deterministic fact selection given a fixture catalog.
Definition of Done: Passes all Task 05 tests.

**Task 02 — Implement Router Endpoint**
Objective: `GET /v1/facts/daily` wired to the service.
Files to Create: `api/facts_router.py`.
Dependencies: Task 01.
Expected Result: Endpoint returns `FactResponse` shape from §13.
Definition of Done: Manual curl/Postman verification against local dev DB.

**Task 03 — Redis Caching Layer**
Objective: Cache response per `(age_band, locale, local_date)`.
Files to Modify: `services/fact_selection_service.py`.
Dependencies: Task 01, Task 02.
Expected Result: Second request within the same day hits cache, not DB.
Definition of Done: Cache-hit verified via Redis key inspection in test.

**Task 04 — Same-Day Cross-Surface Distinctness**
Objective: Ensure resurfacing prompt doesn't duplicate the exact Home-card fact same day.
Implementation Details: Track today's already-selected fact_id in the cache entry; exclude it from resurfacing candidate pool for the same day.
Dependencies: Task 03.
Expected Result: Edge Case 4 satisfied.
Definition of Done: Test confirms no duplicate same-day instance across surfaces.

**Task 05 — Tests**
Objective: Full coverage per §27.
Dependencies: Tasks 01–04.
Expected Result: All green.
Definition of Done: CI passes, including dedup/seasonal-fallback edge cases.

**Task 06 — API Documentation**
Objective: OpenAPI docstring updates.
Dependencies: Task 05.
Definition of Done: `/docs` reflects accurate always-200 behavior.

## 30. Definition of Done
- Endpoint never returns "no fact" for any reachable state — every failure path resolves to a fallback fact.
- Dedup relaxation and seasonal fallback both verified by tests.
- Age band exclusively server-derived; no client override path exists.
- Redis caching functioning per day-stable key.
- Documentation updated.

## 31. Final Verification Checklist
- [ ] Approval-gated selection (no revoked fact ever selectable)
- [ ] Dedup: normal pool strict, small pool gracefully relaxed
- [ ] Seasonal weighting with exhausted-pool fallback
- [ ] Same-day cross-surface distinctness (Edge Case 4)
- [ ] Age-band rollover handled without migration (Edge Case 1)
- [ ] p95 < 300ms verified under load test
- [ ] Client cannot override age-band via any parameter
- [ ] Evergreen fallback verified for total selection-service failure
- [ ] Tests green, documentation updated
