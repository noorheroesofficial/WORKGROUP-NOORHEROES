# N-03 — XP Rule Management UI

> **Reconciliation note (2026-08-18):** supersedes `A11_Rewards_System/NextJS_Admin/01-reward-rule-table-editor.md` (now deprecated).

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the Admin Portal screens for the versioned XP rule table, consuming **B-03 XP Rule Management API**. Split from the Reward Ledger surface (see **N-04 Reward Ledger & Manual Grant UI**) per PRD §1.18's distinct screen grouping (Screens #7–8 vs. #9–10). Source: PRD §1.18 Screens 7–8, §6, §7 item 1.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
3.3 XP Rule Management UI (Admin ID: **N-03**)

## 4. Objective
Give content admins a clear, non-retroactivity-communicating XP Rule Editor — the same helper-text convention used by the Habit Template Editor (N-01) and Badge Criteria Builder (N-05) — so admins never mistake a versioned update for an in-place edit of history.

## 5. Business Requirements
- Screen Inventory (PRD §1.18): #7 XP Rule Table, #8 XP Rule Editor (versioned).
- Frontend AI Code-Gen Prompt item 1 (PRD §7): XP Rule Editor displays "Changes apply only going forward; past awards are never affected" helper text.

## 6. Existing Architecture
React + TypeScript, Admin Portal shell from E.28.

## 7. Existing Code to Reuse
E.28 shell/design tokens; E.29's list→editor data-table pattern.

## 8. Files to Create
- `app/(admin)/engagement/rewards/xp-rules/page.tsx`
- `app/(admin)/engagement/rewards/xp-rules/[id]/page.tsx`
- `app/(admin)/engagement/rewards/xp-rules/[id]/history/page.tsx`
- `components/engagement/rewards/XPRuleTable.tsx`
- `components/engagement/rewards/XPRuleEditorForm.tsx`
- `components/engagement/rewards/XPRuleVersionHistory.tsx`
- `repositories/admin/XPRuleAdminRepository.ts`
- `types/admin/xpRule.ts`
- `__tests__/engagement/rewards/XPRuleEditorForm.test.tsx`

## 9. Files to Modify
- `components/shell/EngagementNavGroup.tsx`
- `lib/analytics/EngagementAdminAnalytics.ts`

## 10. Backend Requirements
Consumes **B-03** endpoints: `GET/POST /v1/admin/xp-rules`, `PATCH /v1/admin/xp-rules/{id}`, `GET /v1/admin/xp-rules/{id}/history`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Page:** XP Rule Table, XP Rule Editor, Version History.
- **Route:** `/engagement/rewards/xp-rules`, `/engagement/rewards/xp-rules/[id]`, `/engagement/rewards/xp-rules/[id]/history`.
- **Component:** `XPRuleTable`, `XPRuleEditorForm` (with mandatory non-retroactivity helper text), `XPRuleVersionHistory` (read-only version timeline).
- **API Client:** `XPRuleAdminRepository`.
- **Type Definition:** `RewardRuleVersion`, `XPRuleCreateInput`, `XPRuleUpdateInput`.
- **Form:** React Hook Form + Zod; `activity_type` dropdown-constrained from the registry; `xp_value` positive integer.
- **Validation:** client mirrors backend's `activity_type` registry and `xp_value` bounds.
- **Authentication/Authorization:** `content_editor`+.
- **Loading/Empty/Error States:** standard.
- **Pagination/Filtering/Sorting:** rule list filterable by `activity_type`; version history paginated.
- **Responsive/Accessibility/RTL:** standard.
- **Analytics:** `xp_rule_created`, `xp_rule_updated`.
- **Performance:** standard.
- **Testing:** signature UI test confirming the non-retroactivity helper text is present on the XP-value field (PRD §7 item 1).

## 13. API Contract
Reuses B-03's contract verbatim (see `Backend/03-xp-rule-management-api.md` §13).

## 14. Database Requirements
N/A.

## 15. Validation
`activity_type` dropdown-constrained; `xp_value` positive integer bounds mirrored client-side.

## 16. Authentication
Inherits E.28 session.

## 17. Authorization
`content_editor`+.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| `422 VALIDATION_ERROR` | Inline field errors |
| `409 DUPLICATE_ACTIVITY_TYPE` | Inline error on `activity_type` field |
| `404` unknown rule | Redirect to table with toast |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
`activity_type` display labels localized.

## 22. RTL
Full RTL support.

## 23. Analytics
`xp_rule_created`, `xp_rule_updated`.

## 24. Performance
Standard React Query caching with invalidation on mutation.

## 25. Security
No security-sensitive client logic beyond standard role-gating; non-retroactivity helper text is a UX-safety requirement, not a security boundary (the boundary is B-03's versioning guarantee).

## 26. Library Requirements
React, TypeScript, React Hook Form, Zod, React Query, Jest/RTL.

## 27. Testing
- **UI test (signature):** XP Rule Editor renders "Changes apply only going forward; past awards are never affected" helper text (PRD §7 item 1).
- **Integration:** full create → update → version-history-reflects-new-entry flow.
- **Unit:** form validation.

## 28. Documentation
Document the shared helper-text convention, referencing its reuse across N-01 (Habit), N-03 (this), and N-05 (Badge).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Types & API Client**
- Task ID: N-03-T01
- Files to Create: `types/admin/xpRule.ts`, `repositories/admin/XPRuleAdminRepository.ts`.
- Dependencies: B-03.
- Definition of Done: typed repository unit-tested.

**Task 02 — XP Rule Table & Editor**
- Task ID: N-03-T02
- Files to Create: `app/(admin)/engagement/rewards/xp-rules/page.tsx`, `[id]/page.tsx`, `components/engagement/rewards/XPRuleTable.tsx`, `XPRuleEditorForm.tsx`.
- Implementation Details: mandatory helper text on the XP-value field.
- Dependencies: Task 01.
- Definition of Done: signature helper-text UI test passes.

**Task 03 — Version History View**
- Task ID: N-03-T03
- Files to Create: `app/(admin)/engagement/rewards/xp-rules/[id]/history/page.tsx`, `components/engagement/rewards/XPRuleVersionHistory.tsx`.
- Dependencies: Task 01.
- Definition of Done: history view renders correctly.

**Task 04 — Permission Gating & Accessibility**
- Task ID: N-03-T04
- Dependencies: Task 02.
- Definition of Done: accessibility audit passes.

**Task 05 — Tests & Documentation**
- Task ID: N-03-T05
- Dependencies: Tasks 01–04.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
XP Rule Table/Editor/History screens functional against B-03; non-retroactivity helper text verified present; permission gating enforced.

## 31. Final Verification Checklist
- [ ] XP Rule Editor displays non-retroactivity helper text (signature test green)
- [ ] `activity_type` field is dropdown-constrained
- [ ] Version history view renders full audit trail
- [ ] `content_editor`+ gating enforced
- [ ] Loading/empty/error states implemented
- [ ] Responsive, accessible, RTL-supported
- [ ] Analytics events fire correctly
- [ ] No school/madrasa/institutional-tier logic introduced
