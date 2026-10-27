# N-01 — Bedtime Content Tagging in Episode Editor

## 1. Feature Context
Two additive fields on A.3's existing Content/Episode Editor (N-01 in A.3's numbering) that let content editors specify which dua/reflection card an episode ends with in Bedtime Mode, and optionally override the default fade-out duration — no new standalone admin page.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
3.1 Bedtime Content Tagging in Episode Editor (ID: **N-01**)

## 4. Objective
Extend A.3's existing episode detail form with a `dua_ending_ref` searchable reference picker and an optional `recommended_fade_duration_seconds` numeric override, wired to B-02's manifest-consuming fields — additive changes to the existing form/API only.

## 5. Business Requirements
- §8 Admin Requirements: "Bedtime Content Tagging Tool: Within the existing Content/Episode Editor, add fields: `dua_ending_ref`, `recommended_fade_duration_seconds` override. CRUD: Update-only additions to the existing content editor (no new standalone page required)."
- §9 (Admin AI prompt item 1): `dua_ending_ref` is a searchable reference picker into the Dua content library, nullable; `recommended_fade_duration_seconds` numeric, defaults to the global config value of 15 if left blank.
- CRUD permissions: Update-only, behind the existing `content_editor` role (part of A.3's content editor permissions) — no new role introduced.

## 6. Existing Architecture
A.3's `src/features/story-content/` module (its Episode Detail Editor page, per A.3's own N-01 blueprint) already exists with `BaseResourceClient`/`RequirePermission`/form-validation conventions established. This sub-feature adds two fields to that existing form and its backing Zod schema/API client — it does not create a new page, module, or repository.

## 7. Existing Code to Reuse
- A.3's `src/app/(dashboard)/stories/series/[episodeId]/page.tsx` (episode detail editor page) — modify, do not fork
- A.3's `src/features/story-content/api/story-content-repository.ts::StoryContentRepositoryImpl` — extend the existing `PATCH` call's payload shape
- A.3's `src/features/story-content/types/story-episode.ts` — extend the existing Zod schema
- A shared reference-picker component (confirm the existing searchable-reference-picker pattern used elsewhere in the Admin Portal, e.g., for linking related content, and reuse it for the dua-content search — do not build a new picker component if one already exists)
- `src/shared/components/require-permission.tsx::RequirePermission`

## 8. Files to Create
- `src/features/story-content/components/dua-ending-ref-picker.tsx` (only if no existing generic reference-picker component can be reused as-is; prefer extending/reusing an existing one)

## 9. Files to Modify
- `src/features/story-content/types/story-episode.ts` — add `dua_ending_ref: z.string().nullable()`, `recommended_fade_duration_seconds: z.number().min(1).max(300).nullable()` to the episode Zod schema
- `src/app/(dashboard)/stories/series/[episodeId]/page.tsx` — render the two new form fields within the existing episode detail form
- `src/features/story-content/api/story-content-repository.ts` — include the two new fields in the existing `updateEpisode()` payload (additive, no new method)
- `src/shared/constants/api-endpoints.ts` — no change expected (reuses A.3's existing `PATCH /v1/admin/content/episodes/{episode_id}`, extended server-side by B-02's coordination note — confirm the admin `PATCH` endpoint's schema has been extended to accept these fields before wiring the client, coordinating with the backend team if B-02's episode-schema extension has not yet landed)

## 10. NextJS Requirements
- `dua_ending_ref` field: rendered as a searchable reference picker into the Dua content library (nullable — a content item can have no bedtime ending configured, in which case the manifest field is simply `null` and K-04 falls back to a generic dua per its own default-handling, confirmed against B-02/K-04's null-handling behavior).
- `recommended_fade_duration_seconds` field: numeric input, placeholder/helper text indicating "defaults to 15s if left blank," validated 1–300 range (sane bounds preventing a nonsensical fade duration).
- Both fields are additive to the existing form — no new tab, section, or page; they slot into the existing episode metadata section of A.3's editor.
- Save behavior: uses the existing form's save/validation flow (draft → pending_review → published per A.3's existing versioning workflow) — these two fields are treated identically to any other episode metadata field for versioning purposes, no special-cased save path.

