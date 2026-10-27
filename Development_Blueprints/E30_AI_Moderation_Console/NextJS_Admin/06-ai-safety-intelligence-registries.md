# N-06 — AI Safety Intelligence Registries

## 1. Feature Context
Parent PRD: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
Backend Dependency: B-01 (amended, `resolution_action` filter), B-07 (Model Version Registry, Blocked Topics Registry)

> **Revision note:** the first pass of this blueprint left both registries blocked pending backend contract confirmation. B-07 now exists and grounds both registries in data E.30 already captures (no invented F.35 dependency) — this revision wires the real endpoints and removes the "do not implement yet" guidance.

## 2. Parent Feature
E.30 — AI Moderation Console & Safety Evaluation Harness

## 3. Sub-feature
**AI Safety Intelligence Registries** (ID: N-06) — Screens 13–15: False-Positive Feedback Log (read-only), Model Version / Blocked Topics Registry, Model Version Detail. Reached from the Admin Portal's "Intelligence" navigation group.

## 4. Objective
Give Trust & Safety and AI/ML engineering a read-only view of accumulated false-positive signals (feeding model-quality review per §11.5) and a reference registry of model versions and the platform's actually-enforced blocked-topic categories — all sourced from data the console already writes, honestly labeled where its granularity is coarser than the screen name might imply.

## 5. Business Requirements
- §1.18 Screen 13: False-Positive Feedback Log, Read-only, model-quality signal, entry from "Intelligence" nav group.
- §1.18 Screens 14–15: Model Version / Blocked Topics Registry and Model Version Detail, entry from "Intelligence" nav group.
- §11.5: false-positive and content-gap signals from this console directly inform model/corpus quality improvements.
- B-07 §10.3: the Blocked Topics Registry reflects the current coarse three-category enforcement taxonomy (`topic_blocked`/`question_redirected`/`question_approved`), not a fine-grained keyword list — this UI must not misrepresent that granularity.

## 6. Existing Architecture
`Page → Hook (React Query) → Repository → apiClient → B-01/B-07`. Lives in `src/features/ai-moderation/` as read-only sub-screens, sibling to N-01/N-05.

## 7. Existing Code to Reuse
- `DataTable`, `EmptyState`, `ErrorView`, `LoadingState`
- N-01's `AiModerationResourceClient.getQueue()` — the False-Positive Log reuses this exact method with a `resolutionAction` filter, no new client class
- `useTranslation()`, `useFormatters()`

## 8. Files to Create
- `src/features/ai-moderation/hooks/use-false-positive-log.ts`
- `src/features/ai-moderation/api/model-version-schemas.ts`
- `src/features/ai-moderation/api/model-version-resource-client.ts`
- `src/features/ai-moderation/hooks/use-model-version-registry.ts`
- `src/features/ai-moderation/hooks/use-model-version-detail.ts`
- `src/features/ai-moderation/hooks/use-blocked-topics-registry.ts`
- `src/features/ai-moderation/components/coarse-taxonomy-notice.tsx`
- `src/app/(dashboard)/intelligence/false-positive-log/page.tsx`
- `src/app/(dashboard)/intelligence/model-versions/page.tsx`
- `src/app/(dashboard)/intelligence/model-versions/[version]/page.tsx`
- `src/app/(dashboard)/intelligence/blocked-topics/page.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` → add:
```ts
AI_MODEL_VERSIONS: {
  BASE: "/v1/admin/ai-model-versions",
  DETAIL: (v: string) => `/v1/admin/ai-model-versions/${v}`,
},
AI_BLOCKED_TOPICS: { BASE: "/v1/admin/ai-blocked-topics" },
```

## 10. Backend Requirements
Consumes:
- `GET /v1/admin/ai-moderation?status=resolved&resolution_action=mark_false_positive` (B-01, amended) for the False-Positive Feedback Log
- `GET /v1/admin/ai-model-versions` / `GET /v1/admin/ai-model-versions/{version}` (B-07) for the Model Version Registry/Detail
- `GET /v1/admin/ai-blocked-topics` (B-07) for the Blocked Topics Registry

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements

### 12.1 False-Positive Feedback Log — reuses N-01's client, no new one
```ts
// src/features/ai-moderation/hooks/use-false-positive-log.ts
import { useQuery } from "@tanstack/react-query";
import { aiModerationResourceClient } from "../api/ai-moderation-resource-client";

export function useFalsePositiveLog() {
  return useQuery({
    queryKey: ["ai-moderation", "false-positive-log"],
    queryFn: ({ signal }) =>
      aiModerationResourceClient.getQueue({ status: "resolved", resolutionAction: "mark_false_positive" }, signal),
  });
}
```
> `getQueue()`'s filter type/param serialization (N-01 §12.2) must be extended to accept `resolutionAction` alongside `status`/`policyCategory` — this is a small addition to N-01's existing client, not a new client class.

