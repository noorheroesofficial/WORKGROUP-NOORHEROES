# N-01 — AI Moderation Queue Dashboard

## 1. Feature Context
Parent PRD: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
Backend Dependency: B-01 (`GET /v1/admin/ai-moderation`)

## 2. Parent Feature
E.30 — AI Moderation Console & Safety Evaluation Harness

## 3. Sub-feature
**AI Moderation Queue Dashboard** (ID: N-01) — the landing screen (Screen 1) under the Admin Portal's "Review"/"Intelligence" navigation groups: a dense, filterable list of flagged AI interactions, following the exact same pattern as E.29's review queues.

## 4. Objective
Give a `child_safety_reviewer` a fast, filterable, permission-gated view of everything currently flagged, with zero new UI primitives — entirely built from existing shared components.

## 5. Business Requirements
- §1.18 Screen 1: AI Moderation Queue — Primary screen, entry from "Review"/"Intelligence" nav, exits to AI Moderation Detail.
- §1.12: zero items in queue → calm "Nothing flagged right now" state.
- §1.13: standard Admin Portal skeleton-loading pattern, consistent with E.28/E.29.
- §2.4: follows the same dense filterable-list pattern as E.29's review queues.

## 6. Existing Architecture
`Page/Component → Hook (React Query) → Repository → apiClient → B-01`, per NEXT-JS-INSTRUCTIONS.md §2's layered architecture. New feature module `src/features/ai-moderation/`, structured identically to `src/features/scholar-review/`.

## 7. Existing Code to Reuse
- `DataTable` (`shared/components/data-table.tsx`) — pagination, loading/error/empty states already handled
- `RequirePermission` (`shared/components/require-permission.tsx`)
- `BaseResourceClient` (`shared/api/base-resource-client.ts`) for the `list()` method
- `useDebouncedValue`, `usePaginationState` (`shared/hooks/`)
- `useAdminSession`/`hasPermission` (`features/auth/hooks/use-admin-session.ts`)

## 8. Files to Create
- `src/features/ai-moderation/api/ai-moderation-resource-client.ts`
- `src/features/ai-moderation/api/ai-moderation-schemas.ts`
- `src/features/ai-moderation/hooks/use-ai-moderation-queue.ts`
- `src/features/ai-moderation/components/queue-filter-bar.tsx`
- `src/app/(dashboard)/review/ai-moderation/page.tsx`
- `src/features/ai-moderation/__tests__/queue-dashboard-permission.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` → add `AI_MODERATION: { BASE: "/v1/admin/ai-moderation", DETAIL: (id) => \`/v1/admin/ai-moderation/${id}\` }`

## 10. Backend Requirements
Consumes B-01: `GET /v1/admin/ai-moderation?status=&policy_category=`.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements

### 12.1 Schemas
```ts
// src/features/ai-moderation/api/ai-moderation-schemas.ts
import { z } from "zod";

export const aiModerationQueueItemSchema = z.object({
  queueItemId: z.string(),
  stageFlagged: z.string(),
  status: z.enum(["pending", "resolved"]),
  policyCategory: z.string(),
  flaggedAt: z.string(),
});
export type AiModerationQueueItem = z.infer<typeof aiModerationQueueItemSchema>;
```

### 12.2 Repository
```ts
// src/features/ai-moderation/api/ai-moderation-resource-client.ts
import { apiClient } from "@/lib/api-client";
import { API_ENDPOINTS } from "@/shared/constants/api-endpoints";
import { z } from "zod";
import { aiModerationQueueItemSchema } from "./ai-moderation-schemas";

export class AiModerationResourceClient {
  async getQueue(filters: { status?: string; policyCategory?: string }, signal?: AbortSignal) {
    const params = new URLSearchParams();
    if (filters.status) params.set("status", filters.status);
    if (filters.policyCategory) params.set("policy_category", filters.policyCategory);
    const { data } = await apiClient.get<unknown>(`${API_ENDPOINTS.AI_MODERATION.BASE}?${params}`, { signal });
    return z.array(aiModerationQueueItemSchema).parse(data);
  }
}
export const aiModerationResourceClient = new AiModerationResourceClient();
```

