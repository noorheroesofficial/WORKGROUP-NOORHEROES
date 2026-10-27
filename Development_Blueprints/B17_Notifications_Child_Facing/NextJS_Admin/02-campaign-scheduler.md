# N-02 — Campaign Scheduler

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). Admin surface for creating/scheduling admin-authored campaigns (e.g., seasonal-event pushes) with preview, test audience, schedule, cancel, and kill switch (FR-7) — every campaign routes through the same backend Policy Engine pipeline as automated triggers.

## 2. Parent Feature
B.17 Notifications (Child-Facing) — NextJS Admin

## 3. Sub-feature
N-02 Campaign Scheduler

## 4. Objective
Build the Campaign Scheduler page: create/schedule campaigns with a live preview, test-audience send, scheduling controls, cancel action, and a global kill switch — all submitted to B-07's API with no separate/bypassing delivery path in this UI.

## 5. Business Requirements
- Live preview (rendering the template with sample data), a test-audience send option (limited to a small, explicitly-marked-as-test segment), scheduling controls, a cancel action for any not-yet-sent scheduled campaign, and a global kill switch halting all in-flight sends (PRD §9 item 2).
- Every campaign created here is submitted to the same backend Policy Engine pipeline as automated triggers — this admin tool has no separate, bypassing delivery path (PRD §9 item 2, §12.5).
- Every mutating action writes an immutable `audit_log` row (PRD §9 preamble).
- Campaign Scheduler CRUD permissions: Create campaign/Read performance/Update pre-send only/Cancel a scheduled send, behind `notification_manager`/`content_editor` role (PRD §8).

