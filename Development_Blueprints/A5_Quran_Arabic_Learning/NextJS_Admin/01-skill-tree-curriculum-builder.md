# N-01 — Skill Tree / Curriculum Builder

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Admin graph-editing UI for `skill_node` definitions and the prerequisite graph, backed by B-09.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
N-01 — Skill Tree / Curriculum Builder (Admin API consumer)

## 4. Objective
Provide a graph-editing UI for curriculum editors to create/edit `skill_node` entities and their prerequisite relationships, with mandatory cycle-detection validation before save and deactivate-only removal.

## 5. Business Requirements
- Admin Requirements §8: full CRUD for `skill_node`, prerequisite graph editing with cycle-detection validation, track assignment. Delete = deactivate only.
- §9 Admin AI Code-Generation Prompt: graph-editing UI (e.g., react-flow-style) for node create/edit with `track`, `related_ayah_id` (searchable picker), `prerequisite_node_ids` (multi-select); save calls a validation endpoint performing cycle detection; on cycle, block save with the cycle path shown; delete action relabeled "Deactivate."

## 6. Existing Architecture
NoorHeroes Admin Portal: **Next.js 15 App Router**, TypeScript, TanStack Query v5, Zod, `BaseResourceClient` repository pattern, `apiClient` HTTP boundary, `RequirePermission` for RBAC-gated UI, `DataTable`/`ConfirmationDialog` shared components, `useTranslation`/`useFormatters`/`useLocalization` for i18n/RTL. This corrects the PRD draft's generic "React + TypeScript" assumption — the actual stack is Next.js 15 App Router with the specific patterns listed above, and this blueprint follows them rather than inventing new ones.

