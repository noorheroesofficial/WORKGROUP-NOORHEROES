# N-03 — Moderator Resolution Action Bar

## 1. Feature Context
Parent PRD: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
Backend Dependency: B-03 (`POST /v1/admin/ai-moderation/{id}/resolve`)

## 2. Parent Feature
E.30 — AI Moderation Console & Safety Evaluation Harness

## 3. Sub-feature
**Moderator Resolution Action Bar** (ID: N-03) — the four-action button row (Approve Refusal, Mark False Positive, Escalate Content Gap, Create Evaluation Case) plus idempotent "already resolved" UI handling. Directly modeled on E.29's `decision-action-bar.tsx`/`segregation-of-duties-block.tsx` pattern pair.

## 4. Objective
Let a moderator resolve a flagged item in one click per action, and — when a race with another moderator produces an "already resolved" server response — show a clear explanatory message instead of an error, mirroring E.29's `SegregationOfDutiesBlock` pattern.

## 5. Business Requirements
- FR-4/§2.2: five-action button row (four here; kill-switch action lives in N-04 as its own visually-distinct component, per §2.1's severity-treatment requirement).
- Frontend AI code-gen prompt item 5 (§7): idempotent UI handling — if resolve returns an "already resolved" response, show a clear "this was already resolved by [reviewer]" message rather than an error.
- §2.2 states: Default, Action-confirming, Resolved.

## 6. Existing Architecture
`Component → Hook (mutation) → Repository → apiClient → B-03`. Lives in `src/features/ai-moderation/components/`, directly parallel to `scholar-review/components/decision-action-bar.tsx`.

## 7. Existing Code to Reuse
- `scholar-review/components/decision-action-bar.tsx` — the exact structural precedent for a mutation-dispatching button row
- `scholar-review/components/segregation-of-duties-block.tsx` — the exact structural precedent for an explanatory blocked/already-handled state, adapted here for "already resolved by [reviewer]" rather than "you can't approve your own edit"
- `useTranslation()`

## 8. Files to Create
- `src/features/ai-moderation/hooks/use-resolve-moderation-item.ts`
- `src/features/ai-moderation/components/resolution-action-bar.tsx`
- `src/features/ai-moderation/components/already-resolved-block.tsx`
- `src/features/ai-moderation/__tests__/idempotent-resolution-ui.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` → add `AI_MODERATION.RESOLVE = (id) => \`/v1/admin/ai-moderation/${id}/resolve\``
- `src/app/(dashboard)/review/ai-moderation/[id]/page.tsx` (N-02) → mount `ResolutionActionBar`

## 10. Backend Requirements
Consumes B-03: `POST /v1/admin/ai-moderation/{id}/resolve`.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements

### 12.1 Already-Resolved Block — the signature component
```tsx
// src/features/ai-moderation/components/already-resolved-block.tsx
"use client";
export function AlreadyResolvedBlock({ resolvedBy, resolutionAction }: { resolvedBy: string; resolutionAction: string }) {
  return (
    <div role="status" className="rounded border-l-4 border-amber-500 bg-amber-50 p-3 text-sm">
      <p className="font-medium">This item was already resolved</p>
      <p className="mt-1 text-neutral-600">
        {resolvedBy} resolved this as &quot;{resolutionAction}&quot; before your action was submitted — no further
        action is needed here.
      </p>
    </div>
  );
}
```

### 12.2 Resolution Action Bar
```tsx
// src/features/ai-moderation/components/resolution-action-bar.tsx
"use client";
import { useState } from "react";
import { useResolveModerationItem } from "../hooks/use-resolve-moderation-item";
import { AlreadyResolvedBlock } from "./already-resolved-block";

const ACTIONS = ["approve_refusal", "mark_false_positive", "escalate_content_gap", "create_evaluation_case"] as const;

export function ResolutionActionBar({ queueItemId }: { queueItemId: string }) {
  const mutation = useResolveModerationItem();
  const [alreadyResolved, setAlreadyResolved] = useState<{ resolvedBy: string; resolutionAction: string } | null>(null);

  if (alreadyResolved) {
    return <AlreadyResolvedBlock {...alreadyResolved} />;
  }

  const handle = async (action: (typeof ACTIONS)[number]) => {
    const result = await mutation.mutateAsync({ queueItemId, action });
    if (result.alreadyResolved) {
      setAlreadyResolved({ resolvedBy: result.resolvedBy, resolutionAction: result.resolutionAction });
    }
  };

  return (
    <div className="flex gap-3">
      {ACTIONS.map((action) => (
        <button key={action} disabled={mutation.isPending} onClick={() => handle(action)}>
          {/* label via useTranslation(`resolutionAction.${action}`) */}
          {action}
        </button>
      ))}
    </div>
  );
}
```

## 13. API Contract
Consumes B-03 §13 exactly, including the `already_resolved`/`resolved_by`/`resolution_action` response fields.

## 14. Database Requirements
Not applicable.

## 15. Validation
Action buttons are disabled while a mutation is in flight, preventing duplicate submits from the same client (a UX nicety — B-03's server-side idempotency is the real guarantee).

## 16. Authentication
Standard session flow.

## 17. Authorization
Action bar rendered only within N-02's already-permission-gated detail page; no additional client-side gating needed here since all four actions share the same `ai-moderation:read` scope (unlike N-04's kill switch, which needs its own stricter gate).

## 18. Error Handling
- **Idempotent no-op (not an error):** `already_resolved: true` response → `AlreadyResolvedBlock`, never a toast/error styling.
- **Genuine failure** (network error, 5xx, validation error): standard error toast/inline message, distinct from the idempotent case.

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
All four action labels and the `AlreadyResolvedBlock` copy via `useTranslation()`; button order reverses correctly under RTL button-row layout.

## 22. RTL
Verified — button row and the resolved-block's left border accent (`border-l-4`) should mirror to `border-r-4` under `dir="rtl"`.

## 23. Analytics
`ai_moderation_approve_expected_refusal`, `ai_moderation_mark_false_positive`, `ai_moderation_escalate_content_gap`, `ai_moderation_evaluation_case_created`, `ai_queue_redundant_action_noop` (fired specifically when `alreadyResolved` is true) per §1.19.

## 24. Performance
Single mutation call per click; no polling needed since the idempotent-response path already handles the race condition gracefully.

## 25. Security
No new security surface — relies entirely on B-03's server-side idempotency and scope enforcement; this component's job is purely presentational correctness for the no-op case.

## 26. Library Requirements
Next.js 15, TypeScript, TanStack Query v5 (`useMutation`), Zod.

## 27. Testing
- **Signature test (CI-blocking, frontend AI code-gen prompt item 5):** mock a resolve response with `already_resolved: true` and confirm `AlreadyResolvedBlock` renders with the correct `resolvedBy`/`resolutionAction`, not a generic error state.
- Unit: each of the four action buttons dispatches the correct `action` string.
- Unit: buttons disabled while `mutation.isPending`.
- Integration: full click → success (non-idempotent) → resolved-state UI update on the parent detail page.

## 28. Documentation
JSDoc noting the parallel to `scholar-review`'s `decision-action-bar.tsx`/`segregation-of-duties-block.tsx` pair, so future maintainers recognize the shared pattern.

## 29. AI Coding Agent Implementation Steps
- **Task 01 — API endpoint constant**: add `RESOLVE` to `AI_MODERATION`.
- **Task 02 — Hook**: `useResolveModerationItem()` mutation.
- **Task 03 — `AlreadyResolvedBlock` component**.
- **Task 04 — `ResolutionActionBar` component** per §12.2.
- **Task 05 — Wire into N-02's detail page**.
- **Task 06 — Idempotent-UI signature test** (CI-blocking).
- **Task 07 — Remaining unit/integration tests**.
- **Task 08 — Documentation**.
- **Task 09 — Final Code Review**: confirm the idempotent-response branch is visually and semantically distinct from a genuine error (no shared "red error box" styling between the two).

## 30. Definition of Done
Four resolution actions functional; idempotent "already resolved" case renders a clear explanatory message (not an error), verified by a CI-blocking test.

## 31. Final Verification Checklist
- [ ] All four resolution actions dispatch correctly
- [ ] Idempotent `already_resolved` response renders `AlreadyResolvedBlock`, not an error (tested)
- [ ] Buttons disabled during in-flight mutation
- [ ] Analytics events fire correctly per action, including the internal no-op event
- [ ] RTL layout verified
- [ ] Tests green in CI
