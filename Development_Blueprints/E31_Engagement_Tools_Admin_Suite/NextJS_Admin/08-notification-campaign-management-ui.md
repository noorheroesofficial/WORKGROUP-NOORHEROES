# N-08 — Notification Campaign Management UI

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the Admin Portal screens for campaign scheduling, segment building, test-device send, and delivery reporting, consuming **B-08 Notification Campaign Management API**. Split from template authoring (see **N-07 Notification Template Management UI**) per PRD §1.18's distinct screen grouping. Source: PRD §1.18 Screens 20–23, §2.2 (Campaign Scheduler screen spec), §6, §7 item 3.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
3.8 Notification Campaign Management UI (Admin ID: **N-08**)

## 4. Objective
Give content admins/notification managers a Campaign Scheduler that automatically detects whether the built segment includes child-mode recipients and, if so, forces template-selection mode — disabling/hiding any free-text body input entirely — mirroring B-08's structural backend rejection, with template options sourced only from N-07's approved template library.

## 5. Business Requirements
- Screen Inventory (PRD §1.18): #20 Campaign Scheduler, #21 Segment Builder, #22 Test-Device Send & Approval, #23 Delivery Report.
- Screen spec (PRD §2.2): template selector (approved templates only for child-targeted segments — free-text entry structurally unavailable in that mode), Segment Builder link, schedule picker, Test-Device Send, Approve-before-full-send gate. States: Draft, Test-sent, Approved, Scheduled, Sent, Canceled.
- Frontend AI Code-Gen Prompt item 3 (PRD §7): auto-detect child-mode recipients in the segment and FORCE template-selection mode, disabling/hiding free-text body input.

## 6. Existing Architecture
React + TypeScript, Admin Portal shell from E.28. Depends on **N-07** for the approved-template selector's data source.

## 7. Existing Code to Reuse
E.28 shell/design tokens; N-07's `NotificationTemplateAdminRepository` for fetching approved templates.

## 8. Files to Create
- `app/(admin)/engagement/notifications/campaigns/page.tsx`
- `app/(admin)/engagement/notifications/campaigns/[id]/page.tsx`
- `app/(admin)/engagement/notifications/campaigns/[id]/delivery-report/page.tsx`
- `components/engagement/notifications/CampaignScheduler.tsx`
- `components/engagement/notifications/SegmentBuilder.tsx`
- `components/engagement/notifications/TemplateVsFreeTextSwitcher.tsx`
- `components/engagement/notifications/TestDeviceSendPanel.tsx`
- `components/engagement/notifications/DeliveryReportView.tsx`
- `repositories/admin/NotificationCampaignAdminRepository.ts`
- `types/admin/notificationCampaign.ts`
- `__tests__/engagement/notifications/TemplateVsFreeTextSwitcher.test.tsx`

## 9. Files to Modify
- `components/shell/EngagementNavGroup.tsx`
- `lib/analytics/EngagementAdminAnalytics.ts`

## 10. Backend Requirements
Consumes **B-08** endpoints: `POST /v1/admin/notification-campaigns`, `PATCH .../{id}`, `POST .../{id}/cancel`, `POST .../{id}/test-send`, `GET .../{id}/delivery-report`. Consumes **B-07** (read-only) for the approved-template picker.

## 11. KMP Requirements
N/A — this UI configures campaigns delivered to the KMP app via B.17's existing delivery pipeline, unmodified here.

