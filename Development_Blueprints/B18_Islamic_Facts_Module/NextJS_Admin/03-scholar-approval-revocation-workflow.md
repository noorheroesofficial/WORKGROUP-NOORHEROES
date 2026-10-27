# N-03 — Scholar Approval & Revocation Workflow

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). Extends the existing scholar-review queue (already built for A.3/A.5/A.6) to cover `fact_version` rows.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
3.3 Scholar Approval & Revocation Workflow (ID: N-03)

## 4. Objective
Reuse the existing scholar-review queue component, extended to list pending `fact_version` rows, with approve/reject actions and a "Revoke" action for already-published versions requiring a reason field — all restricted to `scholar_reviewer` role.

## 5. Business Requirements
- §8: Scholar Approval Workflow — approve/reject/revoke behind `scholar_reviewer` role, revocation supported for already-published versions.
- §9 item 3: reuse the existing scholar-review queue component from A.3/A.5/A.6's admin modules.
- Edge Case 8: reject an approval attempt lacking an actual scholar-review record — enforced server-side (B-06), this UI must always route through the proper review-record-creating flow, never a bypass shortcut.

## 6. Existing Architecture
Reuses A.3/A.5/A.6's existing scholar-review queue component, extended (not rebuilt) to handle `fact_version` as an additional reviewable content type.

## 7. Existing Code to Reuse
- A.3/A.5/A.6's existing review-queue list/detail components, approve/reject action handlers.
- Existing role-context RBAC pattern for `scholar_reviewer`.

## 8. Files to Create
- `components/islamic-facts/FactApprovalRevokeAction.tsx` — the Revoke action, since existing A.3/A.5/A.6 queues may not have needed a post-publish revocation action before (confirm before assuming it already exists generically).

## 9. Files to Modify
- Existing scholar-review queue component — register `fact_version` as a reviewable content type, using its existing generic list/detail rendering rather than a parallel facts-specific queue UI.
- `lib/api/islamicFacts.ts` (N-01) — add `approveFactVersion()`, `rejectFactVersion()`, `revokeFactVersion()`.

## 10. Backend Requirements
Consumes B-06's `POST /v1/admin/facts/versions/{version_id}/approve|reject|revoke`. No backend code produced here.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Page/Route:** pending `fact_version` rows appear in the existing shared review queue route, using its existing list rendering (fact text/explanation/sources shown in its detail panel, adapted to this content type's fields).
- **Component:** approve/reject actions use the existing queue's standard action buttons/flow; `FactApprovalRevokeAction` (new) requires a reason text field, confirmation dialog, restricted to `scholar_reviewer` role.
- **Authorization/Permissions:** `scholar_reviewer` role required; a `content_editor` who authored the fact must not see approve/reject/revoke actions for their own submission (standard separation-of-duties UI treatment, mirroring A.3/A.5/A.6's existing pattern).
- **Loading/Empty State:** inherited from the existing shared queue component ("No facts pending review" empty state).
- **Error State:** approve-without-valid-review-context surfaces the `422` inline (Edge Case 8); revoke-without-reason blocked client-side with server-side `422` backstop.
- **Pagination/Filtering:** inherited from the existing shared review-queue component (filter by content type = fact, if the queue supports multi-type filtering).
- **Accessibility:** inherited from existing queue component; new Revoke action's confirmation dialog and reason field follow the same accessibility standard as the rest of the queue.

## 13. API Contract
**Required API:** `POST /v1/admin/facts/versions/{version_id}/approve`, `.../reject`, `.../revoke` (B-06).
**Authentication:** Bearer, admin.
**Authorization:** `scholar_reviewer` role.
**Request (revoke):** `{ "reason": "..." }` (required, non-empty).
**Error Responses:** `403` (wrong role), `422` (missing reason on revoke, or no valid review-record context on approve — Edge Case 8).

## 14. Database Requirements
N/A directly — consumes B-06's API (backed by B-01's `scholar_approval` table).

## 15. Validation
Revoke reason field required, minimum length enforced client-side (mirroring whatever minimum B-06 enforces server-side, if any — confirm exact rule).

