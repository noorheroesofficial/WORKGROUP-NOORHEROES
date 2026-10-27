# N-01 — Story & Episode Content Editor

## 1. Feature Context
The primary content-editorial surface: a series-and-episode tree with a per-episode form covering unlock configuration, bedtime eligibility, and a choice-point builder that hard-caps at 3 options — mirroring the same cap enforced server-side (B-11) and in the Android player (K-04). Delete is always "Archive"; no real delete button exists anywhere on this page.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
3.1 Story & Episode Content Editor (ID: **N-01**)

## 4. Objective
Build the series/episode tree view and detail editor form against B-11's admin content API, with a structured `unlock_threshold_config` sub-form, a hard-capped choice-point builder, and a draft → pending_review → published version workflow.

## 5. Business Requirements
- §8: series-and-episode tree, per-episode detail form (metadata, `unlock_threshold_config` structured sub-form supporting all three modes, `is_bedtime_eligible` toggle, choice-point builder hard-capped at 3).
- §9: "Add option" button disables itself with a tooltip once 3 options exist. Submitting a new version → `status=pending_review`; only an approved version → `status=published`. Delete relabeled "Archive", sets `status=archived` only — no real delete button anywhere.
- CRUD permissions: full CRUD (delete = archive only) behind `content_editor` role.

## 6. Existing Architecture
`src/features/story-content/` module, following the existing `BaseResourceClient`/`DataTable`/`RequirePermission` pattern established elsewhere in the Admin Portal.

## 7. Existing Code to Reuse
- `src/shared/api/base-resource-client.ts::BaseResourceClient`
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/data-table.tsx::DataTable`
- `src/shared/components/confirmation-dialog.tsx::ConfirmationDialog` (repurposed for "Archive" confirmation, not delete)
- `src/shared/hooks/use-pagination-state.ts::usePaginationState`
- `src/shared/hooks/use-debounced-value.ts`

## 8. Files to Create
- `src/app/(dashboard)/stories/series/page.tsx` — series/episode tree view
- `src/app/(dashboard)/stories/series/[episodeId]/page.tsx` — episode detail editor
- `src/features/story-content/api/story-content-repository.ts` — `StoryContentRepositoryImpl`
- `src/features/story-content/hooks/use-story-series.ts`, `use-episode-detail.ts`, `use-submit-episode-version.ts`
- `src/features/story-content/components/series-episode-tree.tsx`
- `src/features/story-content/components/unlock-threshold-config-form.tsx` — structured sub-form for the three modes
- `src/features/story-content/components/choice-point-builder.tsx` — hard-capped at 3 options
- `src/features/story-content/components/version-history-diff.tsx`
- `src/features/story-content/types/story-episode.ts` — Zod schemas

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `STORY_CONTENT.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item gated by `content_editor`

## 10. NextJS Requirements
- `ChoicePointBuilder`: "Add option" button structurally disables itself (not just visually) once `options.length === 3`, with a tooltip explaining the cap — the underlying form state (Zod schema `.max(3)`) makes a 4th option unrepresentable, not merely UI-hidden.
- `UnlockThresholdConfigForm`: renders a different sub-form per selected mode (`playback_percentage` → percentage slider/input; `final_interaction` → choice-point selector; `quiz_completion` → quiz-linkage selector) — a discriminated-union Zod schema backing the form.
- Archive action: the only "delete"-shaped affordance on the page is labeled "Archive", requires confirmation via `ConfirmationDialog`, and calls `POST .../archive` — no `DELETE` HTTP call exists anywhere in this module's repository.
- Version submission: "Submit for Review" button moves the draft to `pending_review`; "Publish" button is disabled (not hidden) until the version's approval status (read from the API response) allows it, with a tooltip explaining why if disabled.

## 11. Required API
**Admin API** — B-11: `POST /v1/admin/content/series`, `POST /v1/admin/content/series/{series_id}/episodes`, `PATCH /v1/admin/content/episodes/{episode_id}`, `POST /v1/admin/content/episodes/{episode_id}/submit-review`, `POST /v1/admin/content/episodes/{episode_id}/publish`, `POST /v1/admin/content/episodes/{episode_id}/archive`, `GET /v1/admin/content/episodes/{episode_id}/versions`.

## 12. Authentication / Authorization
`useAdminSession()` for base auth; `RequirePermission permission="content_editor"` gating the entire page tree; every mutating button additionally disabled (not just server-rejected) for users lacking the permission, per the existing defense-in-depth convention.

