# N-04 — Voice Search Quality Monitor

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). Read-only dashboard tracking voice-search transcription confidence distribution and clarification-needed rate — an AI/model-quality signal for the AI-ops team, structurally incapable of exposing any transcript or per-child data.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
N-04 — Voice Search Quality Monitor

## 4. Objective
Build a read-only dashboard showing transcription confidence-score distribution and clarification-needed-rate trend over time, restricted to `ai_ops`/`product_admin` roles.

## 5. Business Requirements
- Admin Requirements §8: Voice Search Confidence/Quality Monitor (read-only), aggregate tracking of transcription confidence distribution and clarification-needed rate.
- RBAC: read-only behind `ai_ops`/`product_admin`.
- Underpinned by B-07's structurally PII-free `voice_search_confidence_log` (no transcript, no `child_id` column) — this page can only ever display what that table structurally allows, which is confidence scores and a boolean flag, nothing else.

## 6. Existing Architecture
New page under `src/features/search/`, same repository/hook/chart pattern as N-02.

## 7. Existing Code to Reuse
- `LoadingState`, `EmptyState`, `ErrorView`, `RequirePermission`.
- Existing `recharts` conventions (histogram/distribution chart + trend line).
- `search-monitoring-repository.ts` extended with a voice-quality method.

## 8. Files to Create
- `src/features/search/hooks/use-voice-quality.ts`.
- `src/features/search/types/voice-quality.types.ts` (Zod schema matching B-07 §13's voice-quality response).
- `src/features/search/components/confidence-distribution-chart.tsx`.
- `src/features/search/components/clarification-rate-trend-chart.tsx`.
- `src/app/(dashboard)/search/voice-quality/page.tsx`.
- `src/features/search/__tests__/use-voice-quality.test.ts`.

## 9. Files to Modify
- `search-monitoring-repository.ts` — add `getVoiceQuality()` method.
- Sidebar navigation config — add "Voice Search Quality" entry.

## 10. Backend Requirements
Consumes B-07: `GET /admin/v1/search/voice-quality`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- `useVoiceQuality()` React Query hook.
- `ConfidenceDistributionChart` (histogram/bucketed bar chart) of confidence-score buckets.
- `ClarificationRateTrendChart` (line/area chart) of clarification-needed rate over time.
- RBAC: `ai_ops`/`product_admin` only.
- No table/row-level display of individual voice-search events anywhere on this page — only the two aggregate charts, matching what the backend's PII-free schema structurally permits.

## 13. API Contract
`GET /admin/v1/search/voice-quality` → `{ confidence_buckets: [...], clarification_rate_trend: [...] }` per B-07 §13.

## 14. Database Requirements
N/A (frontend consumes API only).

## 15. Validation
N/A (read-only display).

## 16. Authentication
Standard admin session via `apiClient`.

## 17. Authorization
`RequirePermission` for `ai_ops`/`product_admin`.

## 18. Error Handling
Standard `QueryErrorState`/`EmptyState` conventions.

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Chart labels/axis text via `useTranslation`.

## 22. RTL
Standard RTL support via existing chart/layout conventions.

## 23. Analytics
No dedicated event beyond standard admin-page-view tracking, if present.

## 24. Performance
Chart data bounded to a reasonable trailing window (e.g., last 30–90 days); React Query caching.

## 25. Security
This page's entire security posture rests on B-07's `voice_search_confidence_log` table being structurally incapable of holding transcript/child-id data — the frontend adds a second layer of assurance by simply never rendering an individual-event view, only the two aggregate charts.

## 26. Library Requirements
Existing stack only.

## 27. Testing
- Hook test: correct parsing of the voice-quality response shape.
- Component test: charts render from fixture aggregate data.
- RBAC test: page hidden/blocked for a role without `ai_ops`/`product_admin`.

## 28. Documentation
TSDoc noting this page must never be extended with an individual-voice-event drill-down, consistent with B-07's PII-free-by-design backend schema.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Define Types**
Files to create: `voice-quality.types.ts`.

**Task 02 — Extend Repository & Add Hook**
Files to modify: `search-monitoring-repository.ts`; files to create: `use-voice-quality.ts`.

**Task 03 — Build ConfidenceDistributionChart & ClarificationRateTrendChart**
Files to create: two chart components.

**Task 04 — Assemble Page & Wire RBAC + Navigation**
Files to create: `page.tsx`; files to modify: sidebar config.

**Task 05 — Add Tests**

**Task 06 — Final Review**
Objective: confirm no individual-event/per-child display exists anywhere on this page — aggregate charts only.

## 30. Definition of Done
- Dashboard live, RBAC-gated, showing accurate confidence distribution and clarification-rate trend from B-07 data.

## 31. Final Verification Checklist
- [ ] Only aggregate charts rendered — no individual voice-event or per-child display anywhere.
- [ ] RBAC restricts access to `ai_ops`/`product_admin`.
- [ ] Charts correctly reflect live B-07 data.
- [ ] Localization and RTL verified.
- [ ] Empty state distinct from error state.
