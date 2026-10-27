# B-01 — Ramadan Campaign Lifecycle & Region-Keyed Activation Window Service

## 1. Feature Context
The state machine governing which of the six lifecycle phases (Pre-Ramadan Countdown, Active, Laylatul Qadr, Eid Transition, Eid Celebration, Post-Eid Tail) a family is currently in — resolved exclusively from the authenticated parent's own Region setting, never a client-supplied value, since date/region manipulation is this module's single most consequential attack surface.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
1.1 Ramadan Campaign Lifecycle & Region-Keyed Activation Window Service (ID: **B-01**)

## 4. Objective
Build `GET /v1/ramadan/campaign-status`, resolving `region` exclusively from the authenticated parent's Profile record server-side, computing the current lifecycle phase and night number.

## 5. Business Requirements
- FR-1: six-phase lifecycle (14-day countdown, 30-day active, Laylatul Qadr nights 21/23/25/27/29, Eid transition, 3-day celebration, 14-day post-Eid tail).
- FR-2: activation window keyed to Parent Profile Region, never device locale.
- §5 Backend AI prompt item 1 (highest-priority guarantee): region resolved EXCLUSIVELY from the parent's own Profile record server-side — a client-supplied region parameter has ZERO effect on phase computation.
- Edge Case 1: Region change mid-Ramadan recalculates the window going forward; already-completed nights are preserved.

## 6. Existing Architecture
New `ramadan` bounded context (13th context alongside the 12 in `FAST-API-INSTRUCTIONS.md`, following identical Router → Service → Repository → Infrastructure layering), `app/ramadan/routers/campaign_router.py`, orchestrating B-02's Hijri Calendar Service.

## 7. Existing Code to Reuse
- A.1's Parent Profile `region` field (read-only source of truth)
- `app/shared/base_service.py::BaseService`, `app/shared/base_repository.py::BaseRepository[ModelT]`
- E.28's `AuditLogService.log_action()` (for admin-side campaign mutations, B-08)
- `core/deps.py::get_current_parent`, `ParentSessionContext`

## 8. Files to Create
- `app/ramadan/routers/campaign_router.py` (public `campaign-status` read)
- `app/ramadan/routers/admin_campaign_router.py` (proposed admin CRUD, §11)
- `app/ramadan/services/campaign_lifecycle_service.py`
- `app/ramadan/repositories/campaign_repository.py`
- `app/ramadan/schemas/campaign_status_schema.py`
- `app/ramadan/schemas/admin_campaign_schema.py` (proposed: `CampaignCreateRequest`, `CampaignUpdateRequest`, `CampaignListResponse`)
- `app/ramadan/models/campaign.py`
- `alembic/versions/xxxx_create_ramadan_campaigns_table.py`

## 9. Files to Modify
- `app/ramadan/routers/__init__.py` — register router
- `main.py` — include the `ramadan` router group if a new bounded context requires explicit registration per §1 of `FAST-API-INSTRUCTIONS.md`

## 10. Backend Requirements
- `CampaignLifecycleService.get_status(authenticated_parent)`: reads `region` from the parent's own Profile record via the authenticated session — any `region` query parameter on the incoming request, if present at all, is never read or referenced anywhere in the phase-computation code path (structurally ignored, not merely validated-and-overridden).
- Phase computation: given the region's `ramadan_campaigns.hijri_start_date`/`eid_date` (from B-02), derives `phase` (`pre_ramadan_countdown`/`active`/`laylatul_qadr`/`eid_transition`/`eid_celebration`/`post_eid_tail`) and `current_night` via straightforward date arithmetic against server time.
- Region-change handling: when a parent's Region changes, the service resolves against the NEW region's campaign record for all future-facing computation, while `ramadan_journey_progress` (B-05, keyed to `child_id`/`mission_id`, not region) remains entirely unaffected — no migration/recalculation of past progress rows is ever needed since progress isn't region-keyed in the first place.
- **Admin Campaign CRUD (proposed, pending backend-team confirmation — see §11):** PRD §8/§9 imply an Admin-side full CRUD surface over `ramadan_campaigns` consumed by N-01's Ramadan Campaign Manager, but PRD §3.4's API List enumerates only the read endpoint below and B-08's override-write endpoint. `CampaignRepository` and `CampaignLifecycleService` are extended in this blueprint with `list_campaigns()`, `create_campaign()`, and `update_campaign()` methods so the proposed admin endpoints in §11 have a real service layer to call — implement against this proposal, but flag it for a real API-contract sign-off before shipping to production, since it was inferred from PRD prose rather than an enumerated spec.

