# N-02 — Moral Summary Review Queue

## 1. Feature Context
The scholar's safety-net editor: a paginated queue of AI-generated morals flagged for low confidence, each with an approval field that only a `scholar_reviewer` can submit. This page's approve button is disabled — not just server-rejected — for anyone without that exact role, mirroring B-12's API-level enforcement.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
3.2 Moral Summary Review Queue (ID: **N-02**)

## 4. Objective
Build a paginated review-queue page against B-12, reading the confidence threshold from a shared config endpoint (never hardcoded), with a `scholar_reviewer`-gated approval editor per row.

## 5. Business Requirements
- §8: full CRUD gated by scholar-approval requirement before any moral can be marked `human_reviewed=true` and used live.
- §9: queue shows rows where `ai_generated=true` and `ai_confidence_score` below the configured threshold, read from a shared config endpoint, not hardcoded; approve requires `scholar_reviewer` role enforced via RBAC context; approve button disabled entirely (not just server-reject) for unauthorized users.

## 6. Existing Architecture
`src/features/moral-review/` module, following the existing `DataTable`/`RequirePermission` pattern.

## 7. Existing Code to Reuse
- `src/shared/components/data-table.tsx::DataTable`
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/hooks/use-pagination-state.ts::usePaginationState`
- `src/shared/api/base-resource-client.ts::BaseResourceClient`

## 8. Files to Create
- `src/app/(dashboard)/stories/moral-review/page.tsx`
- `src/features/moral-review/api/moral-review-repository.ts` — `MoralReviewRepositoryImpl`
- `src/features/moral-review/hooks/use-moral-review-queue.ts`, `use-confidence-threshold.ts`, `use-approve-moral.ts`
- `src/features/moral-review/components/moral-review-row.tsx` — AI text + confidence score + approval editor
- `src/features/moral-review/types/moral-version.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `MORAL_REVIEW.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item gated by `scholar_reviewer`

## 10. NextJS Requirements
- `useConfidenceThreshold()`: fetches the threshold from `GET /admin/v1/config/moral-confidence-threshold` — no hardcoded numeric threshold anywhere in this module's source; the fetched value is used purely for display context (the actual filtering happens server-side in B-12's query).
- `MoralReviewRow`: shows AI-generated text + confidence score; approval editor (textarea + approve button) rendered but the approve button is `disabled` whenever `hasPermission(admin, "scholar_reviewer")` is false — via the existing `hasPermission()` utility, not a separate ad hoc check.
- Approving calls `POST /admin/v1/moral-summaries/{version_id}/approve`; on success, the row is removed from the queue (optimistic or refetch — coding agent's choice, but must not show a stale approved row still awaiting action).

## 11. Required API
**Admin API** — B-12: `GET /admin/v1/moral-summaries/review-queue`, `GET /admin/v1/config/moral-confidence-threshold`, `POST /admin/v1/moral-summaries/{version_id}/approve`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; page-level `RequirePermission` may allow a broader read-scope (confirm against existing admin conventions), but the approve action specifically requires `scholar_reviewer`, checked via `hasPermission()` and disabling the control — never merely hiding it (hiding it would remove the auditable "this is off-limits" signal the PRD implies).

## 13. Loading / Empty / Error States
Queue-loading skeleton; empty state when zero rows are below threshold ("No morals currently need review"); approval-submission error state distinct from a queue-load error.

## 14. Responsive UI / Accessibility
Row layout collapses to a stacked card on narrow viewports; confidence score conveyed with both a numeric value and a text label ("Low confidence: 0.62"), never color alone.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`; confirm Admin Portal RTL scope before assuming mirroring is in scope for this page.

## 16. Security
- `scholar_reviewer` gating enforced via `hasPermission()` at the component level, in addition to B-12's independent API-level `403` — defense in depth explicitly required by the PRD.
- Confidence threshold is fetched, never hardcoded, so this page always reflects the same live threshold B-06 actually uses server-side.

## 17. Testing
Unit: approve button disabled for non-scholar-reviewer sessions (assert `disabled` attribute, not merely absent styling); threshold fetched from the config endpoint, not hardcoded (grep-style test asserting no numeric literal threshold exists in the approval-filtering logic — filtering itself lives server-side, so this is really a "no client-side re-filtering with a hardcoded number" test). Integration: full approve flow removes the row from the queue.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `moral-version.ts` response schema. Files: `types/moral-version.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `MoralReviewRepositoryImpl`**
Objective: Repository for the three B-12 endpoints. Follow: existing repository conventions. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `useModerationQueue`/`useConfidenceThreshold`/`useApproveMoral` Hooks**
Objective: React Query hooks. Dependencies: Task 02. Tests: covered by Task 06. Definition of Done: hooks wired correctly.

**Task 04 — Implement `MoralReviewRow` with Permission-Gated Approve Button**
Objective: AI text + score display, `hasPermission()`-gated disabled approve button. Dependencies: Task 03. Tests: **mandatory permission test** — disabled attribute assertion for a non-scholar-reviewer mock session. Definition of Done: test passes.

**Task 05 — Implement the Review Queue Page**
Objective: Compose `RequirePermission` + `DataTable`/list + `MoralReviewRow` + pagination + states. Dependencies: Task 04. Tests: empty-state test. Definition of Done: page smoke test passes against a mocked API.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm no hardcoded confidence threshold exists anywhere in the module, confirm the approve button is genuinely disabled (not just styled) for unauthorized roles. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Queue reads and displays rows exactly as returned by B-12 (server-side filtered, no client-side re-filtering)
- [ ] Confidence threshold fetched from the config endpoint, zero hardcoded numeric threshold in this module
- [ ] Approve button is `disabled` (not merely styled/hidden) for any session lacking `scholar_reviewer`
- [ ] Approval flow removes the row from the queue on success
- [ ] Empty state shown correctly when zero rows are below threshold
- [ ] Confidence score conveyed with text, not color alone

## 20. Definition of Done
Scholars can review and approve safe moral-summary replacements through a permission-gated, live-threshold-aware queue that mirrors B-12's guarantees exactly, with defense-in-depth RBAC enforcement.
