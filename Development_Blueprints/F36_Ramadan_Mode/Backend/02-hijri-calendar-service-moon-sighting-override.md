# B-02 — Hijri Calendar Service & Moon-Sighting Override

## 1. Feature Context
The server-side authority for Hijri (Islamic lunar calendar) date computation that produces each region's Ramadan start date and Eid date, with a regional moon-sighting override table so a disputed sighting can correct the algorithmic result without either client ever performing its own date math.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
1.2 Hijri Calendar Service & Moon-Sighting Override (ID: **B-02**)

## 4. Objective
Implement an internal `HijriCalendarService` that computes region-adjusted Hijri Ramadan start/Eid dates, exposes a read path consumed by B-01, and an admin-only write (override) path consumed exclusively by B-08.

## 5. Business Requirements
- FR-4: server-side Hijri calendar service with a regional moon-sighting override table.
- FR-3: a moon-sighting-disputed Eid date triggers an Admin override that updates `ramadan_campaigns` and pushes a one-time notification.
- §5 Backend AI prompt: Hijri calendar calculation library plus a regional moon-sighting override table.

## 6. Existing Architecture
`ramadan` bounded context, `app/ramadan/services/hijri_calendar_service.py` — a leaf service with no router of its own; consumed internally by B-01 (read) and B-08 (write).

## 7. Existing Code to Reuse
- `app/shared/base_service.py::BaseService`
- No existing Hijri-date logic elsewhere in the codebase — this is genuinely new infrastructure, confirmed via search of `FAST-API-INSTRUCTIONS.md`'s 12 bounded contexts (none own calendar computation).

## 8. Files to Create
- `app/ramadan/services/hijri_calendar_service.py`
- `app/ramadan/repositories/moon_sighting_override_repository.py`
- `app/ramadan/models/moon_sighting_override.py`
- `alembic/versions/xxxx_create_moon_sighting_override_table.py`
- `app/ramadan/schemas/hijri_dates_schema.py`

## 9. Files to Modify
None — pure internal service addition, no router registration required.

## 10. Backend Requirements
- `HijriCalendarService.get_dates(region: str) -> HijriDates`: returns `hijri_start_date`, `eid_date` for the region, checking the override table first and falling back to the algorithmic calculation library.
- `HijriCalendarService.apply_override(region, corrected_eid_date, source_note, acting_admin_id)`: writes to the override table and updates `ramadan_campaigns.eid_date`/`eid_date_overridden` — called exclusively by B-08's `EidOverrideService`, never exposed on a public router.
- Sanity-bound validation: `corrected_eid_date` must fall within a small window (e.g. ±3 days) of the algorithmically-expected date, rejecting gross data-entry errors.
- Multi-region support: two regions may have genuinely different confirmed sighting dates for the same season — no assumption of a single global date.

## 11. Required API / API Contract
No direct external endpoint — **internal service only**, consumed by B-01 (`GET /v1/ramadan/campaign-status`) and B-08 (`POST /v1/admin/ramadan/eid-date-override`).

## 12. Database Requirements
Extends `ramadan_campaigns.hijri_start_date`/`eid_date`/`eid_date_overridden` (B-01's table); new `moon_sighting_overrides(override_id PK, region, corrected_eid_date, source_note, applied_by_admin_id, applied_at)` audit-style table (append-only, distinct from the mutable `ramadan_campaigns` row it feeds).

## 13. Validation
`corrected_eid_date` sanity-bounded; `region` must be a supported/known region value (reuse A.1's region enum/lookup, do not invent a parallel region list).

## 14. Authentication
N/A directly (internal service) — inherits caller's auth context (B-01's parent session for reads, B-08's `super_admin` session for writes).

## 15. Authorization
Write path (`apply_override`) callable only from B-08's service layer — enforced by not exposing any router for this service, not merely by convention.

## 16. Error Handling
Unsupported/unmapped region: raise a domain exception the caller (B-01) translates into `phase: "not_active"`, not a 500.

## 17. Offline First
N/A — server-only computation.

## 18. Local Data
N/A — this service exists specifically so no client ever computes Hijri dates locally.

## 19. Localization
N/A — dates returned in ISO 8601; display formatting is client-side (K-01/K-05) per region locale (En/Hi/Ar/Ur).

## 20. RTL
N/A.

## 21. Analytics
Indirectly triggers `ramadan_region_window_recalculated` (via B-01) and `ramadan_eid_date_admin_override_applied` (via B-08) — this service itself emits no events directly, keeping event ownership with the caller.

## 22. Performance
Calculation results cacheable per-region per-season; override-table lookups indexed on `(region)`.

## 23. Security
This service is the single place Hijri dates are computed platform-wide — its non-exposure as a public router is itself a control surface reduction, and every write is attributable to an acting admin via `moon_sighting_overrides.applied_by_admin_id`.

## 26. Library Requirements
A Hijri calendar calculation library (e.g. `hijri-converter` or equivalent Python package — confirm against the team's approved dependency list before adding; not currently present per the codebase's 12-context review). SQLAlchemy 2.0 async, Alembic.

## 27. Testing
Unit: date-computation correctness across at least two regions with divergent expected dates; sanity-bound rejection of an out-of-window override value. Integration: **mandatory** — override write immediately visible to B-01's next `campaign-status` read; unsupported-region raises the correct domain exception.

## 28. Documentation
Internal docstring/README note in `app/ramadan/services/hijri_calendar_service.py` stating this is the platform's sole Hijri-date authority — no other module may perform Hijri-date arithmetic.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm and Add the Hijri Calculation Library**
Objective: Select and add an approved Hijri calendar library. Why: no existing dependency covers this. Files to Modify: `pyproject.toml`/`requirements.txt`. Definition of Done: library importable, license-compatible.

**Task 02 — Write Migration for `moon_sighting_overrides`**
Objective: Append-only override audit table. Files to Create: `alembic/versions/xxxx_create_moon_sighting_override_table.py`, `models/moon_sighting_override.py`. Dependencies: Task 01. Tests: migration test. Definition of Done: schema created.

**Task 03 — Implement `MoonSightingOverrideRepository`**
Objective: Region-keyed override lookups/writes. Files to Create: `repositories/moon_sighting_override_repository.py`. Dependencies: Task 02. Tests: repository tests. Definition of Done: tests pass.

**Task 04 — Implement `HijriCalendarService.get_dates()`**
Objective: Override-table-first, algorithmic-fallback date resolution. Files to Create: `services/hijri_calendar_service.py`. Dependencies: Task 03, Task 01. Tests: multi-region correctness test. Definition of Done: tests pass.

**Task 05 — Implement `HijriCalendarService.apply_override()`**
Objective: Admin-only write path with sanity-bound validation, consumed exclusively by B-08. Dependencies: Task 04. Tests: **mandatory** — sanity-bound rejection test; override-visible-on-next-read test. Definition of Done: tests pass.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §27. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm no router exposes `apply_override` directly and no other bounded context imports this service for anything but the two sanctioned call sites (B-01, B-08). Definition of Done: checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] Hijri dates computed correctly for at least two divergent regions
- [ ] Override write immediately reflected in subsequent reads — mandatory test passing
- [ ] Sanity-bound validation rejects out-of-window override values
- [ ] No public router exposes this service — internal-only, verified by code review
- [ ] Every override attributable to an acting admin via the audit table

## 31. Definition of Done
A single, non-duplicated, server-side source of Hijri-date truth exists for the entire platform, with a properly bounded and auditable correction path for moon-sighting disputes.
