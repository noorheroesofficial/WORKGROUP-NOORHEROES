# N-04 — AI Feature Kill Switch Console

## 1. Feature Context
Parent PRD: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
Backend Dependency: B-04 (`POST /v1/admin/ai-features/{feature}/suspend` / `/reinstate`, `GET .../active-suspensions`)

## 2. Parent Feature
E.30 — AI Moderation Console & Safety Evaluation Harness

## 3. Sub-feature
**AI Feature Kill Switch Console** (ID: N-04) — Screens 5–7: Kill Switch Confirmation (the single most visually severe treatment in the entire Admin Portal), Feature Suspended State / Active Kill Switches List, Reinstate Confirmation. Directly modeled on `content-cms/components/emergency-suspend-action.tsx`'s absent-not-disabled pattern, extended with a **new, more severe** visual treatment than E.29's suspend action.

## 4. Objective
Make "Suspend Feature" completely absent (not disabled) from the UI for any admin without a safety role, and — for those who do have it — present the platform's single most visually serious confirmation modal, distinct from every other confirmation in the Admin Portal.

## 5. Business Requirements
- §2.1: Kill-Switch Visual Severity — "the platform's most visually serious treatment in the entire Admin Portal ... distinct from E.29's 'serious but calm' content-suspension treatment ... reserved exclusively for this action given its severity class."
- §2.2 Kill Switch Confirmation: clear statement of which feature will be suspended and the immediate platform-wide effect, single confirm action, note that this is fully audited. States: Default, Confirming, Confirmed.
- Frontend AI code-gen prompt item 2 (§7): this modal uses the platform's MOST visually severe design tokens; test confirming it is the *only* action in the entire AI Moderation module using this treatment.
- Frontend AI code-gen prompt item 3: role-based rendering — button absent (not merely disabled) for any role fixture other than the designated safety roles.
- Edge Case 8: rejected at the service layer if attempted despite UI absence (B-04's job; this component's job is the absence itself, and correctly surfacing a 403 if somehow bypassed).

## 6. Existing Architecture
`Component → Hook (mutation) → Repository → apiClient → B-04`. Lives in `src/features/ai-moderation/components/`.

## 7. Existing Code to Reuse
- `content-cms/components/emergency-suspend-action.tsx` — the **exact** absent-not-disabled precedent (`if (!hasPermission(...)) return null;`)
- `ConfirmationDialog`'s `isDanger` prop as the **baseline** to visually exceed, not reuse as-is — this action needs a genuinely distinct, more severe variant per §2.1
- `useAdminSession`/`hasPermission`

## 8. Files to Create
- `src/features/ai-moderation/hooks/use-suspend-ai-feature.ts`
- `src/features/ai-moderation/hooks/use-reinstate-ai-feature.ts`
- `src/features/ai-moderation/hooks/use-active-suspensions.ts`
- `src/features/ai-moderation/components/suspend-ai-feature-action.tsx`
- `src/features/ai-moderation/components/kill-switch-confirmation-modal.tsx` (new severity-tier variant, not a reuse of `ConfirmationDialog`)
- `src/features/ai-moderation/components/active-kill-switches-list.tsx`
- `src/features/ai-moderation/components/reinstate-confirmation-modal.tsx`
- `src/app/(dashboard)/review/ai-moderation/kill-switches/page.tsx`
- `src/features/ai-moderation/__tests__/kill-switch-severity-treatment.test.tsx`
- `src/features/ai-moderation/__tests__/suspend-action-absence.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` → add `AI_FEATURES: { SUSPEND: (f) => \`/v1/admin/ai-features/${f}/suspend\`, REINSTATE: (f) => \`/v1/admin/ai-features/${f}/reinstate\`, ACTIVE: "/v1/admin/ai-features/active-suspensions" }`

## 10. Backend Requirements
Consumes B-04's three endpoints.

## 11. KMP Requirements
Not applicable to this console; A.5 owns the client-side graceful-degradation UI a child sees when a feature is suspended (Edge Case 3) — out of this document's scope, not duplicated here.

## 12. NextJS Requirements

