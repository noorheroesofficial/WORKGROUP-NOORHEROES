# N-03 — Modesty & Appropriateness Review Queue

## 1. Feature Context
NoorHeroes Admin Portal (Next.js). Part of Feature A.12 — Avatar System. Review queue UI for newly-submitted avatar assets (bases and items), enforcing segregation of duties between submitter and approver, backed by B-05.

## 2. Parent Feature
A.12 Avatar System — NextJS Admin

## 3. Sub-feature
N-03 Modesty & Appropriateness Review Queue

## 4. Objective
Build a review-queue page listing `pending_review` avatar bases/items with approve/reject actions, structurally disabling self-approval in the UI as a defense-in-depth layer atop B-05's server-side enforcement — backing FR-12 and PRD §8/§9's segregation-of-duties requirement.

## 5. Business Requirements
- Every newly-submitted avatar item/base asset routes through this review queue before publish — no exemption for "just a cosmetic" (FR-12).
- The approve action is disabled/hidden in the UI when the current admin is the original submitter (segregation of duties) — enforced additionally and authoritatively server-side by B-05, this UI-level disable is a defense-in-depth UX affordance, not the security boundary itself.
- Reject requires reviewer notes, surfaced back to the submitter for re-editing via N-01/N-02's update paths.
- Queue covers both entity types (avatar bases from N-01, avatar items from N-02) in one unified surface, filterable by type.

## 6. Existing Architecture
Follows the existing Admin Portal shell: `src/app/(dashboard)/avatars/review-queue/page.tsx` route, `src/features/avatar-review/{api,hooks,components}` feature module, reusing `DataTable`, `RequirePermission` per N-01/N-02's established pattern. Mirrors A.3 Story Module's Scholar Review Workflow Admin UI pattern (moral-summary review/approval queue) as the direct structural precedent for a segregation-of-duties-enforced review surface.

## 7. Existing Code to Reuse
- `DataTable`, `RequirePermission`, `hasPermission`, `useAdminSession` (per N-01/N-02)
- A.3's Scholar Review Workflow queue component structure (direct precedent for the approve/reject-with-notes pattern)

## 8. Files to Create
- `src/app/(dashboard)/avatars/review-queue/page.tsx`
- `src/features/avatar-review/api/avatar-review-repository.ts`
- `src/features/avatar-review/hooks/use-review-queue.ts`
- `src/features/avatar-review/hooks/use-approve-review-item.ts`
- `src/features/avatar-review/hooks/use-reject-review-item.ts`
- `src/features/avatar-review/components/ReviewQueueTable.tsx`
- `src/features/avatar-review/components/RejectReasonDialog.tsx`
- `src/features/avatar-review/types.ts`

## 9. Files to Modify
- Admin Portal sidebar/navigation config — add "Review Queue" entry under the "Avatar System" section

