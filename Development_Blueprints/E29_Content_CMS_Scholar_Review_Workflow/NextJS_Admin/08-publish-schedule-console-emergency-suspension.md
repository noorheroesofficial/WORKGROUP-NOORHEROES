# N-08 — Publish/Schedule Console & Emergency Suspension

## 1. Feature Context
The final-mile UI: Publish is unavailable until both required approvals genuinely exist on the target version (sourced from the server, never guessed), and Emergency Suspend is entirely absent from the DOM — not merely disabled — for any admin without a safety-role flag.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
2.8 Publish/Schedule Console & Emergency Suspension (ID: **N-08**)

## 4. Objective
Build the Publish/Schedule screen (gated on both-approvals-present via B-06) and the Emergency Suspend action (visible only to safety roles), plus the Version History/Diff Viewer, reachable from any content item detail.

## 5. Business Requirements
- §7 frontend AI-prompt requirement #4: Publish action's availability requires BOTH `scholar_reviewer` AND `child_safety_reviewer` decisions on the target version, sourced from the server's review-history response; disabled with only one present.
- §7 frontend AI-prompt requirement #6: Emergency Suspend visible ONLY for admins whose role includes a safety-role flag; absent from the UI entirely for non-safety roles, not merely disabled.
- FR-6 (UI reflection): episode-sequencing block surfaced with an explanatory message.

## 6. Existing Architecture
`src/features/publish-console/` module, reached from any fully-or-partially-approved content item's detail view.

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/confirmation-dialog.tsx::ConfirmationDialog`
- N-01's `VersionStatusIndicator` (reused for consistent status display)

## 8. Files to Create
- `src/app/(dashboard)/content/[id]/publish/page.tsx`
- `src/features/publish-console/api/publish-repository.ts`
- `src/features/publish-console/hooks/use-publish-eligibility.ts`, `use-publish-action.ts`, `use-suspend-action.ts`
- `src/features/publish-console/components/publish-eligibility-panel.tsx` — shows both-approvals status
- `src/features/publish-console/components/episode-sequencing-block.tsx`
- `src/features/publish-console/components/emergency-suspend-action.tsx`
- `src/features/publish-console/components/version-history-diff-viewer.tsx`
- `src/features/publish-console/types/publish-eligibility.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `PUBLISH_CONSOLE.*` endpoints

## 10. NextJS Requirements
- `PublishEligibilityPanel`: fetches the target version's review-history response; the Publish button is `disabled` unless both `scholar` and `child_safety` stages show `decision='approve'` — sourced from this response, never a client-side assumption.
- `EpisodeSequencingBlock`: for episode-type content, surfaces the preceding-episode-unlock-threshold-missing condition with explanatory text if B-06 rejects with `409 PRECEDING_EPISODE_UNLOCK_THRESHOLD_MISSING`.
- `EmergencySuspendAction`: rendered conditionally based on `AdminAuthContext`'s resolved permission set containing a safety-role flag — for non-safety roles, this component (and its containing DOM node) is not rendered at all, verified by a DOM-query-absence test, not a `display:none`/disabled check.
- `VersionHistoryDiffViewer`: reachable from any content item detail (not just publish-flow), reuses N-04's `VersionDiffPanel` where applicable.

## 11. Required API
**Admin API** — B-06: `PATCH /v1/admin/content/{id}/publish`. B-07: `POST /v1/admin/content/{id}/suspend`. B-01: `GET /v1/admin/content/{id}/versions`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="publisher"` for the publish action; Emergency Suspend additionally requires a safety-role flag from `AdminAuthContext`.

## 13. Loading / Empty / Error States
Eligibility-check loading state; publish-blocked state (not an error — an expected, explained condition) distinct from a genuine publish-failure error; suspend-confirmation flow with a required-reason field.

## 14. Responsive UI / Accessibility
Eligibility panel conveys approval status with text labels per stage, not color alone; suspend confirmation dialog fully keyboard-operable.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
The Emergency Suspend absence-not-disabled requirement is this component's defining guarantee — verified with a DOM-query test confirming zero trace of the action in the rendered tree for non-safety roles, since a merely-disabled-but-present button could still be inspected/manipulated via browser dev tools in a way an absent element cannot.

## 17. Testing
Unit: both-approvals eligibility derivation, safety-role-flag-gates-suspend-visibility logic. UI: **mandatory** — Publish button remains disabled with only one of the two required approvals present (per PRD frontend AI-prompt requirement #4); **mandatory** — Emergency Suspend is entirely absent from the rendered DOM for a non-safety-role fixture admin, not merely disabled (per PRD frontend AI-prompt requirement #6). Integration: full both-approvals-present → publish → status-updates flow; full suspend-with-reason → status-updates flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `publish-eligibility.ts` schema. Files: `types/publish-eligibility.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `PublishRepositoryImpl`**
Objective: Repository for publish/suspend/version-history endpoints. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `PublishEligibilityPanel`**
Objective: Both-approvals-required derivation and display. Dependencies: Task 02. Tests: **mandatory** — single-approval-disables-publish test. Definition of Done: test passes.

**Task 04 — Implement `EpisodeSequencingBlock`**
Objective: Explanatory message on `409 PRECEDING_EPISODE_UNLOCK_THRESHOLD_MISSING`. Dependencies: Task 02. Tests: error-message-mapping test. Definition of Done: test passes.

**Task 05 — Implement `EmergencySuspendAction` with Absence-Not-Disabled Gating**
Objective: Conditional rendering based on `AdminAuthContext`'s safety-role flag. Dependencies: Task 02. Tests: **mandatory** — DOM-absence test for non-safety-role fixture. Definition of Done: test passes.

**Task 06 — Implement `VersionHistoryDiffViewer`**
Objective: Reusable version history/diff view, reusing N-04's diff panel. Dependencies: N-04, Task 02. Tests: reuse-not-duplication check. Definition of Done: single diff-rendering implementation across the app.

**Task 07 — Implement the Publish Console Page**
Objective: Compose eligibility panel + sequencing block + suspend action + version history. Dependencies: Tasks 03–06. Tests: full-page smoke test. Definition of Done: test passes.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §17, including both mandatory tests. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm Emergency Suspend's absence (not just disabled state) for non-safety roles via actual DOM inspection in tests; confirm publish-eligibility is genuinely server-sourced. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Publish disabled unless both Scholar and Child-Safety approvals are present — mandatory test passing
- [ ] Episode-sequencing block correctly explains the preceding-episode-threshold-missing condition
- [ ] Emergency Suspend is entirely absent from the DOM (not disabled) for non-safety-role admins — mandatory test passing
- [ ] Suspend requires a reason and shows a confirmation step
- [ ] Version History/Diff Viewer reuses N-04's diff component, no duplication

## 20. Definition of Done
Publishing and emergency suspension are gated with provably server-sourced eligibility checks and role-based DOM-level visibility — the final UI-layer reinforcement of B-06's and B-07's backend guarantees.
