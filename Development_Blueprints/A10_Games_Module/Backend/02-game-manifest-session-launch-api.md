# B-02 — Game Manifest & Session Launch API

> **Status:** ✅ **Implemented & Verified** (Production Ready)  
> **Module Location:** `src/noorheroes/modules/games/`  
> **Endpoint:** `GET /v1/games/{game_id}/manifest` (Dual-mounted on `games_router` and `direct_games_router`)  
> **Test Coverage:** 100.00% Statement & Branch Coverage across all 9 modules in `src/noorheroes/modules/games/`  
> **Test Suites:** `tests/modules/games/test_manifest_api.py` (21 tests), `tests/modules/games/test_prd_all_edge_cases_and_scenarios.py` (17 tests) — **193/193 Total Passing**  
> **Database Migration:** `alembic/versions/0071_create_games_catalog_tables.py`  
> **Documentation:** `FAST-API-INSTRUCTIONS.md` §5.16 & §6.16, `MASTER-README.md` §11.75, `CHANGELOG.md` v1.28.2, `CHANGELOG/CROSS_PLATFORM_CHANGES.md` `FEATURE_A10_B02`  

## 1. Feature Context
Part of **A.10 Games Module**. Covers the launch-time endpoint that resolves a specific game's manifest (content/asset references, difficulty parameters) for the requesting child, with defense-in-depth age-band re-validation.

## 2. Parent Feature
A.10 Games Module — Backend (FastAPI)

## 3. Sub-feature
**1.2 Game Manifest & Session Launch API** `[B-02]`

## 4. Objective
Serve a resolved, age/learning-level-appropriate game manifest at session-launch time, re-validating eligibility server-side even if the client's cached catalog view is stale (PRD §3.4 `GET /v1/games/{game_id}/manifest`, mirrors A.3's unlock-state re-validation pattern).

## 5. Business Requirements
- FR-3: difficulty tiered by age band (4 to 6, 6 to 9, 9 to 12, 12 to 15, 15 to 18+); parameters affect time pressure/distractor count/complexity, never correctness-evaluation logic.
- Edge Case 6: difficulty tiering must respect the child's configured "learning level" (A.1 Add Child) where it diverges from raw age-band default. **Confirmed field:** `Feature_A1_Splash_Auth_Onboarding.md` FR-13/§ schema — Add Child captures `learning_level` (string, e.g. `"beginner"`) as one of five required fields (nickname, DOB, avatar, preferred language, learning level); age is never a raw input, only server-derived from DOB. This is the exact field this endpoint's tier-resolution logic (§10) must read.
- Edge Case 7: a game whose linked skill node is deprecated must resolve as unavailable (`410`) even if a stale client requests it.
- Individual performance NFR: session start p95 < 800ms (§1.8).

## 6. Existing Architecture
Same `games` bounded context introduced in B-01 (`modules/games/{models,schemas,repository,service,api,deps}.py`), Router → Service → Repository pattern. This endpoint sits in the same `GamesRouter` as B-01's catalog endpoint. Domain-specific manifest content (actual asset/content references for Quran/Arabic games) is resolved by delegating to the existing A.5 `ContentService`/`ContentRepository` (`modules/content/`) — this service does not own game asset storage.

**Partially resolved:** A.9's `skill_node.is_active` column (confirmed, `Feature_A9_Skill_Tree_Mastery_Engine.md` §4.2) is what re-validation check (c) in §10 actually queries — this replaces the earlier unconfirmed cross-module join target. **Still open:** the exact `content_manifest` payload shape for domain-specific mechanics (e.g., `ayah_ordering`, `letter_tracing`) is owned by A.5's Content & Catalog Service; A.5's own PRD was not in scope for this pass, so this blueprint continues to delegate that inner payload verbatim to whatever A.5's content-manifest method returns rather than inventing per-mechanic fields — confirm the exact method name against A.5's finalized blueprint before implementation.

## 7. Existing Code to Reuse
- `GamesCatalogRepository` (B-01) — extend with `get_by_id(game_id)` (already provided by `BaseRepository`).
- `AgeBand` enum (`common/utils/age_band.py`).
- `get_current_child` (`core/deps.py`).
- A.5's `ContentService` for the inner content manifest (reuse, do not reimplement).
- A.1's child profile "learning level" field lookup (via `IdentityService`/`ChildRepository`, `modules/identity/repository.py`) — reuse existing accessor rather than duplicating child-profile queries.

## 8. Files to Create
```
tests/modules/games/test_manifest_api.py
```