## 11. Required API
**Admin API** — A.3's existing `PATCH /v1/admin/content/episodes/{episode_id}`, extended (coordinate with backend) to accept `dua_ending_ref` and `recommended_fade_duration_seconds` in its request body.

## 12. Authentication / Authorization
Reuses A.3's existing `useAdminSession()` and `RequirePermission permission="content_editor"` gating at the page level — no new permission introduced for these two fields.

## 13. Loading / Empty / Error States
- Reference picker: loading state while searching the Dua content library; empty state ("No matching dua content found") if a search yields no results.
- Numeric field: inline validation error if outside the 1–300 range.
- Save failure: reuses the existing form's save-failure error state and retry affordance.

## 14. Responsive UI / Accessibility
Both new fields follow the existing form's responsive grid and accessibility labeling conventions (label association, error-message `aria-describedby`) — no new layout pattern introduced.

## 15. Localization / RTL
Field labels/helper text via the existing `useTranslation()` hook; confirm against A.3's existing localization scope for the Admin Portal (per A.3's own N-01 note: confirm whether Admin supports RTL locales before assuming — if EN-only, this is explicitly noted rather than silently skipped).

## 16. Security
No new security surface — `content_editor` RBAC enforced identically to every other field in the existing episode form; no new endpoint or elevated permission introduced.

## 17. Testing
Unit: Zod schema validation for both new fields (nullable `dua_ending_ref`, bounded `recommended_fade_duration_seconds`). Integration: form save round-trip including the two new fields against a mocked `PATCH` response; reference-picker search-and-select flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Extend the Episode Zod Schema**
Objective: Add `dua_ending_ref` and `recommended_fade_duration_seconds` to A.3's existing schema. Files to modify: `types/story-episode.ts`. Tests: schema validation tests for both fields (null-allowed, range-bounded). Definition of Done: tests pass, no existing schema field affected.

**Task 02 — Confirm/Coordinate Backend `PATCH` Endpoint Extension**
Objective: Verify A.3's admin episode `PATCH` endpoint accepts the two new fields (coordinated with B-02's backend work); if not yet landed, flag as a blocking dependency rather than proceeding with a client that calls a non-existent field. Definition of Done: confirmed either via API contract or a direct check against the backend team/OpenAPI schema.

**Task 03 — Reuse or Build the Dua Reference Picker**
Objective: Confirm an existing generic reference-picker component in the Admin Portal; reuse it configured for the Dua content library, or build `dua-ending-ref-picker.tsx` only if no reusable component exists. Dependencies: Task 01. Tests: search-and-select flow test. Definition of Done: test passes; component reuse decision documented.

**Task 04 — Add the Fade-Duration Numeric Field**
Objective: Bounded numeric input with helper text. Files to modify: episode detail page. Dependencies: Task 01. Tests: range-validation UI test. Definition of Done: test passes.

**Task 05 — Wire Both Fields into the Existing Save Flow**
Objective: Fields included in the existing `updateEpisode()` payload, versioned identically to other metadata. Files to modify: `story-content-repository.ts`, episode detail page. Dependencies: Task 01–04. Tests: save round-trip integration test. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm no new page/module was created — both fields live entirely within A.3's existing editor; confirm `content_editor` RBAC unchanged. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] `dua_ending_ref` and `recommended_fade_duration_seconds` render within A.3's existing episode form — no new page created
- [ ] `dua_ending_ref` is a searchable, nullable reference picker into the Dua content library
- [ ] `recommended_fade_duration_seconds` validated 1–300, helper text indicates the 15s default
- [ ] Both fields save via the existing versioned draft → pending_review → published workflow
- [ ] `content_editor` RBAC unchanged — no new permission introduced
- [ ] Backend `PATCH` endpoint confirmed to accept both fields before client wiring completed

## 20. Definition of Done
Content editors can tag any episode with a Bedtime dua-ending reference and an optional fade-duration override directly within A.3's existing episode editor, with zero new pages, endpoints, or permissions introduced.
