# B-08 — Architecture Consolidation: Retire Legacy A.2/B-07 Fact Service

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). This is a migration/refactor sub-feature, not new product functionality — it resolves the architectural conflict identified during B.18's breakdown: A.2's own "B-07" (Islamic Fact & Occasion Calendar Service) already implemented a flat, unversioned `GET /v1/facts/daily` against a `home_fact_history` table before B.18's richer versioned/approval-gated schema existed.

## 2. Parent Feature
B.18 — Islamic Facts Module (cross-cutting with A.2 — Child Home Dashboard & AI Personalization)

## 3. Sub-feature
1.8 Architecture Consolidation — Retire Legacy Fact Service (ID: B-08)

## 4. Existing Architecture → Problem → Proposed Improvement → Impact → Implementation → Documentation Update

**Existing Architecture:** A.2's B-07 owns `GET /v1/facts/daily`, backed by `home_fact_history(child_id, seen_fact_ids_last_30d jsonb, updated_at)` — a simple JSON-array dedup structure with no versioning, no scholar-approval gate table, no per-fact granular history.

**Problem:** B.18's B-01/B-02 define the canonical, richer schema (`fact`/`fact_version`/`scholar_approval`/`fact_seen_log`) with structural approval-gate enforcement that A.2's B-07 never had. Two services cannot both legitimately own `/v1/facts/daily`. Leaving both in place risks silent drift (e.g., a fact approved in B.18's system but never surfaced because A.2's B-07 code path doesn't know about the approval-gate join) and directly contradicts Rule 23 (no duplicate/redundant code) and B.18's own FR-5 ("this document owns the fact-content data model... not a duplicate of Home's own card-rendering logic").

**Proposed Improvement:** B.18's B-02 becomes the sole owner of `/v1/facts/daily`. A.2's Home aggregation feed is repointed to call B.18's endpoint. Legacy `home_fact_history` data is migrated into `fact_seen_log`. A.2/B-07's `fact_service.py`/`fact_repository.py`/`home_fact_history` model are deprecated and removed only after cutover verification. A.2/B-07's *occasion resolver* (`islamic_calendar_service.py` — Jummah/Ramadan/Eid greeting text) is explicitly **out of scope** and retained as-is, since it is a distinct concern (greeting composition, not fact content) that happens to be bundled in the same legacy file.

**Impact:** A.2's Home card continues to function identically to the child (no visible behavior change) while gaining B.18's approval-gate rigor, versioning, and richer dedup semantics. A.2's own blueprint documentation requires a follow-up update noting B-07 is superseded for fact-serving purposes.

**Implementation:** See Tasks below.

**Documentation Update:** A.2's blueprint (`Development_Blueprints/A2_Home_Dashboard_AI_Personalization/Backend/07-islamic-fact-occasion-calendar-service.md`) must be annotated to reflect that its fact-serving responsibility has moved to B.18/B-02, retaining only occasion resolution.

## 5. Business Requirements
Rule 23 (Existing Code Cleanup — remove genuinely redundant/duplicate code, do not remove future-ready/unrelated code). Rule 24 (Architecture Improvement — explicit identification required, which this document satisfies). B.18 FR-5 (canonical ownership of fact-content data model).

## 6. Existing Architecture
A.2's B-07: `app/routers/facts.py`, `app/services/fact_service.py`, `app/services/islamic_calendar_service.py`, `app/repositories/fact_repository.py`, `app/models/home_fact_history.py`, nightly pruning job `app/jobs/prune_fact_history.py`.

## 7. Existing Code to Reuse
B.18's B-01 (`fact`/`fact_version`/`scholar_approval`/`fact_seen_log`) and B-02 (`GET /v1/facts/daily` selection logic) — the migration target, already built by this point in the execution sequence.

## 8. Files to Create
- `alembic/versions/xxxx_migrate_home_fact_history_to_fact_seen_log.py` — data migration mapping legacy `seen_fact_ids_last_30d` jsonb arrays into individual `fact_seen_log` rows per child.
- `tests/modules/content/test_legacy_fact_history_migration.py`.
- `tests/integration/test_home_fact_card_regression.py` — confirms Home's fact card renders identically pre/post cutover.

## 9. Files to Modify
- A.2's Home aggregation feed service (`Development_Blueprints/A2.../Backend/01-home-aggregation-feed-api.md`'s implementation) — repoint its fact-serving call from A.2/B-07's endpoint to B.18/B-02's `GET /v1/facts/daily`.
- `src/noorheroes/api/router.py` — remove A.2/B-07's `facts.py` router registration once cutover is verified (retain `islamic_calendar_service.py`'s occasion-resolver route, if it has one, unchanged).

## 10. Backend Requirements
- Data migration: for each `home_fact_history` row, decompose `seen_fact_ids_last_30d` jsonb array into individual `(child_id, fact_id, seen_at)` rows in `fact_seen_log`, using `updated_at` as a best-effort `seen_at` approximation where per-fact timestamps aren't available (documented data-quality caveat, acceptable since this is dedup-history, not user-facing data).
- Staged rollout: run both code paths in parallel behind a feature flag during a verification window; cut Home's aggregation feed over to B.18/B-02 only after confirming output parity on a sample of real child sessions.
- Remove A.2/B-07's `fact_service.py`, `fact_repository.py`, `home_fact_history` model, and `prune_fact_history.py` job **only after** the verification window closes with no discrepancies — do not delete on a timeline, delete on verified evidence.
- Retain `islamic_calendar_service.py` (occasion resolver) untouched — confirm it does not import anything from `fact_service.py` that would break on removal; if it does, extract the shared dependency before deleting.