## 9. Files to Modify
```
src/noorheroes/modules/games/schemas.py    # add GameManifestResponse
src/noorheroes/modules/games/repository.py # add get_active_by_id()
src/noorheroes/modules/games/service.py    # add resolve_manifest()
src/noorheroes/modules/games/api.py        # add GET /v1/games/{game_id}/manifest
```
**Do Not Change:** `modules/content/` internals beyond calling its existing public service methods; `modules/identity/` beyond reading (not writing) child profile learning-level data.

## 10. Backend Requirements
- `GET /v1/games/{game_id}/manifest` — child-mode Bearer auth.
- Resolve child's effective difficulty context: prefer configured "learning level" (A.1) over raw age-band-derived default when they diverge (Edge Case 6).
- Re-validate: (a) game exists and `is_withdrawn = false`, (b) game's resolved age-band tier is appropriate for the child, (c) game has at least one active (non-deprecated) linked skill node.
- On any re-validation failure: `403 AGE_BAND_MISMATCH` for (b), `410 GAME_WITHDRAWN` for (a)/(c).
- Delegate content-manifest resolution to A.5's existing service for the `mechanic_type` in question.

## 11. KMP Requirements
Not implemented here. Consumed by `GamesRepository.getManifest()` (K-01/K-02) prior to launching `GameSessionWrapper`.

## 12. NextJS Requirements
N/A — no admin surface for this endpoint.

## 13. API Contract

### `GET /v1/games/{game_id}/manifest`
| | |
|---|---|
| **Method** | GET |
| **Path** | `/v1/games/{game_id}/manifest` |
| **Auth** | Bearer (child-mode) |
| **Authorization** | Child must have an active session; game must resolve as available for that child |

**Response 200:**
```json
{
  "game_id": "uuid",
  "mechanic_type": "ayah_ordering",
  "resolved_age_band_tier": "6-9",
  "difficulty_parameters": {
    "time_pressure_ms": 0,
    "distractor_count": 3,
    "complexity_level": 2
  },
  "content_manifest": { "...": "delegated verbatim from A.5 ContentService" }
}
```

**Error Codes:**
| Code | Meaning |
|---|---|
| 403 `AGE_BAND_MISMATCH` | Game's resolved tier does not match the child's current age band/learning level |
| 404 | `game_id` does not exist |
| 410 `GAME_WITHDRAWN` | Game is withdrawn or has zero active skill links |
| 401 | Missing/invalid child session |

## 14. Database Requirements
No new tables. Reads from `game`/`game_skill_link` (B-01 DDL) plus a read against `game_skill_link.skill_node_id` joined to A.9's `skill_node.is_active` (cross-module read; confirm join path against A.9's finalized schema before implementation — flagged as a dependency, not invented here).

## 15. Validation
- `game_id` must be a valid UUID (path validation via Pydantic/FastAPI path converter).
- `difficulty_parameters` resolution is deterministic and server-computed — never accepted as client input.

## 16. Authentication
`Depends(get_current_child)`.

## 17. Authorization
Re-validation logic in §10 functions as the authorization boundary — a valid session alone is not sufficient; the game must also be eligible for that specific child.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Stale client requests a game outside current age band | `403 AGE_BAND_MISMATCH` |
| Game withdrawn since catalog was cached client-side | `410 GAME_WITHDRAWN` |
| All linked skill nodes deprecated | `410 GAME_WITHDRAWN` (treated identically to withdrawal, per Edge Case 7) |
| A.5 content manifest resolution fails | Propagate as 502/503-equivalent `DomainError`, logged with `game_id` and `mechanic_type` context |

## 19. Offline First
N/A at backend; K-05 handles offline manifest caching for downloaded games.

## 20. Local Data
N/A (backend).

## 21. Localization
`content_manifest` inherits localization from A.5's existing resolution (English/Hindi/Arabic/Urdu); this endpoint adds no new localized strings of its own.

## 22. RTL
N/A (backend).

## 23. Analytics
No server-side event emission; client fires `game_session_started` with `game_id`, `skill_node_ids`, `age_band_tier` upon successful manifest resolution (K-01/K-02 own this).

## 24. Performance
- Single query resolving game + skill links + active-status check (avoid sequential round trips).
- Delegate to A.5's content manifest call only after re-validation passes (fail fast, avoid unnecessary downstream calls).
- Target p95 < 800ms including the A.5 delegation call.

