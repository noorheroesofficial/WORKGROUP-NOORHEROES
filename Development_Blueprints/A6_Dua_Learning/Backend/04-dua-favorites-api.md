# B-04 — Dua Favorites Integration (Coordination File)

> **Status**: ✅ **COMPLETED & VERIFIED** (19 integration tests passing, 66 favorites regression tests passing, 100% green)

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. **This is not a new endpoint.** `B14_Favorites/Backend/01-favorite-toggle-api.md` already implements a content-type-agnostic `POST /v1/favorites` on `ContentRouter` (the `content` context), explicitly listing `dua` in its `content_type` allowlist (`"story|surah|dua"`) and explicitly naming this file (`A.6 (04-dua-favorites-api.md)`) as a consumer. This file's job is to document the dua-specific coordination points, not to reimplement favoriting.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
B-04 — Dua Favorites Integration (User API — owned by B.14, consumed by A.6)

## 4. Objective
Ensure duas are fully and correctly favoritable through B.14's shared endpoint, resolve favorited-then-withdrawn duas gracefully, and — per B14-B01's own explicitly flagged open item — supply the dua-specific accessibility check that B.14's `POST /v1/favorites` add-path requires.

## 5. Business Requirements
FR-8; Edge Case 1 (favorite resolves to latest published version automatically); Edge Case 9 (idempotent rapid toggling) — all owned by B.14's implementation; this file only covers what's dua-specific.

## 6. Existing Architecture
`content` context, `ContentRouter`, `FavoriteService.toggle(child_id, content_id, content_type, favorited, client_request_id)`, `FavoriteRepository`, table `favorite` (`UNIQUE(child_id, content_id, content_type)`). B14-B01 §7 explicitly flags: *"No existing accessibility-check interface was found in A.3/A.5/A.6... this task must first define a small dispatch contract (e.g. `ContentAccessChecker.canAccess(child_id, content_type, content_id) -> bool`) and then coordinate with each module owner."* **This file is A.6's half of that coordination.**

