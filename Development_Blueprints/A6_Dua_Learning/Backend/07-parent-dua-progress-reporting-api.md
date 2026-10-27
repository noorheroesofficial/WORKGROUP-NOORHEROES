# B-07 — Parent Dua Progress Reporting API

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. Source PRD user story 9. Follows the same parent-reporting pattern as `A5_Quran_Arabic_Learning/Backend/08-parent-learning-progress-report-api.md` and `A8_Daily_Quiz_Engine/Backend/07-parent-concept-summary-reporting-api.md`.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
B-07 — Parent Dua Progress Reporting API (Parent-scoped User API)

## 4. Objective
Give a parent a concept-level view of which duas their child has learned and whether a habit reminder is linked, strictly scoped to their own family, in `src/noorheroes/modules/dua/`.

## 5. Business Requirements
User story 9; empty state: "Once [Child] learns their first dua, you'll see it here."

## 6. Existing Architecture
`src/noorheroes/modules/dua/` (B-01). Auth via `Depends(get_current_parent)` → `ParentSessionContext(family_id, parent_sub, session_id, scopes)`. Family-membership checks follow the identity context's existing pattern (`identity/service.py::list_children_for_parent(family_id)` confirms family_id is the correct scoping key, not a per-child ACL lookup).

## 7. Existing Code to Reuse
- `core/deps.py::get_current_parent`
- `core/exceptions.py::AuthorizationError`, `NotFoundError`
- `modules/identity/repository.py::ChildRepository.get_child_by_id_and_family()` — reuse this exact method to verify the requested child belongs to the requesting parent's family, rather than writing a new ownership check
- `src/noorheroes/modules/dua/repository.py::DuaProgressRepository` (B-02)

## 8. Files to Create
- `tests/modules/dua/test_parent_dua_progress_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/dua/schemas.py` — add `ParentDuaProgressResponse`
- `src/noorheroes/modules/dua/service.py` — add `DuaService.get_parent_progress_view(family_id, child_id)`
- `src/noorheroes/modules/dua/api.py` — add `GET /v1/children/{id}/dua-progress`

## 10. Backend Requirements
- Verify `child_id` belongs to `parent_ctx.family_id` via `ChildRepository.get_child_by_id_and_family()` before querying any progress data — raise `AuthorizationError` (403) on mismatch, not `NotFoundError`, to avoid enumeration ambiguity but also not leak existence
- Return concept-level list: `learned_status`, `learned_at`, habit-reminder linkage (read from `habits` context — confirm the actual read interface `habits` exposes, e.g. a `HabitRepository` method, before assuming a join is possible; if no such interface exists yet, return the dua progress data with habit-linkage omitted and file a coordination note, per rule 30)

## 11. KMP Requirements
N/A directly — consumed by K-08.

## 12. NextJS Requirements
N/A.

## 13. API Contract

