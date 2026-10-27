# B-07 — Islamic Fact & Occasion Calendar Service

## 1. Feature Context
NoorHeroes Child App, Feature A.2. Powers the "Islamic Fact of the Day" Home section and the occasion reference in the Home greeting (e.g., "Jummah Mubarak").

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
1.7 Islamic Fact & Occasion Calendar Service (ID: B-07)

## 4. Objective
Implement `GET /v1/facts/daily` with 30-day non-repetition per child, evergreen fallback for small catalogs, and an Islamic-occasion resolver used by B-02's greeting composition, gracefully omitting the occasion when the calendar service is unavailable.

## 5. Business Requirements
Per PRD FR-2, FR-13, Edge Case 8, §4.2, §4.5:
- Fact must be scholar-approved, versioned, not repeated for the same child within a rolling 30-day window where catalog size allows.
- Occasion reference (Jummah, Ramadan, Eid) sourced from an Islamic calendar service; on service failure, greeting omits the occasion silently — never an error or stale/incorrect date claim.
- `home_fact_history.seen_fact_ids_last_30d` pruned by a nightly job.

## 6. Existing Architecture
FastAPI service-layer pattern; fan-out dependency of B-01 (`IslamicCalendarClient`) and a dependency of B-02's greeting composition.

## 7. Existing Code to Reuse
Existing scheduled-job infrastructure for the nightly pruning job (reuse the platform's existing job scheduler/cron mechanism rather than introducing a new one).

## 8. Files to Create
- `app/routers/facts.py`
- `app/services/fact_service.py`, `app/services/islamic_calendar_service.py`
- `app/repositories/fact_repository.py`
- `app/models/home_fact_history.py`
- `alembic/versions/xxxx_create_fact_history_table.py`
- `app/jobs/prune_fact_history.py` (nightly pruning job)
- `tests/unit/test_fact_dedup_window.py`
- `tests/unit/test_occasion_resolver_failure_omission.py`

## 9. Files to Modify
- `app/main.py`
- Existing job-scheduler registration file (wherever nightly jobs are registered on this platform)

## 10. Backend Requirements
- `GET /v1/facts/daily` selects a scholar-approved fact not present in the child's `seen_fact_ids_last_30d`, falling back to the evergreen pool when the eligible set is exhausted for a small locale catalog.
- Occasion resolver (`resolve_occasion(date, locale) -> str | None`) called synchronously by B-02's greeting composition; returns `None` on any internal failure (never raises up into the greeting flow).
- Nightly job prunes `seen_fact_ids_last_30d` rolling window per child.

## 11. KMP Requirements
Not implemented here. Consumed by K-01/B-01's `islamic_fact` section.

## 12. NextJS Requirements
Not applicable directly — N-04 (Islamic Fact & Occasion Calendar Manager) owns CRUD on the fact pool and occasion mappings this service reads from.

## 13. API Contract

**Endpoint:** `GET /v1/facts/daily`
**Auth:** Bearer (child-mode)
**Response 200:** Scholar-approved fact for the day, deduped against the child's last-30-days-seen list server-side.

## 14. Database Requirements
Per PRD §4.2, §4.5: `home_fact_history(child_id FK, seen_fact_ids_last_30d jsonb, updated_at)` — rolling window, pruned nightly. Fact pool and occasion-mapping tables owned/created by N-04 (coordinate migration ordering; B-07 depends on those tables existing and read-accessible).

## 15. Validation
Fact must have `scholar_status = 'approved'` before being eligible for serving (enforced as a query filter, mirroring N-04's write-side validation — defense in depth, not reliance on the admin form alone).

## 16. Authentication
Bearer JWT (child-mode session).

## 17. Authorization
Scoped to authenticated `child_id`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Fact pool exhausted (small locale) | Serve evergreen fallback fact |
| Islamic Calendar Service failure | Occasion omitted silently from greeting; no error propagated |
| Fact Service failure | B-01 hides `islamic_fact` card gracefully |

## 19. Offline First
Not applicable server-side.

## 20. Local Data
Not applicable (backend).

## 21. Localization
Fact text and occasion phrases stored per locale (EN/HI/AR/UR); query filters by child's `preferred_language`.

## 22. RTL
N/A (backend).

## 23. Analytics
Backend does not fire `islamic_fact_viewed`/`islamic_fact_clicked` (client-fired).

## 24. Performance
`seen_fact_ids_last_30d` stored as jsonb array — acceptable at expected catalog/child scale; revisit as a normalized join table only if catalog size or query performance becomes a measured issue.

## 25. Security
No PII beyond `child_id` reference; scholar-approval filter prevents unapproved/draft content from ever being served, even if N-04's admin UI has a bug.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0, Alembic, existing job scheduler, pytest-asyncio.

## 27. Testing
- Unit: 30-day dedup window correctness (fact not repeated; window rolls correctly).
- Unit: evergreen fallback triggers when eligible set is empty.
- Unit: occasion resolver returns `None` (not exception) on internal failure.
- Integration: nightly pruning job correctness.

## 28. Documentation
OpenAPI docs; document the `scholar_status = 'approved'` filter as a mandatory defense-in-depth check, not solely reliant on N-04's admin gate.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `home_fact_history` Table + Migration**
- Objective: Rolling-window seen-fact tracking table.
- Why Required: FR-13 dedup requirement.
- Existing Architecture to Follow: Alembic/SQLAlchemy conventions.
- Existing Files to Reuse: Base model class.
- Files to Create: `app/models/home_fact_history.py`, `alembic/versions/xxxx_create_fact_history_table.py`
- Files to Modify: none
- Implementation Details: `child_id FK` (unique per child), `seen_fact_ids_last_30d jsonb`, `updated_at`.
- Business Rules: One row per child.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Migration test.
- Documentation: Docstring.
- Dependencies: None.
- Do Not Change: Do not modify PostgreSQL credentials.
- Expected Result: Table created.
- Definition of Done: Migration passes.

**Task 02 — Implement Fact Selection Service with Dedup + Evergreen Fallback**
- Objective: `GET /v1/facts/daily`.
- Why Required: Core feature logic.
- Existing Architecture to Follow: Service/repository pattern; depends on N-04's fact-pool table (read-only here).
- Existing Files to Reuse: Task 01 model.
- Files to Create: `app/repositories/fact_repository.py`, `app/services/fact_service.py`, `app/routers/facts.py`
- Files to Modify: `app/main.py`
- Implementation Details: Filter fact pool by `scholar_status='approved'` and locale, exclude IDs in `seen_fact_ids_last_30d`, pick one, append to the child's seen list, fall back to evergreen pool if eligible set is empty.
- Business Rules: Never repeats within 30 days where catalog allows.
- Validation: Approval-status filter.
- Error Handling: Evergreen fallback on exhaustion.
- Security: Approval filter as defense-in-depth.
- Performance: Indexed lookup on fact pool by locale/status (index owned by N-04's migration).
- Localization: Locale-filtered.
- RTL: N/A.
- Analytics: N/A.
- Tests: Dedup window unit tests; evergreen fallback unit test.
- Documentation: OpenAPI docs.
- Dependencies: Task 01; N-04 fact-pool table must exist.
- Do Not Change: N/A.
- Expected Result: Working endpoint.
- Definition of Done: Tests pass.

**Task 03 — Implement Occasion Resolver + Nightly Pruning Job**
- Objective: `resolve_occasion()` for B-02's greeting, and the 30-day rolling-window pruning job.
- Why Required: FR-2 greeting personalization and §4.5 retention rule.
- Existing Architecture to Follow: Existing job-scheduler registration pattern on this platform.
- Existing Files to Reuse: Occasion-mapping table (owned by N-04).
- Files to Create: `app/services/islamic_calendar_service.py`, `app/jobs/prune_fact_history.py`
- Files to Modify: Existing job-scheduler registration file
- Implementation Details: `resolve_occasion(date, locale)` wraps all lookups in try/except, returning `None` on any failure; pruning job runs nightly, trims `seen_fact_ids_last_30d` entries older than 30 days per child.
- Business Rules: Never raises into the greeting flow (Edge Case 8).
- Validation: N/A.
- Error Handling: All failure paths converge to `None`, not an exception.
- Security: N/A.
- Performance: Pruning job batched, not per-child synchronous loop if child count is large.
- Localization: Occasion phrases per locale.
- RTL: N/A.
- Analytics: N/A.
- Tests: Unit test — force an internal exception, assert `resolve_occasion` returns `None`, not raises; integration test for pruning job correctness.
- Documentation: Docstring warning against ever letting this function raise.
- Dependencies: Task 01; N-04 occasion-mapping table.
- Do Not Change: Do not let failure here block greeting composition (B-02) or Home rendering (B-01).
- Expected Result: Resolver + job.
- Definition of Done: Tests pass; job registered and verified in staging schedule.

## 30. Definition of Done
Facts served without 30-day repetition where catalog allows, evergreen fallback works, occasion resolution never breaks the greeting flow on failure; all tests green.

## 31. Final Verification Checklist
- [x] Fact dedup window verified across a rolling 30-day scenario
- [x] Evergreen fallback triggers correctly for exhausted small-catalog locales
- [x] `scholar_status='approved'` filter enforced server-side
- [x] Occasion resolver never raises; returns `None` on failure
- [x] Nightly pruning job correctly trims stale seen-fact entries
- [x] All tests pass

## 32. Implementation Summary

- **Status**: Completed & Verified
- **Implementation Date**: 2026-09-25
- **Alembic Migration**: `alembic/versions/0085_create_home_fact_and_calendar_tables.py` creating `islamic_fact`, `islamic_occasion_mapping`, and `home_fact_history` tables with composite indexing and foreign keys.
- **Core Domain Module**: `src/noorheroes/modules/facts/`
  - `models.py`: `IslamicFact`, `IslamicOccasionMapping`, `HomeFactHistory` with cross-dialect JSON compatibility.
  - `schemas.py`: Pydantic V2 schemas (`DailyFactResponse`, `FactDetailResponse`, `FactCreateRequest`, `FactUpdateRequest`, `OccasionMappingResponse`, etc.) enforcing mandatory scholar approval before `active=True`.
  - `repository.py`: `FactRepository` implementing 30-day rolling window seen checks, evergreen fallback selection, history record/pruning, and admin CRUD.
  - `islamic_calendar_service.py`: `IslamicCalendarService` fail-safe occasion resolver (guaranteed to return `None` and never raise, with Friday/Jummah localized greeting support for EN, AR, UR, HI).
  - `service.py`: `FactService` integrating child timezone local date derivation, 30-day deduplication, deterministic daily fact selection, evergreen fallback, and occasion resolution.
  - `deps.py`: FastAPI dependency injection providers.
  - `api.py`: `GET /v1/facts/daily` with sibling tenancy check and child authorization.
  - `admin_api.py`: Admin CRUD endpoints (`/admin/v1/facts`, `/admin/v1/occasions`) supporting NextJS Admin N-04.
  - `tasks.py`: Celery task `facts.prune_fact_history` with beat schedule configured in `core/celery_app.py`.
- **Backwards Compatibility Facades**:
  - `app/models/home_fact_history.py`, `app/models/islamic_fact.py`, `app/models/islamic_occasion_mapping.py`
  - `app/repositories/fact_repository.py`
  - `app/services/fact_service.py`, `app/services/islamic_calendar_service.py`
  - `app/routers/facts.py`
  - `app/jobs/prune_fact_history.py`
- **Test Suites (38 Tests Passed - Zero Missing Scenarios)**:
  - `tests/unit/test_fact_dedup_window.py` (8 unit tests: 30-day exclusion, rolling window expiry, multi-child isolation, nightly history pruning, Celery task execution, deterministic daily fact selection, subsequent day fact rolling, and timezone boundary evaluation)
  - `tests/unit/test_occasion_resolver_failure_omission.py` (7 unit tests: Jummah in 4 locales, non-occasion day None, custom day mapping, custom Hijri date range mapping, fail-safe exception absorption, greeting service occasion omission, and unsupported locale fallback)
  - `tests/unit/test_fact_evergreen_fallback.py` (14 unit tests: evergreen fallback on pool exhaustion, standard fact priority before evergreen fallback, non-approved facts exclusion, schema draft active rejection, empty catalog static fallback, approved but deactivated exclusion, evergreen pool resilience when all seen, localized text resolution & base text fallback, unsupported locale normalization to EN, age-band specific filtering precision, empty DB 4-locale cold-start resilience, domain-level child tenancy enforcement, fail-open history recording resilience, and service-layer admin scholar approval gating)
  - `tests/unit/test_fact_migration.py` (2 unit tests: 0085 migration upgrade and downgrade DDL)
  - `tests/integration/test_fact_daily_flow.py` (7 integration tests: HTTP GET /v1/facts/daily cycle, multi-locale headers, sibling tenancy 403 Forbidden, unauthenticated 401 rejection, content-safety anti-billing audit, age-band specific filtering, async pruning task execution, backwards compatibility facades, and full Admin CRUD flow for NextJS Admin N-04)


