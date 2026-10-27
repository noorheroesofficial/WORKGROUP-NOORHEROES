# N-03 — Media Manager (Upload, Safety Pipeline Status, Library)

## 1. Feature Context
The upload/status/library surface fronting B-02's fail-closed safety pipeline. Its defining UI guarantee: a media item can never be selected for attachment to content until the server confirms `status='pass'` — the UI has no override, no "attach anyway," no shortcut.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
2.3 Media Manager (Upload, Safety Pipeline Status, Library) (ID: **N-03**)

## 4. Objective
Build the media Upload flow (Uploading → Scanning → Transcoding → Ready|Quarantined), the Quarantine Detail view, and the Library (browse, CDN purge, emergency disable) against B-02, with attachment-selection structurally gated on `status='pass'`.

## 5. Business Requirements
- FR-4: multipart upload, virus scanning, transcoding/thumbnail jobs, loudness normalization, caption validation, audio-track mapping, rights/license fields, CDN purge, emergency disable.
- §7 frontend AI-prompt requirement #2: never allow a "Ready" media item to be selectable for attachment until the server confirms `status='pass'`.

## 6. Existing Architecture
`src/features/media-manager/` module, embeddable within N-01's Media Timeline tab and as a standalone "Media" navigation surface.

## 7. Existing Code to Reuse
- `src/shared/components/data-table.tsx::DataTable`
- `src/shared/components/loading-state.tsx::LoadingState`
- `src/shared/components/require-permission.tsx::RequirePermission`

## 8. Files to Create
- `src/app/(dashboard)/media/page.tsx` — Library
- `src/app/(dashboard)/media/upload/page.tsx` — Upload flow
- `src/features/media-manager/api/media-repository.ts`
- `src/features/media-manager/hooks/use-media-upload.ts`, `use-media-status-poll.ts`, `use-media-library.ts`
- `src/features/media-manager/components/safety-pipeline-status.tsx` — Uploading → Scanning → Transcoding → Ready|Quarantined stepper
- `src/features/media-manager/components/quarantine-detail.tsx`
- `src/features/media-manager/components/media-picker.tsx` — attachment-selection component, embedded elsewhere (N-01's Media Timeline tab)
- `src/features/media-manager/types/media-asset.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `MEDIA_MANAGER.*` endpoints
- `src/features/content-cms/components/story-editor-tabs/MediaTimelineTab.tsx` (N-01) — uses `MediaPicker` for attachment

## 10. NextJS Requirements
- `useMediaStatusPoll()`: polls `GET /v1/admin/media/{id}/status` after upload until a terminal state (`pass`/`quarantined`) is reached, driving `SafetyPipelineStatus`'s stepper UI.
- `MediaPicker`: the **only** component through which media gets attached to content elsewhere in the app — its selectable-item list is filtered to `status='pass'` at the query level (not merely visually greyed-out for other statuses); a `pending`/`quarantined` item is structurally absent from the selectable set.
- `QuarantineDetail`: shows the quarantine reason plainly, no dead-end — a clear "Re-upload" CTA back to the Upload flow.
- CDN purge / emergency disable actions in the Library, permission-gated to safety roles for the emergency-disable action specifically.

## 11. Required API
**Admin API** — B-02: `POST /v1/admin/media`, `GET /v1/admin/media/{id}/status`, `POST /v1/admin/media/{id}/purge-cdn`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="content_editor"` for upload/library; emergency-disable additionally requires a safety-role check.

## 13. Loading / Empty / Error States
Upload progress state; empty Library state; polling-timeout error state (pipeline taking unusually long) distinct from a hard failure.

## 14. Responsive UI / Accessibility
Status stepper conveyed with text labels at each stage, not icon/color alone; Library grid responsive with a list-view fallback for accessibility.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
The attachment-selection gate (`status='pass'` only) is this module's single most important UI-level guarantee, mirrored from B-02's server-side exclusion — explicitly tested to confirm the UI cannot be tricked into offering a non-passed item.

## 17. Testing
Unit: status-polling terminal-state detection, quarantine-reason display. UI: **mandatory** — a media item in `pending` or `quarantined` state cannot be attached to a content draft via the `MediaPicker` UI (per PRD frontend AI-prompt requirement #2). Integration: full upload → poll → pass → attach flow; full upload → poll → quarantine → re-upload flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `media-asset.ts` schema. Files: `types/media-asset.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `MediaRepositoryImpl`**
Objective: Repository for upload/status/purge endpoints. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `useMediaStatusPoll` and `SafetyPipelineStatus`**
Objective: Polling hook + stepper UI. Dependencies: Task 02. Tests: terminal-state-stops-polling test. Definition of Done: test passes.

**Task 04 — Implement `MediaPicker` with Server-Filtered Selection**
Objective: Attachment-selection component whose query itself filters to `status='pass'`. Dependencies: Task 02. Tests: **mandatory** — pending/quarantined-cannot-be-attached UI test. Definition of Done: test passes.

**Task 05 — Implement `QuarantineDetail`**
Objective: Reason display + re-upload CTA. Dependencies: Task 02. Tests: reason-rendering test. Definition of Done: test passes.

**Task 06 — Implement Library Page with CDN Purge / Emergency Disable**
Objective: Browse, purge, safety-role-gated disable. Dependencies: Task 02. Tests: role-gating test on emergency disable. Definition of Done: test passes.

**Task 07 — Wire `MediaPicker` into N-01's Media Timeline Tab**
Objective: Confirm reuse, not duplication. Dependencies: N-01. Definition of Done: single source of attachment-selection logic across the app.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §17, including the mandatory attachment-gating test. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm the attachment-selection gate is query-level (server-filtered), not a client-side visual-only filter. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Media items in `pending`/`quarantined` state are structurally absent from the `MediaPicker`'s selectable set, not merely greyed out
- [ ] Status stepper correctly reflects Uploading → Scanning → Transcoding → Ready|Quarantined
- [ ] Quarantine Detail shows the reason plainly with a clear re-upload path
- [ ] CDN purge and emergency-disable actions function correctly, emergency-disable role-gated
- [ ] `MediaPicker` is the single reused attachment-selection component across the app (no duplicate implementation in N-01)

## 20. Definition of Done
Media upload, safety-pipeline status, and library management are fully functional with a structurally enforced, server-filtered attachment-selection gate mirroring B-02's fail-closed guarantee at the UI layer.