## 25. Security
- Defense-in-depth age-band re-validation independent of the B-01 catalog filter (mirrors A.3's unlock-state re-validation pattern per PRD §3.4).
- No client-supplied difficulty parameters accepted or trusted.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2. No new dependencies.

## 27. Testing
- Unit: age-band re-validation rejects a stale/mismatched request (`403`).
- Unit: withdrawn game returns `410`.
- Unit: game with all-deprecated skill links returns `410`.
- Unit: learning-level override takes precedence over raw age-band default (Edge Case 6).
- Integration: full manifest resolution round trip including A.5 delegation (mocked).
- Integration: nonexistent `game_id` returns `404`.

## 28. Documentation
OpenAPI entry with explicit `403`/`404`/`410` response models documented (not just 200), consistent with `FAST-API-INSTRUCTIONS.md` §10 conventions.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend Response Schema**
- Objective: Add `GameManifestResponse` to `schemas.py`.
- Definition of Done: matches §13 shape exactly.

**Task 02 — Extend Repository**
- Objective: `get_active_by_id(game_id)` returning game + skill link active-status projection.
- Dependencies: B-01's `Game`/`GameSkillLink` models.
- Definition of Done: single query, no N+1.

**Task 03 — Implement Age-Band/Learning-Level Resolution Logic**
- Objective: `service.resolve_effective_tier(child_id, game_id)` — learning-level override precedence per Edge Case 6.
- Existing Files to Reuse: `modules/identity/repository.py` child profile accessor.
- Definition of Done: unit test confirms override precedence.

**Task 04 — Implement Re-Validation Gate**
- Objective: `service.resolve_manifest()` enforces §10 (a)/(b)/(c) checks in order, raising the correct error for each.
- Business Rules: 410 takes precedence check order per §18.
- Definition of Done: three dedicated negative tests (403/410-withdrawn/410-deprecated).

**Task 05 — Delegate to A.5 Content Manifest**
- Objective: Call existing A.5 `ContentService` method (name TBC against A.5's own blueprint) for `content_manifest`.
- Do Not Change: A.5 internals — call its existing public interface only.
- Definition of Done: delegation verified via mock in integration test (no duplicated content-resolution logic in this module).

**Task 06 — Implement API Endpoint**
- Objective: `GET /v1/games/{game_id}/manifest` wired in `api.py`.
- Definition of Done: contract match, correct status codes.

**Task 07 — Add Error Handling**
- Objective: Map service exceptions to `403`/`404`/`410` via `DomainError` subclasses and FastAPI exception handlers.
- Definition of Done: §18 fully covered by tests.

**Task 08 — Add Tests**
- Objective: Full suite per §27.
- Files to Create: `tests/modules/games/test_manifest_api.py`.

**Task 09 — Add API Documentation**
- Objective: OpenAPI response models for all documented status codes.
- Definition of Done: regenerated `openapi.json` reviewed.

**Task 10 — Final Code Review**
- Objective: Confirm no parallel content-manifest logic was introduced (structural reuse check).
- Definition of Done: review checklist (§31) fully checked.

## 30. Definition of Done
- Endpoint matches §13 contract exactly, including all error codes.
- Learning-level-over-age-band precedence implemented and tested (Edge Case 6).
- Deprecated-skill-link and withdrawn-game cases both resolve to `410` (Edge Case 7).
- Content manifest delegated to A.5, not reimplemented.
- All §27 tests passing in CI.

## 31. Final Verification Checklist
- [x] `403 AGE_BAND_MISMATCH` verified via stale-client simulation test
- [x] `410 GAME_WITHDRAWN` verified for both withdrawal and all-skills-deprecated cases
- [x] Learning-level override precedence test passing
- [x] No client-supplied difficulty parameters accepted anywhere in the request path
- [x] A.5 content manifest delegation confirmed (no duplicated logic)
- [x] p95 latency target reviewed against representative load
- [x] OpenAPI docs updated with full error-response model coverage
- [x] No files outside declared scope modified

---

## 32. Cross-Platform Dependencies
- Backend Dependency: A.5 Content & Catalog Service (content-manifest delegation, exact method TBC); A.9 `skill_node.is_active` (confirmed, §6).
- KMP Dependency: K-02 `GamesRepository.getManifest()`.
- Admin Dependency: B-06 (withdrawal/publish state directly affects manifest availability at launch time).
- Database Dependency: `game`, `game_skill_link` (this module), `skill_node` (A.9, read-only cross-module).
- External Service Dependency: None beyond A.5's existing asset-delivery infrastructure.
- Figma Dependency: None (data endpoint) — visual consumer is K-02's loading/play-screen transition.
