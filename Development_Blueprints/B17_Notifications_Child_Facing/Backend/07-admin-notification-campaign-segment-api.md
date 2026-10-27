# B-07 — Admin Notification Campaign & Segment API

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). Every campaign (even automated, trigger-based ones) is governed by the same server-side policy engine — no notification path may bypass quiet-hours/fatigue-budget enforcement (FR-4), including admin-authored campaigns layered on top of the automated trigger catalog (FR-7).

## 2. Parent Feature
B.17 Notifications (Child-Facing) — Backend (FastAPI)

## 3. Sub-feature
B-07 Admin Notification Campaign & Segment API

## 4. Objective
Implement the Admin API for creating, previewing, scheduling, canceling, and kill-switching admin-authored campaigns (e.g., seasonal-event pushes), plus a segment-audience builder — with every campaign routed through the same B-03 Policy Engine pipeline as automated triggers, never a separate bypassing delivery path.

## 5. Business Requirements
- Every campaign supports preview, test audience, schedule, cancel, and kill switch (FR-7) — applies to admin-authored campaigns, not the automated trigger catalog itself.
- A family-wide campaign (e.g., Ramadan mode activation) must resolve to delivering an appropriately-worded version to the parent's binding AND to each currently-active child's binding across however many devices the family has, respecting each binding's own policy checks independently — a child's own quiet-hours still apply to their copy of a family-wide campaign (Edge Case 9).
- Segment Builder never directly exposes raw child identities to the campaign-authoring admin — aggregate segment size estimates only.
- Every mutating action (create/schedule/cancel/kill-switch) writes an immutable audit log row.

## 6. Existing Architecture
- Extends `src/noorheroes/modules/notifications/` (`FAST-API-INSTRUCTIONS.md` §5.8).
- Campaign creation must call into B-02's `NotificationIntentService` to create per-recipient intents (one per parent/active-child binding in the resolved segment), which then flow through B-03's Policy Engine identically to automated triggers — this sub-feature must not implement its own delivery path.
- Reuses the existing Admin Portal RBAC/audit-log infrastructure already established elsewhere in the Admin bounded context (`FAST-API-INSTRUCTIONS.md` §5.2).

## 7. Existing Code to Reuse
- `NotificationIntentService.create_intent()` (B-02) — campaigns create intents through this same service, tagged with a `campaign_id` reference.
- Existing Admin audit-log utility (from `admin` context).
- Existing Analytics segment-data source (read-only).

## 8. Files to Create
- `src/noorheroes/modules/notifications/campaign_service.py` — `CampaignService(BaseService)`.
- `src/noorheroes/modules/notifications/campaign_repository.py` — `CampaignRepository(BaseRepository[NotificationCampaign])`.
- `src/noorheroes/modules/notifications/segment_builder.py` — `SegmentBuilder.resolve(filters) -> SegmentEstimate`.
- Extend `models.py`: `NotificationCampaign`.
- `alembic/versions/<rev>_create_notification_campaign_table.py`.
- Extend `schemas.py`: `CampaignCreateRequest`, `CampaignPreviewResponse`, `CampaignResponse`, `SegmentFilterRequest`, `SegmentEstimateResponse`.
- Extend `api.py`: `POST/GET/PATCH /v1/admin/notifications/campaigns`, `POST /v1/admin/notifications/campaigns/{id}/preview`, `POST /v1/admin/notifications/campaigns/{id}/test-send`, `POST /v1/admin/notifications/campaigns/{id}/cancel`, `POST /v1/admin/notifications/campaigns/{id}/kill-switch`, `POST /v1/admin/notifications/segments/estimate`.
- `tests/modules/notifications/test_campaign_service.py`.

## 9. Files to Modify
- `src/noorheroes/modules/notifications/intent_service.py` — accept an optional `campaign_id` reference on intent creation.

