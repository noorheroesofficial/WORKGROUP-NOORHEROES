# N-10 — Coupon Management UI

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the Admin Portal screens for coupon list/editor and the redemption report, consuming **B-10**. Source: PRD §1.18 Screens 26–28, §6.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
3.10 Coupon Management UI (Admin ID: **N-10**)

## 4. Objective
Give content/billing-ops admins a Coupon Editor that enforces mandatory usage-cap and expiry fields client-side (mirroring the backend's non-nullable requirement), and a Redemption Report that correctly and clearly reflects the backend's atomic redemption-cap enforcement results.

## 5. Business Requirements
- Screen Inventory (PRD §1.18): #26 Coupon List, #27 Coupon Editor, #28 Coupon Redemption Report.
- FR-8 screens/CRUD (PRD §1.7): `usage_cap`, `expires_at` mandatory.

## 6. Existing Architecture
React + TypeScript, Admin Portal shell from E.28.

## 7. Existing Code to Reuse
E.28 shell/design tokens; E.29's list→editor data-table pattern.

## 8. Files to Create
- `app/(admin)/engagement/coupons/page.tsx`
- `app/(admin)/engagement/coupons/[id]/page.tsx`
- `app/(admin)/engagement/coupons/[id]/redemption-report/page.tsx`
- `components/engagement/coupons/CouponListTable.tsx`
- `components/engagement/coupons/CouponEditorForm.tsx`
- `components/engagement/coupons/RedemptionReportView.tsx`
- `repositories/admin/CouponAdminRepository.ts`
- `types/admin/coupon.ts`
- `__tests__/engagement/coupons/CouponEditorForm.test.tsx`

## 9. Files to Modify
- `components/shell/EngagementNavGroup.tsx`
- `lib/analytics/EngagementAdminAnalytics.ts`

## 10. Backend Requirements
Consumes **B-10** endpoints: `POST/GET/PATCH /v1/admin/coupons`, `POST /v1/admin/coupons/{id}/deactivate`, `GET /v1/admin/coupons/{id}/redemption-report`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Page:** Coupon List, Coupon Editor, Redemption Report.
- **Route:** `/engagement/coupons`, `/engagement/coupons/[id]`, `/engagement/coupons/[id]/redemption-report`.
- **Component:** `CouponListTable`, `CouponEditorForm` (`code`, `discount_type`/`discount_value` with bounds pre-check, `usage_cap` **required, non-nullable field in the form schema**, `expires_at` **required, non-nullable, must be future date**), `RedemptionReportView`.
- **API Client:** `CouponAdminRepository`.
- **Type Definition:** `Coupon`, `CouponCreateInput` (`usage_cap: number` and `expires_at: string` are non-optional in the TypeScript type — no `?` modifier, mirroring the backend's mandatory-field guarantee).
- **Form:** React Hook Form + Zod; `usage_cap` and `expires_at` have no default and no "skip" affordance — the form cannot be submitted without them.
- **Validation:** `discount_value` bounds pre-checked client-side per `discount_type` (percent 1–100, fixed-amount positive); `expires_at` must be a future date.
- **Authentication/Authorization:** `content_editor`+/`billing_ops`.
- **Loading/Empty/Error States:** standard.
- **Pagination/Filtering/Sorting:** by active/expired status.
- **Responsive/Accessibility/RTL:** standard.
- **Analytics:** `coupon_created`, `coupon_redemption_cap_reached` (observed via redemption report refresh).
- **Performance:** redemption report polled at a reasonable interval only while viewing an active coupon nearing its cap.
- **Testing:** integration test — redemption report correctly reflects a concurrent-redemption-cap test scenario's outcome (PRD §6.10).

## 13. API Contract
Reuses B-10's contract verbatim (see `Backend/10-coupon-management-api.md` §13).

## 14. Database Requirements
N/A.

## 15. Validation
`usage_cap`/`expires_at` mandatory, non-nullable in both the Zod schema and TypeScript type; `discount_value` bounds checked client-side per `discount_type`.

## 16. Authentication
Inherits E.28 session.

## 17. Authorization
`content_editor`+/`billing_ops`.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Attempt to submit without `usage_cap`/`expires_at` | Blocked client-side; fields marked required with clear messaging |
| Server `409 DUPLICATE_CODE` | Inline error on `code` field |
| Server `422 VALIDATION_ERROR` (bounds) | Inline error on `discount_value` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Coupon-related UI copy localized; `code` itself not localized.

## 22. RTL
Full RTL support.

## 23. Analytics
`coupon_created`.

## 24. Performance
Redemption report data cached with a short stale-time; avoids re-fetching on every render.

## 25. Security
Client-side mandatory-field enforcement for `usage_cap`/`expires_at` is a UX convenience — B-10's DB-level `CHECK` constraints remain the authoritative guarantee; the Redemption Report must never imply real-time redemption counting is client-computed (it always reflects the server's atomic counter, fetched fresh).

## 26. Library Requirements
React, TypeScript, React Hook Form, Zod, React Query, Jest/RTL.

## 27. Testing
- **UI test:** `CouponEditorForm` blocks submission without `usage_cap`/`expires_at`.
- **Integration:** redemption report correctly displays a concurrency-test outcome (e.g., seed a coupon with `usage_cap=5`, simulate 10 redemptions via B-10's API directly, then load the Redemption Report UI and confirm it shows `redeemed_count: 5`, `usage_cap: 5`).
- **Unit:** discount-bounds validation logic.

## 28. Documentation
Document that the Redemption Report always displays server-computed, never client-estimated, redemption counts.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Types & API Client**
- Task ID: N-10-T01
- Files to Create: `types/admin/coupon.ts`, `repositories/admin/CouponAdminRepository.ts`.
- Implementation Details: `usage_cap`/`expires_at` non-optional in the TypeScript type.
- Dependencies: B-10.
- Definition of Done: typed repository unit-tested.

**Task 02 — Coupon List Screen**
- Task ID: N-10-T02
- Files to Create: `app/(admin)/engagement/coupons/page.tsx`, `components/engagement/coupons/CouponListTable.tsx`.
- Dependencies: Task 01.
- Definition of Done: list renders with all states.

**Task 03 — Coupon Editor with Mandatory-Field Enforcement**
- Task ID: N-10-T03
- Files to Create: `app/(admin)/engagement/coupons/[id]/page.tsx`, `components/engagement/coupons/CouponEditorForm.tsx`.
- Dependencies: Task 01.
- Definition of Done: mandatory-field-blocking UI test passes.

**Task 04 — Redemption Report View**
- Task ID: N-10-T04
- Files to Create: `app/(admin)/engagement/coupons/[id]/redemption-report/page.tsx`, `components/engagement/coupons/RedemptionReportView.tsx`.
- Dependencies: Task 01.
- Definition of Done: integration test confirming correct display of a concurrency-test outcome passes.

**Task 05 — Permission Gating & Accessibility**
- Task ID: N-10-T05
- Dependencies: Tasks 02–04.
- Definition of Done: accessibility audit passes.

**Task 06 — Tests & Documentation**
- Task ID: N-10-T06
- Dependencies: Tasks 01–05.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Coupon List/Editor/Redemption Report screens functional against B-10; mandatory-field enforcement proven client-side; redemption report proven to correctly reflect atomic-cap-enforcement outcomes.

## 31. Final Verification Checklist
- [ ] `usage_cap`/`expires_at` mandatory, submission blocked without them
- [ ] Discount bounds validated client-side per `discount_type`
- [ ] Redemption Report accurately reflects server-computed `redeemed_count`/`usage_cap`
- [ ] Deactivate action functional
- [ ] `content_editor`+/`billing_ops` gating enforced
- [ ] Loading/empty/error states implemented
- [ ] Responsive, accessible, RTL-supported
- [ ] Analytics events fire correctly
- [ ] No school/madrasa/institutional-tier logic introduced
