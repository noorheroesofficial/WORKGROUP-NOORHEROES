# N-01 — Ramadan Campaign Manager

## 1. Feature Context
The admin surface for configuring `ramadan_campaigns` per region ahead of each season, plus the `super_admin`-restricted Eid-date-override action for moon-sighting disputes — the single admin screen with the platform-wide blast radius of an incorrect entry, since every family's activation window derives from this data.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
3.1 Ramadan Campaign Manager (ID: **N-01**)

## 4. Objective
Build the Campaign Manager page: list/CRUD `ramadan_campaigns` per region, plus a `super_admin`-only "Override Eid Date" action calling B-08.

## 5. Business Requirements
- §8: Ramadan Campaign Manager — configure `ramadan_campaigns` per region, trigger Eid-date-override on dispute.
- §8 CRUD permissions: Campaign Manager = full CRUD behind `content_editor`/`super_admin` (Eid-date-override restricted to `super_admin`).
- §9 Admin AI prompt item 1: CRUD for `ramadan_campaigns` per region, with an "Override Eid Date" action restricted to `super_admin`.

## 6. Existing Architecture
Next.js 15 App Router feature module `src/features/ramadan/campaign-manager/`, following the platform's standard layering: Page → Feature Hook (React Query) → Repository (`BaseResourceClient` subclass) → `apiClient` → Backend REST API, per `NEXT-JS-INSTRUCTIONS.md` §2.

## 7. Existing Code to Reuse
- `BaseResourceClient<Entity, Create, Update, Filters>` (extend for `CampaignResourceClient`)
- `DataTable`, `ConfirmationDialog`, `RequirePermission`, `FilterPanel`, `LoadingState`, `ErrorView`, `EmptyState`, `QueryErrorState` shared components
- `useElevatedSession` (2FA step-up hook, for the Override action)
- `useTranslation`, `useFormatters`

## 8. Files to Create
- `src/app/(dashboard)/ramadan/campaigns/page.tsx`
- `src/features/ramadan/campaign-manager/api/campaign-resource-client.ts`
- `src/features/ramadan/campaign-manager/hooks/use-campaigns.ts`
- `src/features/ramadan/campaign-manager/hooks/use-override-eid-date.ts`
- `src/features/ramadan/campaign-manager/components/campaign-table.tsx`
- `src/features/ramadan/campaign-manager/components/campaign-form.tsx`
- `src/features/ramadan/campaign-manager/components/override-eid-date-dialog.tsx`
- `src/features/ramadan/campaign-manager/types/campaign.ts`

## 9. Files to Modify
- `src/shared/components/dashboard-shell.tsx` — add "Ramadan" nav section/entry, `RequirePermission`-gated

## 10. NextJS Requirements
- **Page/Route:** `/ramadan/campaigns`, session-gated per `getDashboardSession()`.
- **Component:** `CampaignTable` (DataTable-based list per region), `CampaignForm` (create/update `hijri_start_date`/`eid_date` per region), `OverrideEidDateDialog` (ConfirmationDialog-based, `super_admin`-gated).
- **API Client/Type Definition:** `CampaignResourceClient extends BaseResourceClient<Campaign, CampaignCreate, CampaignUpdate, CampaignFilters>`; Zod schemas for runtime response validation.
- **Form/Validation:** date-field sanity-bound validation mirroring B-08's server-side rule (Zod schema shared/duplicated validation logic, server remains authority).
- **Authentication/Authorization/Permissions:** `RequirePermission permission="ramadan_campaigns:write"` for general CRUD (`content_editor`/`super_admin`); a second, stricter `RequirePermission permission="ramadan_campaigns:override"` (or equivalent `super_admin`-only check) wrapping only the Override action.
- **Loading/Empty/Error State:** `LoadingState` during fetch, `EmptyState` for a region with no configured campaign yet, `QueryErrorState` for fetch failures.
- **Pagination/Filtering/Sorting:** `usePaginationState` + `FilterPanel` filtering by region.
- **Responsive UI/Accessibility:** `DataTable`'s existing responsive/accessible patterns; `ConfirmationDialog` for the high-impact Override action, given its broad regional effect.

## 11. API Contract
### Proposed Campaign CRUD (pending confirmation — see B-01 §11)
Matches the proposal now added to B-01's blueprint. **Mark PROPOSED in code review until a real contract is signed off.**
- `GET /v1/admin/ramadan/campaigns` → `200 { items: [{ campaign_id, region, hijri_start_date, eid_date, eid_date_overridden }], page, page_size, total }`. Paginated.
- `POST /v1/admin/ramadan/campaigns` `{ region, hijri_start_date, eid_date }` → `201`. `409` on `UNIQUE(region, year)` conflict.
- `PATCH /v1/admin/ramadan/campaigns/{campaign_id}` `{ hijri_start_date?, eid_date? }` → `200`. Does **not** accept `eid_date_overridden` — that field is only ever set through the Override action below.

`POST /v1/admin/ramadan/eid-date-override` `{region, corrected_eid_date, source_note}` → `200` (B-08, confirmed contract).

## 12. Database Requirements
N/A directly (admin client) — reads/writes `ramadan_campaigns` via the backend API only, never direct DB access.

## 13. Validation
Zod schema for the campaign form mirroring B-08's sanity-bound date validation; `region` required, selected from a controlled list (reuse `CountrySelector`/region-list pattern if regions map to countries, per `NEXT-JS-INSTRUCTIONS.md`'s `CountrySelector` component).