## 10. Backend Requirements
- `CampaignService.create()` validates the campaign's template against B-04's blocklist validator before allowing schedule.
- `preview()` renders the template with sample data without creating any intents.
- `test_send()` creates intents scoped only to an explicitly-marked test segment.
- `schedule()` resolves the segment (parent + each currently-active child binding per family in scope) and creates one intent per resolved recipient via `NotificationIntentService.create_intent(campaign_id=...)`.
- `cancel()` is only valid for campaigns not yet sent; cancels all pending intents tagged with that `campaign_id`.
- `kill_switch()` immediately halts all in-flight sends for a campaign — marks all `processing`/`pending` intents for that `campaign_id` as `canceled` and signals the delivery worker to stop picking up further intents for it.
- `SegmentBuilder.resolve()` returns only an aggregate count/size estimate, never a list of child identities.
- Every mutating action writes an `audit_log` row (`actor_id`, `action`, `campaign_id`, `timestamp`).

## 11. KMP Requirements
Not applicable — campaign delivery reuses the standard mobile push/deep-link path (B-05/B-06); no campaign-specific KMP work.

## 12. NextJS Requirements
UI for this API is N-02 Campaign Scheduler and N-03 Segment Builder.

## 13. API Contract

**Required API — Admin API**
- **HTTP Method:** POST
- **Endpoint:** `/v1/admin/notifications/campaigns`
- **Request:** `{ "template_id": "uuid", "segment_filters": {...}, "scheduled_at": "iso8601" }`
- **Response 201:** `{ "campaign_id": "uuid", "status": "scheduled" }`
- **Authentication:** Bearer (admin session)
- **Authorization:** `notification_manager` or `content_editor` role
- **Validation:** template must pass B-04 blocklist if targeting any child segment; `scheduled_at` must be in the future
- **Error Responses:** `401`, `403`, `422` (blocklist violation or invalid segment filters)

- **HTTP Method:** POST `/v1/admin/notifications/campaigns/{id}/kill-switch` — halts all in-flight sends; `200` with updated status; `403` for insufficient role; `409` if campaign already fully sent (nothing to halt).

## 14. Database Requirements
- `notification_campaigns`: `campaign_id UUID PK`, `template_id UUID FK`, `segment_filters JSONB`, `status VARCHAR CHECK IN ('draft','scheduled','sending','sent','canceled','killed')`, `scheduled_at TIMESTAMPTZ`, `created_by UUID`, `created_at TIMESTAMPTZ`.
- `notification_intents.campaign_id` (nullable FK, added via migration to B-02's table).
- Uses existing `audit_log` table (admin context).

## 15. Validation
- Child-facing-targeted campaign templates must pass the B-04 blocklist before scheduling is allowed.
- `scheduled_at` must be a future timestamp; test-send segment must be explicitly marked test.

## 16. Authentication
Bearer JWT via admin session dependency.

## 17. Authorization
`notification_manager`/`content_editor` for create/schedule/cancel; same roles for kill-switch given its operational-safety nature.

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Template fails blocklist check | `422`, campaign cannot be scheduled |
| Cancel attempted on already-sent campaign | `409 Conflict` |
| Kill-switch attempted on fully-sent campaign | `409 Conflict`, nothing to halt |
| Segment resolves to zero recipients | Campaign created but flagged with a warning; scheduling still allowed (product decision — verify with PM if launch should be blocked; default behavior: allow with warning) |
| Database failure during schedule | Rollback, no partial intent set created |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Campaign delivers the template rendered per each recipient's own locale (reuses B-04's `TemplateRenderer`, not a single fixed-locale send).

## 22. RTL
N/A (backend); rendered copy direction handled by B-04.

## 23. Analytics
Campaign-level sends contribute to the same `notification_intent_created`/`notification_sent`/`notification_suppressed` event stream as automated triggers, tagged with `campaign_id` for attribution.

## 24. Performance
Segment resolution and per-recipient intent creation for a large family-wide campaign must be batched, not a synchronous per-recipient loop within the request/response cycle — schedule as a background task, return `202`-style scheduled confirmation immediately.