## 13. Loading / Empty / Error States
Tree-loading skeleton; empty state for a series with zero episodes yet ("Add your first episode"); form-validation error states inline per field; submission-failure error state with retry, distinct from a validation error.

## 14. Responsive UI / Accessibility
Tree view collapses to an accordion on narrow viewports; choice-point builder's option cards are keyboard-navigable and screen-reader-labeled with their position ("Option 1 of 3").

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`; form field order and tree indentation mirror in RTL admin locales if the Admin Portal supports RTL locales (confirm against existing Admin Portal localization scope before assuming — if Admin is EN-only, note this explicitly and skip RTL work).

## 16. Security
- `content_editor` RBAC enforced via `RequirePermission` at the page level and per-mutating-control level (defense in depth with B-11's API-level enforcement).
- No delete capability exists in this module's UI or repository layer — architecturally mirrors B-11's backend guarantee.

## 17. Testing
Unit: choice-point 3-option cap (schema-level, cannot construct a 4th), unlock-config discriminated-union validation per mode, publish-button-disabled-until-approved logic. Integration: full draft → submit-review → (mocked approval) → publish flow; archive confirmation flow; zero-`DELETE`-call assertion across the module.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schemas & Add API Endpoints**
Objective: `story-episode.ts` with the discriminated-union `unlock_threshold_config` schema and `.max(3)` choice-point options schema. Files: `types/story-episode.ts`, `api-endpoints.ts`. Tests: schema rejects a 4th option and an unrecognized unlock-config shape. Definition of Done: both rejection tests pass.

**Task 02 — Implement `StoryContentRepositoryImpl`**
Objective: Repository wrapping `apiClient` for all seven B-11 endpoints, with no `delete()` method defined at all. Follow: `BaseResourceClient` conventions. Tests: mocked-fetch tests per endpoint. Dependencies: Task 01. Definition of Done: repository has zero delete-shaped method.

**Task 03 — Implement Data Hooks**
Objective: `useStorySeries`, `useEpisodeDetail`, `useSubmitEpisodeVersion` (React Query). Follow: existing hook conventions. Dependencies: Task 02. Tests: covered by Task 08. Definition of Done: hooks wired to repository correctly.

**Task 04 — Implement `SeriesEpisodeTree`**
Objective: Collapsible tree with lock/status indicators per episode. Dependencies: Task 03. Tests: empty-series-state test. Definition of Done: test passes.

**Task 05 — Implement `UnlockThresholdConfigForm`**
Objective: Mode-switching structured sub-form. Dependencies: Task 01. Tests: per-mode validation tests. Definition of Done: tests pass.

**Task 06 — Implement `ChoicePointBuilder` with Hard Cap**
Objective: "Add option" disables at 3, tooltip shown, schema-enforced. Dependencies: Task 01. Tests: cap-enforcement test (schema and UI-disabled-state both). Definition of Done: test passes, matches K-04/B-11's identical constraint.

**Task 07 — Implement `VersionHistoryDiff` and Submit/Publish/Archive Controls**
Objective: Version history view, submit-for-review, publish (disabled until approved), archive-with-confirmation. Dependencies: Tasks 03, 06. Tests: publish-disabled-until-approved test, archive-confirmation-flow test. Definition of Done: tests pass.

**Task 08 — Implement the Two Pages**
Objective: Tree page + detail editor page composing all components above with loading/empty/error states. Dependencies: Tasks 04–07. Definition of Done: full-page smoke tests against a mocked API pass.

**Task 09 — Add Full Test Suite**
Objective: Complete coverage per §17, including the zero-`DELETE`-call module-wide assertion. Definition of Done: all green in CI.

**Task 10 — Final Code Review**
Objective: Confirm no delete-shaped affordance or API call exists anywhere in the module; confirm the choice-point cap and unlock-config validation exactly mirror B-11/K-04's constraints. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Choice-point builder cannot represent a 4th option at the schema level, not just visually disabled
- [ ] Unlock-threshold config form correctly branches per mode with validated shapes
- [ ] "Publish" disabled (with explanatory tooltip) until the version is approved
- [ ] "Archive" is the only removal affordance anywhere in the module — zero `DELETE` HTTP calls exist
- [ ] `content_editor` RBAC enforced at both page and per-control level
- [ ] Version history/diff view renders correctly
- [ ] Full draft → pending_review → published flow works end-to-end against B-11

## 20. Definition of Done
Content editors can fully manage the story/episode catalog through a versioned, archive-only editor whose choice-point cap and unlock-config validation exactly mirror the backend (B-11) and Android (K-04) constraints, with zero delete capability anywhere in the UI.
