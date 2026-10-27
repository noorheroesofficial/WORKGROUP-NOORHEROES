# B-11 — Seasonal Cross-Mechanic Coordination API

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the read/aggregation API backing the Seasonal Calendar — a shared, cross-module scheduling-convenience view spanning habits, challenges, banners, and notification campaigns. Source: PRD §1.7 FR-11, §1.16, §1.17, §2.1, §3.4 (Screen Inventory #29).

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
1.11 Seasonal Cross-Mechanic Coordination API (Backend ID: **B-11**)

## 4. Objective
Give super admins and content admins a single aggregated read view of everything scheduled across the seven engagement mechanics within a seasonal window, while structurally guaranteeing this coordination layer never bypasses any individual mechanic's own independent validation rules — it is a scheduling convenience only.

## 5. Business Requirements
- FR-11 (PRD §1.7): a Super Admin or Content Admin may schedule habit sets, challenges, rewards, banners, and notification campaigns under one shared seasonal window/calendar view, but each underlying mechanic's own validation rules still apply independently — coordination is a scheduling convenience, never a bypass.
- Acceptance Criteria (PRD §1.9): given an admin schedules a coordinated seasonal event across multiple mechanics, each individual mechanic still independently enforces its own validation rules.
- User Flow (PRD §1.16): admin uses the shared seasonal calendar view to schedule multiple mechanics together, while each mechanic's own independent validation still applies.

## 6. Existing Architecture
Pure read/aggregation layer atop B-01 through B-10's already-implemented endpoints — introduces no new business logic or validation rules of its own. FastAPI/SQLAlchemy 2.0/PostgreSQL.

## 7. Existing Code to Reuse
- B-01 through B-10's repository read methods (reused directly for aggregation, not reimplemented).
- Each mechanic's own creation endpoint remains the sole write path — this sub-feature does not introduce a parallel "batch create" endpoint that could bypass individual validation; if a batch-convenience endpoint is implemented, it must internally call each mechanic's own existing service method per PRD's non-bypass requirement.

## 8. Files to Create
- `app/routers/admin/seasonal_calendar_router.py`
- `app/schemas/admin/seasonal_calendar_schemas.py`
- `app/services/admin/seasonal_calendar_service.py`
- `tests/admin/test_seasonal_calendar_api.py`

## 9. Files to Modify
- `app/routers/admin/__init__.py`

## 10. Backend Requirements
- **Database:** no new tables — this is a read-aggregation service querying `habit_templates`, `challenges`, `banner`, `notification_campaigns` (and optionally `reward_rule_version`/`badges` if included in the seasonal view) filtered by a date window.
- **Migration:** none.
- **Model:** none new; reuses existing models from B-01–B-10.
- **Schema/DTO:** `SeasonalCalendarItem` (`mechanic_type`, `id`, `title`, `starts_at`, `ends_at`, `status`), `SeasonalCalendarRead` (list of items grouped/color-codeable by `mechanic_type`).
- **Repository:** N/A as a distinct repository — service directly composes calls to B-01–B-10's existing repository `list()` methods filtered by date range.
- **Service:** `SeasonalCalendarService.get_calendar(window_start, window_end)` — calls each mechanic's existing list method with date-range filters, merges results into one aggregated response; performs no writes.
- **Router:** `GET /v1/admin/seasonal-calendar?starts_at=&ends_at=`.
- **Dependency Injection:** `require_role_any(["content_editor", "super_admin"])`.
- **Authentication/Authorization:** admin JWT; read access per E.28 RBAC matrix (any Engagement-module-visible role).
- **Validation:** `starts_at < ends_at` on the query window.
- **Business Rules:** this endpoint MUST NOT expose any write/schedule action that bypasses B-01–B-10's own individual validation — if a "schedule seasonal event" convenience action is built, it is implemented as a thin orchestration layer that calls each mechanic's existing, already-validated create endpoint/service method internally, never a shortcut around them.
- **Exception Handling:** `422` for invalid date window.
- **Logging:** standard read-endpoint logging (no dedicated audit-log entries needed, since no mutation occurs here — each underlying mechanic already audit-logs its own writes).
- **Caching:** short-TTL Redis cache of the aggregated view per window, invalidated on any write to any of the underlying mechanics (or simply left to a short TTL given this is a low-write-frequency internal read view).
- **Transaction:** N/A (read-only, no transaction needed beyond individual query sessions).
- **Pagination/Filtering/Sorting:** filter by `mechanic_type`, `starts_at`/`ends_at` window; sort by `starts_at`.

## 11. KMP Requirements
N/A — admin-only.

## 12. NextJS Requirements
Consumed by **N-11 Seasonal Calendar Coordination View**, which renders the aggregated response as a color-coded cross-mechanic timeline and links each block back into that mechanic's own editor (B-01–B-10's respective UIs).

## 13. API Contract

