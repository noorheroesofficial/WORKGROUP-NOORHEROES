# N-01 — Content List & Story Editor

## 1. Feature Context
The primary editorial authoring surface: a content list/browse and a 10-tab Story Editor session (Metadata through Review History) with periodic autosave, since editors work in long, interruptible sessions and must never lose work to a connectivity blip.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
2.1 Content List & Story Editor (ID: **N-01**)

## 4. Objective
Build the Content List browse page and the 10-tab Story Editor authoring session against B-01, with a persistent draft/version-status indicator and autosave resilient to connectivity blips.

## 5. Business Requirements
- FR-2: Story Editor sections — Metadata, Script/Scene Blocks, Interactive Choices, Moral Summary, Quiz, References, Media Timeline, Captions/Audio Tracks, Age/Region/Locale Eligibility, Review History.
- §6.4: shared `ContentEditorContext` per editing session holds draft state with periodic autosave.
- §1.12: empty state ("no drafts yet, create your first"); §1.13: skeleton loading.

## 6. Existing Architecture
`src/features/content-cms/` module, reusing E.28's navigation shell, `AdminAuthContext`, and design-token package.

## 7. Existing Code to Reuse
- `src/shared/components/data-table.tsx::DataTable`
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/empty-state.tsx::EmptyState`
- `src/shared/components/loading-state.tsx::LoadingState`
- A rich-text/structured-content editor library (new dependency, see §20)

## 8. Files to Create
- `src/app/(dashboard)/content/page.tsx` — Content List
- `src/app/(dashboard)/content/[id]/editor/page.tsx` — Story Editor shell (10 tabs as sub-routes or tab state)
- `src/features/content-cms/api/content-repository.ts` — `ContentRepositoryImpl`
- `src/features/content-cms/context/content-editor-context.tsx` — `ContentEditorContext` (draft state + autosave)
- `src/features/content-cms/hooks/use-content-list.ts`, `use-content-detail.ts`, `use-autosave.ts`
- `src/features/content-cms/components/story-editor-tabs/` — `MetadataTab.tsx`, `ScriptSceneBlocksTab.tsx`, `InteractiveChoicesTab.tsx`, `MoralSummaryTab.tsx`, `QuizTab.tsx` (embeds N-02), `ReferencesTab.tsx`, `MediaTimelineTab.tsx` (embeds N-03), `CaptionsAudioTracksTab.tsx`, `EligibilityTab.tsx`, `ReviewHistoryTab.tsx`
- `src/features/content-cms/components/version-status-indicator.tsx`
- `src/features/content-cms/types/content-item.ts` — Zod schema (discriminated union per `content_type`)

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `CONTENT_CMS.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item under "Content" group, gated by `content_editor`

## 10. NextJS Requirements
- `ContentEditorContext`: holds the current draft's `content_json` in memory, autosaves via a debounced `PATCH` call on change (per PRD requirement: survives a simulated connectivity blip — retry-on-reconnect via a local pending-write queue, not a lost edit).
- 10-tab sub-navigation persists tab state within a single editing session; `VersionStatusIndicator` (draft/pending_review/published/etc.) always visible regardless of active tab.
- "Submit for Review" action available from the Review History tab, calling B-01/B-04's submission path.
- Content List empty state and skeleton per PRD §1.12/§1.13.

## 11. Required API
**Admin API** — B-01: `POST/GET/PATCH /v1/admin/content`, `GET /v1/admin/content/{id}/versions`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="content_editor"` gating the entire module.

## 13. Loading / Empty / Error States
Content List skeleton and "no drafts yet" empty state; editor-load skeleton; autosave-failure indicator distinct from a hard save error.

## 14. Responsive UI / Accessibility
Tab rail collapses to a dropdown on narrow viewports; each tab's form fields properly labeled for screen readers; version-status indicator has a text label, not color alone.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`; Admin Portal is dense-professional-tool register per E.28 §2.1, RTL scope to be confirmed against E.28's own established localization coverage before assuming full mirroring is required.

## 16. Security
`content_editor` RBAC enforced via `RequirePermission`; autosave writes only ever target the current admin's own draft session (server-side ownership check on every autosave PATCH, not just client-side session scoping).

## 17. Testing
Unit: autosave debounce/retry-on-reconnect logic, tab-state persistence across navigation. Integration: draft state survives a simulated connectivity blip via the autosave mechanism (mandatory, per PRD frontend AI-prompt requirement #1); full create-draft → edit-across-tabs → submit-for-review flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `content-item.ts` discriminated-union schema per `content_type`. Files: `types/content-item.ts`, `api-endpoints.ts`. Tests: schema validation per type. Definition of Done: schema used by Task 03.

**Task 02 — Implement `ContentRepositoryImpl`**
Objective: Repository for B-01's four endpoints. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `ContentEditorContext` with Autosave**
Objective: Debounced autosave, local pending-write queue for connectivity blips. Dependencies: Task 02. Tests: **mandatory** — connectivity-blip-survival test. Definition of Done: test passes.

**Task 04 — Implement `VersionStatusIndicator`**
Objective: Persistent status badge across all tabs. Dependencies: Task 03. Tests: status-value-rendering test. Definition of Done: test passes.

**Task 05 — Implement the 10 Story Editor Tab Components**
Objective: One component per tab, all reading/writing through `ContentEditorContext`. Dependencies: Task 03. Tests: per-tab field validation tests. Definition of Done: all 10 tabs functional against fixture data.

**Task 06 — Implement Content List Page**
Objective: Browse/search/filter with empty/loading states. Dependencies: Task 02. Tests: empty-state test. Definition of Done: test passes.

**Task 07 — Implement the Story Editor Shell Page**
Objective: Compose tab rail + `VersionStatusIndicator` + 10 tab components + submit-for-review action. Dependencies: Tasks 03–06. Tests: full-session smoke test. Definition of Done: test passes.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm autosave never silently drops an edit; confirm the tab-status indicator is genuinely server-sourced, not locally guessed. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Autosave survives a simulated connectivity blip with zero data loss (mandatory test)
- [ ] Version-status indicator visible and accurate across all 10 tabs
- [ ] Content List renders correct empty/loading states
- [ ] Submit-for-review action correctly transitions the item into B-04's review queue
- [ ] `content_editor` RBAC enforced at the module level

## 20. Definition of Done
Content Editors have a resilient, full-featured 10-tab authoring environment backed by B-01, with autosave that survives real-world connectivity gaps — the primary entry point into E.29's entire review pipeline.