## 14. Authentication
Standard Admin Portal session (`getDashboardSession()`), Bearer token via `apiClient`.

## 15. Authorization
`RequirePermission` at two levels: general CRUD (`content_editor`/`super_admin`), Override action (`super_admin` only) — enforced client-side for UX, with the server (B-08) as the actual authority.

## 16. Error Handling
`QueryErrorState` for list-fetch failures; form-level error display for create/update failures; `403` from the Override endpoint surfaced as a clear "insufficient permission" message, not a generic error.

## 17. Localization
All labels, form fields, and dialog copy via `useTranslation()` — zero hardcoded strings, per the Admin Portal's backend-driven localization principle.

## 18. RTL
Table/form/dialog layouts direction-aware via the Admin Portal's existing RTL support.

## 19. Analytics
N/A explicitly enumerated for admin actions in §1.19 (which lists child/parent-app events) — if the platform's Admin Portal has its own action-audit analytics, wire consistent with that existing pattern rather than inventing a new one.

## 20. Performance
Small dataset (one row per region) — standard `DataTable` pagination is sufficient, no special virtualization needed.

## 21. Caching
React Query default caching/staleness for the campaign list; explicit cache invalidation on successful create/update/override mutations.

## 22. Testing
Component tests: `CampaignForm` validation logic; `OverrideEidDateDialog` permission-gating (renders/hides correctly per role). Integration tests: **mandatory** — a `content_editor`-scoped session cannot trigger the Override action (mirrors B-08's server-side mandatory test); successful override refetches and displays the corrected date.

## 23. Documentation
Inline JSDoc on `CampaignResourceClient` noting the §11 CRUD contract is PROPOSED pending real sign-off against the backend team, mirroring B-01's equivalent note.

## 24. AI Coding Agent Implementation Steps

**Task 01 — Implement Against the Proposed Campaign CRUD Contract**
Objective: Build to §11's proposed shape (matches B-01's proposal exactly); flag for a joint frontend/backend contract review before production release rather than blocking implementation on it. Definition of Done: contract cross-referenced against B-01's blueprint for consistency; review flagged in the PR description.

**Task 02 — Define Types and Zod Schemas**
Objective: `Campaign`, `CampaignCreate`, `CampaignUpdate`, `CampaignFilters`. Files to Create: `types/campaign.ts`. Definition of Done: types compile, Zod schemas validate sample payloads.

**Task 03 — Implement `CampaignResourceClient`**
Objective: Extend `BaseResourceClient` for CRUD (once Task 01 resolves) plus a dedicated override method. Files to Create: `api/campaign-resource-client.ts`. Dependencies: Task 01, Task 02. Tests: repository unit tests with mocked `apiClient`. Definition of Done: tests pass.

**Task 04 — Implement `useCampaigns` and `useOverrideEidDate` Hooks**
Objective: React Query list/mutation hooks. Files to Create: `hooks/use-campaigns.ts`, `hooks/use-override-eid-date.ts`. Dependencies: Task 03. Tests: hook tests with mocked repository. Definition of Done: tests pass.

**Task 05 — Build `CampaignTable`**
Objective: `DataTable`-based region list with filtering. Files to Create: `components/campaign-table.tsx`. Dependencies: Task 04. Tests: rendering/pagination tests. Definition of Done: tests pass.

**Task 06 — Build `CampaignForm`**
Objective: Create/update form with sanity-bound date validation. Files to Create: `components/campaign-form.tsx`. Dependencies: Task 04. Tests: validation tests. Definition of Done: tests pass.

**Task 07 — Build `OverrideEidDateDialog` with `super_admin` Gating**
Objective: `ConfirmationDialog`-based override action, strictly `super_admin`-gated. Files to Create: `components/override-eid-date-dialog.tsx`. Dependencies: Task 04. Tests: **mandatory** — permission-gating test (`content_editor` cannot access). Definition of Done: test passes.

**Task 08 — Build the Page and Wire Navigation**
Objective: `/ramadan/campaigns` page, dashboard-shell nav entry. Files to Create: `app/(dashboard)/ramadan/campaigns/page.tsx`. Files to Modify: `dashboard-shell.tsx`. Dependencies: Task 05, Task 06, Task 07. Tests: page-level integration test. Definition of Done: test passes.

**Task 09 — Add Localization, Accessibility, and Full Test Suite**
Objective: Complete §17/§22 coverage, mandatory test included. Definition of Done: all green in CI.

**Task 10 — Final Code Review**
Objective: Confirm the Override action's client-side gate is genuinely `super_admin`-only and no broader role can reach it via a UI path. Definition of Done: checklist in §25 checked.

## 25. Definition of Done
Admins can safely configure each region's Ramadan campaign ahead of the season, with the one action capable of platform-wide disruption — the Eid-date override — properly restricted, confirmed, and audited end-to-end.

## 26. Final Verification Checklist
- [ ] Campaign CRUD built against the proposed contract in §11, cross-referenced against B-01 for consistency
- [ ] Proposed contract flagged for real sign-off before production release
- [ ] Override action strictly `super_admin`-gated, `content_editor` correctly blocked client-side and server-side — mandatory test passing
- [ ] Successful override refetches and displays the corrected date without a page reload
- [ ] Full localization, zero hardcoded strings