### 12.1 Suspend Action — Absent, Not Disabled (signature component)
```tsx
// src/features/ai-moderation/components/suspend-ai-feature-action.tsx
"use client";
import { useState } from "react";
import { hasPermission, useAdminSession } from "@/features/auth/hooks/use-admin-session";
import { KillSwitchConfirmationModal } from "./kill-switch-confirmation-modal";

const SAFETY_PERMISSION = "ai-moderation:kill-switch";

export function SuspendAiFeatureAction({ feature }: { feature: string }) {
  const { admin } = useAdminSession();
  const [isOpen, setIsOpen] = useState(false);

  if (!hasPermission(admin, SAFETY_PERMISSION)) {
    return null; // ABSENT entirely — no disabled button, no hint this action exists — direct
                 // precedent: content-cms/components/emergency-suspend-action.tsx
  }

  return (
    <>
      <button onClick={() => setIsOpen(true)} className="kill-switch-trigger">
        Suspend Feature
      </button>
      <KillSwitchConfirmationModal feature={feature} isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </>
  );
}
```

### 12.2 Kill Switch Confirmation Modal — the MOST Severe Treatment (signature component)
```tsx
// src/features/ai-moderation/components/kill-switch-confirmation-modal.tsx
"use client";
import { useSuspendAiFeature } from "../hooks/use-suspend-ai-feature";

/**
 * The single most visually severe confirmation treatment in the entire
 * Admin Portal (§2.1) — deliberately NOT built on top of the shared
 * `ConfirmationDialog`'s `isDanger` variant, since that is E.29's
 * "serious but calm" suspend treatment. This component uses a distinct,
 * more urgent red-bordered/warning-icon design token set, reserved
 * EXCLUSIVELY for this action across the whole AI Moderation module.
 */
export function KillSwitchConfirmationModal({ feature, isOpen, onClose }: { feature: string; isOpen: boolean; onClose: () => void }) {
  const mutation = useSuspendAiFeature();
  if (!isOpen) return null;

  return (
    <div role="dialog" aria-modal="true" className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
      <div className="kill-switch-modal w-full max-w-md rounded border-4 border-red-600 bg-white p-6">
        {/* distinct from ConfirmationDialog's thin isDanger border — thicker, more urgent */}
        <div className="flex items-center gap-2 text-red-700">
          {/* warning icon */}
          <h2 className="font-bold">Suspend AI {feature} for all users?</h2>
        </div>
        <p className="mt-2 text-sm text-neutral-700">
          This takes effect platform-wide within 60 seconds and is fully audited.
        </p>
        <div className="mt-4 flex justify-end gap-2">
          <button onClick={onClose} disabled={mutation.isPending}>Cancel</button>
          <button
            onClick={() => mutation.mutate({ feature })}
            disabled={mutation.isPending}
            className="bg-red-600 font-bold text-white"
          >
            Suspend Now
          </button>
        </div>
      </div>
    </div>
  );
}
```

### 12.3 Active Kill Switches List / Feature Suspended State
Read-only list from `useActiveSuspensions()`, each row offering a `ReinstateConfirmationModal` trigger — reachable both from this standalone page and cross-referenced from the Operations Dashboard (E.28), per §6.3.

## 13. API Contract
Consumes B-04 §13 exactly.

## 14. Database Requirements
Not applicable.

## 15. Validation
Not applicable beyond the confirm-step itself.

## 16. Authentication
Standard session flow.

## 17. Authorization
`SuspendAiFeatureAction`'s own `hasPermission(admin, "ai-moderation:kill-switch")` check achieves the absent-not-disabled requirement directly — consistent with `RequirePermission`'s no-fallback pattern, applied here as an explicit inline check since the component needs to conditionally render a *trigger* (not wrap arbitrary children).

## 18. Error Handling
- Suspend attempted despite the UI somehow being stale (e.g., a permission downgrade mid-session) → server's `403 FORBIDDEN` surfaced clearly in the modal, not a silent failure.
- Network/5xx failure → modal remains open with an inline error, action not silently lost.

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
All modal copy via `useTranslation()`, including the feature name interpolation; the "fully audited" note is always shown, in every language, never omitted for brevity.