## 6. Existing Architecture
- Extends the Admin Portal "Notification Management" module (PRD §8).
- Embeds N-03 Segment Builder as a sub-component of the campaign creation flow (PRD §9 item 2 lists Segment Builder as part of Campaign Scheduler's tooling).
- Follows `NEXT-JS-INSTRUCTIONS.md` conventions for forms, tables, RBAC.

## 7. Existing Code to Reuse
- N-01's template selector (choosing which governed template the campaign uses).
- Existing Admin Portal RBAC/role-context provider, audit-log display components (if any exist elsewhere in the portal).

## 8. Files to Create
- `app/(admin)/notifications/campaigns/page.tsx` — list view (draft/scheduled/sending/sent/canceled/killed).
- `app/(admin)/notifications/campaigns/new/page.tsx` — creation wizard (template select → segment → preview → schedule).
- `components/notifications/CampaignPreview.tsx`.
- `components/notifications/CampaignTestSendControl.tsx`.
- `components/notifications/CampaignKillSwitchButton.tsx` (with confirmation modal, given its destructive/high-impact nature).
- `lib/api/notifications/campaigns.ts` — API client.
- `lib/types/notifications.ts` — extend with `NotificationCampaign`, `CampaignStatus`.
- `tests/notifications/CampaignScheduler.test.tsx`.

## 9. Files to Modify
- Admin Portal navigation — add "Campaigns" entry under Notification Management.

## 10. Backend Requirements
Consumes B-07's `POST/GET/PATCH /v1/admin/notifications/campaigns`, `/preview`, `/test-send`, `/cancel`, `/kill-switch` exactly as documented.

## 11. KMP Requirements
Not applicable — campaign delivery reuses the standard mobile push/deep-link path; no admin-specific KMP work.

## 12. NextJS Requirements
- Page: campaign list with status filter (draft/scheduled/sending/sent/canceled/killed).
- Page: creation wizard — select template (from N-01), configure segment (embeds N-03), preview with sample data, choose schedule time or test-send.
- Component: kill-switch control with a clear confirmation step given its destructive, immediate, in-flight-halting effect.
- API Client: typed wrapper over B-07's endpoints.
- Type Definition: `NotificationCampaign` matching B-07's schema.
- Form/Validation: `scheduled_at` must be a future timestamp (client-side hint, server-authoritative).
- Authentication/Authorization: `notification_manager`/`content_editor` role gates create/schedule/cancel/kill-switch; read-only view for other permitted roles.
- Loading/Empty/Error States: per standard portal conventions.
- Pagination/Filtering/Sorting: campaign list paginated, filterable by status.
- Responsive UI/Accessibility: standard portal conventions.
- Testing: full creation → preview → test-send → schedule → cancel/kill-switch flow.

## 13. API Contract
Consumes B-07 §13 exactly, including the `422` blocklist-violation response when a child-facing-targeted campaign's template fails B-04's gate.

## 14. Database Requirements
N/A (frontend only; data owned by B-07's `notification_campaigns` table).

## 15. Validation
Client-side scheduling-time and segment-completeness checks are advisory; server validation (B-07) is authoritative, including the blocklist gate re-verification.

## 16. Authentication
Admin session via existing Admin Portal auth context.

## 17. Authorization
`notification_manager`/`content_editor` role required for all mutating actions; kill-switch additionally requires an explicit confirmation step in the UI given its operational-safety criticality.

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Template fails blocklist (`422`) at campaign creation | Clear error directing admin back to N-01 to fix the template, or select a different one |
| Cancel attempted on already-sent campaign (`409`) | Inline error, cancel control disabled once status is `sending`/`sent` |
| Kill-switch attempted on fully-sent campaign (`409`) | Inline error, kill-switch control disabled once status is `sent` |
| Segment resolves to zero recipients | Warning shown before allowing schedule, not a hard block (mirrors B-07's default behavior) |
| Network/API failure | Toast/error state with retry |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Campaign preview renders the template rendered per-locale (reusing B-04's renderer via preview API); admin can preview across all four locales before scheduling.

## 22. RTL
Preview correctly renders AR/UR text direction when previewing those locale variants.

## 23. Analytics
Not applicable directly; campaign-level send/suppression events are captured server-side and surfaced via N-04's reporting dashboard.

## 24. Performance
Campaign list paginated server-side; preview rendering is on-demand (not eagerly computed for every locale on page load).

## 25. Security
No separate delivery path exists in this UI — every "Schedule"/"Test Send" action calls the exact same B-07 endpoints that route through B-03's Policy Engine; verify this via an integration test asserting the UI never calls any alternate/direct-send endpoint.

## 26. Library Requirements
Next.js (App Router), TypeScript, React, existing Admin Portal component library.

## 27. Testing
- Unit: campaign creation form validation.
- Integration: full wizard flow (template select → segment → preview → schedule).
- Integration: kill-switch requires confirmation and correctly disables once a campaign is fully sent.
- Integration: template blocklist violation during campaign creation surfaces correctly and blocks scheduling.
- Security: verify no alternate/bypassing send path exists in the client code (static/contract test).

## 28. Documentation
Document the kill-switch's destructive, immediate-effect nature prominently in the component and in any admin user documentation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Types & API Client**
- Files to Create: `lib/api/notifications/campaigns.ts`, type extensions.

**Task 02 — Implement Campaign List Page**
- Files to Create: `campaigns/page.tsx`.
- Implementation Details: status filter, pagination.
- Tests: list rendering test.

**Task 03 — Implement Creation Wizard (Template + Segment + Preview)**
- Files to Create: `campaigns/new/page.tsx`, `CampaignPreview.tsx`.
- Existing Files to Reuse: N-01 template selector, N-03 Segment Builder (embedded).
- Tests: wizard flow integration test.

**Task 04 — Implement Test-Send Control**
- Files to Create: `CampaignTestSendControl.tsx`.
- Business Rules: PRD §9 item 2 — limited to explicitly-marked-as-test segment.
- Tests: test-send flow test.

**Task 05 — Implement Schedule & Cancel Actions**
- Files to Modify: `campaigns/[id]/page.tsx` (or wizard's final step).
- Error Handling: `409` handling per §18.
- Tests: schedule + cancel flow tests.

**Task 06 — Implement Kill-Switch Control with Confirmation**
- Files to Create: `CampaignKillSwitchButton.tsx`.
- Why Required: PRD §9 item 2, operationally critical safety control.
- Tests: mandatory confirmation-step test; disabled-when-fully-sent test.

**Task 07 — Implement RBAC Gating**
- Files to Modify: all campaign-related components.
- Authorization: `notification_manager`/`content_editor`.
- Tests: RBAC rendering test per role.

**Task 08 — Write Full Test Suite, Security Verification, and Documentation**
- Tests: per §27, including the no-bypass-path security test.
- Documentation: per §28.

## 30. Definition of Done
- Full campaign lifecycle (create/preview/test-send/schedule/cancel/kill-switch) implemented in the UI, exclusively via B-07's API.
- Kill-switch requires explicit confirmation and correctly reflects campaign status constraints.
- No alternate/bypassing send path exists anywhere in this UI.

## 31. Final Verification Checklist
- [ ] Campaign list correctly filters/paginates by status
- [ ] Creation wizard produces a valid campaign via B-07's exact API contract
- [ ] Preview renders correctly across all four locales
- [ ] Test-send is scoped only to an explicitly-marked test segment
- [ ] Cancel is disabled once a campaign is sending/sent, matching server-side `409` behavior
- [ ] Kill-switch requires confirmation and is disabled once fully sent
- [ ] No alternate/bypassing delivery path exists in the client code
- [ ] RBAC correctly gates all mutating actions
- [ ] Full test suite passes
