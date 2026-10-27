# N-06 — Content-Completeness Deadline Tracker

## 1. Feature Context
The human-facing view of the PRD's single hardest, zero-tolerance requirement: 100% scholar approval for all 30 nights at least 3 weeks before the region-adjusted Ramadan start date. This tracker is the operational surface for what the backend already enforces as a P0 alert — it does not introduce a second source of truth, it visualizes the same signal.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
3.6 Content-Completeness Deadline Tracker (ID: **N-06**)

## 4. Objective
Build a read-only checklist sourced from E.29's review-queue status, with a countdown to the hard 3-week deadline and red/amber/green readiness indicators.

## 5. Business Requirements
- §8: Content-Completeness Deadline Tracker (Read-only) — surfaces which content units haven't completed scholar approval ahead of the hard 3-week deadline.
- §9 Admin AI prompt item 6: read-only checklist sourced from E.29's review-queue status, countdown to the hard 3-week deadline, red/amber/green readiness indicators.
- §1.8: content-completeness deadline — system-trackable, not aspirational; zero-tolerance.
- §10 DevOps: Alert (P0) starting at the 3-week-before-Ramadan deadline if any content unit hasn't completed scholar approval, escalating daily until resolved — this tracker is the human-facing counterpart to that same backend alert condition.
- §12.8: the hard, system-tracked content-completeness deadline operationalizes zero-tolerance for skipping scholar review under deadline pressure.

## 6. Existing Architecture
`src/features/ramadan/deadline-tracker/`, reading directly from E.29's existing review-queue status API (per `NEXT-JS-INSTRUCTIONS.md` §3's `CmsRepositoryImpl` pattern) — this module performs no independent approval-tracking logic of its own.

## 7. Existing Code to Reuse
- E.29's review-queue status query (exact hook/repository TBD, confirm before implementation)
- `StatusBadge` (red/amber/green readiness indicator)
- `DataTable`, `LoadingState`, `ErrorView`, `EmptyState`

## 8. Files to Create
- `src/app/(dashboard)/ramadan/deadline-tracker/page.tsx`
- `src/features/ramadan/deadline-tracker/hooks/use-deadline-status.ts`
- `src/features/ramadan/deadline-tracker/components/deadline-countdown-banner.tsx`
- `src/features/ramadan/deadline-tracker/components/readiness-checklist.tsx`

## 9. Files to Modify
- `src/shared/components/dashboard-shell.tsx` — add "Deadline Tracker" nav entry under Ramadan

## 10. NextJS Requirements
- **Page/Route:** `/ramadan/deadline-tracker`, entirely read-only.
- **Component:** `DeadlineCountdownBanner` (days remaining until the region's 3-week-before-Ramadan deadline, prominent when in the red zone); `ReadinessChecklist` (30-row table, one per night, per-region if multi-region is active simultaneously, sourced from E.29's review-queue status, `StatusBadge`-rendered red/amber/green).
- **Readiness logic:** red = unapproved with deadline passed or imminent; amber = unapproved but deadline not yet reached; green = scholar-approved — exact threshold boundaries should mirror whatever the backend's P0 alert logic uses (confirm against §10's DevOps alert configuration rather than inventing independent thresholds, since a mismatch between this display and the actual alert would be actively misleading).
- **Loading/Empty/Error State:** standard shared-component states; a fully-green checklist should read as a positive, unambiguous "content-complete" state, not just an absence of red rows.
- **Accessibility:** readiness status conveyed by icon+text, not color alone (§9's "red/amber/green" requirement must not become a colorblind-inaccessible pattern).

## 11. API Contract
### Proposed Deadline-Status Endpoint (pending confirmation)
Not enumerated in PRD §3.4. Following E.29's existing review-queue pattern (§3 `CmsRepositoryImpl`/`useCmsArticles`) plus the deadline-timestamp concept from §10's backend P0 alert, this blueprint proposes:

`GET /v1/admin/ramadan/content-completeness?region=` → `200 { deadline_at: <ISO 8601 timestamp>, nights: [{ night_number, is_laylatul_qadr, content_version_id, approval_status: "approved"|"pending"|"unassigned", readiness: "green"|"amber"|"red" }] }`
- **Auth:** `get_current_admin`. **Authz:** `require_admin_scope("content_editor")` or `require_admin_scope("product_admin")` — read-only, per §8's CRUD table.
- `readiness` is computed server-side using the exact same threshold logic as §10's DevOps P0 alert (single source of truth for "red") — this endpoint does not duplicate that threshold calculation independently; it is proposed specifically so both the alert and this tracker read from one implementation.
- `deadline_at` is the region's algorithmically-derived "3 weeks before Hijri start date" timestamp (sourced from B-02's Hijri Calendar Service), never computed client-side.

**Mark PROPOSED in code review until a real contract is signed off**, and until the readiness-threshold logic is confirmed to genuinely be shared code with the backend's P0 alert rather than two independently-maintained implementations (see §23's mismatch-risk note, now resolved by this endpoint owning both).