## 25. Security
No admin-exclusive bypass path exists — every campaign-created intent flows through the identical B-03 Policy Engine as automated triggers (PRD §12.5); this is verified via integration test asserting campaign intents are suppressible exactly like automated ones.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Celery (batch intent creation), Pydantic v2, pytest.

## 27. Testing
- Unit: campaign lifecycle state transitions (`draft→scheduled→sending→sent`, `→canceled`, `→killed`).
- Integration: family-wide campaign resolves to parent + each active child binding across multiple devices, each subject to its own policy checks (Edge Case 9).
- Integration: campaign template failing blocklist cannot be scheduled.
- Integration: kill-switch halts in-flight sends — assert no further intents for that `campaign_id` are processed after invocation.
- Integration: campaign-created intent is suppressible by the Policy Engine identically to an automated-trigger intent (no bypass).

## 28. Documentation
OpenAPI docs for all campaign lifecycle endpoints; document the no-bypass guarantee prominently.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create NotificationCampaign Model, Migration, and campaign_id FK on Intents**
- Files to Create/Modify: `models.py`, migration, `intent_service.py`.

**Task 02 — Implement SegmentBuilder**
- Files to Create: `segment_builder.py`.
- Implementation Details: filter by age band/locale/plan/engagement state; return aggregate estimate only, never raw identities.
- Tests: unit test asserting no individual child identity is ever returned.

**Task 03 — Implement CampaignService Create/Preview/Test-Send**
- Files to Create: `campaign_service.py`, `campaign_repository.py`.
- Business Rules: FR-7, blocklist validation via B-04.
- Tests: unit + integration tests for each action.

**Task 04 — Implement CampaignService Schedule (Family-Wide Resolution)**
- Objective: Correctly resolve family-wide segments to parent + each active child binding.
- Business Rules: Edge Case 9.
- Implementation Details: batched background intent creation via Celery, each intent created through `NotificationIntentService.create_intent(campaign_id=...)`.
- Tests: the mandatory Edge Case 9 integration test.

**Task 05 — Implement Cancel & Kill-Switch**
- Files to Modify: `campaign_service.py`.
- Implementation Details: cancel pending/processing intents by `campaign_id`; kill-switch additionally signals the delivery worker to stop further pickup.
- Tests: kill-switch halts in-flight sends test.

**Task 06 — Wire Admin API Endpoints & Audit Logging**
- Files to Modify: `api.py`, `schemas.py`.
- Authentication/Authorization: admin RBAC per §17.
- Implementation Details: audit log row on every mutating action.
- Tests: endpoint integration tests.

**Task 07 — Add No-Bypass Verification Test & Documentation**
- Objective: Prove campaign intents are policy-suppressible identically to automated ones.
- Tests: the mandatory no-bypass integration test.
- Documentation: per §28.

## 30. Definition of Done
- Full campaign lifecycle (create/preview/test-send/schedule/cancel/kill-switch) implemented and tested.
- Family-wide campaigns correctly resolve per-child, per-device, with independent policy enforcement.
- No separate delivery path exists — verified via the no-bypass integration test.
- Segment Builder never exposes raw child identities.

## 31. Final Verification Checklist
- [ ] Preview, test-send, schedule, cancel, and kill-switch all implemented and functional
- [ ] Campaign templates targeting child segments pass B-04 blocklist before scheduling is allowed
- [ ] Family-wide campaigns resolve to parent + each active child binding, respecting independent quiet-hours per child
- [ ] Segment Builder returns aggregate estimates only, never raw child identities
- [ ] Kill-switch halts all in-flight sends for a campaign immediately
- [ ] Campaign-created intents are suppressible by the Policy Engine identically to automated-trigger intents (no bypass verified)
- [ ] Every mutating action writes an immutable audit log row
- [ ] Full test suite passes