## 12. NextJS Requirements
- **Page:** Campaign Scheduler, Segment Builder (linked), Test-Device Send & Approval, Delivery Report.
- **Route:** `/engagement/notifications/campaigns`, `/engagement/notifications/campaigns/[id]`, `/engagement/notifications/campaigns/[id]/delivery-report`.
- **Component:** `CampaignScheduler` (composes `SegmentBuilder` + `TemplateVsFreeTextSwitcher` + schedule picker + `TestDeviceSendPanel`), `TemplateVsFreeTextSwitcher` (the signature component — inspects the current segment definition client-side and forces template-only mode when child-mode recipients are detected; template dropdown sourced only from N-07's `approved=true` templates), `DeliveryReportView`.
- **API Client:** `NotificationCampaignAdminRepository`.
- **Type Definition:** `NotificationCampaign`, `SegmentDefinition`, `CampaignCreateInput` (a discriminated union: `{ mode: "template"; template_id: string }` or `{ mode: "freetext"; free_text_body: string }` — the type system itself prevents constructing a `freetext` payload when the segment is child-inclusive, via a runtime-checked helper, not just a UI convention).
- **Form:** React Hook Form + Zod; schema selection (`template` vs `freetext` object shape) is conditionally validated based on segment composition.
- **Validation:** `TemplateVsFreeTextSwitcher` calls a client-side "does this segment include child-mode recipients" resolver (mirroring B-08's server-side logic) on every segment change, and when true: hides/disables the free-text textarea entirely (not just grays it out — it must not be present in the DOM/tab order at all), requires template selection, and only lists `approved=true` templates from N-07.
- **Authentication/Authorization:** `content_editor`+/`notification_manager`.
- **States:** Draft, Test-sent, Approved, Scheduled, Sent, Canceled — implemented as an explicit campaign status state machine driving which actions are available.
- **Loading/Empty/Error States:** standard.
- **Pagination/Filtering/Sorting:** campaign list by status.
- **Responsive/Accessibility/RTL:** standard; localization coverage indicator shown in Segment Builder per Edge Case 7.
- **Analytics:** `notification_campaign_scheduled`, `notification_test_device_send_completed`.
- **Performance:** debounce segment-composition resolution calls.
- **Testing:** signature UI test for both child-inclusive (template-only, free-text absent from DOM) and parent-only (free-text permitted) segment compositions (PRD §7 item 3).

## 13. API Contract
Reuses B-08's contract verbatim (see `Backend/08-notification-campaign-management-api.md` §13).

## 14. Database Requirements
N/A.

## 15. Validation
Client-side segment-composition detection mirrors backend logic; server (B-08) remains authoritative — if a stale client state somehow permits a free-text submission for what turns out to be a child-inclusive segment, the server's `422 FREETEXT_NOT_ALLOWED_FOR_CHILD_AUDIENCE` is gracefully surfaced.

## 16. Authentication
Inherits E.28 session.

## 17. Authorization
`content_editor`+/`notification_manager`.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Server `422 FREETEXT_NOT_ALLOWED_FOR_CHILD_AUDIENCE` (stale client state) | Form switches to template-only mode with explanatory message, preserves entered template selection if any |
| Server `422 TEMPLATE_NOT_APPROVED` | Template dropdown refreshes to exclude the now-invalid selection with explanatory message |
| Server `422 TRANSLATION_COVERAGE_GAP` | Segment Builder highlights the specific locale(s) lacking translation, blocks scheduling until resolved |
| `409 CAMPAIGN_ALREADY_SENT` on edit attempt | Edit form becomes read-only with explanatory banner |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Central — Segment Builder surfaces per-locale translation-coverage status sourced from N-07's templates.

## 22. RTL
Full RTL support.

## 23. Analytics
`notification_campaign_scheduled`, `notification_test_device_send_completed`.

## 24. Performance
Debounced (400ms) segment-composition resolution; delivery report data fetched with polling only while campaign status is `sent` and report is still aggregating.

## 25. Security
`TemplateVsFreeTextSwitcher`'s DOM-level removal (not just disabling) of the free-text input when child-mode recipients are detected is treated as this sub-feature's primary child-safety UI contribution, directly mirroring B-08's structural backend rejection — this is the PRD's signature test requirement (§7 item 3) and must be CI-blocking.

## 26. Library Requirements
React, TypeScript, React Hook Form, Zod (discriminated union schema), React Query, Jest/RTL.

## 27. Testing
- **UI test (signature, child-inclusive):** build a segment including a child age-band; assert the free-text textarea is entirely absent from the rendered DOM and template selection (from N-07's approved list) is required.
- **UI test (signature, parent-only):** build a parent-only segment; assert the free-text textarea IS present and usable.
- **Integration:** Edge Case 7 — segment including an untranslated locale blocks scheduling with a clear message.
- **Unit:** segment-composition resolver logic.

## 28. Documentation
Document the client-side segment-composition resolver's exact parity requirement with B-08's server-side logic — if they drift, the UI's forced-template-mode could become either too permissive (bad) or too restrictive (annoying); both are flagged as regressions.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Types & API Client**
- Task ID: N-08-T01
- Files to Create: `types/admin/notificationCampaign.ts`, `repositories/admin/NotificationCampaignAdminRepository.ts`.
- Dependencies: B-08, N-07.
- Definition of Done: typed repository unit-tested.

**Task 02 — Segment Builder & Composition Resolver**
- Task ID: N-08-T02
- Files to Create: `components/engagement/notifications/SegmentBuilder.tsx`.
- Implementation Details: client-side resolver determining child-inclusive vs. parent-only, mirroring B-08.
- Dependencies: Task 01.
- Definition of Done: resolver unit-tested against multiple segment compositions.

**Task 03 — Campaign Scheduler with Template/Free-Text Switcher (Signature Task)**
- Task ID: N-08-T03
- Files to Create: `components/engagement/notifications/CampaignScheduler.tsx`, `components/engagement/notifications/TemplateVsFreeTextSwitcher.tsx`.
- Implementation Details: DOM-level removal (not disabling) of free-text input for child-inclusive segments; template dropdown sourced from N-07's approved templates only.
- Dependencies: Tasks 01–02.
- Definition of Done: both signature UI tests (child-inclusive, parent-only) pass — CI-blocking per PRD §7 item 3.

**Task 04 — Test-Device Send, Approval Gate, Delivery Report**
- Task ID: N-08-T04
- Files to Create: `components/engagement/notifications/TestDeviceSendPanel.tsx`, `components/engagement/notifications/DeliveryReportView.tsx`, `app/(admin)/engagement/notifications/campaigns/[id]/delivery-report/page.tsx`.
- Dependencies: Task 03.
- Definition of Done: full Draft → Test-sent → Approved → Scheduled → Sent state flow functional.

**Task 05 — Campaign List Screen**
- Task ID: N-08-T05
- Files to Create: `app/(admin)/engagement/notifications/campaigns/page.tsx`, `app/(admin)/engagement/notifications/campaigns/[id]/page.tsx`.
- Dependencies: Tasks 01–04.
- Definition of Done: list and detail screens functional.

**Task 06 — Permission Gating & Accessibility**
- Task ID: N-08-T06
- Dependencies: Tasks 03–05.
- Definition of Done: accessibility audit passes.

**Task 07 — Tests & Documentation**
- Task ID: N-08-T07
- Dependencies: Tasks 01–06.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Campaign/segment/test-send/delivery-report screens functional against B-08 and N-07; signature template-vs-free-text forcing behavior proven for both audience compositions; translation-coverage gap detection surfaced clearly.

## 31. Final Verification Checklist
- [ ] Free-text input entirely absent from DOM for child-inclusive segments (signature test green)
- [ ] Free-text input present and usable for parent-only segments (signature test green)
- [ ] Template dropdown sourced only from N-07's approved templates
- [ ] Segment Builder surfaces translation-coverage gaps per locale (Edge Case 7)
- [ ] Campaign status state machine (Draft/Test-sent/Approved/Scheduled/Sent/Canceled) implemented
- [ ] Edit blocked once campaign already sent
- [ ] Delivery Report renders accurate delivery/open rates
- [ ] `content_editor`+/`notification_manager` gating enforced
- [ ] Loading/empty/error states implemented
- [ ] Responsive, accessible, RTL-supported
- [ ] Analytics events fire correctly
- [ ] No school/madrasa/institutional-tier logic introduced