## 16. Authentication
Standard Admin Portal auth.

## 17. Authorization
`scholar_reviewer` role required; separation of duties enforced (author cannot approve own submission).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Approve without valid review context | `422` from B-06 surfaced as an inline error (Edge Case 8) |
| Revoke without reason | Client-side validation blocks submit; server-side `422` as backstop |
| Wrong role | Actions not rendered; `403` backstop if somehow triggered |

## 19. Offline First
N/A — online-only admin surface.

## 20. Local Data
N/A.

## 21. Localization
Fact text/explanation shown in the review detail panel renders correctly for English, Hindi, Arabic, and Urdu content within the admin queue UI.

## 22. RTL
Fact text/explanation shown in the review detail panel renders correctly RTL for Arabic/Urdu content within the (LTR) admin queue UI.

## 23. Analytics
N/A — audit logging of approve/reject/revoke is B-06's server-side responsibility, with revocation flagged high-sensitivity.

## 24. Performance
Negligible — reuses existing queue's pagination/loading performance characteristics.

## 25. Security
Revoke action is a genuinely new capability (existing A.3/A.5/A.6 queues may only have supported pre-publish approve/reject) — confirm this is additive to the shared component, not a facts-specific fork, so other content types benefit from the same revocation capability if/when needed.

## 26. Library Requirements
Existing shared review-queue component library — no new libraries.

## 27. Testing
- Unit: revoke reason required, submit blocked without it.
- Unit: approve/reject actions correctly hidden for non-`scholar_reviewer` roles.
- Integration: `fact_version` rows correctly appear in and are actionable from the shared queue.
- Integration: Edge Case 8 — approve attempt without valid review context surfaces the `422` error correctly.

## 28. Documentation
Document the extension point used to register `fact_version` as a reviewable content type, for future content types to follow the same pattern.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Shared Queue Component Extensibility**
Objective: Verify the existing A.3/A.5/A.6 review-queue component can be extended with a new content type without a parallel build.
Why Required: Rule 30 — do not assume, confirm actual extensibility before building.
Dependencies: None (research task).
Definition of Done: Confirmed extension point (e.g., a content-type adapter interface) identified.

**Task 02 — Register `fact_version` as Reviewable Content Type**
Objective: Wire fact_version data into the existing queue's list/detail rendering.
Files to Modify: existing shared queue component.
Dependencies: Task 01.
Definition of Done: Pending fact versions appear correctly in the queue.

**Task 03 — API Client Extension**
Objective: `approveFactVersion()`, `rejectFactVersion()`, `revokeFactVersion()`.
Dependencies: B-06 deployed or contract-mocked, N-01's API client file existing.
Definition of Done: Typed client functions available.

**Task 04 — Revoke Action Component**
Objective: `FactApprovalRevokeAction.tsx` with reason field and confirmation.
Dependencies: Task 03.
Definition of Done: Revoke flow functioning correctly, restricted to `scholar_reviewer`.

**Task 05 — Assess Generalizing Revoke to the Shared Queue**
Objective: If the existing queue lacks a revoke capability for other content types, assess whether to build it as a shared queue feature vs. facts-specific.
Dependencies: Task 04.
Definition of Done: Decision documented; if generalized, other content types (A.3/A.5/A.6) gain the capability as a side benefit, noted for future work, not scope creep for this blueprint.

**Task 06 — Tests**
Dependencies: Tasks 01–05.
Definition of Done: All green.

## 30. Definition of Done
- `fact_version` fully integrated into the existing shared review queue, no parallel queue UI built.
- Revoke action functioning with required reason field, restricted correctly.
- Edge Case 8 correctly surfaced in the UI.

## 31. Final Verification Checklist
- [ ] `fact_version` appears in and is actionable from the existing shared queue, not a new parallel UI
- [ ] Revoke requires a reason, restricted to `scholar_reviewer`
- [ ] Approve-without-valid-review-record correctly rejected and surfaced (Edge Case 8)
- [ ] Separation of duties: a `content_editor` cannot approve their own submission
- [ ] Accessibility inherited correctly from the shared component
