# N-01 — Games Catalog Editor

## 1. Feature Context
Part of **A.10 Games Module**. Covers the admin CRUD form for game catalog entries, including the mandatory `skill_node_ids` picker and the client-side Publish-button-disabled UX courtesy backing B-04's hard server-side gate (PRD §9 item 1).

## 2. Parent Feature
A.10 Games Module — NextJS Admin

## 3. Sub-feature
**3.1 Games Catalog Editor** `[N-01]`

## 4. Objective
Build a CRUD form for game entries (title, skill_area, mechanic_type, age_band_difficulty_config, required skill_node_ids multi-select) that disables the Publish action while skill_node_ids is empty, and routes Quran/Tajweed/Dua-linked games through the existing scholar-review workflow component before publish (PRD §9).

## 5. Business Requirements
- §8: Games Catalog Editor = full CRUD (delete = withdraw), behind `content_editor` role, scholar-approval-gated for Quran/Tajweed/Dua-linked games.
- §9 item 1: Publish action DISABLED (not just validated-on-submit) while `skill_node_ids` is empty — UI-level courtesy in addition to backend's hard `422` rejection (B-04).
- §12.5: the UI disabling is explicitly a UX courtesy, not the actual security boundary — this distinction must be preserved, not conflated.

## 6. Existing Architecture
Next.js 15 App Router, TypeScript, TanStack Query v5, Zod. Strict layering: UI Component → Custom React Query Hook → Repository/`BaseResourceClient` → `apiClient` → Backend REST API (`NEXT-JS-INSTRUCTIONS.md` §2). New feature module `src/features/games-catalog/` with `api/`, `hooks/`, `components/` subdirectories, following the exact structure used by `family-management`/`users`/`cms` features.