## 7. Existing Code to Reuse
- `BaseResourceClient` — extend for `SkillNodeResourceClient` (`GET/POST/PUT` against B-09's routes).
- `RequirePermission` — gate the entire builder page behind `curriculum_editor`.
- `DataTable`, `ConfirmationDialog` (repurposed for the "Deactivate" confirmation, not "Delete").
- `useTranslation`, `useFormatters`, `useLocalization` for all UI copy and RTL layout.
- `usePaginationState`, `useDebouncedValue` (for the ayah-picker search).

## 8. Files to Create
- `src/features/learning-curriculum/api/skill-node-resource-client.ts` (extends `BaseResourceClient`)
- `src/features/learning-curriculum/api/curriculum-graph-client.ts` (cycle-validation endpoint call)
- `src/features/learning-curriculum/hooks/use-skill-nodes.ts` (TanStack Query hook)
- `src/features/learning-curriculum/hooks/use-save-skill-node.ts` (mutation hook, includes cycle-check flow)
- `src/features/learning-curriculum/hooks/use-deactivate-skill-node.ts`
- `src/features/learning-curriculum/components/curriculum-graph-canvas.tsx` (graph-editing UI)
- `src/features/learning-curriculum/components/skill-node-editor-panel.tsx` (create/edit form: track, ayah picker, prerequisites multi-select)
- `src/features/learning-curriculum/components/ayah-search-picker.tsx`
- `src/features/learning-curriculum/schemas/skill-node.schema.ts` (Zod)
- `src/app/(dashboard)/learning/curriculum/page.tsx`
- `src/features/learning-curriculum/__tests__/skill-node-editor-panel.test.tsx`
- `src/features/learning-curriculum/__tests__/curriculum-graph-canvas.test.tsx`

## 9. Files to Modify
- Dashboard sidebar navigation config — add "Curriculum Builder" entry, gated by `curriculum_editor` permission via `RequirePermission`.

## 10. Backend Requirements
Consumes B-09 (`POST/PUT /v1/admin/learning/skill-nodes`, `POST /v1/admin/learning/skill-nodes/{node_id}/deactivate`, `POST /v1/admin/content/validate-graph`).

## 11. KMP Requirements
N/A (admin-only).

## 12. NextJS Requirements
- **Graph canvas**: a `react-flow`-based (or equivalent graph-visualization library already used elsewhere in the Admin Portal — confirm before introducing a new dependency) node-and-edge editor rendering `skill_node` entities and their prerequisite relationships.
- **Node editor panel**: create/edit form with `track` select, `related_ayah_id` searchable picker (`ayah-search-picker.tsx`, debounced search via `useDebouncedValue`), `prerequisite_node_ids` multi-select from existing nodes.
- **Cycle-detection on save**: before committing, call B-09's `/validate-graph` endpoint; on `409`/`valid: false`, block the save and render the returned cycle path clearly (e.g., a highlighted path in the canvas plus a textual list) rather than a generic error toast.
- **Deactivate, not delete**: the removal action is labeled "Deactivate" throughout the UI (button text, confirmation dialog, tooltips) — no "Delete" terminology anywhere, consistent with the API only exposing a deactivate route.
- **RBAC**: entire page gated behind `curriculum_editor` role via `RequirePermission`; unauthorized users never see the page rendered (not just a disabled button).
- **Pagination/search**: node list uses `usePaginationState` and `useDebouncedValue` for search, consistent with existing Admin Portal list patterns (e.g., `useUsers`/`useFamilyList`).

## 13. API Contract
Per B-09 §13: `POST/PUT /v1/admin/learning/skill-nodes`, `POST /v1/admin/learning/skill-nodes/{node_id}/deactivate`, `POST /v1/admin/content/validate-graph`.

## 14. Database Requirements
N/A (client consumes API only).

## 15. Validation
Zod schema (`skill-node.schema.ts`) mirrors B-09's request contract client-side for immediate form feedback; server-side validation (B-09) remains authoritative — client validation is a UX convenience, not a substitute.

## 16. Authentication
Reuses existing Admin Portal session (`useAdminSession`), Bearer token attached automatically by `apiClient`.

## 17. Authorization
`RequirePermission` wraps the entire page/route; `curriculum_editor` role required. No UI element for mutating actions rendered for unauthorized roles (not merely disabled).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Cycle detected on save | Block save, render the returned cycle path clearly, no generic error toast |
| Validation failure (missing fields, invalid ayah reference) | Inline field-level Zod + server error display |
| API failure during save | Toast/inline error with retry, form state preserved (no data loss on failure) |
| Unauthorized access | Page not rendered at all (RequirePermission gate) |

## 19. Offline First
N/A (admin web app, connectivity assumed).

## 20. Local Data
N/A (TanStack Query cache only, standard stale-time/cache-time behavior consistent with other Admin Portal list hooks).

## 21. Localization
All UI copy via `useTranslation`; ayah/content labels rendered in the admin's selected locale via `useFormatters`/`useLocalization`.

## 22. RTL
Full RTL layout support via `useLocalization`'s RTL-status flag, consistent with the rest of the Admin Portal.

## 23. Analytics
N/A (internal admin tooling; standard audit-log coverage from B-09 suffices, no separate admin-analytics event taxonomy required per existing Admin Portal conventions).

## 24. Performance
Graph canvas must remain responsive for realistically-sized curriculum graphs (dozens to low-hundreds of nodes); paginate/search the node-picker and prerequisite multi-select rather than rendering the entire node set unfiltered in a dropdown.

## 25. Security
`curriculum_editor` RBAC strictly enforced; no client-side-only permission check (server re-validates on every B-09 call regardless).

## 26. Library Requirements
Next.js 15, TypeScript, TanStack Query v5, Zod, existing Admin Portal component library. Graph-visualization library: confirm whether one is already in use elsewhere in the Admin Portal before adding `react-flow` or an equivalent as a new dependency.

## 27. Testing
- Component test: `SkillNodeEditorPanel` field validation (Zod schema).
- Component test: cycle-detection error rendering shows the returned cycle path clearly.
- Component test: "Deactivate" (never "Delete") terminology verified across button/dialog/tooltip text.
- Integration test: `curriculum_editor`-gated page renders nothing for unauthorized roles.

## 28. Documentation
Inline component documentation noting the deactivate-only removal design and why (historical reference integrity, per B-09).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Existing Graph-Visualization Library Usage**
- Task ID: N-01-T01
- Objective: Check whether the Admin Portal already uses a graph/flow visualization library elsewhere before introducing a new dependency.
- Dependencies: None (verification task, per Rule 30).
- Definition of Done: Decision documented (reuse existing or justify adding `react-flow`).

**Task 02 — Implement `SkillNodeResourceClient` and `CurriculumGraphClient`**
- Task ID: N-01-T02
- Existing Files to Reuse: `BaseResourceClient`.
- Dependencies: B-09.
- Definition of Done: CRUD + validate-graph calls succeed against staging.

**Task 03 — Implement Zod Schema and Query/Mutation Hooks**
- Task ID: N-01-T03
- Dependencies: N-01-T02.
- Definition of Done: Hooks unit-tested with mocked API responses.

**Task 04 — Build `AyahSearchPicker`**
- Task ID: N-01-T04
- Implementation Details: Debounced search via `useDebouncedValue` against the existing ayah-lookup endpoint (confirm exact endpoint, likely part of the `content` context's existing catalog API).
- Dependencies: N-01-T03.
- Definition of Done: Picker returns correct results for sample queries.

**Task 05 — Build `SkillNodeEditorPanel`**
- Task ID: N-01-T05
- Implementation Details: Form with track select, ayah picker, prerequisites multi-select, Zod validation.
- Dependencies: N-01-T03, N-01-T04.
- Definition of Done: Form renders and validates correctly.

**Task 06 — Build `CurriculumGraphCanvas`**
- Task ID: N-01-T06
- Implementation Details: Node/edge visualization, cycle-path highlighting on validation failure.
- Dependencies: N-01-T01, N-01-T05.
- Definition of Done: Canvas renders sample graph correctly, cycle-path highlighting verified.

**Task 07 — Wire Page, RBAC, and Navigation**
- Task ID: N-01-T07
- Files to Create: `src/app/(dashboard)/learning/curriculum/page.tsx`. Files to Modify: sidebar nav config.
- Dependencies: N-01-T06.
- Definition of Done: Page reachable only for `curriculum_editor` role.

**Task 08 — Tests**
- Task ID: N-01-T08
- Dependencies: N-01-T01–T07.
- Definition of Done: All green in CI.

## 30. Definition of Done
Curriculum Builder live, cycle-detection enforced on save with clear error UX, deactivate-only removal, `curriculum_editor` RBAC strictly enforced, full RTL/localization, fully tested.

## 31. Final Verification Checklist
- [ ] Cycle detection blocks save and clearly shows the cycle path
- [ ] "Deactivate" terminology used consistently, no "Delete" language anywhere
- [ ] Page not rendered at all for non-`curriculum_editor` roles
- [ ] Ayah picker and prerequisite multi-select performant for realistic graph sizes
- [ ] RTL/localization verified
- [ ] Full test suite green in CI
