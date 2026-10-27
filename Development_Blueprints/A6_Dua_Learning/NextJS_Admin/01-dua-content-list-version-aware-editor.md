# N-01 — Dua Content List & Version-Aware Editor

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. Source PRD §8/§9 items 1 and 4. Sibling content-editor pattern: `A3_Stories_Module/NextJS_Admin/01-story-episode-content-editor.md`, `A5_Quran_Arabic_Learning/NextJS_Admin/02-quran-content-management-skill-node-linkage.md` — each content-bearing feature owns its own admin editor screen (matching each feature owning its own backend bounded context), so this file stays dua-owned, now grounded in the real admin portal architecture.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
N-01 — Dua Content List & Version-Aware Editor

## 4. Objective
Give `content_editor`-scoped admins a category-grouped table of duas with a detail editor, using the real `BaseResourceClient`/`apiClient`/`DataTable`/`RequirePermission` stack documented in `NEXT-JS-INSTRUCTIONS.md`, not generic placeholders.

## 5. Business Requirements
Admin Requirements §8; §9 items 1 and 4.

## 6. Existing Architecture
`NEXT-JS-INSTRUCTIONS.md` §5: `BaseResourceClient` (abstract, `list(filters, signal)`/`get(id, signal)`/`create(input)`/`update(id, input)`/`delete(id)`, Zod-validated) — extend it for `DuaResourceClient`, following `FamilyResourceClient`'s exact pattern (extends `BaseResourceClient`, adds custom methods like its `.suspend()`). §6: low-level `apiClient.get/post/patch/delete(path, options)` used inside the resource client, not called directly from components. §8: `DataTable`, `RequirePermission`, `ConfirmationDialog`, `FilterPanel`, `SearchBar`, `StatusBadge`, `EmptyState`, `ErrorView`, `LoadingState`, `QueryErrorState`. §9: custom hooks follow the `useFamilyList(filters)`/`useFamilyDetail(familyId)` pattern — this file needs `useDuaList(filters)`, `useDuaDetail(id)`, `useCreateDua()`, `useUpdateDua()`, `useArchiveDua()`. §6: RBAC via `hasPermission(admin, permission)` + `<RequirePermission>` component, not a bespoke role-string check.