## 10. Backend Requirements
Consumes B-05 (`GET /v1/admin/avatars/review-queue`, `POST .../approve`, `POST .../reject`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- `ReviewQueueTable` lists pending items across both entity types (base/item), with columns: entity type, name/thumbnail, submitted-by (admin name), submitted-at.
- Approve action button: disabled with a tooltip ("You submitted this — a different reviewer must approve it") when `currentAdmin.admin_id === item.submitted_by_admin_id`, sourced from `useAdminSession`.
- Reject action opens `RejectReasonDialog` requiring non-empty notes before submission.
- On `403 SELF_APPROVAL_FORBIDDEN` from the backend (should be prevented by the UI disable, but handled as defense-in-depth for any race/stale-state case), surface a clear toast explaining the segregation-of-duties rule rather than a generic error.
- Filtering by entity type (base/item); pagination; sorting by submitted-at.
- `RequirePermission permission="avatars:review:write"` guarding approve/reject actions (scoped to `trust_safety`/`content_editor` per B-05).
- Loading, empty ("no items pending review"), and error states per existing Admin Portal conventions.

## 13. API Contract
`GET /v1/admin/avatars/review-queue`, `POST /v1/admin/avatars/review-queue/{entityType}/{entityId}/approve`, `POST .../reject` (B-05) — Admin API, Bearer admin session, `trust_safety`/`content_editor` scope.

## 14. Database Requirements
N/A (frontend consumes backend API only).

## 15. Validation
Reject action requires non-empty `review_notes` (client-side pre-check mirroring B-05's server-side `422` requirement).

## 16. Authentication
`useAdminSession` — admin Bearer session required for the route; `admin_id` from this session drives the self-approval UI-disable comparison.

## 17. Authorization
`RequirePermission` guarding approve/reject actions; the self-approval UI-disable is an **additional** UX-level control layered on top of RBAC, not a replacement for it — B-05 remains the authoritative enforcement point for both.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Current admin is the submitter | Approve button disabled with explanatory tooltip; reject remains available if genuinely warranted by policy (flagged: confirm with product whether self-reject is permitted — this blueprint assumes reject is not restricted by segregation-of-duties since rejection returns the item for re-editing rather than granting trust, but this should be explicitly confirmed rather than silently assumed as final) |
| `403 SELF_APPROVAL_FORBIDDEN` reaches the client despite UI disable (stale session state) | Clear toast explaining the rule, queue view refreshed |
| Reject without notes | Inline validation error, submission blocked client-side |
| Network/API failure | Error state with retry |
| Empty queue | Friendly "no items pending review" empty state |

## 19. Offline First
Not applicable (Admin Portal is online-only by design).

## 20. Local Data
Not applicable.

## 21. Localization
Follow existing Admin Portal localization conventions (verify against existing pages, per N-01's precedent flag).

## 22. RTL
Follow existing Admin Portal RTL support level (verify against existing pages, per N-01's precedent flag).

## 23. Analytics
Not applicable (internal admin tooling); `AdminAuditLog` (B-05) is the operational record of truth for all approve/reject decisions.

## 24. Performance
Standard paginated table performance via `DataTable`; low-traffic admin surface.

## 25. Security
The self-approval UI-disable is this page's headline UX affordance but is explicitly **not** the security boundary — B-05's server-side check (submitter ≠ approver, enforced at the repository layer) is authoritative, per `NEXT-JS-INSTRUCTIONS.md`'s "backend endpoints enforce permissions" principle applied here to the segregation-of-duties rule specifically.

## 26. Library Requirements
Next.js App Router, React Query, existing Admin Portal shared component library.

## 27. Testing
Component tests for `ReviewQueueTable`/`RejectReasonDialog`; hook tests for approve/reject mutations; RBAC-guard rendering tests; **self-approval UI-disable test** (P0: render the queue with `currentAdmin.admin_id` matching an item's `submitted_by_admin_id`, assert the approve button is disabled with the correct tooltip); `403 SELF_APPROVAL_FORBIDDEN` toast-handling test for the stale-state race case.

## 28. Documentation
Update Admin Portal navigation documentation with the "Review Queue" entry; document the flagged reject-vs-segregation-of-duties open question (§18) for product confirmation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `avatar-review` Feature Module**
- Objective: `src/features/avatar-review/{api,hooks,components}` following the N-01/N-02 reference pattern, structurally mirroring A.3's Scholar Review Workflow queue module.
- Files to Create: `types.ts`, `api/avatar-review-repository.ts`
- Definition of Done: module compiles with typed API client methods for both entity types.

**Task 02 — Implement Queue/Approve/Reject Hooks**
- Files to Create: `hooks/use-review-queue.ts`, `use-approve-review-item.ts`, `use-reject-review-item.ts`
- Tests: hook unit tests (mocked API repository), including `403 SELF_APPROVAL_FORBIDDEN` response handling.
- Definition of Done: hooks correctly wrap B-05's endpoints with React Query.

**Task 03 — Build `ReviewQueueTable` with Self-Approval Disable (P0)**
- Files to Create: `components/ReviewQueueTable.tsx`
- Existing Files to Reuse: `DataTable`, `useAdminSession`.
- Implementation Details: approve-button disable logic comparing `currentAdmin.admin_id` to `item.submitted_by_admin_id`.
- Tests (P0): self-approval UI-disable test.
- Definition of Done: P0 test passes; button correctly disabled/enabled across all fixture combinations.

**Task 04 — Build `RejectReasonDialog` Component**
- Files to Create: `components/RejectReasonDialog.tsx`
- Implementation Details: required non-empty notes field.
- Tests: form validation test.
- Definition of Done: dialog correctly blocks empty-notes submission.

**Task 05 — Wire Page Route with RBAC Guard**
- Files to Create: `src/app/(dashboard)/avatars/review-queue/page.tsx`
- Files to Modify: sidebar/navigation config.
- Definition of Done: route live, reachable via navigation, correctly RBAC-guarded.

**Task 06 — Final Code Review**
- Do Not Change: A.3's Scholar Review Workflow module (structural reference only, not modified); B-05's backend segregation-of-duties enforcement (this UI must respect it, not attempt to replace it).
- Expected Result: PR merge-ready, with the reject-vs-segregation-of-duties open question (§18) flagged for product sign-off before final merge.

## 30. Definition of Done
Review Queue page live, RBAC-guarded, correctly disabling self-approval in the UI as a defense-in-depth layer atop B-05's authoritative server-side enforcement, with a working reject-with-notes flow.

## 31. Final Verification Checklist
- [ ] Queue lists pending items across both entity types (base/item)
- [ ] Approve button correctly disabled with tooltip when current admin is the submitter (P0 test passing)
- [ ] `403 SELF_APPROVAL_FORBIDDEN` handled gracefully as a defense-in-depth case, not assumed unreachable
- [ ] Reject requires non-empty notes
- [ ] `RequirePermission` guards approve/reject actions
- [ ] Loading/empty/error states implemented
- [ ] Component and hook tests passing
- [ ] Reject-vs-segregation-of-duties open question flagged for product confirmation, not silently assumed
