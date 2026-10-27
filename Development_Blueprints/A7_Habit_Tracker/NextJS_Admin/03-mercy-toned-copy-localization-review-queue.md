# N-03 — Mercy-Toned Copy Localization Review Queue

## 1. Feature Context
NoorHeroes Admin Portal. Localization review workflow UI backing B-11, ensuring mercy-toned copy is culturally reviewed — not just translated — before publish.

## 2. Parent Feature
A.7 Habit Tracker — NextJS Admin

## 3. Sub-feature
N-03 Mercy-Toned Copy Localization Review Queue

## 4. Objective
Build a review queue listing pending copy strings per locale, requiring `localization_reviewer` sign-off before `status='published'`, with a "flag for re-review" action.

## 5. Business Requirements
- Dual-role gate: `content_editor` for draft management, `localization_reviewer` for publish sign-off.
- Reviewer confirms cultural appropriateness, not just translation accuracy — the UI should present both the source and translated text side by side with context (which screen/scenario the copy appears in).
- Already-published strings can be flagged for re-review at any time.

## 6. Existing Architecture
`src/app/(dashboard)/habits/mercy-copy-review/page.tsx`, `src/features/mercy-copy-review/{api,hooks,components}`.

## 7. Existing Code to Reuse
`DataTable`, `usePaginationState`, `RequirePermission`, `useAdminSession`; existing localization-review UI patterns if the Admin Portal already has a general content-review queue elsewhere (reuse layout conventions).

## 8. Files to Create
- `src/app/(dashboard)/habits/mercy-copy-review/page.tsx`
- `src/features/mercy-copy-review/api/mercy-copy-review-repository.ts`
- `src/features/mercy-copy-review/hooks/use-mercy-copy-review-queue.ts`
- `src/features/mercy-copy-review/hooks/use-publish-mercy-copy.ts`
- `src/features/mercy-copy-review/hooks/use-flag-for-rereview.ts`
- `src/features/mercy-copy-review/components/MercyCopyReviewTable.tsx`
- `src/features/mercy-copy-review/components/CopyReviewDetailPanel.tsx` (side-by-side source/translation view)

## 9. Files to Modify
- Admin Portal sidebar/navigation config — add "Mercy Copy Review" entry

## 10. Backend Requirements
Consumes B-11 (`/v1/admin/habits/mercy-copy-review`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Table of pending copy strings, filterable by locale and status (`pending`/`published`/`flagged`).
- Detail panel showing source text, translated text, and the screen/scenario context where the copy appears (streak-broken message, mercy suggestion, recovery framing, etc.).
- Publish action gated behind `localization_reviewer` permission — visibly disabled (not hidden) for `content_editor`-only users, with an explanatory tooltip, to make the sign-off requirement clear rather than confusing.
- "Flag for re-review" action available on published items.
- Loading, empty, error states.

## 13. API Contract
`GET/POST/PATCH /v1/admin/habits/mercy-copy-review` (B-11) — Admin API, dual-role gate.

## 14. Database Requirements
N/A (frontend only).

## 15. Validation
Publish button disabled client-side for non-`localization_reviewer` sessions; server (B-11) remains authoritative and independently rejects unauthorized publish attempts.

## 16. Authentication
`useAdminSession`.

## 17. Authorization
`RequirePermission` for `content_editor` (draft CRUD) and separately for `localization_reviewer` (publish action) — both checked independently per action, not a single combined gate.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Publish attempted without reviewer permission | Button disabled client-side with explanatory tooltip; if somehow reached, 403 surfaced as a toast |
| Re-review flag on non-published content | Action unavailable/disabled for non-published rows |
| Network/API failure | Standard error state with retry |

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
This page itself manages localization content; the Admin Portal UI chrome (buttons, labels) uses `useTranslation()`/`useLocalization()` (**confirmed** per `NEXT-JS-INSTRUCTIONS.md`), independent of whichever locale's copy is being reviewed in the detail panel.

## 22. RTL
Detail panel must correctly render Arabic/Urdu copy for reviewer assessment (mixed-direction layout: LTR admin chrome, RTL content preview where applicable).

## 23. Analytics
Not applicable (audit-logged admin workflow per B-11).

## 24. Performance
Standard paginated queue performance via `DataTable`.

## 25. Security
Dual independent permission checks are the primary control; server-side (B-11) is authoritative.

## 26. Library Requirements
Next.js App Router, React Query, existing Admin Portal shared components.

## 27. Testing
Component tests for the review table and detail panel; hook tests for publish/flag mutations; RBAC-guard tests for both `content_editor`-only and `localization_reviewer` sessions.

## 28. Documentation
Inline help text explaining the "cultural appropriateness, not just translation accuracy" review standard, referencing PRD §8.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `mercy-copy-review` Feature Module**
- Files to Create: `types.ts`, `api/mercy-copy-review-repository.ts`
- Definition of Done: module compiles with typed API client.

**Task 02 — Implement Queue/Publish/Flag Hooks**
- Files to Create: `hooks/use-mercy-copy-review-queue.ts`, `use-publish-mercy-copy.ts`, `use-flag-for-rereview.ts`
- Definition of Done: hooks correctly wrap B-11's endpoints.

**Task 03 — Build Review Table & Detail Panel**
- Files to Create: `MercyCopyReviewTable.tsx`, `CopyReviewDetailPanel.tsx`
- Implementation Details: side-by-side source/translation view with screen-context labeling.
- Tests: component render tests.
- Definition of Done: reviewer can assess cultural appropriateness with full context visible.

**Task 04 — Implement Dual-Permission Gating**
- Implementation Details: independent `RequirePermission`/`hasPermission` checks for draft-edit vs. publish actions.
- Tests: RBAC rendering tests for both role combinations.
- Definition of Done: publish action correctly gated and clearly explained when unavailable.

**Task 05 — Wire Page Route**
- Files to Create: `page.tsx`
- Files to Modify: sidebar/navigation config.
- Definition of Done: route live and reachable.

**Task 06 — Final Code Review**
- Expected Result: PR merge-ready.

## 30. Definition of Done
Mercy-copy review queue live, dual-role-gated, providing reviewers full context for cultural-appropriateness sign-off.

## 31. Final Verification Checklist
- [ ] Queue filterable by locale and status
- [ ] Detail panel shows source, translation, and usage context together
- [ ] Publish action gated to `localization_reviewer` specifically, with clear disabled-state explanation
- [ ] Flag-for-re-review available on published items
- [ ] Loading/empty/error states implemented
- [ ] Tests passing