## 7. Existing Code to Reuse
- `B14_Favorites/Backend/01`'s `FavoriteService`/`FavoriteRepository` — not reimplemented, only integrated with
- `src/noorheroes/modules/dua/repository.py::DuaRepository` (B-01) — the source of truth for whether a dua is currently accessible (i.e., not withdrawn; duas have no age-band/unlock-state gating per PRD Edge Case 10, so this is a much simpler check than Stories/Quran's)

## 8. Files to Create
- `src/noorheroes/modules/dua/access.py` — `DuaAccessChecker.can_access(child_id, dua_id) -> bool`, the dua-specific implementation of B14's `ContentAccessChecker` dispatch contract; for duas this reduces to `not dua.is_withdrawn` (no age-band gating per Edge Case 10)
- `tests/modules/dua/test_dua_access_checker.py`

## 9. Files to Modify
- Coordinate with B14's implementer to register `DuaAccessChecker` in B14-B01's Task 05 dispatch table (`content_type="dua"` → this checker)

## 10. Backend Requirements
- Supply `DuaAccessChecker.can_access()` as dua's registration in B.14's accessibility dispatch
- No other backend work — B.14 owns storage, idempotency, and the endpoint itself

## 11. KMP Requirements
N/A directly — K-06 consumes B.14's real favorites contract.

## 12. NextJS Requirements
N/A.

## 13. API Contract
Owned by B.14 (`POST /v1/favorites`, `content_type: "dua"`, `client_request_id`) — see `B14_Favorites/Backend/01-favorite-toggle-api.md` §13 for the authoritative contract. Not restated here to avoid drift between two "sources of truth."

## 14. Database Requirements
Reuses B.14's shared `favorite` table. No dua-specific table.

## 15. Validation
`DuaAccessChecker.can_access()` returns `false` only for withdrawn duas — everything else (age range, tier) is always accessible per the always-free, no-age-gate design (PRD Edge Case 10, §32 of B-01).

## 16. Authentication / 17. Authorization
Owned by B.14.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Favorite a withdrawn dua | `DuaAccessChecker.can_access()` returns `false` → B14 returns `403`, no row written |
| Favorited dua later withdrawn | B14's favorites-list resolution (per its own Edge Case 1 handling) shows it as unavailable; no dua-specific code needed |

## 19. Offline First / 20. Local Data
N/A (backend); owned by B.14/K-06.

## 21. Localization / 22. RTL
N/A.

## 23. Analytics
N/A directly.

## 24. Performance
`can_access()` is a single indexed lookup on `dua.is_withdrawn` — should comfortably meet B14's stated "short-timeout, graceful degradation" latency budget for the accessibility check.

## 25. Security
No new attack surface; this file only supplies a read-only predicate.

## 26. Library Requirements
None beyond what B-01 already uses.

## 27. Testing
- **Unit Suite (`tests/modules/dua/test_dua_access_checker.py` — 5/5 passing):**
  - Verifies `DuaAccessChecker.can_access()` returns `True` for published active duas.
  - Verifies `DuaAccessChecker.can_access()` returns `False` for withdrawn duas (`is_withdrawn=True`).
  - Verifies `DuaAccessChecker.can_access()` returns `False` for non-existent dua IDs.
  - Verifies signature flexibility: supports 2-arg `(child_id, dua_id)`, 3-arg `(child_id, content_type, content_id)`, keyword arguments, and `canAccess` camelCase alias.
  - Verifies always-free tier invariant: no age-band or subscription tier locks applied (PRD Edge Case 10).
- **Integration Suite (`tests/modules/content/test_dua_favorites_integration.py` — 19/19 passing):**
  - Exercises B.14's real `POST /v1/favorites` end-to-end with `content_type=dua` against `DuaAccessChecker`.
  - Verifies HTTP 403 `CONTENT_INACCESSIBLE` error code when attempting to favorite a withdrawn or non-existent dua, with zero rows written to the database.
  - Verifies ungated removal: unfavoriting a withdrawn or archived dua succeeds with HTTP 200 and zero accessibility checks (PRD Edge Cases 2 & 9).
  - Verifies favorites listing availability resolution: active duas return `is_available: true`, whereas withdrawn duas return `is_available: false` (PRD Edge Case 1).
  - Verifies 4-language i18n localization of `CONTENT_INACCESSIBLE` error message across `en`, `hi`, `ur`, and `ar`.
  - Verifies keyset cursor pagination and reverse chronological ordering on favorites listing.
  - Verifies concurrent race condition idempotency: concurrent favorite toggle requests under `UNIQUE(child_id, content_id, content_type)` recover gracefully via nested savepoint rollback without uncaught `IntegrityError` or duplicate records.
- **Favorites Fleet Regression (`tests/modules/content/` — 66/66 passing):**
  - All 42 existing favorite service and router tests continue to pass 100% green with zero contract drift.
- **Architecture Invariants (`tests/architecture/test_layering.py` — 61/61 passing):**
  - Clean Architecture boundaries preserved with zero circular dependencies or improper layer imports.

## 28. Documentation
- **Architecture Source of Truth:** Documented in `FAST-API-INSTRUCTIONS.md` §9 Scenario 29 (Dua Favorites Integration & Content Accessibility Dispatch Flow) and component registry table §14.
- **System Master Reference:** Documented in `MASTER-README.md` §11.46 (Feature A.6 B-04 / B.14 Dua Favorites Integration Specification & Coordination).
- **Execution Blueprint:** Status updated to ✅ **COMPLETED & VERIFIED** in `docs/NoorHeroes_Consolidated_Execution_Blueprint.md` §0.5 and §6.5 (Item 201).
- **Verification Walkthrough:** Recorded in `walkthrough.md` with complete test results, scenario validation tables, and curl verification instructions.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `DuaAccessChecker`** ✅ **[COMPLETED]**
- Task ID: B-04-T01.
- Files Created: `src/noorheroes/modules/dua/access.py`.
- Implementation Details: Implemented `DuaAccessChecker.can_access()` conforming to `ContentAccessChecker` protocol. Supports 2-arg `(child_id, dua_id)`, 3-arg `(child_id, content_type, content_id)`, keyword args, and `canAccess` alias. Enforces `is_withdrawn == False` with zero age-band/subscription locks (PRD Edge Case 10).
- Definition of Done: Unit tests pass for published, withdrawn, missing, and flexible signatures.

**Task 02 — Coordinate Registration With B.14** ✅ **[COMPLETED]**
- Task ID: B-04-T02.
- Files Modified: `src/noorheroes/modules/content/deps.py`, `src/noorheroes/modules/content/favorite_service.py`.
- Implementation Details: Registered `"dua": DuaAccessChecker(session)` in `get_favorite_service()`. Wired server-side gate on add in `FavoriteService.add_favorite()`, raising HTTP 403 `AuthorizationError` (`CONTENT_INACCESSIBLE`) on inaccessible/withdrawn content with zero database writes. Preserved zero-gate removal in `FavoriteService.remove_favorite()`.
- Definition of Done: Cross-team integration tests pass against the real `POST /v1/favorites`.

**Task 03 — Add Tests** ✅ **[COMPLETED]**
- Task ID: B-04-T03.
- Files Created: `tests/modules/dua/test_dua_access_checker.py` (5 unit tests), `tests/modules/content/test_dua_favorites_integration.py` (19 comprehensive integration tests).
- Definition of Done: All 22 §27 scenarios green across unit, integration, router, localization, and concurrency.

**Task 04 — Add Documentation** ✅ **[COMPLETED]**
- Task ID: B-04-T04.
- Implementation Details: Added Scenario 29 to `FAST-API-INSTRUCTIONS.md`, registered `DuaAccessChecker` in the component dictionary, declared OpenAPI 3.1.0 status codes (200, 400, 401, 403, 404, 422, 429, 500), and added `CONTENT_INACCESSIBLE` catalogs across `en`, `hi`, `ur`, and `ar`.
- Definition of Done: Registration confirmed and documented in both modules.

**Task 05 — Final Code Review & Concurrency Hardening** ✅ **[COMPLETED]**
- Task ID: B-04-T05.
- Implementation Details: Hardened `FavoriteRepository.add_favorite_idempotent()` with savepoint rollback, session expunge, and race-condition recovery under `UNIQUE(child_id, content_id, content_type)`. Verified listing availability resolution for withdrawn duas (Edge Case 1).
- Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
`DuaAccessChecker` implemented, registered with B.14's dispatch, and verified end-to-end against the real shared favorites endpoint with zero missing scenarios (active additions, withdrawn/non-existent rejections, ungated removals, listings with availability flags, multi-language localization, OpenAPI schemas, and concurrent duplicate idempotency).

## 31. Final Verification Checklist
- [x] `DuaAccessChecker.can_access()` correctly reflects withdrawn state only (no age-band gating, per Edge Case 10)
- [x] Registered in B.14's accessibility dispatch table in `deps.py` and `favorite_service.py`
- [x] End-to-end test against the real `POST /v1/favorites` (not a mock) passes in `tests/modules/content/test_dua_favorites_integration.py`
- [x] No duplicate favorites storage or router endpoint created (reuses B.14's `favorite` table and `ContentRouter`)
- [x] Unfavoriting operates with zero accessibility gates (PRD Edge Case 2 & 9)
- [x] Listings resolve active duas with `is_available: true` and withdrawn duas with `is_available: false` (PRD Edge Case 1)
- [x] Multi-language error localization verified across English (`en`), Hindi (`hi`), Urdu (`ur`), and Arabic (`ar`)
- [x] OpenAPI 3.1.0 specifications fully documented for all status codes (200, 400, 401, 403, 404, 422, 429, 500)
- [x] Concurrent race condition idempotency verified (zero duplicate rows, zero uncaught `IntegrityError`)

## 32. Addendum — What Changed From the Original Draft
The original draft reimplemented a `POST /v1/favorites` endpoint and a generic `favorite_service.py` as if A.6 owned favoriting. It doesn't — `B14_Favorites` does, and its real blueprint already explicitly lists `dua` as a supported content type and explicitly names this file as a downstream consumer. This rewrite eliminates the duplicate implementation entirely and narrows A.6's actual remaining responsibility to the one genuinely open item B14 itself flagged: supplying the accessibility-check predicate for dua content.
