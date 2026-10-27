# N-04 — Family Garden Milestone Configuration

## 1. Feature Context
NoorHeroes Admin Portal. CRUD interface for family-level Noor Garden milestone thresholds and celebration content, backing B-12.

## 2. Parent Feature
A.7 Habit Tracker — NextJS Admin

## 3. Sub-feature
N-04 Family Garden Milestone Configuration

## 4. Objective
Build a CRUD page for milestone definitions (garden_zone, threshold, celebration_content_ref), restricted to `content_editor`.

## 5. Business Requirements
- Full CRUD, delete = deactivate/archive.
- `garden_zone` restricted to the documented zone enum; must remain compatible with `family_streak`'s aggregate-only schema (no per-child fields ever introduced via this config).

## 6. Existing Architecture
`src/app/(dashboard)/habits/garden-milestones/page.tsx`, `src/features/garden-milestones/{api,hooks,components}`.

## 7. Existing Code to Reuse
`DataTable`, `usePaginationState`, `RequirePermission`, `useAdminSession`. **Still genuinely unresolved (confirmed, not just assumed):** no shared content-reference picker component exists anywhere in the Admin Portal's component library yet — `A2_Home_Dashboard_AI_Personalization/NextJS_Admin/02-daily-mission-curation-tool.md` independently raises the identical open flag. Coordinate with whichever of these two features implements a picker first; do not build two competing versions.

## 8. Files to Create
- `src/app/(dashboard)/habits/garden-milestones/page.tsx`
- `src/features/garden-milestones/api/garden-milestones-repository.ts`
- `src/features/garden-milestones/hooks/use-garden-milestones.ts`
- `src/features/garden-milestones/hooks/use-create-garden-milestone.ts`
- `src/features/garden-milestones/hooks/use-update-garden-milestone.ts`
- `src/features/garden-milestones/hooks/use-deactivate-garden-milestone.ts`
- `src/features/garden-milestones/components/GardenMilestoneTable.tsx`
- `src/features/garden-milestones/components/GardenMilestoneFormDialog.tsx`

## 9. Files to Modify
- Admin Portal sidebar/navigation config — add "Garden Milestones" entry

## 10. Backend Requirements
Consumes B-12 (`/v1/admin/habits/garden-milestones`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- CRUD table: garden_zone, threshold, celebration_content_ref, active status.
- Create/Edit form with `garden_zone` dropdown restricted to the known enum, `celebration_content_ref` picker (reuse existing content picker if available).
- Deactivate action with confirmation.
- Pagination, filtering (by zone/active status).

## 13. API Contract
`GET/POST/PATCH /v1/admin/habits/garden-milestones` (B-12) — Admin API, `content_editor` scope.

## 14. Database Requirements
N/A (frontend only).

## 15. Validation
`garden_zone` restricted to enum via dropdown (prevents free-text entry); `threshold` positive-integer validation.

## 16. Authentication
`useAdminSession`.

## 17. Authorization
`RequirePermission permission="habits:garden-milestones:write"` (or project's equivalent `content_editor`-scoped permission string).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Invalid garden_zone/content_ref | Inline form error from the 422 response |
| Unauthorized | `RequirePermission` hides write actions |
| Network/API failure | Standard error state with retry |

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
**Confirmed:** Admin Portal supports multi-locale via `useTranslation()`/`updateLanguagePreference('hi'|'ar'|'en')` (`NEXT-JS-INSTRUCTIONS.md`) — table/form labels must use `useTranslation()`, not hardcoded English.

## 22. RTL
**Confirmed:** drive layout via `useLocalization()`'s RTL status; table column order and form layout must mirror correctly.

## 23. Analytics
Not applicable (audit-logged admin action per B-12).

## 24. Performance
Standard paginated table performance.

## 25. Security
`RequirePermission` client-side guard is defense-in-depth; B-12 is authoritative.

## 26. Library Requirements
Next.js App Router, React Query, existing Admin Portal shared components.

## 27. Testing
Component tests for table/form; hook tests for CRUD mutations; RBAC-guard tests.

## 28. Documentation
Inline help text cross-referencing B-06's structural no-sibling-comparison guarantee, noting milestone config must never introduce per-child fields.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `garden-milestones` Feature Module**
- Files to Create: `types.ts`, `api/garden-milestones-repository.ts`
- Definition of Done: module compiles with typed API client.

**Task 02 — Implement CRUD Hooks**
- Files to Create: `hooks/use-garden-milestones.ts`, `use-create-garden-milestone.ts`, `use-update-garden-milestone.ts`, `use-deactivate-garden-milestone.ts`
- Definition of Done: hooks correctly wrap B-12's endpoints.

**Task 03 — Build Table & Form Dialog**
- Files to Create: `GardenMilestoneTable.tsx`, `GardenMilestoneFormDialog.tsx`
- Implementation Details: zone dropdown, content-ref picker, threshold validation.
- Tests: component and form validation tests.
- Definition of Done: CRUD flow fully functional.

**Task 04 — Wire Page Route with RBAC Guard**
- Files to Create: `page.tsx`
- Files to Modify: sidebar/navigation config.
- Definition of Done: route live, RBAC-guarded.

**Task 05 — Final Code Review**
- Do Not Change: `family_streak`'s no-child-field schema guarantee — milestone config must remain compatible.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Family Garden Milestone Configuration page live, `content_editor`-gated, fully functional CRUD with deactivate-only delete.

## 31. Final Verification Checklist
- [ ] CRUD table renders with pagination/filtering
- [ ] `garden_zone` restricted to enum via dropdown
- [ ] Delete action is deactivate/archive only
- [ ] `RequirePermission` guards all write actions
- [ ] Loading/empty/error states implemented
- [ ] Tests passing
