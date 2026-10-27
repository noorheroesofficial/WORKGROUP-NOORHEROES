# N-02 — Skill-Mapping Compliance Dashboard

## 1. Feature Context
Part of **A.10 Games Module**. Covers the read-only dashboard surfacing every published game's compliance status (Compliant/At Risk), giving editorial an early-warning window before B-05's reconciliation job auto-withdraws an orphaned game (PRD §8, §9 item 2).

## 2. Parent Feature
A.10 Games Module — NextJS Admin

## 3. Sub-feature
**3.2 Skill-Mapping Compliance Dashboard** `[N-02]`

## 4. Objective
Render a read-only, paginated table of all published games with a status column (Compliant/At Risk), sourced from `GET /admin/v1/games/compliance` (B-06), with At Risk entries linking directly to N-01's editor for re-linking or acknowledgment (PRD §9 item 2).

## 5. Business Requirements
- §8: standing compliance view supporting the 100% zero-filler-content audit pass rate success metric (§1.4).
- §9 item 2: At Risk = any linked skill_node has `is_active=false`; links directly to the game's editor.
- §11.3 Dashboard Metrics: skill-mapping-compliance rate should be a flat 100% line — any dip is itself the alert.

## 6. Existing Architecture
Same `src/features/games-catalog/` module extended with a compliance sub-feature, or a sibling `src/features/games-compliance/` module — following the existing pattern of dedicated feature directories per PRD/architecture domain (mirrors how `dashboard` stats have their own `DashboardRepositoryImpl`/`useDashboardStats` separate from entity CRUD repositories).

## 7. Existing Code to Reuse
- `DataTable`, `StatusBadge` (`src/shared/components/`) — `StatusBadge` reused directly for the Compliant/At Risk pill (existing "visual status pill component" per `NEXT-JS-INSTRUCTIONS.md` §3).
- `usePaginationState`, `FilterPanel`, `SearchBar`.
- `RequirePermission` — read-only access, likely a broader `games:read` permission than the editor's `games:write`.
- `BaseResourceClient.list()` pattern for the compliance listing (read-only resource, no create/update/delete methods needed — a thin repository wrapping just `list()`).

## 8. Files to Create
```
src/features/games-catalog/api/games-compliance-client.ts
src/features/games-catalog/api/games-compliance-schema.ts
src/features/games-catalog/hooks/use-games-compliance.ts
src/features/games-catalog/components/games-compliance-table.tsx
src/app/(dashboard)/games-catalog/compliance/page.tsx
src/features/games-catalog/__tests__/games-compliance-table.test.tsx
```

## 9. Files to Modify
```
src/shared/constants/api-endpoints.ts       # API_ENDPOINTS.GAMES.COMPLIANCE
src/shared/components/dashboard-shell.tsx   # add Compliance Dashboard nav entry under Games Catalog
```
**Do Not Change:** N-01's editor internals — this dashboard only links out to them.

## 10. Backend Requirements
Consumes B-06's `GET /admin/v1/games/compliance` exactly as documented.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- `GamesComplianceTable`: columns = game title, skill_area, status (`StatusBadge` variant: green "Compliant" / amber "At Risk"), "View/Edit" action linking to `/games-catalog/{gameId}`.
- Pagination, search, and filter-by-status (Compliant/At Risk) using existing `DataTable`/`FilterPanel`/`SearchBar` conventions.
- Read-only — no mutation actions on this page itself, consistent with §8's "Skill-Mapping Compliance Dashboard = Read-only" permission spec.
- Loading/empty/error states via `LoadingState`/`EmptyState`/`QueryErrorState`.

## 13. API Contract
Consumes B-06 §13 `GET /admin/v1/games/compliance` exactly:
```json
{ "games": [ { "game_id": "uuid", "title": "string", "status": "Compliant" } ] }
```

## 14. Database Requirements
N/A (frontend only).

## 15. Validation
N/A — read-only display, no form input to validate beyond filter/search query params.

## 16. Authentication
Relies on existing session flow.