### 12.2 Model Version Schemas & Client
```ts
export const modelVersionSummarySchema = z.object({
  modelVersion: z.string(),
  flaggedInteractionCount: z.number(),
  lastSeenAt: z.string(),
});
export const modelVersionDetailSchema = modelVersionSummarySchema.extend({
  evaluationRuns: z.array(
    z.object({
      runId: z.string(),
      criticalFindingsCount: z.number(),
      nonCriticalFindingsCount: z.number(),
      runAt: z.string(),
    })
  ),
});

export class ModelVersionResourceClient {
  async list(signal?: AbortSignal) {
    const { data } = await apiClient.get<unknown>(API_ENDPOINTS.AI_MODEL_VERSIONS.BASE, { signal });
    return z.array(modelVersionSummarySchema).parse(data);
  }
  async getDetail(version: string, signal?: AbortSignal) {
    const { data } = await apiClient.get<unknown>(API_ENDPOINTS.AI_MODEL_VERSIONS.DETAIL(version), { signal });
    return modelVersionDetailSchema.parse(data);
  }
}
```

### 12.3 Blocked Topics Registry — with the Coarse-Taxonomy Notice (signature component)
```tsx
// src/features/ai-moderation/components/coarse-taxonomy-notice.tsx
"use client";
export function CoarseTaxonomyNotice() {
  return (
    <p role="note" className="text-sm text-neutral-600">
      This registry reflects the platform's current enforcement categories (blocked, redirected, approved) — it is
      not a fine-grained list of individual blocked keywords or phrases.
    </p>
  );
}
```
This notice is rendered unconditionally at the top of the Blocked Topics Registry page — it is not an error/empty state, it is a permanent, honest scope statement, per B-07 §10.3's documented limitation.

### 12.4 Model Version Detail — Interaction Stats + Evaluation History
Combines `flaggedInteractionCount`/`lastSeenAt` with the `evaluationRuns` list (reusing N-05's `FindingsBreakdown` component for each run row, rather than re-implementing critical/non-critical rendering here).

## 13. API Contract
Consumes B-01's amended endpoint (§13 of that blueprint) and B-07's three endpoints (§13 of that blueprint) exactly.

## 14. Database Requirements
Not applicable.

## 15. Validation
Not applicable (read-only).

## 16. Authentication
Standard session flow.

## 17. Authorization
`RequirePermission permission="ai-moderation:read"` gates all four screens, consistent with the rest of the console — no elevated permission needed, since this is aggregated metadata, never transcript content.

## 18. Error Handling
Standard `ErrorView`/retry via `DataTable`/query hooks; `404` on an unknown `{version}` in the detail route renders a clear "no data recorded for this model version" state, distinct from a generic error.

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
All labels, the coarse-taxonomy notice, and the not-found message via `useTranslation()`.

## 22. RTL
All four screens' table/notice layouts verified under `dir="rtl"`.

## 23. Analytics
No dedicated events specified in §1.19 for these screens; the False-Positive Log reuses `ai_moderation_queue_viewed`'s tracking pattern since it is, mechanically, a filtered queue view.

## 24. Performance
Read-only, low-traffic operator screens; standard `DataTable` pagination if any list grows large.

## 25. Security
No new security surface — read-only, behind the existing `ai-moderation:read` scope, sourced entirely from already-redacted aggregate data.

## 26. Library Requirements
Next.js 15, TypeScript, TanStack Query v5, Zod — no new dependencies.

## 27. Testing
- Unit: False-Positive Log renders correctly, reusing `AiModerationResourceClient.getQueue()` with the new filter param.
- Unit: Model Version Registry and Detail render correctly against B-07's schemas.
- Unit: `CoarseTaxonomyNotice` always renders on the Blocked Topics Registry page (not conditionally).
- Unit: unknown `{version}` detail route renders the not-found state, not a generic error.
- Integration: full model-version list → detail → evaluation-run-history flow.

## 28. Documentation
JSDoc on `CoarseTaxonomyNotice` explaining why it exists (mirrors B-07's own documented limitation) so it isn't mistakenly removed as "just a caption" in a future edit.

## 29. AI Coding Agent Implementation Steps
- **Task 01 — API endpoint constants**: `AI_MODEL_VERSIONS`, `AI_BLOCKED_TOPICS`.
- **Task 02 — Extend `AiModerationResourceClient.getQueue()`** (N-01) to accept `resolutionAction`.
- **Task 03 — `useFalsePositiveLog()` hook**.
- **Task 04 — Model Version schemas + `ModelVersionResourceClient`**.
- **Task 05 — `useModelVersionRegistry()`, `useModelVersionDetail()`, `useBlockedTopicsRegistry()` hooks**.
- **Task 06 — `CoarseTaxonomyNotice` component**.
- **Task 07 — Four pages**: false-positive log, model-version list, model-version detail, blocked-topics registry.
- **Task 08 — Tests** per §27.
- **Task 09 — Documentation**.
- **Task 10 — Final Code Review**: confirm the False-Positive Log did not spawn a duplicate API client, and the coarse-taxonomy notice renders unconditionally.

## 30. Definition of Done
All four registry screens implemented against B-01's amended endpoint and B-07's three real endpoints; coarse-taxonomy limitation honestly surfaced in the UI, not hidden.

## 31. Final Verification Checklist
- [ ] False-Positive Feedback Log reuses N-01's client with the new `resolutionAction` filter — no duplicate client
- [ ] Model Version Registry and Detail render against B-07's real endpoints
- [ ] Blocked Topics Registry renders `CoarseTaxonomyNotice` unconditionally
- [ ] Unknown `{version}` detail route shows a clear not-found state
- [ ] `RequirePermission` gates all four screens
- [ ] RTL layout verified
- [ ] Tests green in CI
