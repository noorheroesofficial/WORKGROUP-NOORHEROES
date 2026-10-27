# N-02 — Offline Sync Integrity Monitoring Dashboard

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). Read-only dashboard giving `product_admin`/`trust_safety` visibility into the Offline Sync Engine's integrity signals — sync-batch volume, the (positively-framed) duplicate-prevention rate, and rejected-event breakdown by domain/event-type.

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
N-02 — Offline Sync Integrity Monitoring Dashboard

## 4. Objective
Build a read-only dashboard showing sync-batch volume over time, the duplicate-prevention rate framed as a positive integrity signal, and a rejected-event breakdown table by `event_type`, restricted to `product_admin`/`trust_safety`.

## 5. Business Requirements
- §8 Admin Requirements: Offline Sync Integrity Monitor (read-only) — sync-batch volume, duplicate-prevention rate (a positive signal), rejected-event rate by domain/event-type.
- §11.1: `offline_sync_duplicate_prevented` is a positive integrity-health signal, not a warning.
- DevOps §10: any production-detected duplicate event that should have been caught by dedup is P0 — this dashboard is where that would first become visible to staff as an anomaly (a duplicate showing up as `applied` twice would be the red flag, not the `duplicate`-status count itself).

## 6. Existing Architecture
New page under `src/features/downloads/`, sibling to N-01, reusing the same `recharts`-based dashboard pattern and `DataTable` convention.

## 7. Existing Code to Reuse
- `DataTable`, `LoadingState`, `EmptyState`, `ErrorView`/`QueryErrorState`, `RequirePermission`, `DashboardShell`.
- N-01's `downloads-monitoring-repository.ts` extended with a sibling sync-health method, keeping the `downloads` feature module's API layer cohesive rather than duplicating a repository.
- Existing `recharts` conventions.

## 8. Files to Create
- `src/features/downloads/hooks/use-offline-sync-health.ts`.
- `src/features/downloads/types/sync-health.types.ts` (Zod schema matching B-07 §13's sync-health response).
- `src/features/downloads/components/sync-batch-volume-chart.tsx`.
- `src/features/downloads/components/duplicate-prevention-rate-card.tsx`.
- `src/features/downloads/components/rejected-events-by-type-table.tsx`.
- `src/app/(dashboard)/downloads/sync-health/page.tsx`.
- `src/features/downloads/__tests__/use-offline-sync-health.test.ts`.

## 9. Files to Modify
- `src/features/downloads/api/downloads-monitoring-repository.ts` (N-01) — extend with `getSyncHealth(window)`.
- Sidebar navigation config — add "Offline Sync Integrity" entry under the Downloads section.

## 10. Backend Requirements
Consumes B-07: `GET /v1/admin/sync/health?window=`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- `useOfflineSyncHealth(window)` React Query hook calling `GET /v1/admin/sync/health`.
- `SyncBatchVolumeChart` (recharts) plotting `batches_processed`/`events_applied` over time.
- `DuplicatePreventionRateCard` — a prominent, positively-framed stat card (e.g., "1,245 duplicate submissions correctly caught this week"), not styled as a warning/error metric.
- `RejectedEventsByTypeTable` (`DataTable`) listing `event_type`, `count`, with sortable columns — a non-zero rejection rate for a given `event_type` is a signal for engineering follow-up, surfaced neutrally (not alarmingly) since low-volume rejection is expected/normal per the feature's own error-handling design.
- Window selector matching N-01's convention.
- RBAC: `product_admin`/`trust_safety` only.

## 13. API Contract
`GET /v1/admin/sync/health?window=72h` → `{ series: [{ bucket, batches_processed, events_applied, events_duplicate_prevented, events_rejected }], rejected_by_event_type: [{ event_type, count }] }` per B-07 §13.

## 14. Database Requirements
N/A (frontend consumes API only).

## 15. Validation
Window selector restricted to B-07's allow-listed values.

## 16. Authentication
Standard admin session via `apiClient`.

## 17. Authorization
`RequirePermission` for `product_admin`/`trust_safety`.

## 18. Error Handling
Standard `QueryErrorState`/`EmptyState` conventions; zero sync activity in the window is a neutral empty state.

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Chart/table labels, positive-framing copy on the duplicate-prevention card, via `useTranslation`.

## 22. RTL
Standard RTL support; table column order and chart mirroring follow existing convention.

## 23. Analytics
No dedicated event beyond standard admin-page-view tracking; this page is itself a monitoring surface for B.15's own analytics taxonomy.

## 24. Performance
Query data bounded by the selected window; React Query caching; rejected-events table paginated/sortable via existing `DataTable` capability rather than rendering an unbounded list.

## 25. Security
Read-only; relies on B-07's backend RBAC. No per-child/per-family data surfaced — only aggregate counts and `event_type` breakdowns.

## 26. Library Requirements
Existing stack: Next.js, TanStack Query, recharts, Zod.

## 27. Testing
- Hook test: correct parsing of the sync-health response shape, including the `rejected_by_event_type` array.
- Component test: `DuplicatePreventionRateCard` renders the positive framing copy correctly, not a warning-style presentation.
- Component test: `RejectedEventsByTypeTable` sorts correctly by count.
- RBAC test: page hidden/blocked for a role without `product_admin`/`trust_safety`.

## 28. Documentation
TSDoc noting the duplicate-prevention metric is intentionally framed positively per §11.1, and why a non-zero rejection rate is expected/normal rather than alarming by default.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Define Types**
Files to create: `sync-health.types.ts`.

**Task 02 — Extend Repository & Implement Hook**
Files to modify: `downloads-monitoring-repository.ts`; files to create: `use-offline-sync-health.ts`.

**Task 03 — Build SyncBatchVolumeChart**
Files to create: `sync-batch-volume-chart.tsx`.

**Task 04 — Build DuplicatePreventionRateCard**
Files to create: `duplicate-prevention-rate-card.tsx`.

**Task 05 — Build RejectedEventsByTypeTable**
Files to create: `rejected-events-by-type-table.tsx`.

**Task 06 — Assemble Page & Wire RBAC + Navigation**
Files to create: `page.tsx`; files to modify: sidebar config.

**Task 07 — Add Tests**

**Task 08 — Final Review**

## 30. Definition of Done
- Dashboard live, RBAC-gated, showing accurate batch-volume chart, positively-framed duplicate-prevention metric, and sortable rejected-events table.

## 31. Final Verification Checklist
- [ ] Charts/table render correctly from live B-07 data.
- [ ] Duplicate-prevention metric uses positive framing, not warning styling.
- [ ] Rejected-events table sortable and correctly broken down by `event_type`.
- [ ] RBAC restricts access to `product_admin`/`trust_safety`.
- [ ] No per-child/per-family identifying data surfaced.
- [ ] Localization and RTL verified.