## 11. Required API / API Contract
`GET /v1/ramadan/campaign-status` (no region parameter accepted/required from the client at all) → `200 { "phase", "current_night", "hijri_start_date", "eid_date" }`.
**Authentication:** `get_current_parent`. **Authorization:** authenticated-parent, no elevated scope. **Validation:** no `region` field on the request schema. **Error Responses:** `phase: "not_active"` (200) when no campaign exists for the resolved region — never a 4xx/5xx for this case.

### Proposed Admin Campaign CRUD API (pending confirmation)
Inferred from PRD §8 ("Configure `ramadan_campaigns` per region") and §8's CRUD-permission table, following the same router/service/repository layering as the endpoint above and B-08. **Mark PROPOSED in code review until a real contract is signed off.**

- `GET /v1/admin/ramadan/campaigns` → `200 { items: [{ campaign_id, region, hijri_start_date, eid_date, eid_date_overridden }], page, page_size, total }`. Paginated per the platform's standard list-endpoint convention. **Auth:** `get_current_admin`. **Authz:** `require_admin_scope("content_editor")` (per §8's CRUD table).
- `POST /v1/admin/ramadan/campaigns` `{ region, hijri_start_date, eid_date }` → `201 { campaign_id, region, hijri_start_date, eid_date, eid_date_overridden: false }`. **Validation:** `UNIQUE(region, year-derived-from-hijri_start_date)` conflict → `409`. **Authz:** `require_admin_scope("content_editor")`.
- `PATCH /v1/admin/ramadan/campaigns/{campaign_id}` `{ hijri_start_date?, eid_date? }` → `200` updated record. **Validation:** does not accept `eid_date_overridden` directly — that flag is only ever set via B-08's dedicated override endpoint, never through this general-purpose PATCH, so the two write paths (routine pre-season configuration vs. moon-sighting override) stay structurally distinct and separately auditable. **Authz:** `require_admin_scope("content_editor")`.
- All three writes emit an `audit_log` row via E.28's `AuditLogService.log_action()`, consistent with B-08's existing pattern.

## 12. Database Requirements
`ramadan_campaigns(campaign_id PK, region, hijri_start_date, eid_date, eid_date_overridden)`, `UNIQUE(region, year-derived-from-hijri_start_date)`. Index `(region)`.

## 13. Validation
No client-supplied `region` field exists on the request schema at all — its absence from the schema is itself part of the guarantee, not merely an ignored-if-present field.