## 7. Existing Code to Reuse
- `BaseResourceClient` (`src/shared/api/`) — extend as `GamesResourceClient` for standard CRUD (`list`, `get`, `create`, `update`, `delete`→withdraw).
- `DataTable`, `FilterPanel`, `SearchBar`, `EmptyState`, `ErrorView`, `LoadingState`, `QueryErrorState` (`src/shared/components/`).
- `RequirePermission` — gate the entire editor behind `games:write` (new permission string, following the existing `users:read`-style convention).
- `useTranslation()`, `useFormatters()` — all UI text and any numeric display.
- `usePaginationState`, `useDebouncedValue` — for any list view within the editor context (e.g., existing games list before opening the create/edit form).
- `ConfirmationDialog` — for the withdraw (delete) action confirmation.
- `apiClient` (never called directly from components — only via the repository, per §12 Do/Don't).

## 8. Files to Create
```
src/features/games-catalog/api/games-resource-client.ts
src/features/games-catalog/api/games-schema.ts                 # Zod schemas: gameSchema, gameCreateInputSchema, gameUpdateInputSchema
src/features/games-catalog/hooks/use-games-list.ts
src/features/games-catalog/hooks/use-game-detail.ts
src/features/games-catalog/hooks/use-create-game.ts
src/features/games-catalog/hooks/use-update-game.ts
src/features/games-catalog/hooks/use-withdraw-game.ts
src/features/games-catalog/components/games-catalog-table.tsx
src/features/games-catalog/components/game-editor-form.tsx
src/features/games-catalog/components/skill-node-multiselect.tsx
src/features/games-catalog/components/age-band-difficulty-subform.tsx
src/app/(dashboard)/games-catalog/page.tsx
src/app/(dashboard)/games-catalog/[gameId]/page.tsx
src/features/games-catalog/__tests__/game-editor-form.test.tsx
```

## 9. Files to Modify
```
src/shared/constants/api-endpoints.ts       # add API_ENDPOINTS.GAMES.BASE, .COMPLIANCE, .AUDIT_LOG
src/shared/components/dashboard-shell.tsx   # add Games Catalog nav entry behind RequirePermission
src/shared/constants/permissions.ts         # add "games:write", "games:read" permission strings
```
**Do Not Change:** `BaseResourceClient` itself — extend, don't modify.

## 10. Backend Requirements
Consumes B-06's `POST /admin/v1/games`, `PATCH /admin/v1/games/{id}`, `DELETE /admin/v1/games/{id}` (withdraw semantics) exactly as documented, plus B-04's `422 SKILL_MAPPING_REQUIRED` error contract.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- `GamesResourceClient extends BaseResourceClient<Game, GameCreateInput, GameUpdateInput, GameFilters>`.
- `GameEditorForm`: title, skill_area (dropdown, sourced from a domain-registry endpoint — confirm exact source against A.9's finalized registry API before implementation, flagged as a dependency), mechanic_type (dropdown of existing implemented mechanics — configures parameters for existing mechanics, does not define new interaction code), `AgeBandDifficultySubform` (structured sub-form per tier: 4 to 6, 6 to 9, 9 to 12, 12 to 15, 15 to 18+, each with time-pressure/distractor-count/complexity fields), `SkillNodeMultiselect` (required).
- Publish button: `disabled={skillNodeIds.length === 0}` with a tooltip explaining why (PRD §9 item 1) — this is client-side UX only; the actual enforcement is B-04's server-side `422`.
- On `422 SKILL_MAPPING_REQUIRED` from the server (e.g., a race condition where the button state was stale), display the error clearly via `QueryErrorState`, not a silent failure.
- Quran/Tajweed/Dua-linked game publish attempts route through the existing scholar-review workflow component (reused from A.5/A.6's admin modules — exact component import path to be confirmed against those modules, not invented here).

## 13. API Contract
Consumes B-06 §13 contracts (`POST`/`PATCH`/`DELETE /admin/v1/games[/{id}]`) exactly.

## 14. Database Requirements
N/A (frontend only).

## 15. Validation
Zod schemas (`games-schema.ts`) mirror backend validation: `title` non-empty, `skill_area`/`mechanic_type` from registered enums, `age_band_difficulty_config` requires all four tiers present, `skill_node_ids` array (client-side warns/disables Publish on empty, but does not hard-block Save-as-Draft).

## 16. Authentication
Relies on existing session cookie / Bearer token flow (`apiClient`, `useAdminSession()`) — no new auth logic.

## 17. Authorization
`RequirePermission permission="games:write"` wraps the entire editor; read-only fallback view (or hidden nav entry) for admins lacking this permission — client-side gating only, backend RBAC (B-06 §17) is the actual boundary.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `422 SKILL_MAPPING_REQUIRED` from server | Clear inline error via `QueryErrorState`, Publish button re-disabled if state was stale |
| `422 SIGNOFF_REQUIRED` (difficulty change on published game without learning_science sign-off) | Inline error directing to the sign-off field |
| `403` (insufficient permission) | `RequirePermission` fallback UI, no form rendered |
| Network/API failure on save | `ErrorView` with retry, form state preserved (not cleared) |
| Duplicate/conflicting entry | Inline field-level error mapped from backend response |

## 19. Offline First
N/A — admin portal is always-online per its architecture.

## 20. Local Data
N/A (TanStack Query cache only, standard React Query caching semantics, no persistent local storage).

## 21. Localization
All labels/tooltips/error messages via `useTranslation()`; `age_band_difficulty_config` numeric fields formatted via `useFormatters()`.

## 22. RTL
Form layout, multiselect, and sub-form must render correctly for Arabic/Urdu admin locales (existing `useLocalization()`/RTL convention reused, not reinvented).

## 23. Analytics
No dedicated client analytics events specified in the PRD for this admin surface beyond the standing Anti-Filler Audit Log (N-04, backend-driven) — admin actions are tracked via B-06's audit logging, not a separate frontend analytics event stream.

## 24. Performance
- `DataTable` pagination for the pre-edit games list (reuse existing pagination/search pattern, avoid unbounded list rendering).
- Debounced skill-node search within `SkillNodeMultiselect` (`useDebouncedValue`) to avoid excessive API calls while typing.
- Form re-renders minimized via React Query's cache + controlled-form-state best practices (avoid unnecessary re-fetch on every keystroke).

## 25. Security
- Publish-button disabling is explicitly documented (in code comments and this blueprint) as a UX courtesy only — B-04's server-side gate is the actual security boundary (PRD §12.5), preventing a false sense of security from client-only enforcement.
- No secrets/credentials handled in this module.

## 26. Library Requirements
Next.js 15, TypeScript, TanStack Query v5, Zod. No new libraries beyond what the admin portal already uses.

## 27. Testing
- Unit: Publish button disabled state correctly reflects `skillNodeIds.length === 0`.
- Unit: `AgeBandDifficultySubform` requires all four tiers before allowing submit.
- Integration: form submission → `422 SKILL_MAPPING_REQUIRED` → error displayed, Publish re-disabled.
- Integration: Quran/Tajweed/Dua-tagged game routes through scholar-review component before publish becomes available.
- Accessibility: form fields correctly labeled, multiselect keyboard-navigable, tooltip on disabled Publish button screen-reader-accessible.

## 28. Documentation
Component-level JSDoc on `GameEditorForm` explicitly noting the UX-courtesy-vs-security-boundary distinction for the Publish button, cross-referencing B-04.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schemas**
- Objective: `gameSchema`, `gameCreateInputSchema`, `gameUpdateInputSchema` in `games-schema.ts`.
- Definition of Done: schemas match B-06 §13 request/response shapes exactly.

**Task 02 — Implement GamesResourceClient**
- Objective: `class GamesResourceClient extends BaseResourceClient<...>` with a `withdraw(id)` custom method (mirroring `FamilyResourceClient.suspend()`'s pattern).
- Existing Files to Reuse: `BaseResourceClient`.
- Definition of Done: `list`/`get`/`create`/`update`/`withdraw` all implemented and Zod-validated.

**Task 03 — Register API Endpoints**
- Objective: Add `API_ENDPOINTS.GAMES.*` entries.
- Files to Modify: `api-endpoints.ts`.

**Task 04 — Implement React Query Hooks**
- Objective: `useGamesList`, `useGameDetail`, `useCreateGame`, `useUpdateGame`, `useWithdrawGame`.
- Definition of Done: mirrors `useFamilyList`/`useSuspendFamily` conventions exactly.

**Task 05 — Build SkillNodeMultiselect Component**
- Objective: Required multiselect sourced from the skill-node registry endpoint (dependency confirmed against A.9).
- Definition of Done: debounced search, keyboard-accessible.

**Task 06 — Build AgeBandDifficultySubform Component**
- Objective: Structured sub-form per age tier (4 to 6, 6 to 9, 9 to 12, 12 to 15, 15 to 18+) with time-pressure/distractor-count/complexity fields.
- Definition of Done: validates all four tiers present before allowing submit.

**Task 07 — Build GameEditorForm**
- Objective: Full form assembling all fields; Publish button disabled logic per §12.
- Definition of Done: disabled-state unit test passes.

**Task 08 — Integrate Scholar-Review Routing**
- Objective: Quran/Tajweed/Dua-tagged games route through the existing A.5/A.6 scholar-review component before Publish is available.
- Dependencies: confirm exact component/import path against A.5/A.6's finalized admin modules.
- Definition of Done: integration test confirms non-bypassable routing for tagged content types.

**Task 09 — Build Games Catalog Table & List Page**
- Objective: `GamesCatalogTable` using `DataTable`, `FilterPanel`, `SearchBar`, wired into `src/app/(dashboard)/games-catalog/page.tsx`.
- Definition of Done: pagination/search/filter functioning per existing conventions.

**Task 10 — Wire RequirePermission & Navigation**
- Objective: `games:write`/`games:read` permissions added, nav entry gated, editor page gated.
- Files to Modify: `permissions.ts`, `dashboard-shell.tsx`.

**Task 11 — Add Tests**
- Objective: Full suite per §27.

**Task 12 — Add Documentation**
- Objective: JSDoc per §28.

**Task 13 — Final Code Review**
- Objective: Confirm the UX-courtesy-vs-security-boundary distinction is clearly documented and that no component bypasses `RequirePermission`.
- Definition of Done: review checklist (§31) fully checked.

## 30. Definition of Done
- Full CRUD editor implemented per B-06's contract, with Zod validation matching the backend exactly.
- Publish button correctly disabled/enabled based on `skill_node_ids`, with the UX-courtesy nature explicitly documented.
- Scholar-review routing confirmed for Quran/Tajweed/Dua-linked games.
- RBAC (`RequirePermission`) correctly gates the entire feature.
- All §27 tests passing.

## 31. Final Verification Checklist
- [ ] Publish button disabled state correctly tied to `skillNodeIds.length === 0`
- [ ] `422 SKILL_MAPPING_REQUIRED` server response displayed clearly, not silently swallowed
- [ ] Scholar-review routing confirmed for Quran/Tajweed/Dua-tagged games
- [ ] `RequirePermission` correctly gates the editor (no client-only-hidden-but-reachable routes)
- [ ] All form fields localized, RTL-correct
- [ ] Accessibility verified (labels, keyboard navigation, screen-reader tooltip)
- [ ] No direct `apiClient` calls from components (routed through repository/hooks only)
- [ ] No files outside declared scope modified

---

## 32. Cross-Platform Dependencies
- Backend Dependency: B-06 (CRUD), B-04 (skill-mapping gate, server-side enforcement backing this UI's courtesy disabling).
- KMP Dependency: None.
- Admin Dependency: N-02 (Compliance Dashboard links back into this editor), N-03 (Age-Band Difficulty panel embedded within this form).
- Database Dependency: None (frontend only).
- External Service Dependency: A.5/A.6 scholar-review workflow component — exact import path unresolved, flagged for confirmation against those modules' finalized admin blueprints.
- Figma Dependency: Games Catalog Editor, Age-Band Difficulty Sub-form — Figma Required.
