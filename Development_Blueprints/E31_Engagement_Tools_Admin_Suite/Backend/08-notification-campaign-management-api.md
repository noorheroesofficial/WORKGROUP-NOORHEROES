# B-08 — Notification Campaign Management API

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the campaign scheduling, segment-building, test-send/approval, and delivery-reporting surface, split out from template authoring (see **B-07 Notification Template Management API**) because the PRD treats the Campaign Scheduler/Segment Builder/Test-Device Send/Delivery Report (Screens #20–23) as a distinct workflow from the Template Library/Editor (#18–19). Source: PRD §1.7 FR-6 (campaign portion), §1.18 Screens 20–23, §3.4, §5 item 4.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
1.8 Notification Campaign Management API (Backend ID: **B-08**)

## 4. Objective
Let content admins/notification managers build and schedule audience-segmented campaigns, while structurally guaranteeing that any campaign whose resolved audience includes child-mode recipients can only use B-07's approved templates — never free-text admin-authored copy — and that quiet-hours/bedtime policy is enforced server-side by B.17's delivery engine regardless of campaign configuration.

## 5. Business Requirements
- FR-6 (PRD §1.7, campaign portion): campaign scheduler, segment builder, delivery report. CRUD: create campaign, read delivery/open rates, update scheduled campaign (pre-send only), cancel a scheduled send.
- **Hard rule:** child-targeted campaigns restricted to approved templates only (from B-07) — no free-text admin-authored copy reaches a child surface without review.
- **Hard rule:** quiet-hours and bedtime policy enforced server-side regardless of campaign settings.
- Edge Case 7 (PRD §1.10): a campaign's audience segment includes a locale where none of the selected templates have been translated → must fail validation or clearly flag the gap before scheduling completes.

## 6. Existing Architecture
Extends B.17's Notification Service. FastAPI/SQLAlchemy 2.0/PostgreSQL, Router → Service → Repository layering. Depends on **B-07** for the set of approved, translated templates.

## 7. Existing Code to Reuse
- B.17's existing delivery engine, quiet-hours/bedtime enforcement logic, and delivery/open-rate tracking (not reimplemented here — this layer only schedules).
- B-07's `NotificationTemplateAdminRepository` for resolving approved templates and their translation coverage.
- E.28's audit log + RBAC; Localization Management's translation-coverage-threshold logic (cross-ref, reused not reimplemented).

## 8. Files to Create
- `app/routers/admin/notification_campaigns_router.py`
- `app/schemas/admin/notification_campaign_schemas.py`
- `app/services/admin/notification_campaign_admin_service.py`
- `app/repositories/admin/notification_campaign_admin_repository.py`
- `tests/admin/test_notification_campaign_admin_api.py`

## 9. Files to Modify
- `app/routers/admin/__init__.py`
- `app/core/audit.py` (`notification_campaign.scheduled`, `notification_campaign.freetext_child_copy_blocked`)

## 10. Backend Requirements
- **Database:** `notification_campaigns` (existing/extended from B.17), with `segment_definition JSONB`, `template_id` (nullable, FK to B-07's `notification_templates`), `free_text_body` (nullable, rejected structurally when audience is child-inclusive).
- **Migration:** additive only.
- **Model:** `NotificationCampaign`.
- **Schema/DTO:** `NotificationCampaignCreate` (`segment`, `template_id` OR `free_text_body`, `scheduled_at`), `NotificationCampaignUpdate` (pre-send only), `DeliveryReportRead`.
- **Repository:** `create_campaign()`, `list_campaigns()`, `update_campaign()` (blocked once `status != 'draft'/'scheduled'`), `cancel_campaign()`, `get_delivery_report()`.
- **Service:** `NotificationCampaignAdminService` — resolves audience segment to determine child-inclusive vs. parent-only; enforces `template_id` required + `free_text_body` rejected for child-inclusive audiences; validates translation coverage for every locale in the segment against the selected template (via B-07) before allowing `status` to transition to `scheduled`; delegates actual send/quiet-hours enforcement to B.17's existing delivery engine.
- **Router:** `POST /v1/admin/notification-campaigns`, `GET /v1/admin/notification-campaigns`, `PATCH /v1/admin/notification-campaigns/{id}` (pre-send only), `POST /v1/admin/notification-campaigns/{id}/cancel`, `POST /v1/admin/notification-campaigns/{id}/test-send`, `GET /v1/admin/notification-campaigns/{id}/delivery-report`.
- **Dependency Injection:** `require_role_any(["content_editor", "notification_manager"])`.
- **Validation:** child-inclusive audience → `template_id` required (must reference an `approved=true` template from B-07), `free_text_body` must be absent/null (reject with `422` if supplied); parent-only audience → `free_text_body` permitted; translation-coverage check across resolved locales before allowing `status` to transition to `scheduled`.
- **Business Rules:** quiet-hours/bedtime enforcement is NOT reimplemented here — this layer only schedules; B.17's existing delivery engine applies the policy at send time, and this layer must not expose any campaign field that could override it.
- **Exception Handling:** `422 FREETEXT_NOT_ALLOWED_FOR_CHILD_AUDIENCE`, `422 TRANSLATION_COVERAGE_GAP`, `422 TEMPLATE_NOT_APPROVED`.
- **Logging:** log every blocked free-text-for-child attempt as a security signal.
- **Caching:** N/A beyond what B.17 already caches for delivery.
- **Transaction:** campaign create/update + audit log in one transaction.
- **Pagination/Filtering/Sorting:** campaign list paginated, filterable by status.

## 11. KMP Requirements
N/A — admin-only. The KMP app is a notification recipient via B.17's existing delivery/receipt handling, unmodified by this layer.

## 12. NextJS Requirements
Consumed by **N-08 Notification Campaign Management UI**, whose Campaign Scheduler must auto-detect child-inclusive segments and force template-selection mode client-side, mirroring this backend's structural rejection.

## 13. API Contract

### `POST /v1/admin/notification-campaigns`
- **Request (child-inclusive audience):**
```json
{
  "segment": { "age_band": ["6 to 9", "9 to 12"], "locale": ["en", "ar"], "plan": "any", "engagement_state": "active" },
  "template_id": "uuid",
  "scheduled_at": "2026-09-01T10:00:00Z"
}
```
- **Request (parent-only audience, free-text permitted):**
```json
{
  "segment": { "audience_type": "parent_only", "plan": "premium" },
  "free_text_body": "Don't miss our Ramadan collection!",
  "scheduled_at": "2026-09-01T10:00:00Z"
}
```
- **Response (201):** `NotificationCampaignRead`
- **Errors:** `401`, `403`, `422 FREETEXT_NOT_ALLOWED_FOR_CHILD_AUDIENCE`, `422 TRANSLATION_COVERAGE_GAP`, `422 TEMPLATE_NOT_APPROVED`, `422 VALIDATION_ERROR`

### `PATCH /v1/admin/notification-campaigns/{id}`
- Only permitted while `status` ∈ {`draft`, `scheduled`}; rejected with `409 CAMPAIGN_ALREADY_SENT` otherwise.

### `POST /v1/admin/notification-campaigns/{id}/test-send`
- **Response (200):** dispatches to registered test devices; does not affect `status`.

### `POST /v1/admin/notification-campaigns/{id}/cancel`
- **Response (200):** `{ "id": "uuid", "status": "canceled" }`

### `GET /v1/admin/notification-campaigns/{id}/delivery-report`
- **Response (200):** delivery/open rates per PRD.

## 14. Database Requirements
- `notification_campaigns`: `segment_definition JSONB`, `template_id FK nullable` (references B-07's `notification_templates`), `free_text_body TEXT nullable`, `status`, application-layer-enforced binding rule that `free_text_body IS NULL` whenever the resolved segment is child-inclusive (cross-field conditional constraints impractical as a raw DB CHECK).

## 15. Validation
Child-inclusive audience → `template_id` required and must reference an `approved=true` template; `free_text_body` rejected; translation coverage validated per locale in segment against the template's translation set (via B-07) before scheduling.

## 16. Authentication
Admin JWT (E.28).

## 17. Authorization
`content_editor`+/`notification_manager` per PRD §2.3.

## 18. Error Handling
| Scenario | Response |
|---|---|
| Free-text body for child-inclusive audience | `422 FREETEXT_NOT_ALLOWED_FOR_CHILD_AUDIENCE` |
| `template_id` references an unapproved template | `422 TEMPLATE_NOT_APPROVED` |
| Segment includes a locale with no template translation | `422 TRANSLATION_COVERAGE_GAP` |
| Update attempted after campaign already sent | `409 CAMPAIGN_ALREADY_SENT` |
| Unknown campaign id | `404 NOT_FOUND` |
| Unauthorized/forbidden | `401`/`403` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Translation-coverage-threshold validation reused from Localization Management (cross-ref E.34) rather than reimplemented, applied against B-07's template translation set.

## 22. RTL
N/A at API layer.

## 23. Analytics
`notification_campaign_scheduled`, `notification_campaign_freetext_child_copy_blocked` (internal/security signal), `notification_test_device_send_completed` per PRD §1.19.

## 24. Performance
Audience-segment resolution uses indexed queries against the child/parent population tables; avoid resolving the full audience synchronously for very large segments — consider an async resolution job for delivery-report accuracy at scale (align with B.17's existing pattern).

## 25. Security
Approved-template-only enforcement for child-inclusive audiences is this sub-feature's primary child-safety contribution (PRD §12.7) — reuses B-07/B.17's governance rather than introducing a second, parallel copy-review mechanism (PRD §3.5).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2, pytest-asyncio.

## 27. Testing
- Unit: audience-segment child-inclusive detection logic.
- Integration: signature test — free-text body rejected when audience includes child-mode recipients (PRD §5 item 4); second test confirming parent-only-targeted campaign MAY use free-text body successfully; third test confirming `template_id` referencing an unapproved (from B-07) template is rejected.
- Edge cases: Edge Case 7 — translation-coverage gap in a seasonal-campaign segment.
- Negative cases: unauthorized, update-after-sent.

## 28. Documentation
OpenAPI docs explicitly describing the audience-detection-driven validation branching and the dependency on B-07's approval status.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Database Model**
- Task ID: B-08-T01
- Files to Create/Modify: `app/models/notification_campaign.py` (extend if needed, FK to B-07's template model).
- Tests: migration test.
- Dependencies: B-07 (template model must exist).
- Do Not Change: B.17's existing delivery-engine tables/logic.
- Definition of Done: migration applies cleanly.

**Task 02 — Audience Resolution & Child-Inclusive Detection Service**
- Task ID: B-08-T02
- Objective: Build the logic that resolves a segment definition and determines if it includes any child-mode recipients.
- Files to Create: `app/services/admin/notification_campaign_admin_service.py`.
- Dependencies: Task 01.
- Definition of Done: unit tests covering various segment compositions (child-only, parent-only, mixed).

**Task 03 — Template/Free-Text Validation Branch**
- Task ID: B-08-T03
- Implementation Details: reject `free_text_body` for child-inclusive resolved audiences; require `template_id` in that case, validated against B-07's `approved=true` templates; permit `free_text_body` for parent-only.
- Tests: signature tests per §27.
- Dependencies: Task 02.
- Definition of Done: both signature tests green — highest-priority guarantee for this sub-feature.

**Task 04 — Translation Coverage Validation**
- Task ID: B-08-T04
- Implementation Details: call into Localization Management's existing coverage-threshold check for each locale in the resolved segment, against B-07's template translation set.
- Tests: Edge Case 7 test.
- Dependencies: Task 02, B-07.
- Definition of Done: test passes.

**Task 05 — API Endpoints**
- Task ID: B-08-T05
- Files to Create: `app/routers/admin/notification_campaigns_router.py`.
- Dependencies: Tasks 02–04.
- Definition of Done: integration tests green.

**Task 06 — Documentation & Final Review**
- Task ID: B-08-T06
- Dependencies: Tasks 01–05.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Free-text-for-child-audience rejection proven; parent-only free-text permission proven; unapproved-template rejection proven; translation-coverage gap detection proven; pre-send-only update enforcement proven; all endpoints audited and tested.

## 31. Final Verification Checklist
- [ ] Child-inclusive audience campaign requires `template_id`, rejects `free_text_body` (`422`)
- [ ] Parent-only audience campaign permits `free_text_body`
- [ ] `template_id` must reference an `approved=true` template from B-07
- [ ] Translation-coverage gap detected and blocks/flags scheduling (Edge Case 7)
- [ ] Campaign update blocked once already sent (`409`)
- [ ] Test-send and cancel-scheduled-send endpoints functional
- [ ] Delivery report endpoint returns accurate delivery/open rates
- [ ] Audit log entries written for every mutation, including blocked free-text attempts
- [ ] Unauthorized/forbidden paths tested
- [ ] No school/madrasa/institutional-tier logic introduced
- [ ] PostgreSQL/Redis credentials untouched
