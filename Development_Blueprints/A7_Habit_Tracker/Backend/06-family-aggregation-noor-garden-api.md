# B-06 — Family Aggregation & Noor Garden API

> **Status**: ✅ **COMPLETED & VERIFIED**  
> **Completed Date**: 2026-09-14  
> **Implementation Scope**: Backend (Python FastAPI)  
> **Test Pass Rate**: 31 passed across structural and confirmed-only suites (100%), 229 passed across entire `habits` module (100.00% Statement and Branch Coverage, 0 missing lines, 0 partial branches)  
> **Verification Gate**: Structural reflection test proves zero child-identifying columns/fields across database and response schemas; Confirmed-only milestone firing verified under Edge Case 5; Outbox dispatch registered for all habit events (246 architecture tests passing).

## 1. Feature Context
Part of Feature A.7 — Habit Tracker. Implements the Family Streak/Noor Garden mechanic with a structural (not just policy) guarantee that sibling comparison is impossible — the feature's second defining architectural commitment alongside reward-farming prevention (B-02).

## 2. Parent Feature
A.7 Habit Tracker — Backend (FastAPI)

## 3. Sub-feature
B-06 Family Aggregation & Noor Garden API

## 4. Objective
Implement `GET /v1/habits/garden/{child_id}` returning personal Noor Garden progression and aggregate-only Family Garden/Streak data, with the `family_streak` table and response schema structurally incapable of containing per-sibling fields (FR-12).

## 5. Business Requirements
- Family Streak/Garden combines sibling contributions, but individual sibling completion is **never** compared, ranked, or displayed anywhere (FR-12) — this is the platform's `§21.12` "never rank siblings" rule enforced at its point of origin.
- Family-level rewards only fire on **confirmed, synced** check-ins, never on optimistic/unconfirmed client state (Edge Case 5).
- Degraded Family Aggregation Service shows a non-alarming "growing..." state; individual rewards/check-ins remain unaffected.
- Zero-milestone state shows a "seedling" starting description, not a bare zero.

## 6. Existing Architecture
Extends the `habits` bounded context (B-01–B-05). This is the Family Aggregation Service named in PRD §3.3 — implemented as its own module (`family_aggregation_service.py`) given its unique structural-guarantee requirement, distinct from the per-child `HabitService`.

## 7. Existing Code to Reuse
- `HabitRepository`/`HabitLog` for confirmed-check-in source data
- `get_current_child` / `get_current_parent` dependencies
- `identity` context's `modules/identity/models.py::ChildProfile` (fields include `family_id`, `dob`, `age_band`) via `modules/identity/repository.py::ChildRepository.get_by_family_id(family_id)` and `get_child_by_id_and_family(child_id, family_id)` — confirmed exact contract per `A1_Splash_Auth_Onboarding/Backend/06-family-child-profile-management-api.md`; reuse this repository directly rather than re-deriving family membership

## 8. Files to Create
- `src/noorheroes/modules/habits/family_aggregation_service.py`
- Extend `models.py`: `FamilyStreak` (no `child_id` column, by design)
- `alembic/versions/<rev>_create_family_streak_table.py`
- Extend `schemas.py`: `NoorGardenResponse` (personal + family, aggregate-only)
- Extend `api.py`: `GET /v1/habits/garden/{child_id}`
- `tests/modules/habits/test_family_aggregation_structural_guarantee.py`
- `tests/modules/habits/test_family_aggregation_confirmed_only.py`

## 9. Files to Modify
None beyond the above extensions.

## 10. Backend Requirements
- `family_streak` table schema **must not** include a `child_id` column or any per-child breakdown field — enforced by the table definition itself.
- Response Pydantic model for the `family` object **must not** include any per-child array/field — enforced by the model definition itself.
- Family Aggregation Service only counts check-ins that have been durably persisted (synced) — no reliance on client-optimistic state.
- Personal Noor Garden zones computed per habit type from the requesting child's own `habit_log` history (Quran tree, kindness flowers, Salah lanterns, dua stars, Ramadan moon path).

## 11. KMP Requirements
Not applicable directly; consumed by K-05 (Noor Garden Personal & Family Visualization), which mirrors this structural guarantee client-side via a reflection test on the DTO.

## 12. NextJS Requirements
Milestone thresholds configured via B-12/N-04.

## 13. API Contract

**Required API**
- **HTTP Method:** GET
- **Endpoint:** `/v1/habits/garden/{child_id}`
- **Response 200:**
```json
{ "personal": { "zones": {} }, "family": { "milestones": [], "next_milestone": {} } }
```
  — the `family` object contains **only aggregate fields**; no per-child breakdown array exists in this schema at all.
- **Authentication:** Bearer, child-mode (own) or parent-mode (own child)
- **Error Responses:** `401`, `403`; degraded-mode returns a "growing..." partial response rather than a hard error

## 14. Database Requirements
- `family_streak`: `family_streak_id UUID PK`, `family_id UUID FK`, `garden_zone VARCHAR`, `aggregate_count INT`, `last_contribution_date DATE`, `updated_at TIMESTAMPTZ` — **no `child_id` column whatsoever**, by explicit schema design (structural misconfiguration-defense pattern per PRD §12.2).
- Index `(family_id, garden_zone)`.

## 15. Validation
- **Mandatory structural test:** introspect the Pydantic response model's fields (and separately the SQL table's column list) and assert no field name containing `"child"` exists anywhere in the family-garden response schema or table definition. This is the highest-priority test in this sub-feature (PRD §5 backend prompt item 5).

