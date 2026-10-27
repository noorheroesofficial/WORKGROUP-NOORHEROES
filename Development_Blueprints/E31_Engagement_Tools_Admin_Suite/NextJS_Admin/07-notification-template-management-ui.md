# N-07 — Notification Template Management UI

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the Admin Portal screens for the notification template library, consuming **B-07 Notification Template Management API**. Split from campaign scheduling (see **N-08 Notification Campaign Management UI**) per PRD §1.18's distinct screen grouping. Source: PRD §1.18 Screens 18–19, §6.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
3.7 Notification Template Management UI (Admin ID: **N-07**)

## 4. Objective
Give content admins/notification managers a clear authoring surface for push/in-app notification templates, with visible approval-status indication so admins understand a template must pass content-safety review before it becomes usable in a child-targeted campaign (N-08).

## 5. Business Requirements
- Screen Inventory (PRD §1.18): #18 Notification Template Library, #19 Notification Template Editor.
- Cross-cutting: templates authored here feed N-08's Campaign Scheduler, which enforces approved-template-only for child-inclusive audiences.

## 6. Existing Architecture
React + TypeScript, Admin Portal shell from E.28.

## 7. Existing Code to Reuse
E.28 shell/design tokens; E.29's list→editor data-table pattern; B.17's existing template-approval/content-safety-review UI patterns if already present elsewhere in the Admin Portal (reuse rather than reimplement a second review UI).

## 8. Files to Create
- `app/(admin)/engagement/notifications/templates/page.tsx`
- `app/(admin)/engagement/notifications/templates/[id]/page.tsx`
- `components/engagement/notifications/TemplateLibraryTable.tsx`
- `components/engagement/notifications/TemplateEditorForm.tsx`
- `components/engagement/notifications/TranslationCoverageIndicator.tsx`
- `repositories/admin/NotificationTemplateAdminRepository.ts`
- `types/admin/notificationTemplate.ts`
- `__tests__/engagement/notifications/TemplateEditorForm.test.tsx`

## 9. Files to Modify
- `components/shell/EngagementNavGroup.tsx`
- `lib/analytics/EngagementAdminAnalytics.ts`

## 10. Backend Requirements
Consumes **B-07** endpoints: `POST/GET /v1/admin/notification-templates`, `PATCH /v1/admin/notification-templates/{id}`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Page:** Template Library, Template Editor.
- **Route:** `/engagement/notifications/templates`, `/engagement/notifications/templates/[id]`.
- **Component:** `TemplateLibraryTable` (shows `approved` status badge per template), `TemplateEditorForm` (per-locale translation fields, channel selector), `TranslationCoverageIndicator`.
- **API Client:** `NotificationTemplateAdminRepository`.
- **Type Definition:** `NotificationTemplate`, `NotificationTemplateCreateInput`.
- **Form:** React Hook Form + Zod; per-locale translation inputs (English, Hindi, Arabic, Urdu).
- **Validation:** default-locale translation required before submit; `channel` required.
- **Authentication/Authorization:** `content_editor`+/`notification_manager`.
- **Loading/Empty/Error States:** standard; explicit "Pending Review" state distinct from "Approved" and "Rejected" (content-safety pipeline outcome).
- **Pagination/Filtering/Sorting:** by `channel`, `approved` status.
- **Responsive/Accessibility/RTL:** full RTL for Arabic/Urdu translation input fields.
- **Analytics:** `notification_template_created`.
- **Performance:** standard.
- **Testing:** UI test confirming editing an approved template surfaces a "this will require re-review" warning before submit, and that the resulting status updates to "Pending Review" after save.

## 13. API Contract
Reuses B-07's contract verbatim (see `Backend/07-notification-template-management-api.md` §13).

## 14. Database Requirements
N/A.

## 15. Validation
Default-locale translation required; `channel` ∈ {`push`, `in_app`}.

## 16. Authentication
Inherits E.28 session.

## 17. Authorization
`content_editor`+/`notification_manager`.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Server `422 CONTENT_REVIEW_REJECTED` | Clear rejection message with guidance to revise copy |
| Missing default-locale translation | Inline field error |
| `404` unknown template | Redirect to library with toast |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Central — templates authored per-locale (English, Hindi, Arabic, Urdu); `TranslationCoverageIndicator` shows which locales are complete.

## 22. RTL
Full RTL support for Arabic/Urdu translation input fields.

## 23. Analytics
`notification_template_created`.

## 24. Performance
Standard React Query caching.

## 25. Security
Editing an approved template must clearly warn the admin that it resets to "Pending Review" — preventing an admin from assuming a small copy tweak stays approved without re-review, mirroring B-07's structural re-review-on-edit guarantee.

## 26. Library Requirements
React, TypeScript, React Hook Form, Zod, React Query, Jest/RTL.

## 27. Testing
- **UI test:** editing an approved template shows a re-review warning and the resulting status updates to "Pending Review".
- **Integration:** full template create → review-pending → approved flow (assuming a review-outcome webhook/poll is simulated in tests).
- **Unit:** form validation.

## 28. Documentation
Document the approval-status state machine (Pending Review / Approved / Rejected) and its dependency relationship with N-08's campaign scheduler.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Types & API Client**
- Task ID: N-07-T01
- Files to Create: `types/admin/notificationTemplate.ts`, `repositories/admin/NotificationTemplateAdminRepository.ts`.
- Dependencies: B-07.
- Definition of Done: typed repository unit-tested.

**Task 02 — Template Library Screen**
- Task ID: N-07-T02
- Files to Create: `app/(admin)/engagement/notifications/templates/page.tsx`, `components/engagement/notifications/TemplateLibraryTable.tsx`.
- Implementation Details: approval-status badge per row.
- Dependencies: Task 01.
- Definition of Done: list renders with all states.

**Task 03 — Template Editor with Re-Review Warning**
- Task ID: N-07-T03
- Files to Create: `app/(admin)/engagement/notifications/templates/[id]/page.tsx`, `components/engagement/notifications/TemplateEditorForm.tsx`, `components/engagement/notifications/TranslationCoverageIndicator.tsx`.
- Dependencies: Task 01.
- Definition of Done: signature re-review-warning UI test passes.

**Task 04 — Permission Gating & Accessibility**
- Task ID: N-07-T04
- Dependencies: Tasks 02–03.
- Definition of Done: accessibility audit passes.

**Task 05 — Tests & Documentation**
- Task ID: N-07-T05
- Dependencies: Tasks 01–04.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Template Library/Editor screens functional against B-07; re-review-on-edit behavior clearly communicated; translation coverage visible.

## 31. Final Verification Checklist
- [ ] Template Library shows approval-status badge per template
- [ ] Editing an approved template warns of re-review before submit
- [ ] Translation coverage indicator shows per-locale completeness
- [ ] Default-locale translation required client-side
- [ ] `content_editor`+/`notification_manager` gating enforced
- [ ] Loading/empty/error states implemented
- [ ] Responsive, accessible, RTL-supported
- [ ] Analytics events fire correctly
- [ ] No school/madrasa/institutional-tier logic introduced
