# N-09 — Banner Management UI

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the Admin Portal screens for banner list/editor with placement scheduling, consuming **B-09**. Source: PRD §1.18 Screens 24–25, §6, §7 item 5.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
3.9 Banner Management UI (Admin ID: **N-09**)

## 4. Objective
Give content admins a Banner Editor that conditionally shows/validates the `destination_url` field based on the selected placement's `is_child_facing` flag — flagging an external URL as invalid for a child-facing placement and permitting it for a parent-facing one, mirroring B-09's scoped backend validation exactly.

## 5. Business Requirements
- Screen Inventory (PRD §1.18): #24 Banner List, #25 Banner Editor (with placement scheduler).
- Frontend AI Code-Gen Prompt item 5 (PRD §7): conditionally show/validate `destination_url` based on `is_child_facing`; test confirming external URL flagged invalid for child-facing, permitted for parent-facing.

## 6. Existing Architecture
React + TypeScript, Admin Portal shell from E.28.

## 7. Existing Code to Reuse
E.28 shell/design tokens; E.29's `ContentUploadRepository` for banner imagery.

## 8. Files to Create
- `app/(admin)/engagement/banners/page.tsx`
- `app/(admin)/engagement/banners/[id]/page.tsx`
- `components/engagement/banners/BannerListTable.tsx`
- `components/engagement/banners/BannerEditorForm.tsx`
- `components/engagement/banners/PlacementScheduler.tsx`
- `repositories/admin/BannerAdminRepository.ts`
- `types/admin/banner.ts`
- `__tests__/engagement/banners/BannerEditorForm.test.tsx`

## 9. Files to Modify
- `components/shell/EngagementNavGroup.tsx`
- `lib/analytics/EngagementAdminAnalytics.ts`

## 10. Backend Requirements
Consumes **B-09** endpoints: full CRUD on `/v1/admin/banners`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Page:** Banner List, Banner Editor.
- **Route:** `/engagement/banners`, `/engagement/banners/[id]`.
- **Component:** `BannerListTable`, `BannerEditorForm` (placement dropdown, `destination_url` field, imagery upload, date-range scheduler), `PlacementScheduler`.
- **API Client:** `BannerAdminRepository`.
- **Type Definition:** `Banner`, `BannerCreateInput`.
- **Form:** React Hook Form + Zod; Zod `.refine()` cross-field validation — when `placement`'s resolved `is_child_facing` is `true`, `destination_url` must match the internal-domain pattern (`noorheroes://` or `noorheroes.com`), else any well-formed URL is accepted.
- **Validation:** the `destination_url` field's validity is recomputed live whenever `placement` changes, showing an inline error immediately if an already-entered external URL becomes invalid after switching to a child-facing placement.
- **Authentication/Authorization:** `content_editor`+.
- **Loading/Empty/Error States:** standard.
- **Pagination/Filtering/Sorting:** by placement/status.
- **Responsive/Accessibility/RTL:** standard.
- **Analytics:** `banner_created`.
- **Performance:** standard.
- **Testing:** signature UI test confirming external URL flagged invalid for child-facing placement selection and permitted for parent-facing selection (PRD §7 item 5).

## 13. API Contract
Reuses B-09's contract verbatim (see `Backend/09-banner-management-api.md` §13).

## 14. Database Requirements
N/A.

## 15. Validation
Cross-field Zod `.refine()`: `is_child_facing(placement) === true` → `destination_url` must match `/^(noorheroes:\/\/|https:\/\/(www\.)?noorheroes\.com)/`; otherwise any valid URL.

## 16. Authentication
Inherits E.28 session.

## 17. Authorization
`content_editor`+.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| External URL entered for a child-facing placement | Inline validation error immediately, before submit |
| Server `422 EXTERNAL_LINK_NOT_ALLOWED_CHILD_FACING` (defensive fallback) | Same inline error surfaced from server response |
| Image fails upload-safety pipeline | Upload area shows E.29 rejection reason |
| `starts_at >= ends_at` | Inline date-range error |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Banner alt-text/copy via localization-key editor.

## 22. RTL
Full RTL support; banner imagery preview mirrors layout direction where the design calls for it.

## 23. Analytics
`banner_created`.

## 24. Performance
Standard; imagery preview lazy-loaded.

## 25. Security
The conditional `destination_url` validation exactly mirroring `is_child_facing` is treated as this sub-feature's primary child-safety UI contribution — the signature test proves both directions (blocked for child-facing, permitted for parent-facing) so the restriction is never accidentally applied universally (which would incorrectly break legitimate parent-facing external links, e.g., Subscription upsell).

## 26. Library Requirements
React, TypeScript, React Hook Form, Zod, React Query, Jest/RTL.

## 27. Testing
- **UI test (signature, part 1):** select a child-facing placement, enter an external `destination_url`, assert inline validation error appears and submit is blocked.
- **UI test (signature, part 2):** select a parent-facing placement, enter the same external `destination_url`, assert no validation error and submit succeeds.
- **Integration:** full banner-create flow for both placement types.

## 28. Documentation
Document the exact regex/pattern used for internal-domain matching in both this UI and cross-reference B-09's backend implementation, flagging that the two must stay in sync.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Types & API Client**
- Task ID: N-09-T01
- Files to Create: `types/admin/banner.ts`, `repositories/admin/BannerAdminRepository.ts`.
- Dependencies: B-09.
- Definition of Done: typed repository unit-tested.

**Task 02 — Banner List Screen**
- Task ID: N-09-T02
- Files to Create: `app/(admin)/engagement/banners/page.tsx`, `components/engagement/banners/BannerListTable.tsx`.
- Dependencies: Task 01.
- Definition of Done: list renders with all states.

**Task 03 — Banner Editor with Conditional URL Validation (Signature Task)**
- Task ID: N-09-T03
- Files to Create: `app/(admin)/engagement/banners/[id]/page.tsx`, `components/engagement/banners/BannerEditorForm.tsx`, `components/engagement/banners/PlacementScheduler.tsx`.
- Implementation Details: Zod `.refine()` cross-field validation as described in §15; imagery upload via shared `ContentUploadRepository`.
- Dependencies: Task 01.
- Definition of Done: both signature UI tests (blocked/permitted) pass — CI-blocking per PRD §7 item 5.

**Task 04 — Permission Gating & Accessibility**
- Task ID: N-09-T04
- Dependencies: Task 03.
- Definition of Done: accessibility audit passes.

**Task 05 — Tests & Documentation**
- Task ID: N-09-T05
- Dependencies: Tasks 01–04.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Banner List/Editor screens functional against B-09; conditional `destination_url` validation proven correct in both directions (blocked for child-facing, permitted for parent-facing).

## 31. Final Verification Checklist
- [ ] External URL rejected client-side for child-facing placement selection
- [ ] External URL permitted client-side for parent-facing placement selection
- [ ] Placement change re-validates an already-entered `destination_url` live
- [ ] Imagery upload uses shared `ContentUploadRepository`, surfaces E.29 rejection reasons
- [ ] `starts_at < ends_at` validated
- [ ] `content_editor`+ gating enforced
- [ ] Loading/empty/error states implemented
- [ ] Responsive, accessible, RTL-supported
- [ ] Analytics events fire correctly
- [ ] No school/madrasa/institutional-tier logic introduced