## 7. Existing Code to Reuse
- `BaseResourceClient` (extend, don't reimplement CRUD plumbing)
- `apiClient`, `parseApiError`, `logger`
- `DataTable`, `RequirePermission`, `ConfirmationDialog`, `FilterPanel`, `SearchBar`, `StatusBadge`, `EmptyState`, `ErrorView`, `LoadingState`
- `useDebouncedValue`, `usePaginationState`, `useTranslation`, `useFormatters`

## 8. Files to Create
- `src/features/dua/api/DuaResourceClient.ts` (extends `BaseResourceClient`)
- `src/features/dua/api/duaSchemas.ts` (Zod schemas)
- `src/features/dua/hooks/useDuaList.ts`, `useDuaDetail.ts`, `useCreateDua.ts`, `useUpdateDua.ts`, `useArchiveDua.ts`
- `src/features/dua/pages/DuaListPage.tsx`
- `src/features/dua/pages/DuaEditorPage.tsx`
- `src/features/dua/components/DuaEditorForm.tsx`
- `src/features/dua/components/VersionHistoryTab.tsx`
- `src/features/dua/components/FreeTierComplianceBanner.tsx`
- `src/features/dua/__tests__/DuaEditorForm.test.tsx`
- `src/features/dua/__tests__/DuaListPage.test.tsx`

## 9. Files to Modify
- Admin navigation/sidebar config — add "Dua Management" entry, wrapped in `<RequirePermission>`

## 10. Backend Requirements
Consumes B-08 (`POST/PATCH/GET /v1/admin/dua`, `GET /v1/admin/dua/{id}/versions`, `POST /v1/admin/dua/{id}/archive`) and B-11 (`GET/POST/PATCH /v1/admin/dua/categories`).

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- `DuaListPage`: `DataTable` grouped by category, `FilterPanel` (category/status), `SearchBar`, pagination via `usePaginationState`
- `DuaEditorPage`/`DuaEditorForm`: Arabic text, transliteration, translation, audio upload, `source_citation` (required, client + server validated), age_min/age_max, category selector (populated from B-11's real category list, not hardcoded — see N-04), `habit_suggestion_eligible` toggle
- Submit-for-review surfaces the backend's `422` field-level error inline via `parseApiError`, mapped to the correct form field — not a generic toast
- `VersionHistoryTab` — prior `DuaContentVersion` rows with scholar-approval status
- `FreeTierComplianceBanner` — permanent, module-wide
- Archive action via `ConfirmationDialog`

## 13. API Contract
Per B-08 §13.

## 14. Database Requirements
N/A (frontend).

## 15. Validation
Zod schema mirrors backend validation (source_citation/audio required) for fast feedback; server response is always authoritative on mismatch.

## 16. Authentication
Existing admin session (`useAdminSession()`).

## 17. Authorization
`<RequirePermission permission="dua:content_editor">` (or the real permission string once confirmed against `hasPermission`'s actual permission taxonomy — **do not assume `content_editor` is a literal permission string without checking `NEXT-JS-INSTRUCTIONS.md`'s actual RBAC model**, since the backend's scope names and the frontend's permission strings may not be 1:1).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Submit without audio | Inline field error via `parseApiError`, mapped to the audio field |
| Submit without source_citation | Inline field error |
| Network/API failure | `ErrorView`/`QueryErrorState`, form data preserved |
| Loading | `LoadingState` |
| Empty category | `EmptyState` |

## 19. Offline First / 20. Local Data
N/A (admin web).

## 21. Localization
Editor supports per-locale authoring; admin UI copy via `useTranslation()`.

## 22. RTL
Admin UI RTL support for Arabic-locale admin users, per the platform's existing RTL handling (confirm the actual mechanism — `useThemeStore()` or a dedicated RTL provider — before assuming).

## 23. Analytics
N/A (internal admin tool).

## 24. Performance
`DataTable` pagination (not full-catalog load), `useDebouncedValue` for search input.

## 25. Security
`RequirePermission` + backend's authoritative `403` — UI-side hiding is a convenience layer, never the actual security boundary.

## 26. Library Requirements
Existing Next.js/React/TypeScript/Zod/React-Query (implied by the `useXxx` hook pattern) stack — no new dependencies.

## 27. Testing
- Unit: form validation (Zod schema)
- Integration: submit-for-review without audio surfaces the correct inline error via `parseApiError`
- Integration: editing a published dua creates a visible new version entry
- Accessibility: `RequirePermission`-gated actions correctly hidden/disabled for non-permitted users
- Responsive: table/editor across breakpoints

## 28. Documentation
Module README noting the free-tier banner is permanent.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Real Permission String**
Task ID: N-01-T01. Objective: check `NEXT-JS-INSTRUCTIONS.md`'s actual RBAC/permission model (`hasPermission(admin, permission)`'s real permission taxonomy) before hardcoding `"dua:content_editor"` as if confirmed. Definition of Done: documented correct permission string.

**Task 02 — Implement `DuaResourceClient`**
Task ID: N-01-T02. Files to Create: `DuaResourceClient.ts`, `duaSchemas.ts`. Existing Architecture to Follow: `FamilyResourceClient extends BaseResourceClient` pattern. Definition of Done: typed client matches B-08's contract.

**Task 03 — Implement Hooks**
Task ID: N-01-T03. Files to Create: all `useXxx` hooks listed in §8. Existing Architecture to Follow: `useFamilyList`/`useFamilyDetail` pattern. Definition of Done: hooks correctly wrap `DuaResourceClient` methods.

**Task 04 — Implement List Page**
Task ID: N-01-T04. Files to Create: `DuaListPage.tsx`. Existing Files to Reuse: `DataTable`, `FilterPanel`, `SearchBar`, `usePaginationState`. Definition of Done: renders grouped-by-category with pagination/filter/search.

**Task 05 — Implement Editor Form**
Task ID: N-01-T05. Files to Create: `DuaEditorForm.tsx`. Dependencies: N-04's category list. Definition of Done: form validates and submits correctly.

**Task 06 — Implement Inline Server-Validation Error Surfacing**
Task ID: N-01-T06. Existing Files to Reuse: `parseApiError`. Definition of Done: audio/source-citation errors mapped to correct fields.

**Task 07 — Implement Version History Tab**
Task ID: N-01-T07. Files to Create: `VersionHistoryTab.tsx`. Definition of Done: prior versions render correctly.

**Task 08 — Implement Free-Tier Banner**
Task ID: N-01-T08. Files to Create: `FreeTierComplianceBanner.tsx`. Definition of Done: renders on every page in this module.

**Task 09 — Implement RBAC**
Task ID: N-01-T09. Dependencies: Task 01. Existing Files to Reuse: `RequirePermission`, `hasPermission`. Definition of Done: correct permission string enforced.

**Task 10 — Implement Archive**
Task ID: N-01-T10. Existing Files to Reuse: `ConfirmationDialog`. Definition of Done: soft-delete confirmed.

**Task 11 — Add States & Tests**
Task ID: N-01-T11. Definition of Done: all §18/§27 scenarios covered.

**Task 12 — Add Documentation**
Task ID: N-01-T12. Definition of Done: README written.

**Task 13 — Final Code Review**
Task ID: N-01-T13. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
List/editor functional using the real `BaseResourceClient`/`DataTable`/`RequirePermission` stack, correct permission string enforced, visible versioning, permanent free-tier banner.

## 31. Final Verification Checklist
- [ ] `DuaResourceClient extends BaseResourceClient`, not a bespoke fetch wrapper
- [ ] Real permission string confirmed and used, not assumed
- [ ] Audio/source-citation errors surface inline via `parseApiError`
- [ ] Editing a published dua visibly creates a new version
- [ ] `FreeTierComplianceBanner` present on every page
- [ ] `DataTable`/`FilterPanel`/`SearchBar`/`RequirePermission` reused, not rebuilt

## 32. Addendum — What Changed From the Original Draft
Corrected from a generic Next.js App Router placeholder scheme (`app/admin/content/dua/page.tsx`, invented `apiClient`/`DataTable` names that happened to guess right on naming but not on actual method signatures) to the real, documented `BaseResourceClient`-extension pattern, real hook naming convention, and real shared components (`RequirePermission`, `ConfirmationDialog`, `FilterPanel`, etc.) from `NEXT-JS-INSTRUCTIONS.md`. Flags that the exact RBAC permission string needs confirming against the real permission taxonomy rather than assumed equal to the backend's `content_editor` scope name.
