# N-05 — Child-Safety Review Queue & Detail

## 1. Feature Context
The distinct, final human gate before anything can be scheduled/published — separate from Scholar Review, focused specifically on age/safety fit, reusing most of N-04's structure but scoped to a different role and a narrower decision set.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
2.5 Child-Safety Review Queue & Detail (ID: **N-05**)

## 4. Objective
Build the Child-Safety Review Queue and Detail screens against B-04, scoped to `child_safety_reviewer` role and `review_stage='child_safety'` items, with Pass / Request Changes decision actions.

## 5. Business Requirements
- FR-9: Child-Safety Review is a distinct, separate final gate — scholar approval alone is never sufficient to publish.
- §1.18 screens 23–24: Child-Safety Review Queue, Child-Safety Review Detail.

## 6. Existing Architecture
`src/features/child-safety-review/` module, structurally parallel to N-04 but role- and decision-set-scoped differently; shares the diff/source-viewer components where genuinely reusable (component-level reuse from N-04, not a full duplication).

## 7. Existing Code to Reuse
- `src/features/scholar-review/components/source-viewer.tsx`, `version-diff-panel.tsx` (N-04, reused as-is)
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/hooks/use-pagination-state.ts::usePaginationState`

## 8. Files to Create
- `src/app/(dashboard)/review/child-safety-queue/page.tsx`
- `src/app/(dashboard)/review/child-safety-queue/[id]/page.tsx`
- `src/features/child-safety-review/api/child-safety-review-repository.ts`
- `src/features/child-safety-review/hooks/use-child-safety-queue.ts`, `use-child-safety-detail.ts`, `use-submit-child-safety-decision.ts`
- `src/features/child-safety-review/components/child-safety-decision-bar.tsx` — Pass / Request Changes only (no Reject/Escalate, per the narrower decision set implied by this being a focused age/safety pass rather than the full scholar-review decision set)
- `src/features/child-safety-review/types/child-safety-review.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `CHILD_SAFETY_REVIEW.*` endpoints (reusing B-04's underlying `/v1/admin/reviews` path, role-scoped server-side)
- `src/shared/components/dashboard-shell.tsx` — nav item under "Review" group, gated by `child_safety_reviewer`

## 10. NextJS Requirements
- Queue and Detail structurally mirror N-04 but call the same B-04 endpoints with the requesting admin's `child_safety_reviewer` role naturally scoping results server-side (no separate backend sub-feature needed — confirmed against B-04's role-scoped query).
- `ChildSafetyDecisionBar`: focused Pass/Request-Changes action set — if PRD intent is actually the same four-way decision set as Scholar Review, reuse `DecisionActionBar` from N-04 directly rather than building a narrower variant (confirm against §2.3's click-mapping table, which lists only a generic "Pass/Request Changes confirmation" for this screen — default to the narrower two-action set unless further specification indicates otherwise).
- Same SoD-hint derivation pattern as N-04 (child-safety reviewers are also subject to the same segregation-of-duties guarantee).

## 11. Required API
**Admin API** — B-04: `GET /v1/admin/reviews` (role-scoped to `child_safety_reviewer`), `GET /v1/admin/reviews/{id}`, `PATCH /v1/admin/reviews/{id}`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="child_safety_reviewer"`.

## 13. Loading / Empty / Error States
Mirrors N-04's states, scoped to this queue.

## 14. Responsive UI / Accessibility
Mirrors N-04's accessibility requirements.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
Same SoD-hint pattern as N-04, reused rather than reimplemented — component-level reuse ensures no divergent, weaker implementation is accidentally introduced for this second reviewer role.

## 17. Testing
Unit: role-scoping confirmation (this queue only ever shows `review_stage='child_safety'` items). UI: SoD-hint test mirroring N-04's mandatory test, applied to this role. Integration: full pass → item becomes publish-eligible (both approvals present) flow, verified against B-06's publish-eligibility check.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `child-safety-review.ts` schema (likely near-identical shape to N-04's `review.ts` — confirm and reuse the type where possible rather than duplicating). Files: `types/child-safety-review.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `ChildSafetyReviewRepositoryImpl`**
Objective: Repository reusing B-04's endpoints. Tests: mocked-fetch tests confirming role-scoped queue results. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Reuse N-04's `SourceViewer`/`VersionDiffPanel` Components**
Objective: Confirm direct reuse, no duplication. Dependencies: N-04. Definition of Done: zero duplicated diff/source-viewer code.

**Task 04 — Implement `ChildSafetyDecisionBar` (Reusing N-04's SoD-Hint Logic)**
Objective: Pass/Request-Changes actions with the same server-sourced SoD-hint derivation as N-04. Dependencies: N-04's pattern. Tests: SoD-hint test for this role. Definition of Done: test passes.

**Task 05 — Implement the Queue and Detail Pages**
Objective: Compose reused + role-specific components with loading/empty/error states. Dependencies: Tasks 02–04. Tests: full-page smoke tests. Definition of Done: tests pass.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm maximal component reuse from N-04, confirm this queue is genuinely a distinct, separate gate from Scholar Review in the UI (not merely a re-skinned duplicate that could confuse reviewers about which stage they're acting on). Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Queue strictly shows only `review_stage='child_safety'` items
- [ ] SoD-hint enforcement mirrors N-04's mandatory guarantee for this role
- [ ] Source viewer/diff components reused from N-04, not duplicated
- [ ] Pass action correctly makes the item publish-eligible when combined with existing Scholar approval
- [ ] `child_safety_reviewer` RBAC enforced via `RequirePermission`

## 20. Definition of Done
Child-Safety Reviewers have a distinct, correctly-scoped final review gate that maximally reuses N-04's proven diff/source-viewer/SoD-hint components — completing the two-stage human review requirement B-06's publish-eligibility check enforces.