## 14. Authentication
`get_current_parent` (or `get_current_user` resolving to the parent's own session).

## 15. Authorization
Standard authenticated-parent access — no elevated scope required for a read-only status check.

## 16. Error Handling
No `ramadan_campaigns` record for the parent's region: returns a `phase: "not_active"` state rather than an error (the season simply hasn't been configured/hasn't started for that region yet).

## 17. Offline First
N/A at this endpoint (server orchestration layer) — client-side offline behavior for consumers of this response is covered in K-01/K-02.

## 18. Local Data
N/A — server is the sole source of truth for phase/night; no local computation permitted downstream (enforced structurally in K-01).

## 19. Localization
N/A — response is data-only (enum phase values, ISO dates); all display-string localization happens client-side in KMP.

## 20. RTL
N/A — no directional UI at this layer.

## 21. Analytics
`ramadan_region_window_recalculated` per §1.19, logged when a parent's region change triggers a different active campaign record going forward.

## 22. Performance
Indexed lookup on `region`; response cacheable per-region with a short TTL given its low mutation frequency (campaign dates rarely change outside admin overrides).

## 23. Security
Server-side-only region resolution is this sub-feature's single highest-priority guarantee — mandatory test confirms that even if a request includes a `region` query/body parameter with a different value, the response is computed using the parent's actual Profile region, proving the parameter has zero effect (ideally by confirming the schema itself has no such field, making this a structural rather than logical guarantee).

## 26. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Alembic. No new libraries.

## 27. Testing
Unit: phase-computation date-arithmetic logic for all six phases. Integration: **mandatory** — a request including a client-supplied `region` value different from the parent's actual Profile region produces a response computed from the Profile region, not the supplied one (ideally proven via schema-introspection showing no such field exists); region-change-mid-Ramadan test confirming prior `ramadan_journey_progress` rows remain intact and unaffected while future phase computation uses the new region.

## 28. Documentation
OpenAPI docstring explicitly stating region is never accepted as a request parameter, resolved server-side only.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Write Migration for `ramadan_campaigns`**
Objective: Table with region-uniqueness constraint. Why: source-of-truth table every other Ramadan sub-feature reads. Files to Create: `alembic/versions/xxxx_create_ramadan_campaigns_table.py`, `app/ramadan/models/campaign.py`. Do Not Change: no existing tables touched (additive only, FR-11). Tests: migration up/down test. Definition of Done: schema created, migration reversible.

**Task 02 — Define Schemas Without a Region Field**
Objective: `CampaignStatusResponse`. Why This Is Required: the absence of a request-side region field is itself the security guarantee. Files to Create: `schemas/campaign_status_schema.py`. Dependencies: Task 01. Tests: **mandatory** — schema-introspection test confirming no region-accepting field exists on the request path. Definition of Done: test passes.

**Task 03 — Implement `CampaignRepository`**
Objective: Region-keyed campaign lookup, generic enough to later support Admin CRUD once that contract is confirmed (see §10). Existing Architecture to Follow: `BaseRepository[ModelT]`. Files to Create: `repositories/campaign_repository.py`. Dependencies: Task 01. Tests: repository tests. Definition of Done: tests pass.

**Task 04 — Implement `CampaignLifecycleService` with Profile-Sourced Region**
Objective: Phase/night computation reading region exclusively from the authenticated parent's Profile. Business Rules: six-phase state machine per FR-1. Files to Create: `services/campaign_lifecycle_service.py`. Dependencies: Task 03. Security: region resolution is profile-sourced only. Tests: **mandatory** — client-supplied-region-has-zero-effect test. Definition of Done: test passes.

**Task 05 — Implement the Router Endpoint**
Objective: `GET /v1/ramadan/campaign-status`. Files to Create: `routers/campaign_router.py`. Files to Modify: `routers/__init__.py`. Dependencies: Task 04. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 06 — Implement Region-Change Handling**
Objective: Confirm prior progress unaffected, future computation uses new region. Dependencies: Task 04. Tests: **mandatory** — region-change-preserves-progress test. Definition of Done: test passes.

**Task 07 — Implement Proposed Admin Campaign CRUD**
Objective: `list_campaigns()`, `create_campaign()`, `update_campaign()` on `CampaignRepository`/`CampaignLifecycleService`, plus `admin_campaign_router.py` exposing the three proposed endpoints from §11. Files to Create: `routers/admin_campaign_router.py`, `schemas/admin_campaign_schema.py`. Dependencies: Task 04, E.28's `AuditLogService`. Security: `require_admin_scope("content_editor")`; `eid_date_overridden` never settable via this router (only via B-08). Tests: CRUD tests, `UNIQUE(region, year)` conflict test, audit-log-written test, and a test confirming `PATCH` rejects an `eid_date_overridden` field in the request body. Definition of Done: tests pass.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §27, both mandatory tests included, plus Task 07's CRUD tests. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm zero code path anywhere reads a client-supplied region value for phase computation; confirm the proposed admin CRUD endpoints are clearly marked PROPOSED pending real contract sign-off, and that `eid_date_overridden` is unreachable from the general CRUD router. Definition of Done: checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] Region resolved exclusively from the parent's Profile record — mandatory test passing, ideally via schema-level absence of any region-accepting field
- [ ] Phase/night computation correct for all six lifecycle phases
- [ ] Region change mid-Ramadan recalculates future phase without affecting prior progress — mandatory test passing
- [ ] No `ramadan_campaigns` record for a region returns `not_active`, not an error
- [ ] Proposed Admin Campaign CRUD (§11) implemented and audit-logged, with `eid_date_overridden` reachable only through B-08's dedicated endpoint
- [ ] Proposed CRUD contract sign-off obtained from the API-contract owner before production release

## 31. Definition of Done
Ramadan's activation window is computed with a provably server-side-only, unmanipulable region source — this module's single highest-priority security guarantee.