### 12.3 Page
```tsx
// src/app/(dashboard)/review/ai-moderation/page.tsx
"use client";
import { RequirePermission } from "@/shared/components/require-permission";
import { DataTable } from "@/shared/components/data-table";
import { useAiModerationQueue } from "@/features/ai-moderation/hooks/use-ai-moderation-queue";
import { usePaginationState } from "@/shared/hooks/use-pagination-state";

export default function AiModerationQueuePage() {
  const { page, pageSize, setPage, setPageSize } = usePaginationState(1, 20);
  const { data, isLoading, error, refetch } = useAiModerationQueue({ page, pageSize });

  return (
    <RequirePermission permission="ai-moderation:read">
      <DataTable
        columns={[
          { header: "Policy Category", accessorKey: "policyCategory" },
          { header: "Stage Flagged", accessorKey: "stageFlagged" },
          { header: "Status", accessorKey: "status" },
          { header: "Flagged At", accessorKey: "flaggedAt" },
        ]}
        data={data?.items ?? []}
        isLoading={isLoading}
        error={error}
        onRetry={refetch}
        page={page}
        pageSize={pageSize}
        totalItems={data?.total}
        onPageChange={setPage}
        onPageSizeChange={setPageSize}
        onRowClick={(row) => { /* navigate to /review/ai-moderation/[id] */ }}
      />
    </RequirePermission>
  );
}
```

## 13. API Contract
Consumes B-01 exactly as specified in that blueprint's §13.

## 14. Database Requirements
Not applicable.

## 15. Validation
Filter values (`status`, `policyCategory`) validated client-side against known enums before being sent, mirroring the server's own validation as a UX nicety (not a security boundary).

## 16. Authentication
Standard session flow.

## 17. Authorization
`<RequirePermission permission="ai-moderation:read">` wraps the whole page — server-side `403` remains the actual boundary (NEXT-JS-INSTRUCTIONS.md §12: "never rely solely on client UI hiding for authorization").

## 18. Error Handling
`DataTable`'s built-in `ErrorView`/`onRetry` handles fetch failures; no bespoke error UI needed for this screen.

## 19. Offline First
Not applicable (§1.14).

## 20. Local Data
Not applicable.

## 21. Localization
All column headers, filter labels, and the empty-state copy via `useTranslation()`.

## 22. RTL
Table and filter-bar layout mirror correctly under `dir="rtl"` — reuse `DataTable`'s existing RTL-safe layout, no custom CSS needed.

## 23. Analytics
Fire `ai_moderation_queue_viewed` on successful queue fetch (mount + refetch), per §1.19.

## 24. Performance
`useAiModerationQueue` should use React Query with a short `staleTime` (queue changes frequently) and `refetchOnWindowFocus` enabled, consistent with other operator-facing queue screens.

## 25. Security
No new security surface — purely a read view behind `ai-moderation:read`, with the actual redaction guarantee owned entirely by B-01's backend contract.

## 26. Library Requirements
Next.js 15, TypeScript, TanStack Query v5, Zod — no new dependencies.

## 27. Testing
- Unit: queue renders correctly for a `child_safety_reviewer` fixture.
- Unit: page content is gated by `RequirePermission` for a fixture admin lacking `ai-moderation:read`.
- Unit: empty-queue state renders "Nothing flagged right now" copy.
- Integration: filter by `status`/`policyCategory` triggers a re-fetch with correct query params.

## 28. Documentation
JSDoc on `AiModerationResourceClient` noting it is the sole client entry point for B-01's queue/detail endpoints.

## 29. AI Coding Agent Implementation Steps
- **Task 01 — API endpoints constant**: add `AI_MODERATION` to `api-endpoints.ts`.
- **Task 02 — Schemas**: `ai-moderation-schemas.ts`.
- **Task 03 — Repository**: `AiModerationResourceClient.getQueue()`.
- **Task 04 — Hook**: `useAiModerationQueue()` (React Query wrapper).
- **Task 05 — Queue Filter Bar component**.
- **Task 06 — Page**: `/review/ai-moderation` route using `DataTable`.
- **Task 07 — Tests**: permission-gating and empty-state tests.
- **Task 08 — Documentation**.
- **Task 09 — Final Code Review**: confirm zero bespoke table/pagination code was written where `DataTable` already covers the requirement.

## 30. Definition of Done
Queue dashboard renders, filters, paginates, and is permission-gated, entirely via reused shared components; empty/loading/error states verified.

## 31. Final Verification Checklist
- [ ] Route `/review/ai-moderation` renders the queue via `DataTable`
- [ ] Filters by `status` and `policyCategory` work correctly
- [ ] Empty state shows "Nothing flagged right now"
- [ ] `RequirePermission` gates the page for `ai-moderation:read`
- [ ] `ai_moderation_queue_viewed` fires on load
- [ ] RTL layout verified
- [ ] Tests green in CI
