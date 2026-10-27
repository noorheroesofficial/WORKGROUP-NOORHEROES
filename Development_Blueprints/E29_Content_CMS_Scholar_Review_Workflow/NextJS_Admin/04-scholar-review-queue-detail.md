# N-04 — Scholar Review Queue & Detail

## 1. Feature Context
The scholar's primary workspace: assigned queue, source viewer, side-by-side version diff, timestamped media comments, and a decision action bar whose Approve button is disabled — with a clear explanation, never silently — the moment the current reviewer's identity matches the version's `last_edited_by`.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
2.4 Scholar Review Queue & Detail (ID: **N-04**)

## 4. Objective
Build the Scholar Review Queue and Detail screens against B-04, deriving the segregation-of-duties UI hint exclusively from the server's `last_edited_by` field, with a document-review-tool-style diff and timestamped comment scrubber.

## 5. Business Requirements
- FR-8: assigned queue, source viewer, side-by-side version diff, timestamped comments for audio/video, regional/jurisprudential notes, Approve/Request Changes/Reject/Escalate actions.
- §7 frontend AI-prompt requirement #3: segregation-of-duties UI hint derived exclusively from server-provided `last_edited_by`, compared against `AdminAuthContext`'s current admin identity — disabled state with explanatory message when they match.
- §2.2: source viewer, side-by-side diff (additions/removals color-coded), media player with timestamped-comment scrubber, decision action bar.

## 6. Existing Architecture
`src/features/scholar-review/` module, following the Admin Portal's dense document-review-tool visual register (E.28 §2.1).

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/hooks/use-pagination-state.ts::usePaginationState`
- A diff-rendering library/component (new, see §20)
- A media waveform/scrubber component library (new, see §20)

## 8. Files to Create
- `src/app/(dashboard)/review/scholar-queue/page.tsx`
- `src/app/(dashboard)/review/scholar-queue/[id]/page.tsx`
- `src/features/scholar-review/api/scholar-review-repository.ts`
- `src/features/scholar-review/hooks/use-scholar-queue.ts`, `use-review-detail.ts`, `use-submit-decision.ts`
- `src/features/scholar-review/components/source-viewer.tsx`
- `src/features/scholar-review/components/version-diff-panel.tsx`
- `src/features/scholar-review/components/timestamped-comment-scrubber.tsx`
- `src/features/scholar-review/components/decision-action-bar.tsx` — Approve/Request Changes/Reject/Escalate, SoD-aware
- `src/features/scholar-review/components/segregation-of-duties-block.tsx`
- `src/features/scholar-review/types/review.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `SCHOLAR_REVIEW.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item under "Review" group, gated by `scholar_reviewer`

## 10. NextJS Requirements
- `DecisionActionBar`: computes `isSelfEdited = reviewDetail.last_edited_by === adminAuthContext.currentAdmin.id` — when true, renders `SegregationOfDutiesBlock` (disabled buttons + explanatory message) instead of active decision buttons; this comparison is the **only** source of the UI hint, never a separate client-side heuristic.
- `VersionDiffPanel`: side-by-side or inline-highlighted diff, additions/removals/changes color-coded, per standard document-diff convention.
- `TimestampedCommentScrubber`: waveform/scrubber with numbered comment pins at specific timestamps, each expandable.
- Queue empty state: "Queue clear."

## 11. Required API
**Admin API** — B-04: `GET /v1/admin/reviews`, `GET /v1/admin/reviews/{id}`, `PATCH /v1/admin/reviews/{id}`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="scholar_reviewer"`.

## 13. Loading / Empty / Error States
Queue loading skeleton, "Queue clear" empty state; detail-load skeleton; decision-submission error state distinct from a SoD-blocked state (the latter is not an error, it's an expected, explained condition).

## 14. Responsive UI / Accessibility
All diff content and comments screen-reader-navigable in linear reading order per PRD §2.2, not solely positional/visual.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`; content itself may be multi-locale but the review tool chrome follows Admin Portal's own localization scope.

## 16. Security
The SoD UI hint is the load-bearing defense-in-depth layer alongside B-03's dual-layer backend enforcement — tested explicitly with a fixture where `last_edited_by` matches the current admin.

## 17. Testing
Unit: `isSelfEdited` derivation logic. UI: **mandatory** — a fixture version where `last_edited_by` matches the current admin renders the Approve/Request-Changes/Reject action bar in a disabled state with an explanatory message instead of active buttons (per PRD frontend AI-prompt requirement #3). Integration: full queue → detail → approve → item-moves-to-child-safety-queue flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `review.ts` schema. Files: `types/review.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `ScholarReviewRepositoryImpl`**
Objective: Repository for B-04's three endpoints. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `SourceViewer` and `VersionDiffPanel`**
Objective: Reference-text viewer, color-coded diff. Dependencies: Task 02. Tests: diff-rendering test. Definition of Done: test passes.

**Task 04 — Implement `TimestampedCommentScrubber`**
Objective: Waveform/scrubber with expandable comment pins. Dependencies: Task 02. Tests: pin-placement test. Definition of Done: test passes.

**Task 05 — Implement `DecisionActionBar` with Mandatory SoD Hint**
Objective: `isSelfEdited` derivation exclusively from server data + `AdminAuthContext`. Dependencies: Task 02. Tests: **mandatory** — self-edited-fixture disables action bar test. Definition of Done: test passes.

**Task 06 — Implement `SegregationOfDutiesBlock`**
Objective: Clear, explanatory blocked-state message (never just a disabled button with no explanation, per PRD §2.1). Dependencies: Task 05. Tests: message-content test. Definition of Done: test passes.

**Task 07 — Implement the Queue and Detail Pages**
Objective: Compose all components with loading/empty/error states. Dependencies: Tasks 03–06. Tests: full-page smoke tests. Definition of Done: tests pass.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §17, including the mandatory SoD UI test. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm the SoD hint has zero alternate derivation path outside the server-`last_edited_by`-vs-`AdminAuthContext` comparison. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] SoD UI hint derives exclusively from server `last_edited_by` vs. current admin identity — mandatory test passing
- [ ] Blocked state shows a clear explanation, never a bare disabled button
- [ ] Diff and comments are screen-reader-navigable in linear reading order
- [ ] Approve/Request Changes/Reject/Escalate all wire correctly to B-04
- [ ] Queue empty state matches "Queue clear" copy

## 20. Definition of Done
Scholars have a full-context, document-review-grade workspace whose UI-level segregation-of-duties guarantee is provably sourced from the server, never a client-side guess — the primary human interface to E.29's most safety-critical backend guarantee (B-03).
