# N-05 — Evaluation Harness Dashboard & Release Gate

## 1. Feature Context
Parent PRD: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
Backend Dependency: B-05 (`POST /v1/admin/ai-evaluations`, `GET /v1/admin/ai-evaluations/runs/{id}`)

## 2. Parent Feature
E.30 — AI Moderation Console & Safety Evaluation Harness

## 3. Sub-feature
**Evaluation Harness Dashboard & Release Gate** (ID: N-05) — Screens 8–11: Evaluation Case Detail, Evaluation Harness Dashboard, Evaluation Run Detail, Release Gate Decision. The Release Gate Decision display's rendering condition is this sub-feature's signature guarantee.

## 4. Objective
Give AI/ML engineers a clear view of evaluation runs, distinguishing critical from non-critical findings, with the gate-blocked state rendered **only** when `critical_findings_count > 0` — never approximated by any other condition.

## 5. Business Requirements
- §1.18 Screens 8–11: Evaluation Case Detail, Evaluation Harness Dashboard, Evaluation Run Detail (findings, critical/non-critical breakdown), Release Gate Decision (pass/blocked).
- Frontend AI code-gen prompt item 4 (§7): Release Gate Decision display clearly distinguishes critical from non-critical findings, gate-blocked state rendered only when `critical_findings_count > 0` — test both gate-passed and gate-blocked rendering states based on this exact condition.
- Edge Case 5: zero critical findings but several non-critical findings → release may proceed; non-critical findings still tracked/shown, not hidden.
- Edge Case 7: an evaluation case referencing since-withdrawn content remains valid, clearly annotated.
- §1.12: "No evaluation cases recorded yet" empty state for a newly-deployed AI feature.