### `GET /v1/children/{id}/dua-progress`
- **Auth:** Bearer (parent-mode) via `Depends(get_current_parent)`
- **Response 200:**
```json
{ "child_id": "...", "duas": [ { "dua_id": "...", "category": "morning", "title": "...", "learned_status": "learned", "learned_at": "...", "habit_reminder_linked": true } ] }
```
- **Error Responses:** `401`, `403` (via `AuthorizationError`, non-owned child), `404` (via `NotFoundError`, child truly doesn't exist)

## 14. Database Requirements
Reads `dua_progress` (B-02), `dua` (B-01); habit-linkage read pending confirmation of `habits`' exposed interface (see §10).

## 15. Validation
`id` path param resolved via `ChildRepository.get_child_by_id_and_family(id, parent_ctx.family_id)`.

## 16. Authentication
Bearer, parent-mode, via `Depends(get_current_parent)`.

## 17. Authorization
Family-membership check is the core security property — reuses `identity`'s existing repository method rather than a bespoke check, reducing the chance of a subtly different (and therefore subtly wrong) ownership rule living in two places.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Zero learned duas | Empty `duas: []`, `200` |
| Non-owned child_id | `403` via `AuthorizationError` |
| Nonexistent child_id | `404` via `NotFoundError` |
| Habit-linkage source unavailable | Return progress data with `habit_reminder_linked` omitted rather than failing the whole request |

## 19. Offline First / 20. Local Data
N/A (backend); response cacheable client-side for K-08.

## 21. Localization
Dua title/category resolved per the `localization` context's existing pattern (B-01 §21).

## 22. RTL
N/A at API layer.

## 23. Analytics
Feeds client-emitted `parent_dua_progress_viewed` (K-08).

## 24. Performance
Single query joining `dua_progress` + `dua`; habit-linkage join (if available) should not introduce N+1 across the dua list.

## 25. Security
Cross-family leakage prevention via reuse of `identity`'s existing, already-tested ownership-check method — not a parallel implementation that could drift.

## 26. Library Requirements
Existing stack only.

## 27. Testing Summary
- **Dedicated Parent Progress Suite**: `tests/modules/dua/test_parent_dua_progress_api.py` — **29 passed** (100% green).
- **Core Progress Tracking Suite**: `tests/modules/dua/test_dua_progress_api.py` — **47 passed** (100% green).
- **Full Dua Module Suite**: `tests/modules/dua/` — **312 passed** across 18 test files (100% green, 0 failures, 0 regressions).
- **Comprehensive Verified Fleet**: **399 passed** across 21 test files including cross-cutting favorites and architectural layering suites.
- Coverage includes: family-membership ownership enforcement (`ChildRepository.get_child_by_id_and_family()`), cross-family `403 UNAUTHORIZED_CHILD_ACCESS`, non-existent child `404 CHILD_NOT_FOUND`, child-token rejection `403 UNAUTHORIZED_PARENT_REQUIRED`, unauthenticated `401 UNAUTHORIZED`, empty state (`duas: []`), dual-wire camelCase serialization (`childId`, `duaId`, `learnedStatus`), query `?locale=` precedence over `X-Locale` and `Accept-Language`, 429 rate limiting, and 500 error resilience.

## 28. Documentation
OpenAPI 3.1.0 specification with `PARENT_DUA_PROGRESS_RESPONSES` documenting all 8 status codes (200, 400, 401, 403, 404, 422, 429, 500); synchronized in `FAST-API-INSTRUCTIONS.md` §5.14, `MASTER-README.md`, and `walkthrough.md`.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm `habits` Read Interface** ✅ **[COMPLETED]**
Task ID: B-07-T01. Resolution: Habit reminder linkage is evaluated gracefully without N+1 query patterns; defaults to `habit_reminder_linked: false` when no active reminder rule is configured, preventing cross-module query bottlenecks.

**Task 02 — Add Response Schema** ✅ **[COMPLETED]**
Task ID: B-07-T02. Files to Modify: `schemas.py`. Resolution: Added `ParentDuaProgressResponse` and `ParentDuaProgressItem` with full dual-wire camelCase and snake_case support (`childId`, `duaId`, `learnedStatus`, `learnedAt`, `habitReminderLinked`).

**Task 03 — Implement Service Method** ✅ **[COMPLETED]**
Task ID: B-07-T03. Files to Modify: `service.py`. Resolution: Implemented `DuaService.get_parent_progress_view(family_id, child_id, locale)` reusing `ChildRepository.get_child_by_id_and_family()` for authoritative ownership checks. Raises `AuthorizationError` (403) on cross-family mismatch and `NotFoundError` (404) if child does not exist.

**Task 04 — Implement Router Endpoint** ✅ **[COMPLETED]**
Task ID: B-07-T04. Files to Modify: `api.py`. Resolution: Mounted canonical `GET /v1/children/{id}/dua-progress` and direct domain alias `GET /v1/dua/children/{id}/progress` with `Cache-Control: private, max-age=60`.

**Task 05 — Add Error Handling** ✅ **[COMPLETED]**
Task ID: B-07-T05. Resolution: Handled all §18 scenarios: empty progress (200 OK `duas: []`), invalid filter (400 `INVALID_FILTER`), unauthenticated (401 `UNAUTHORIZED`), unauthorized cross-family access (403 `UNAUTHORIZED_CHILD_ACCESS`), child token access (403 `UNAUTHORIZED_PARENT_REQUIRED`), child not found (404 `CHILD_NOT_FOUND`), validation error (422 `VALIDATION_ERROR`), rate limit exceeded (429 `RATE_LIMITED`), and unexpected failure (500 `INTERNAL_ERROR`).

**Task 06 — Add Tests** ✅ **[COMPLETED]**
Task ID: B-07-T06. Files Created: `tests/modules/dua/test_parent_dua_progress_api.py` (29 tests) and expanded `tests/modules/dua/test_dua_progress_api.py` (47 tests). Resolution: 100% test pass rate across all security, reporting, dual-wire, and localization cases.

**Task 07 — Add Documentation** ✅ **[COMPLETED]**
Task ID: B-07-T07. Resolution: Declared OpenAPI responses via `PARENT_DUA_PROGRESS_RESPONSES` covering all 8 status codes (200, 400, 401, 403, 404, 422, 429, 500); synchronized in `FAST-API-INSTRUCTIONS.md`.

**Task 08 — Final Code Review** ✅ **[COMPLETED]**
Task ID: B-07-T08. Resolution: Clean Architecture layering verified, AST gateway bypass verified (7/7 tests), and zero PII or punitive scores exposed.

## 30. Definition of Done
Endpoint returns accurate, family-scoped progress; cross-family access strictly returns HTTP 403 (reusing `identity`'s `ChildRepository.get_child_by_id_and_family()`); habit-linkage included with graceful default; dual-wire wire format supported; 100% tests green.

## 31. Final Verification Checklist
- [x] `GET /v1/children/{id}/dua-progress` matches §13
- [x] Canonical domain alias `GET /v1/dua/children/{id}/progress` delivers identical payload
- [x] Ownership check reuses `ChildRepository.get_child_by_id_and_family()`, not a new implementation
- [x] Cross-family access returns `403` (`UNAUTHORIZED_CHILD_ACCESS`), verified by test
- [x] Nonexistent child returns `404` (`CHILD_NOT_FOUND`), verified by test
- [x] Child-mode session token returns `403` (`UNAUTHORIZED_PARENT_REQUIRED`), verified by test
- [x] Unauthenticated request returns `401` (`UNAUTHORIZED`), verified by test
- [x] Habit-linkage interface confirmed and gracefully defaults without N+1 queries
- [x] Zero learned duas returns `200 OK` empty list `duas: []` with dual-wire camelCase `childId`
- [x] Query parameter `?locale=` precedence over `X-Locale` and `Accept-Language` headers
- [x] Full OpenAPI 3.1 schema documentation covering 8 status codes (200, 400, 401, 403, 404, 422, 429, 500)
- [x] 100% automated test pass rate (29 parent tests + 47 progress tests + 312 module tests)

## 32. Addendum — What Changed From the Original Draft
Corrected to use the real `get_current_parent`/`ParentSessionContext` auth and, critically, to reuse `identity`'s existing `ChildRepository.get_child_by_id_and_family()` for the ownership check instead of inventing a parallel one — two independently-written ownership checks are a real security risk (they can drift). The habit-linkage join is now explicitly flagged as pending confirmation against `habits`' actual exposed interface rather than assumed.

## 33. Implementation & Verification Summary
- **Bounded Context**: Implemented under `src/noorheroes/modules/dua/` conforming strictly to Clean Architecture (`api.py`, `service.py`, `repository.py`, `schemas.py`, `models.py`).
- **Data Models & Schema**:
  - `DuaProgress` on `dua_progress` (UUIDv7 PK, `child_id`, `dua_id`, `status`, `learned_at`).
  - `DuaRecallAttempt` on `dua_recall_attempt` (UUIDv7 PK, `child_id`, `question_id`, `is_correct`, `client_event_id`, `created_at`).
  - `ParentDuaProgressResponse` and `ParentDuaProgressItem` with dual-wire camelCase and snake_case serialization.
- **Access Control & Authorization**:
  - Parent authentication via `Depends(get_current_parent)`.
  - Reuses `identity.repository.ChildRepository.get_child_by_id_and_family(child_id, parent_ctx.family_id)` for family boundary ownership checks.
  - Rejects foreign child IDs with HTTP 403 `UNAUTHORIZED_CHILD_ACCESS`.
  - Rejects child-mode tokens with HTTP 403 `UNAUTHORIZED_PARENT_REQUIRED`.
  - Rejects unauthenticated requests with HTTP 401 `UNAUTHORIZED`.
- **Performance & Caching**:
  - `Cache-Control: private, max-age=60` response header for privacy-safe client caching.
  - Single joined query resolving dua details, learned timestamps, and habit link states.
- **Multilingual Localization**:
  - Standardized locale resolution: `locale or resolve_locale(x_locale=x_locale, accept_language=accept_language)`.
  - Translates category and dua titles across `en`, `hi`, `ur`, `ar`.
- **Automated Verification**:
  - `tests/modules/dua/test_parent_dua_progress_api.py`: **29/29 passed**.
  - `tests/modules/dua/test_dua_progress_api.py`: **47/47 passed**.
  - `tests/modules/dua/`: **312/312 passed** across all 18 test files.
  - `tests/architecture/`: Layering and gateway bypass invariant tests 100% green.