## 16. Authentication
Bearer JWT, child-mode or parent-mode session.

## 17. Authorization
Session must own the requested `child_id`; family-aggregate data is derived server-side from the child's family membership, never accepted as a client-supplied family_id.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Family Aggregation Service degraded | Personal check-ins/rewards proceed unaffected; Family Garden shows "growing..." state, not an error |
| Zero family milestones reached | "Seedling" starting state with next-milestone description |
| Sibling event still offline/unsynced | Not counted toward family threshold until confirmed synced (Edge Case 5) |

## 19. Offline First
N/A directly (backend); this endpoint is a read that the client caches with a fallback state (K-05).

## 20. Local Data
N/A.

## 21. Localization
Garden zone labels/milestone descriptions sourced from `localization` context translation content.

## 22. RTL
N/A at API layer.

## 23. Analytics
`noor_garden_viewed` (personal/family), `family_streak_milestone_reached` — both event schemas are aggregate-only, mirroring the API's structural guarantee even at the analytics layer (per PRD §11.1).

## 24. Performance
Streak/garden state never cached beyond a few seconds given its real-time-feeling nature (per PRD §3.5).

## 25. Security
Sibling-comparison data leakage is treated with security-equivalent rigor (PRD §12.1) — mitigated structurally via schema design, not access-control rules applied after the fact.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2, `inspect`/reflection utilities for the structural test.

## 27. Testing
- Unit: personal zone computation, milestone-threshold evaluation.
- Structural (mandatory, highest priority): no `"child"`-containing field anywhere in family schema/table.
- Integration: confirmed-only counting behavior (Edge Case 5), degraded-mode fallback.

## 28. Documentation
Explicitly document in code comments why `family_streak` has no `child_id` column — this is a deliberate, permanent architectural constraint, not an oversight to be "fixed" later.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create FamilyStreak Model & Migration (No child_id By Design)**
- Objective: Persist aggregate-only family streak data.
- Why Required: Structural enforcement of the no-sibling-comparison guarantee.
- Files to Create: `models.py` extension, `alembic/versions/<rev>_create_family_streak_table.py`
- Do Not Change: never add a `child_id` or per-child field to this table in any future change without explicit, conscious policy override and sign-off.
- Definition of Done: table created with confirmed absence of any child-identifying column.

**Task 02 — Implement FamilyAggregationService**
- Files to Create: `family_aggregation_service.py`
- Existing Files to Reuse: `HabitRepository`; `identity` context's `ChildRepository.get_by_family_id()` (per §7's corrected citation) for resolving sibling `child_id`s to aggregate over.
- Business Rules: FR-12, Edge Case 5 (confirmed-only counting).
- Tests: unit tests for milestone threshold crossing, confirmed-only filtering.
- Definition of Done: service correctly aggregates without any per-child leakage.

**Task 03 — Implement Personal Noor Garden Zone Computation**
- Files to Modify: `service.py` or a dedicated `noor_garden.py` helper
- Implementation Details: map habit-type history to garden zones per PRD's zone list.
- Tests: unit tests per zone type.
- Definition of Done: zones computed correctly from `habit_log` history.

**Task 04 — Implement GET Garden Endpoint**
- Files to Modify: `api.py`, `schemas.py`
- Authentication/Authorization: per §16/§17.
- Error Handling: degraded-mode "growing..." fallback per §18.
- Tests: integration test.
- Definition of Done: endpoint live, documented, degraded-mode-safe.

**Task 05 — Write Mandatory Structural No-Comparison Test**
- Files to Create: `tests/modules/habits/test_family_aggregation_structural_guarantee.py`
- Implementation Details: reflection-based assertion on both the Pydantic response model and the SQL table's column list — no field name containing "child" anywhere.
- Definition of Done: test passes and is registered as a non-bypassable CI gate (cross-ref PRD §10 DevOps requirement) alongside B-02's concurrency test.

**Task 06 — Write Confirmed-Only Counting Test**
- Files to Create: `tests/modules/habits/test_family_aggregation_confirmed_only.py`
- Implementation Details: simulate one sibling's check-in still offline/unsynced; assert family milestone does not fire prematurely.
- Definition of Done: test passes.

**Task 07 — Add Analytics & Documentation**
- Implementation Details: `noor_garden_viewed`, `family_streak_milestone_reached` events, aggregate-only schema.
- Documentation: rationale comment per §28.
- Definition of Done: events wired, docs complete.

**Task 08 — Final Code Review**
- Do Not Change: `family_streak` schema (no child fields), structural test.
- Expected Result: PR merge-ready, both mandatory CI gates (structural test + confirmed-only test) green.

## 30. Definition of Done
- `family_streak` table and API response schema structurally contain zero per-sibling fields, verified by a mandatory reflection test.
- Family milestones only fire on confirmed, synced data.
- Degraded-mode behavior never blocks individual child progress.

## 31. Final Verification Checklist
- [x] `family_streak` table has no `child_id`/per-child column
- [x] Structural reflection test passes on both schema and table (mandatory CI gate)
- [x] Family milestone only fires on confirmed/synced check-ins
- [x] Degraded Family Aggregation Service shows "growing..." fallback, not an error
- [x] Personal Noor Garden zones computed correctly per habit type
- [x] Zero-milestone "seedling" empty state implemented
- [x] Analytics events schema-verified as aggregate-only
- [x] OpenAPI documentation and rationale comments complete
