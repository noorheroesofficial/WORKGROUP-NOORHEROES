# N-02 — AI Moderation Detail & Redacted Transcript View

## 1. Feature Context
Parent PRD: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
Backend Dependency: B-01 (`GET /v1/admin/ai-moderation/{id}`), B-02 (`POST .../transcript-access-request`)

## 2. Parent Feature
E.30 — AI Moderation Console & Safety Evaluation Harness

## 3. Sub-feature
**AI Moderation Detail & Redacted Transcript View** (ID: N-02) — Screens 2–4: the Detail screen (redacted prompt/output, pipeline breadcrumb, metadata), the Transcript-Access Elevated Permission Gate modal, and the Full Transcript View. This sub-feature's defining guarantee: raw transcript text must be **structurally absent from the DOM** until the server grants access — not merely CSS-hidden.

## 4. Objective
Render full pipeline context from the redacted default response, and gate raw-content display behind an explicit, server-verified action — with a signature test proving the raw content never touches the component tree before that grant.

## 5. Business Requirements
- §2.1: redacted-transcript visual language — `[Child]` placeholder tokens, visually distinguished from genuine content; pipeline-stage breadcrumb.
- §2.2: components — redacted prompt/output panel, pipeline-stage breadcrumb, policy category tag, model version, retrieval-sources list, confidence score, filters-triggered list, "View Full Transcript" action (gated), five-action button row (four here, kill-switch in N-04). States: Default, Transcript-gate-pending, Action-confirming, Resolved. Accessibility: redacted placeholders screen-reader-announced distinctly from genuine text.
- Frontend AI code-gen prompt item 1 (§7): raw transcript text must be absent from the component tree/DOM until the server grants access, not merely visually hidden via CSS (since CSS-hiding would still expose it to inspection).

## 6. Existing Architecture
`Page → Hooks (React Query) → Repository → apiClient → B-01/B-02`. New feature module `src/features/ai-moderation/`, sibling components to N-01, N-03.

## 7. Existing Code to Reuse
- `ConfirmationDialog` (for the Transcript-Access Gate modal shell — extend, not fork, unless the severity-treatment requirements in N-04 force a genuinely new variant)
- `useTranslation()`, `useAdminSession`
- The `RequirePermission`-style "renders nothing unless authorized" pattern

## 8. Files to Create
- `src/features/ai-moderation/api/ai-moderation-detail-schemas.ts`
- `src/features/ai-moderation/hooks/use-ai-moderation-detail.ts`
- `src/features/ai-moderation/hooks/use-transcript-access.ts`
- `src/features/ai-moderation/components/pipeline-stage-breadcrumb.tsx`
- `src/features/ai-moderation/components/redacted-transcript-panel.tsx`
- `src/features/ai-moderation/components/transcript-access-gate-modal.tsx`
- `src/features/ai-moderation/components/full-transcript-view.tsx`
- `src/app/(dashboard)/review/ai-moderation/[id]/page.tsx`
- `src/features/ai-moderation/__tests__/transcript-dom-absence.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` → add `AI_MODERATION.TRANSCRIPT_ACCESS = (id) => \`/v1/admin/ai-moderation/${id}/transcript-access-request\``