### `GET /v1/admin/seasonal-calendar`
- **Authorization:** any Engagement-module-visible admin role
- **Query params:** `starts_at`, `ends_at` (required window bounds)
- **Response (200):**
```json
{
  "window": { "starts_at": "2026-09-01T00:00:00Z", "ends_at": "2026-09-30T23:59:59Z" },
  "items": [
    { "mechanic_type": "habit", "id": "uuid", "title": "Ramadan Fasting Set", "starts_at": "2026-09-01T00:00:00Z", "ends_at": "2026-09-30T23:59:59Z", "status": "scheduled" },
    { "mechanic_type": "challenge", "id": "uuid", "title": "Ramadan Weekly Mission", "starts_at": "2026-09-01T00:00:00Z", "ends_at": "2026-09-08T00:00:00Z", "status": "scheduled" },
    { "mechanic_type": "banner", "id": "uuid", "title": "Ramadan Promo Banner", "starts_at": "2026-09-01T00:00:00Z", "ends_at": "2026-09-30T23:59:59Z", "status": "active" },
    { "mechanic_type": "notification", "id": "uuid", "title": "Ramadan Announcement Campaign", "starts_at": "2026-09-01T09:00:00Z", "ends_at": "2026-09-01T09:00:00Z", "status": "scheduled" }
  ]
}
```
- **Error Responses:** `401`, `403`, `422 INVALID_WINDOW`

## 14. Database Requirements
None new — read-only aggregation across existing tables from B-01–B-10.

## 15. Validation
`starts_at < ends_at` on the requested window.

## 16. Authentication
Admin JWT (E.28).

## 17. Authorization
Any Engagement-module-visible role (broader than the `content_editor`+ write restriction on individual mechanics, since this is read-only).

## 18. Error Handling
| Scenario | Response |
|---|---|
| Invalid date window (`starts_at >= ends_at`) | `422 INVALID_WINDOW` |
| Unauthorized/forbidden | `401`/`403` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
`title` fields resolve through each underlying mechanic's own localization-key pattern.

## 22. RTL
N/A at API layer.

## 23. Analytics
`seasonal_event_scheduled` (PRD §1.19) — emitted by whichever underlying mechanic's own create call fires within a coordinated batch, not duplicated by this aggregation endpoint itself.

## 24. Performance
Aggregation should issue parallel/concurrent queries against each mechanic's table (via `asyncio.gather` over independent DB sessions or a single UNION query if schemas allow) rather than serial sequential queries, to keep the calendar view responsive.

## 25. Security
No new mutation surface — this endpoint cannot itself be a source of a validation-bypass vulnerability since it performs no writes; the security review specifically must confirm no future addition of a "batch schedule" endpoint circumvents B-01–B-10's individual guards.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, `asyncio.gather`, Pydantic v2, pytest-asyncio.

## 27. Testing
- Unit: window-validation logic; response-merging/sorting logic.
- Integration: signature test — schedule items across multiple mechanics within a window, call the calendar endpoint, confirm all items appear correctly grouped by `mechanic_type`.
- Non-bypass regression test: attempt to schedule a coordinated seasonal event that includes an intentionally-overlapping weekly challenge (per B-02's rule) and confirm the challenge-specific `409 DATE_RANGE_OVERLAP` still fires even when the request originates through any seasonal-coordination convenience flow — this is the PRD's explicit acceptance criterion (§1.9 last bullet).
- Negative cases: invalid window, unauthorized.

## 28. Documentation
OpenAPI docs explicitly stating this is a read-only convenience aggregation with zero independent validation authority — every write still routes through and is governed by B-01–B-10.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Aggregation Service**
- Task ID: B-11-T01
- Objective: Build `SeasonalCalendarService.get_calendar()` composing reads from B-01–B-10's existing repositories.
- Files to Create: `app/services/admin/seasonal_calendar_service.py`.
- Implementation Details: parallel queries via `asyncio.gather`; merge and sort by `starts_at`.
- Dependencies: B-01 through B-10 fully implemented.
- Do Not Change: any underlying mechanic's own validation logic.
- Definition of Done: unit tests with mocked underlying repositories confirm correct merging/sorting.

**Task 02 — API Endpoint**
- Task ID: B-11-T02
- Files to Create: `app/routers/admin/seasonal_calendar_router.py`.
- Files to Modify: `app/routers/admin/__init__.py`.
- Dependencies: Task 01.
- Definition of Done: integration test green against a seeded multi-mechanic fixture window.

**Task 03 — Non-Bypass Regression Test**
- Task ID: B-11-T03
- Objective: Prove the PRD's explicit non-bypass acceptance criterion.
- Implementation Details: attempt to schedule an overlapping weekly challenge via whatever entry point represents "coordinated seasonal scheduling" in the implementation (even if that's simply calling B-02's own create endpoint within a seasonal-window context) and confirm B-02's `409 DATE_RANGE_OVERLAP` still fires unmodified.
- Tests: `tests/admin/test_seasonal_calendar_api.py::test_coordinated_scheduling_does_not_bypass_individual_mechanic_validation`.
- Dependencies: Tasks 01–02, B-02.
- Definition of Done: test passes, confirming zero bypass surface.

**Task 04 — Documentation & Final Review**
- Task ID: B-11-T04
- Dependencies: Tasks 01–03.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Aggregated calendar view functional and accurate across all mechanics; explicit non-bypass regression test proves coordination never weakens any individual mechanic's validation; read-only, no new mutation surface introduced.

## 31. Final Verification Checklist
- [ ] `GET /v1/admin/seasonal-calendar` returns correctly merged, sorted items across all mechanics
- [ ] Invalid date window rejected (`422`)
- [ ] Non-bypass regression test confirms B-02's overlap rejection still fires within coordinated scheduling context
- [ ] No new write/mutation endpoint introduced by this sub-feature
- [ ] Unauthorized/forbidden paths tested
- [ ] No school/madrasa/institutional-tier logic introduced
- [ ] PostgreSQL/Redis credentials untouched