## 17. Authorization
`RequirePermission permission="games:read"` (broader than the editor's `games:write`) — any authenticated admin with read access can view compliance status, per §8's "Read-only" designation (no elevated role required beyond baseline admin access, unlike the audit log in N-04).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Compliance fetch failure | `QueryErrorState` with retry |
| Empty result (no published games yet) | `EmptyState` with friendly message |
| Insufficient permission | `RequirePermission` fallback |

## 19. Offline First
N/A.

## 20. Local Data
N/A (React Query cache only).

## 21. Localization
Status labels ("Compliant"/"At Risk") and column headers localized via `useTranslation()`.

## 22. RTL
Table and status badges render correctly for Arabic/Urdu admin locales.

## 23. Analytics
No dedicated client analytics events specified for this read-only admin view.

## 24. Performance
Single aggregated backend query (per B-06 §24) keeps this dashboard responsive at catalog scale; frontend pagination avoids rendering the full list at once.

## 25. Security
Read-only surface, no mutation risk; RBAC still enforced (§17) to prevent exposing compliance/governance detail to entirely unauthorized users, though the bar is lower than the audit log (N-04).

## 26. Library Requirements
Next.js 15, TanStack Query v5, Zod. No new dependencies.

## 27. Testing
- Unit: status computed/displayed correctly from `Compliant`/`At Risk` API values.
- Unit: "At Risk" row links to the correct game's editor URL.
- Integration: filter-by-status correctly narrows the table.
- Integration: empty-catalog state renders `EmptyState`, not an error.

## 28. Documentation
Note in code comments that this dashboard is explicitly an editorial early-warning system, distinct from (and running ahead of) B-05's automated reconciliation job — a game shown "At Risk" here has not yet been auto-withdrawn.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Compliance Zod Schema**
- Objective: `gamesComplianceSchema` matching B-06 §13 response shape.

**Task 02 — Implement GamesComplianceClient**
- Objective: Thin read-only client wrapping `GET /admin/v1/games/compliance`.
- Existing Files to Reuse: `apiClient.get()`.

**Task 03 — Implement useGamesCompliance Hook**
- Objective: React Query hook following `useUsers`/`useFamilyList` conventions.

**Task 04 — Build GamesComplianceTable**
- Objective: `DataTable` + `StatusBadge` per §12.
- Definition of Done: At Risk rows link correctly to N-01's editor.

**Task 05 — Register Route & Navigation**
- Objective: `src/app/(dashboard)/games-catalog/compliance/page.tsx`, nav entry under Games Catalog.

**Task 06 — Wire RequirePermission**
- Objective: `games:read` gate.

**Task 07 — Add Tests**
- Objective: Full suite per §27.

**Task 08 — Add Documentation**
- Objective: Editorial-early-warning-vs-automated-reconciliation distinction documented.

**Task 09 — Final Code Review**
- Objective: Confirm read-only nature strictly preserved (no accidental mutation actions added to this page).
- Definition of Done: review checklist (§31) fully checked.

## 30. Definition of Done
- Compliance dashboard correctly displays Compliant/At Risk status for all published games.
- At Risk rows link directly to the correct game's editor.
- Read-only nature preserved throughout (no mutation actions present).
- Pagination/search/filter functioning per existing conventions.

## 31. Final Verification Checklist
- [ ] Status column correctly reflects backend Compliant/At Risk values
- [ ] At Risk row links resolve to the correct game editor URL
- [ ] Filter-by-status functioning correctly
- [ ] Empty-catalog state renders `EmptyState`, not an error
- [ ] `RequirePermission` (`games:read`) correctly gates the page
- [ ] Localization/RTL verified
- [ ] No mutation actions present on this read-only page
- [ ] No files outside declared scope modified

---

## 32. Cross-Platform Dependencies
- Backend Dependency: B-06 (`GET /admin/v1/games/compliance`).
- KMP Dependency: None.
- Admin Dependency: N-01 (At Risk rows link directly into the editor).
- Database Dependency: None (frontend only).
- External Service Dependency: None.
- Figma Dependency: Skill-Mapping Compliance Dashboard screen — Figma Required.