## 12. Database Requirements
N/A directly — reads E.29's content-review tables via the backend API only.

## 13. Validation
N/A — read-only, no forms, no mutation.

## 14. Authentication
Standard Admin Portal session.

## 15. Authorization
`RequirePermission permission="ramadan_deadline_tracker:read"` — behind `content_editor`/`product_admin` per §8, strictly read-only.

## 16. Error Handling
`QueryErrorState` for fetch failures — given this page's role in a zero-tolerance deadline, a fetch failure should be visually distinct from a genuinely-green checklist (never silently render an empty/blank state that could be mistaken for "all clear").

## 17. Localization
Countdown banner, status labels, and checklist copy via `useTranslation()`.

## 18. RTL
Countdown/checklist layout direction-aware.

## 19. Analytics
Consistent with the Admin Portal's existing action-audit pattern if present — this page has no mutating actions to instrument in the first place.

## 20. Performance
30-row (per active region) checklist is a small dataset — no special performance consideration; countdown banner recalculates client-side from a server-supplied deadline timestamp only (never independently computing the Hijri-derived deadline date, mirroring K-01's server-derivation discipline).

## 21. Caching
React Query caching with a short staleness window given this page's operational urgency during the pre-deadline period — shorter `staleTime` than N-05's analytics dashboard, since this data needs to feel current to whoever is watching it close to the deadline.

## 22. Testing
Component tests: `DeadlineCountdownBanner` renders the correct urgency styling as the deadline approaches/passes; `ReadinessChecklist` status badges render correctly for all three states with non-color-dependent accessibility cues. Integration test: a fetch-failure state is visually distinguishable from a genuinely-complete (all-green) state.

## 23. Documentation
Inline JSDoc noting the readiness-threshold logic must mirror the backend's own P0 alert configuration — any change to one requires reviewing the other.

## 24. AI Coding Agent Implementation Steps

**Task 01 — Implement Against the Proposed Deadline-Status Contract**
Objective: Build to §11's proposed shape; flag for a joint frontend/backend contract review before production release. Definition of Done: contract documented in code comments; review flagged in the PR description.

**Task 02 — Confirm the Backend's `readiness` Computation Is Shared, Not Duplicated**
Objective: Ensure the backend endpoint's `readiness` field genuinely reuses §10's DevOps P0 alert threshold logic (single implementation) rather than this frontend independently re-deriving red/amber/green from raw dates. Definition of Done: confirmed the frontend only displays the server-supplied `readiness` value verbatim — no client-side threshold math exists in this module.

**Task 03 — Implement `useDeadlineStatus` Hook**
Objective: Fetch review-queue status + deadline timestamp. Files to Create: `hooks/use-deadline-status.ts`. Dependencies: Task 01. Tests: hook tests. Definition of Done: tests pass.

**Task 04 — Build `DeadlineCountdownBanner`**
Objective: Server-timestamp-derived countdown with urgency styling. Files to Create: `components/deadline-countdown-banner.tsx`. Dependencies: Task 03. Tests: urgency-styling test at multiple day-remaining values. Definition of Done: test passes.

**Task 05 — Build `ReadinessChecklist`**
Objective: Per-night status table with non-color-dependent accessibility. Files to Create: `components/readiness-checklist.tsx`. Dependencies: Task 03, Task 02. Tests: **mandatory** — accessibility (icon+text, not color-alone) test. Definition of Done: test passes.

**Task 06 — Build the Page and Wire Navigation**
Objective: `/ramadan/deadline-tracker` page. Files to Create: `app/(dashboard)/ramadan/deadline-tracker/page.tsx`. Files to Modify: `dashboard-shell.tsx`. Dependencies: Task 04, Task 05. Tests: page integration test. Definition of Done: test passes.

**Task 07 — Verify Fetch-Failure vs. All-Clear Visual Distinction**
Objective: A failed fetch must never resemble a genuinely-green checklist. Dependencies: Task 06. Tests: **mandatory** — failure-vs-success visual distinction test. Definition of Done: test passes.

**Task 08 — Add Localization and Full Test Suite**
Objective: Complete §17/§22 coverage, both mandatory tests included. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm the countdown never independently computes a Hijri-derived date, and thresholds genuinely match the backend's alert configuration. Definition of Done: checklist in §26 checked.

## 25. Definition of Done
Content/Editorial leadership has an unambiguous, accessible, always-current view of exactly which nights stand between the team and its one non-negotiable deadline — with zero chance of a fetch failure being mistaken for success.

## 26. Final Verification Checklist
- [ ] Deadline-status endpoint built against the proposed §11 contract, flagged for real sign-off before production release
- [ ] `readiness` value displayed verbatim from the server, zero client-side threshold computation
- [ ] Status conveyed by icon+text, not color alone — mandatory test passing
- [ ] Fetch-failure state visually distinct from a genuinely-complete state — mandatory test passing
- [ ] Countdown derived entirely from a server-supplied timestamp, never computed client-side
