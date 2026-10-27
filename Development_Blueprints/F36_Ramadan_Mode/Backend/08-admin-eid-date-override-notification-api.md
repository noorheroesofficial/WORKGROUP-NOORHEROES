# B-08 — Admin Eid-Date Override & Notification API

## 1. Feature Context
The `super_admin`-restricted correction path for the rare but consequential case of a moon-sighting dispute — updating the served Eid date and pushing a one-time notification, so every family's in-progress UI re-syncs to the corrected date on next open.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
1.8 Admin Eid-Date Override & Notification API (ID: **B-08**)

## 4. Objective
Build `POST /v1/admin/ramadan/eid-date-override`, updating `ramadan_campaigns.eid_date` via B-02's override mechanism and triggering a one-time notification through B.17's existing infrastructure.

## 5. Business Requirements
- FR-3: a moon-sighting-disputed Eid date triggers an Admin override that updates the `ramadan_campaigns` record and pushes a one-time notification; in-progress UI re-syncs on next app open.
- §5 Backend AI prompt item 6: update `ramadan_campaigns.eid_date` and trigger a one-time notification via B.17's existing infrastructure — test confirms subsequent campaign-status calls reflect the corrected date.
- §12.5: Eid-date-override restricted to `super_admin` given its broad regional impact.

## 6. Existing Architecture
`ramadan` bounded context, `app/ramadan/routers/admin_eid_override_router.py`, calling B-02's `HijriCalendarService.apply_override()` write path and B.17's existing notification-dispatch service.

## 7. Existing Code to Reuse
- B-02's `HijriCalendarService.apply_override()` (the only sanctioned caller of this write path)
- B.17's `app/notifications/services/notification_dispatch_service.py::NotificationDispatchService` (called as-is for the one-time push)
- E.28's `AuditLogService.log_action()`, `require_admin_scope()`

## 8. Files to Create
- `app/ramadan/routers/admin_eid_override_router.py`
- `app/ramadan/services/eid_override_service.py`
- `app/ramadan/schemas/eid_override_schema.py`

## 9. Files to Modify
- `app/ramadan/routers/__init__.py` — register router

## 10. Backend Requirements
- `EidOverrideService.apply_override()`: calls B-02's `HijriCalendarService.apply_override()` to update `ramadan_campaigns.eid_date` for the specified region and set `eid_date_overridden=true`, then calls `NotificationDispatchService.send_one_time()` (B.17's existing method, not reimplemented) targeting all families in the affected region.
- The write and the notification-trigger happen within the same service call — a partial-failure scenario (date updated but notification dispatch fails) is logged as a distinct alertable condition (cross-ref B.17's own delivery-failure handling) rather than silently succeeding.
- Subsequent `campaign-status` calls (B-01) immediately reflect the corrected date, since B-01 reads directly from `ramadan_campaigns`.

## 11. Required API / API Contract
`POST /v1/admin/ramadan/eid-date-override` `{region, corrected_eid_date, source_note}` → `200`. **Admin API.**

## 12. Database Requirements
Writes to `ramadan_campaigns.eid_date`/`eid_date_overridden` (B-01's schema) and `moon_sighting_overrides` (B-02's schema); writes an `audit_log` row (E.28).

## 13. Validation
`corrected_eid_date` sanity-bounded near the algorithmically-expected date (same bound as B-02's override validation); `region` must reference an existing campaign.

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`require_admin_scope("super_admin")` — this action's broad regional impact justifies the platform's most restrictive scope, above the `content_editor` scope used elsewhere in this module's admin surface.

## 16. Error Handling
`404` for unknown region/campaign; notification-dispatch failure logged and alerted but does not roll back the date update (the date correction itself is the higher-priority action; notification is best-effort but monitored).

## 17. Offline First
N/A — admin-only, always-online operation.

## 18. Local Data
N/A.

## 19. Localization
N/A at this endpoint — the resulting notification's localization is B.17's existing responsibility.

## 20. RTL
N/A.

## 21. Analytics
`ramadan_eid_date_admin_override_applied` per §1.19.

## 22. Performance
Single-region write, low-frequency action; notification dispatch is async/best-effort per B.17's existing pattern.

## 23. Security
`super_admin`-only restriction is this sub-feature's core guarantee, given a mistaken or malicious Eid-date change would affect an entire region's families mid-season — mandatory test confirms a `content_editor`-scoped admin (a lower privilege level used elsewhere in this module) is rejected from this specific endpoint.

## 26. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async. No new libraries.

## 27. Testing
Unit: sanity-bound validation on the corrected date. Integration: **mandatory** — after an override, a subsequent `GET /v1/ramadan/campaign-status` call for the affected region reflects the corrected `eid_date`; **mandatory** — a `content_editor`-scoped admin is rejected from this endpoint, only `super_admin` succeeds; notification-dispatch-failure logs an alertable condition without rolling back the date update.

## 28. Documentation
OpenAPI docstring noting the `super_admin`-only restriction and its rationale.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Schemas**
Objective: `EidDateOverrideRequest`. Files to Create: `schemas/eid_override_schema.py`. Tests: schema validation. Definition of Done: tests pass.

**Task 02 — Implement `EidOverrideService`**
Objective: Calls B-02's write path + B.17's notification dispatch. Files to Create: `services/eid_override_service.py`. Dependencies: B-02, B.17. Tests: **mandatory** — campaign-status-reflects-correction-immediately test. Definition of Done: test passes.

**Task 03 — Implement the Router Endpoint with `super_admin` Scope**
Objective: `POST /v1/admin/ramadan/eid-date-override`. Files to Create: `routers/admin_eid_override_router.py`. Dependencies: Task 02, E.28. Tests: **mandatory** — `content_editor`-rejected/`super_admin`-succeeds scope test. Definition of Done: test passes.

**Task 04 — Implement Partial-Failure Handling**
Objective: Notification-dispatch failure logs/alerts without rolling back the date update. Dependencies: Task 02. Tests: partial-failure test. Definition of Done: test passes.

**Task 05 — Wire Audit Logging**
Objective: Log every override with acting admin, region, and corrected date. Dependencies: Task 03. Tests: audit-entry test. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §27, both mandatory tests included. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm the scope restriction is genuinely `super_admin`-only and cannot be satisfied by any broader role set used elsewhere in this module. Definition of Done: checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] Override immediately reflected in subsequent `campaign-status` calls — mandatory test passing
- [ ] Restricted to `super_admin` only, `content_editor` correctly rejected — mandatory test passing
- [ ] One-time notification dispatched via B.17's existing infrastructure
- [ ] Notification-dispatch failure logged/alerted without blocking the date correction
- [ ] Every override audit-logged

## 31. Definition of Done
Moon-sighting disputes are correctable through a properly restricted, audited, and reliably-propagating admin action — every family's app re-syncs to the corrected date on next open, with the correction itself never silently lost to a notification-delivery hiccup.