## 10. Backend Requirements
Consumes B-01 (`GET .../{id}`) and B-02 (`POST .../transcript-access-request`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements

### 12.1 Detail Schema
```ts
export const aiModerationDetailSchema = z.object({
  redactedPrompt: z.string(),
  redactedOutput: z.string(),
  policyCategory: z.string(),
  modelVersion: z.string().nullable(),
  retrievalSources: z.array(z.string()),
  confidenceScore: z.number(),
  filtersTriggered: z.array(z.string()),
  stageFlagged: z.string(),
});
```

### 12.2 Structural DOM-Absence — the signature component
```tsx
// src/features/ai-moderation/components/full-transcript-view.tsx
"use client";
import { useTranscriptAccess } from "../hooks/use-transcript-access";

export function FullTranscriptView({ queueItemId }: { queueItemId: string }) {
  const { data, status, requestAccess } = useTranscriptAccess(queueItemId);
  // CRITICAL: `data` (raw_prompt/raw_output) is undefined/absent from this
  // component's render tree entirely until the mutation resolves with a
  // grant — there is no pre-fetched, CSS-hidden raw content anywhere in
  // the DOM before that point. Do NOT prefetch this data speculatively.

  if (status === "idle") {
    return <button onClick={requestAccess}>View Full Transcript</button>;
  }
  if (status === "pending") {
    return <p role="status">Requesting access…</p>;
  }
  if (status === "rejected") {
    return <p role="alert">Access denied — this action has been logged.</p>;
  }
  // status === "granted" — ONLY here does raw content enter the tree
  return (
    <div>
      <p>{data!.rawPrompt}</p>
      <p>{data!.rawOutput}</p>
    </div>
  );
}
```

### 12.3 Redacted Panel — Placeholder Visual Language
```tsx
export function RedactedTranscriptPanel({ redactedPrompt, redactedOutput }: { redactedPrompt: string; redactedOutput: string }) {
  return (
    <div className="rounded bg-neutral-100 p-3">
      {/* [Child] tokens render with a subtly different background per §2.1;
          announced distinctly to screen readers via aria-label per §2.2 accessibility */}
      <p aria-label="Redacted prompt, child identifier withheld">{redactedPrompt}</p>
      <p aria-label="Redacted output, child identifier withheld">{redactedOutput}</p>
    </div>
  );
}
```

### 12.4 Pipeline-Stage Breadcrumb
Six-stage horizontal trail (Prompt Filter → Restricted Engine → RAG Boundary → Confidence Score → Output Moderation → Parent Audit), the `stageFlagged` stage visually highlighted (amber per the §2.5 mockup spec), the rest neutral.

## 13. API Contract
Consumes B-01 §13 and B-02 §13 exactly.

## 14. Database Requirements
Not applicable.

## 15. Validation
Not applicable (read/gated-read only).

## 16. Authentication
Standard session flow; the transcript-access mutation carries the admin's existing session — no separate re-authentication step beyond the elevated scope check the server performs.

## 17. Authorization
Page-level: `RequirePermission permission="ai-moderation:read"`. The "View Full Transcript" action itself performs no client-side permission pre-check — the grant/reject decision is derived **strictly from the server's response**, per §6.4 of the parent breakdown ("never assumed client-side based on the admin's general role"), since an admin's general role does not imply the elevated transcript-access scope.

## 18. Error Handling
- Rejected transcript-access request → clear "Access denied — this action has been logged" message (§18 of B-02), not a generic error toast, since the rejection itself is an expected, correctly-audited outcome, not a system failure.
- Detail fetch failure → standard `ErrorView`/retry.

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
All labels via `useTranslation()`; support English/Hindi/Arabic/Urdu per PRD §19, with RTL-safe breadcrumb direction (the six-stage trail should visually reverse order under `dir="rtl"`, not just mirror text).

## 22. RTL
Breadcrumb, redacted panel, and metadata-tag row all verified under `dir="rtl"`, mirroring the Arabic mockup description in PRD §2.5.

## 23. Analytics
`ai_moderation_detail_viewed`, `ai_moderation_transcript_access_requested`, `ai_moderation_transcript_access_granted`, `ai_moderation_transcript_access_rejected` (§1.19).

## 24. Performance
Detail fetch is a single request; transcript-access request is a separate, explicit, non-prefetched mutation — deliberately not bundled into the initial detail fetch, since prefetching would undermine the DOM-absence guarantee even if the raw data were merely unused.

## 25. Security
**This sub-feature's defining guarantee is §12.2's DOM-absence property** — verified by the signature test in §27, not just a visual/CSS check. This is a genuine security property (raw content in the DOM is inspectable regardless of CSS `display: none`), not a cosmetic one.

## 26. Library Requirements
Next.js 15, TypeScript, TanStack Query v5 (mutation, not query, for transcript access — it has side effects: server-side audit writes), Zod.

## 27. Testing
- **Signature test (CI-blocking, frontend AI code-gen prompt item 1):** confirm the raw transcript text is never present in the component tree/DOM until the explicit gated action succeeds — assert via DOM query (`queryByText`/`container.textContent`) that the raw strings are absent both before the request and during a `pending`/`rejected` state, appearing only after a `granted` response.
- Unit: `RedactedTranscriptPanel` renders `[Child]`-style placeholders with the distinct screen-reader `aria-label`.
- Unit: pipeline-stage breadcrumb highlights the correct stage.
- Unit: rejected-access state renders the correct message, not a generic error.
- Integration: full "View Full Transcript" click → grant → raw content appears; and click → reject → denial message, raw content still absent.

## 28. Documentation
JSDoc on `FullTranscriptView` explicitly stating the no-prefetch, DOM-absence contract, so future edits don't accidentally introduce prefetching.

## 29. AI Coding Agent Implementation Steps
- **Task 01 — Schemas**: detail + transcript-access response schemas.
- **Task 02 — Hooks**: `useAiModerationDetail()` (query), `useTranscriptAccess()` (mutation, no prefetch).
- **Task 03 — Pipeline-Stage Breadcrumb component**.
- **Task 04 — Redacted Transcript Panel component** with accessibility labeling.
- **Task 05 — Transcript-Access Gate modal** (reuse `ConfirmationDialog` shell).
- **Task 06 — Full Transcript View component** per §12.2's DOM-absence contract.
- **Task 07 — Detail page** wiring all components together.
- **Task 08 — DOM-absence signature test** (CI-blocking).
- **Task 09 — Remaining unit/integration tests**.
- **Task 10 — Documentation**.
- **Task 11 — Final Code Review**: grep for any prefetch/`useQuery` (vs `useMutation`) usage on the transcript-access path — this must remain an explicit, non-prefetched mutation.

## 30. Definition of Done
Detail screen renders full redacted pipeline context; transcript access is gated behind an explicit, server-verified, non-prefetched action; DOM-absence of raw content before grant verified by a CI-blocking test.

## 31. Final Verification Checklist
- [ ] Detail screen renders all §2.2 components from the redacted response
- [ ] Pipeline-stage breadcrumb correctly highlights the flagged stage
- [ ] Redacted placeholders are screen-reader-distinct (tested)
- [ ] Raw transcript text is DOM-absent until grant (tested, CI-blocking)
- [ ] Rejected access shows a clear denial message, not a generic error
- [ ] Grant/reject state is strictly server-derived, never client-inferred from role
- [ ] RTL layout verified for breadcrumb and panels
- [ ] Tests green in CI