## 22. RTL
The modal's warning-icon-plus-heading layout, border treatment, and button order must all mirror correctly under `dir="rtl"` — verify against the PRD §2.5 Arabic mockup description (icon/heading order, button positions).

## 23. Analytics
`ai_moderation_kill_switch_activated`, `ai_moderation_kill_switch_reinstated` (§1.19).

## 24. Performance
Not a performance-sensitive surface — correctness of the severity treatment and role-gating matters far more here than speed.

## 25. Security
- The absent-not-disabled pattern avoids signaling the existence of this destructive action to unauthorized users (§25 of the parallel E.29 blueprint's reasoning applies identically here).
- The real authorization boundary remains B-04's server-side `403`, not this component.

## 26. Library Requirements
Next.js 15, TypeScript, TanStack Query v5, Zod — no new dependencies; the severe-treatment modal is built with existing Tailwind utility classes, not a new UI library.

## 27. Testing
- **Signature test 1 (CI-blocking, frontend AI code-gen prompt item 3):** `SuspendAiFeatureAction` renders `null` (absent from the DOM), not a disabled button, for any role fixture other than the designated safety roles.
- **Signature test 2 (CI-blocking, item 2):** confirm the kill-switch modal's severity treatment (border/color/icon class set) is used **only** by this component across the entire AI Moderation module — e.g., a snapshot/class-assertion test plus a repo-wide grep-style check that no other component in `features/ai-moderation/` imports `kill-switch-modal`'s distinctive class names.
- Unit: modal renders correct feature name and the "fully audited"/"60 seconds" copy.
- Integration: suspend flow → confirmed state → appears in Active Kill Switches List → reinstate flow → removed from list.

## 28. Documentation
JSDoc on `KillSwitchConfirmationModal` explicitly stating it must never be reused for any other action's confirmation, and on `SuspendAiFeatureAction` citing `emergency-suspend-action.tsx` as its direct precedent.

## 29. AI Coding Agent Implementation Steps
- **Task 01 — API endpoint constants**: `AI_FEATURES` block.
- **Task 02 — Hooks**: `useSuspendAiFeature()`, `useReinstateAiFeature()`, `useActiveSuspensions()`.
- **Task 03 — `SuspendAiFeatureAction`** per §12.1.
- **Task 04 — `KillSwitchConfirmationModal`** as a genuinely new severity-tier component per §12.2 — not a `ConfirmationDialog` prop variant.
- **Task 05 — `ActiveKillSwitchesList`** and **`ReinstateConfirmationModal`**.
- **Task 06 — Standalone kill-switches page**, plus cross-reference wiring from the Operations Dashboard (E.28) and from N-02's detail screen.
- **Task 07 — Absence signature test** (CI-blocking).
- **Task 08 — Severity-treatment-exclusivity signature test** (CI-blocking).
- **Task 09 — Remaining integration tests**.
- **Task 10 — Documentation**.
- **Task 11 — Final Code Review**: confirm the modal is visually and structurally distinct from `ConfirmationDialog` (not just a prop flag on the same component), per the PRD's explicit requirement that this be a deliberate exception.

## 30. Definition of Done
Suspend action absent for non-safety roles (tested); kill-switch confirmation uses a genuinely distinct, most-severe visual treatment exclusive to this action (tested); active-suspensions list and reinstate flow functional.

## 31. Final Verification Checklist
- [ ] `SuspendAiFeatureAction` absent (not disabled) for non-safety-role fixtures — tested
- [ ] Kill-switch modal visually distinct from `ConfirmationDialog`'s `isDanger` variant
- [ ] Severity treatment confirmed exclusive to this one action — tested
- [ ] Modal states (Default, Confirming, Confirmed) implemented
- [ ] Active Kill Switches List and Reinstate flow functional
- [ ] Cross-referenced from Operations Dashboard (E.28) per §6.3
- [ ] RTL layout verified against the PRD's Arabic mockup description
- [ ] Tests green in CI, both signature tests non-bypassable