## 11. KMP Requirements
None — this is a backend-only migration; K-01/K-05 already consume B.18's B-02/B-03 by design, so no KMP change is needed regardless of when this cutover completes.

## 12. NextJS Requirements
Coordinates with N-06 (which performs the equivalent consolidation for A.2/N-04's admin CRUD surface) — both should land in the same release to avoid a window where admin edits go to a table the child-facing API no longer reads from.

## 13. API Contract
No new external contract — `GET /v1/facts/daily`'s response shape is unchanged from B.18/B-02's already-defined contract; this sub-feature is purely about which backend code path Home calls.

## 14. Database Requirements
`home_fact_history` retained (not dropped) through the verification window as a rollback safety net; dropped in a follow-up migration only after B.18's schema has run in production without incident for a defined bake period (recommend matching B.18's phased rollout in §15.1, 2–3 days minimum, extended given this is a migration of existing production data).

## 15. Validation
Migration script validates row counts match between source `home_fact_history` and destination `fact_seen_log` (accounting for the array-to-rows expansion ratio) before considering the migration complete.

## 16. Authentication / 17. Authorization
Unchanged — inherits B.18/B-02's existing auth (child-mode) once cutover completes.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Migration script encounters a malformed `seen_fact_ids_last_30d` value | Log and skip that row (best-effort dedup history is non-critical), do not fail the entire migration |
| Post-cutover regression detected | Feature flag reverts Home's aggregation feed to the legacy endpoint immediately |
| `islamic_calendar_service.py` has a hidden dependency on code slated for removal | Extract shared code first; do not delete until resolved |

## 19-22. Offline/Local Data/Localization/RTL
N/A — backend data migration.

## 23. Analytics
None new; verify existing `fact_of_day_shown`/`fact_card_tapped` events continue firing identically post-cutover (regression test, §27).

## 24. Performance
Migration run as a background job outside request-serving path; no user-facing latency impact.

## 25. Security
No new attack surface; removes a redundant code path, reducing overall surface area.

## 26. Library Requirements
None new.

## 27. Testing
- Unit: migration correctly expands jsonb arrays into individual `fact_seen_log` rows.
- Integration: Home's fact card renders identically (same fact selection outcome) pre/post cutover for a fixture set of child sessions.
- Regression: existing A.2 Home aggregation feed tests continue passing after the repoint.
- Verify `islamic_calendar_service.py`'s occasion resolution is unaffected by the removal of `fact_service.py`.

## 28. Documentation
Update A.2's `07-islamic-fact-occasion-calendar-service.md` blueprint file with an annotation noting fact-serving responsibility moved to B.18/B-02, retaining only the occasion resolver; update B.18's own docs to confirm sole ownership.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Data Migration Script**
Objective: Migrate `home_fact_history` → `fact_seen_log`.
Why Required: Preserve dedup history continuity across the cutover.
Files to Create: `alembic/versions/xxxx_migrate_home_fact_history_to_fact_seen_log.py`.
Dependencies: B.18 B-01 complete.
Error Handling: Skip malformed rows, log, continue.
Expected Result: `fact_seen_log` populated with historical dedup data.
Definition of Done: Row-count validation passes (§15).

**Task 02 — Feature-Flagged Parallel Run**
Objective: Run both A.2/B-07 and B.18/B-02 behind a flag, compare outputs.
Dependencies: Task 01, B.18 B-02 complete.
Expected Result: Parity confirmed on real traffic sample.
Definition of Done: Zero discrepancies over the verification window.

**Task 03 — Cutover A.2's Home Aggregation Feed**
Objective: Repoint Home's fact-serving call to B.18/B-02.
Files to Modify: A.2's Home aggregation feed service.
Dependencies: Task 02 verified clean.
Expected Result: Home card fully served by B.18's canonical endpoint.
Definition of Done: Regression test (Task 05) passes.

**Task 04 — Retire Legacy Code**
Objective: Remove `fact_service.py`, `fact_repository.py`, `home_fact_history` model, `prune_fact_history.py`, retaining `islamic_calendar_service.py`.
Dependencies: Task 03, bake period elapsed with no incidents.
Do Not Change: `islamic_calendar_service.py` (extract shared deps first if any exist).
Expected Result: No redundant fact-serving code remains.
Definition of Done: Code review confirms clean removal, occasion resolver still functions.

**Task 05 — Regression Test**
Objective: Confirm Home's fact card behaves identically pre/post cutover.
Files to Create: `tests/integration/test_home_fact_card_regression.py`.
Dependencies: Task 03.
Definition of Done: Test green before Task 04 proceeds.

**Task 06 — Documentation Update**
Objective: Annotate A.2's B-07 blueprint file and B.18 docs.
Dependencies: Task 04.
Definition of Done: Both blueprint files accurately reflect final ownership.

## 30. Definition of Done
- Single canonical fact-serving code path (B.18/B-02); legacy path removed only after verified parity.
- `islamic_calendar_service.py` (occasion resolver) unaffected and retained.
- Historical dedup data preserved in `fact_seen_log`.
- Documentation on both A.2 and B.18 sides updated to reflect final ownership.

## 31. Final Verification Checklist
- [ ] Parity verified between legacy and new fact-serving paths before cutover
- [ ] Home card regression test passes post-cutover
- [ ] Legacy `fact_service.py`/`fact_repository.py`/`home_fact_history` removed only after bake period, not on a timeline
- [ ] `islamic_calendar_service.py` retained and unaffected
- [ ] Historical dedup data migrated with validated row counts
- [ ] A.2's blueprint documentation annotated
- [ ] Coordinated with N-06 to avoid admin/child data-source mismatch window