## 6. Existing Architecture
`Page → Hooks (React Query) → Repository → apiClient → B-05`. Lives in `src/features/ai-moderation/` (or a sibling `src/features/evaluation-harness/` if the module grows large enough to warrant separation — start co-located per NEXT-JS-INSTRUCTIONS.md's incremental convention).

## 7. Existing Code to Reuse
- `DataTable`, `EmptyState`, `ErrorView`, `LoadingState`
- `StatusBadge` for critical/non-critical/pass/blocked visual states
- `useTranslation()`, `useFormatters()` (for `run_at` date formatting)

## 8. Files to Create
- `src/features/ai-moderation/api/evaluation-schemas.ts`
- `src/features/ai-moderation/api/evaluation-resource-client.ts`
- `src/features/ai-moderation/hooks/use-evaluation-runs.ts`
- `src/features/ai-moderation/hooks/use-evaluation-run-detail.ts`
- `src/features/ai-moderation/hooks/use-evaluation-case-detail.ts`
- `src/features/ai-moderation/components/release-gate-decision.tsx`
- `src/features/ai-moderation/components/findings-breakdown.tsx`
- `src/app/(dashboard)/intelligence/evaluation-harness/page.tsx`
- `src/app/(dashboard)/intelligence/evaluation-harness/runs/[id]/page.tsx`
- `src/features/ai-moderation/__tests__/release-gate-rendering.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` → add `AI_EVALUATIONS: { BASE: "/v1/admin/ai-evaluations", RUN_DETAIL: (id) => \`/v1/admin/ai-evaluations/runs/${id}\` }`

## 10. Backend Requirements
Consumes B-05's case-creation and run-detail endpoints.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements

### 12.1 Release Gate Decision — the signature component
```tsx
// src/features/ai-moderation/components/release-gate-decision.tsx
"use client";
export function ReleaseGateDecision({
  criticalFindingsCount,
  nonCriticalFindingsCount,
}: {
  criticalFindingsCount: number;
  nonCriticalFindingsCount: number;
}) {
  // The ONLY condition that determines the blocked state — no other signal
  // (e.g. non-critical count, run age, etc.) may influence this.
  const gateBlocked = criticalFindingsCount > 0;

  return (
    <div role="status" className={gateBlocked ? "border-red-600 bg-red-50" : "border-green-600 bg-green-50"}>
      <h3>{gateBlocked ? "Release Blocked" : "Release Gate Passed"}</h3>
      <p>Critical findings: {criticalFindingsCount}</p>
      <p>Non-critical findings: {nonCriticalFindingsCount}</p>
      {!gateBlocked && nonCriticalFindingsCount > 0 && (
        <p className="text-sm text-neutral-600">
          Non-critical findings should still be tracked and addressed in a reasonable follow-up timeframe.
        </p>
      )}
    </div>
  );
}
```

### 12.2 Evaluation Case Detail — Withdrawn-Content Annotation
```tsx
{caseDetail.scenario.referencesWithdrawnContent && (
  <p role="note" className="text-amber-700">
    This case references content that has since been withdrawn from the approved corpus. The case remains valid
    as a behavior test of the AI pipeline; the referenced content itself is no longer available.
  </p>
)}
```
> `referencesWithdrawnContent` field name is illustrative — confirm the actual field/shape B-05's `scenario` JSON uses for this annotation before implementation (per B-05 §27's own note that the withdrawn-content signal's exact shape must be confirmed against E.29, not guessed).

## 13. API Contract
Consumes B-05 §13 exactly.

## 14. Database Requirements
Not applicable.

## 15. Validation
Not applicable (read-mostly; case creation form validates a non-empty scenario object client-side, mirroring B-05's server-side check).

## 16. Authentication
Standard session flow.

## 17. Authorization
`RequirePermission permission="ai-moderation:read"` gates the dashboard; no additional restriction beyond that, since evaluation data is informational to any moderator/engineer with console access.

## 18. Error Handling
Standard `ErrorView`/retry via `DataTable`/query hooks; empty-corpus state → "No evaluation cases recorded yet" (§1.12) via `EmptyState`.

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
All labels via `useTranslation()`; findings counts and dates via `useFormatters()`.

## 22. RTL
Findings-breakdown and gate-decision panels verified under `dir="rtl"`.

## 23. Analytics
`ai_evaluation_harness_run_completed` (with `critical_findings_count`, `non_critical_findings_count`), `ai_evaluation_release_gate_passed`, `ai_evaluation_release_gate_blocked` (§1.19) — fired client-side on successful run-detail fetch, reflecting the same condition `ReleaseGateDecision` uses to render.

## 24. Performance
Run-detail and case-detail are lightweight single-record reads; the dashboard list is paginated via `DataTable`'s existing mechanism if the run history grows large.

## 25. Security
No new security surface — read-only informational views behind the same `ai-moderation:read` scope as the rest of the console.

## 26. Library Requirements
Next.js 15, TypeScript, TanStack Query v5, Zod.

## 27. Testing
- **Signature test (CI-blocking, frontend AI code-gen prompt item 4):** `ReleaseGateDecision` renders the blocked state **only** when `criticalFindingsCount > 0` — test both a gate-passed case (`critical: 0, nonCritical: 5`) and a gate-blocked case (`critical: 1, nonCritical: 0`), confirming the rendered state tracks the exact condition, not an approximation.
- Unit: non-critical-only findings render the "still tracked" follow-up note, gate shows passed.
- Unit: empty evaluation-case corpus renders "No evaluation cases recorded yet."
- Unit: withdrawn-content annotation renders correctly once the real field shape is confirmed (B-05 dependency).
- Integration: full case-creation → run-detail → release-gate-decision flow.

## 28. Documentation
JSDoc on `ReleaseGateDecision` explicitly stating the single-condition rule (`criticalFindingsCount > 0`) as the only permitted gating signal.

## 29. AI Coding Agent Implementation Steps
- **Task 01 — API endpoint constants**: `AI_EVALUATIONS` block.
- **Task 02 — Schemas & Repository**.
- **Task 03 — Hooks**: run list, run detail, case detail.
- **Task 04 — `ReleaseGateDecision`** per §12.1's exact-condition rule.
- **Task 05 — `FindingsBreakdown`** component (critical vs. non-critical visual distinction).
- **Task 06 — Evaluation Case Detail** with withdrawn-content annotation (confirm field shape with B-05 first).
- **Task 07 — Dashboard and Run Detail pages**.
- **Task 08 — Release-gate-condition signature test** (CI-blocking).
- **Task 09 — Remaining unit/integration tests**.
- **Task 10 — Documentation**.
- **Task 11 — Final Code Review**: confirm `gateBlocked` is derived from `criticalFindingsCount > 0` alone, with no other variable able to influence it anywhere in the component tree.

## 30. Definition of Done
Dashboard, run detail, and case detail screens implemented; release-gate rendering verified by a CI-blocking test to depend solely on `critical_findings_count > 0`.

## 31. Final Verification Checklist
- [ ] `ReleaseGateDecision` blocks only when `criticalFindingsCount > 0` — tested for both states
- [ ] Non-critical findings displayed and tracked, never hidden, even when gate passes
- [ ] Empty-corpus state renders correctly
- [ ] Withdrawn-content annotation confirmed against real B-05 data shape, not guessed
- [ ] RTL layout verified
- [ ] Tests green in CI
