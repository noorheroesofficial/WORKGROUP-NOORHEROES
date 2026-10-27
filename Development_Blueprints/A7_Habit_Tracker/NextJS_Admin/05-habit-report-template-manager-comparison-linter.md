# N-05 — Habit Report Template Manager & Comparison Linter

## 1. Feature Context
NoorHeroes Admin Portal. Template editor for Weekly Habit Report content blocks with a real-time linter blocking sibling-comparison patterns, backing B-13.

## 2. Parent Feature
A.7 Habit Tracker — NextJS Admin

## 3. Sub-feature
N-05 Habit Report Template Manager & Comparison Linter

## 4. Objective
Build a template editor for Weekly Habit Report content blocks with a client-side pre-check mirroring B-13's server-side comparison linter, restricted to `product_admin` (update-only).

## 5. Business Requirements
- Update-only, `product_admin` restricted.
- Linter (client pre-check + authoritative server gate) flags variable patterns like `{child_a_score}`/`{child_b_score}` and sibling-ranking loop constructs.
- Block save with a clear explanation referencing the no-sibling-comparison policy when a violation is detected.

## 6. Existing Architecture
`src/app/(dashboard)/habits/report-templates/page.tsx`, `src/features/habit-report-templates/{api,hooks,components}`.

## 7. Existing Code to Reuse
`useAdminSession`, `RequirePermission`; existing rich-text/template-editor component if the Admin Portal already has one for other content types (reuse rather than build a new editor from scratch).

## 8. Files to Create
- `src/app/(dashboard)/habits/report-templates/page.tsx`
- `src/features/habit-report-templates/api/report-templates-repository.ts`
- `src/features/habit-report-templates/hooks/use-report-template.ts`
- `src/features/habit-report-templates/hooks/use-update-report-template.ts`
- `src/features/habit-report-templates/components/TemplateEditor.tsx`
- `src/features/habit-report-templates/components/LintViolationPanel.tsx`
- `src/features/habit-report-templates/lib/client-comparison-linter.ts` (lightweight client-side pre-check mirroring B-13's server linter)

## 9. Files to Modify
- Admin Portal sidebar/navigation config — add "Report Templates" entry, `product_admin`-only visibility

## 10. Backend Requirements
Consumes B-13 (`/v1/admin/habits/report-templates`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Template content-block editor for Weekly Habit Report copy.
- Real-time client-side lint feedback as the admin types (responsiveness aid), using `client-comparison-linter.ts` — but the save action always calls the server, which is the authoritative, non-bypassable gate (B-13).
- On server-side rejection (422), display the specific violation(s) and policy-reference explanation returned by the API.
- `RequirePermission` strictly `product_admin`-scoped.

## 13. API Contract
`GET/PATCH /v1/admin/habits/report-templates` (B-13) — Admin API, `product_admin` scope, linter as a hard server-side gate.

## 14. Database Requirements
N/A (frontend only).

## 15. Validation
Client-side linter pre-check is advisory/responsive only; the server-side linter (B-13) is authoritative and must always be called on save — client-side pass must never be treated as sufficient to skip the server call.

## 16. Authentication
`useAdminSession`.

## 17. Authorization
`RequirePermission` strictly `product_admin`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Server linter rejects save (422) | Display violations + policy reference from the API response, block save, do not silently retry |
| Client linter flags a pattern | Inline warning shown live, save button remains enabled (server is authoritative — client warning is advisory) |
| Unauthorized | `RequirePermission` hides the entire page for non-`product_admin` roles |

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
Template content blocks are per-locale; editor should support switching locale context, consistent with N-03's localization-review pattern. Admin Portal chrome itself uses `useTranslation()` (**confirmed**, `NEXT-JS-INSTRUCTIONS.md`).

## 22. RTL
Editor preview must correctly render RTL locale content, using `useLocalization()`'s RTL status (**confirmed** available) to drive the preview's layout direction.

## 23. Analytics
Not applicable (audit-logged admin action per B-13).

## 24. Performance
Client-side linter runs synchronously on keystroke/debounced input without perceptible lag.

## 25. Security
The client-side linter is a UX aid only, never a substitute for B-13's authoritative server-side gate — this must be explicit in the implementation to prevent a future refactor from mistakenly treating client-pass as sufficient.

## 26. Library Requirements
Next.js App Router, React Query, existing Admin Portal shared components, a lightweight regex/pattern-matching utility for the client-side linter mirroring B-13's server logic.

## 27. Testing
Component tests for the editor and violation panel; client-linter unit tests (mirroring B-13's mandatory pattern-detection test cases); integration test for the server-rejection display flow.

## 28. Documentation
Inline help text explaining the linter's authoritative server-side nature and listing the pattern types it checks for, matching B-13's documentation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `habit-report-templates` Feature Module**
- Files to Create: `types.ts`, `api/report-templates-repository.ts`
- Definition of Done: module compiles with typed API client.

**Task 02 — Implement Get/Update Hooks**
- Files to Create: `hooks/use-report-template.ts`, `use-update-report-template.ts`
- Definition of Done: hooks correctly wrap B-13's endpoints, surfacing 422 violation details.

**Task 03 — Implement Client-Side Comparison Linter (Advisory)**
- Files to Create: `lib/client-comparison-linter.ts`
- Implementation Details: mirror B-13's pattern rules for real-time feedback.
- Do Not Change: this linter must never replace or bypass the server-side call.
- Tests: unit tests for pattern detection matching B-13's mandatory test cases.
- Definition of Done: client linter correctly flags the same patterns B-13 blocks.

**Task 04 — Build Template Editor & Violation Panel**
- Files to Create: `TemplateEditor.tsx`, `LintViolationPanel.tsx`
- Tests: component tests, server-rejection display integration test.
- Definition of Done: editor correctly surfaces both client-advisory and server-authoritative linter feedback.

**Task 05 — Wire Page Route with Strict RBAC Guard**
- Files to Create: `page.tsx`
- Files to Modify: sidebar/navigation config.
- Definition of Done: route only accessible to `product_admin`.

**Task 06 — Final Code Review**
- Do Not Change: server-side linter must remain the authoritative, non-bypassable gate.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Report Template Manager live, `product_admin`-restricted, with responsive client-side linting and authoritative server-side enforcement clearly surfaced.

## 31. Final Verification Checklist
- [ ] Client-side linter provides real-time advisory feedback matching B-13's pattern rules
- [ ] Server-side linter remains the authoritative, non-bypassable gate on save
- [ ] 422 violations displayed with policy-reference explanation
- [ ] Page restricted to `product_admin` role only
- [ ] Locale-context switching supported in the editor
- [ ] Tests passing
