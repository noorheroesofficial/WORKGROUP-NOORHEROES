# N-02 — Translation Status Dashboard & Coverage-Drop Alert Monitor

## 1. Feature Context
The at-a-glance readiness view for every locale, with the activation-threshold line marked precisely where the server says it is — never a hardcoded visual guess — plus the monitor that flags an already-active locale's coverage regression without ever implying it will be auto-corrected.

## 2. Parent Feature
E.34 — Localization Management

## 3. Sub-feature
2.2 Translation Status Dashboard & Coverage-Drop Alert Monitor (ID: **N-02**)

## 4. Objective
Build the Translation Status Dashboard and Coverage-Drop Alert Monitor screens against B-03, with the activation-threshold marker sourced from the server's configured value.

## 5. Business Requirements
- §1.18 screens 3, 12: Translation Status Dashboard, Coverage-Drop Alert/Stale-Locale Monitor.
- §2.1/§2.2: per-locale progress-bar grid (Missing/Draft/Approved, color-coded), activation-threshold line clearly marked, "Activate" action disabled/explained if below threshold.
- §7 Frontend AI prompt item 4: threshold marker position reflects the server-configured value, not a hardcoded percentage — tested explicitly.
- Edge Case 1: coverage drop on an active locale is flagged, never silently ignored, never auto-corrected by the UI implying otherwise.

## 6. Existing Architecture
`src/features/coverage-dashboard/` module.

## 7. Existing Code to Reuse
- `src/shared/components/data-table.tsx::DataTable` (or a dedicated grid component for the progress-bar layout)
- `src/shared/components/require-permission.tsx::RequirePermission`

## 8. Files to Create
- `src/app/(dashboard)/platform/coverage/page.tsx`
- `src/app/(dashboard)/platform/coverage/alerts/page.tsx`
- `src/features/coverage-dashboard/api/coverage-repository.ts`
- `src/features/coverage-dashboard/hooks/use-coverage-dashboard.ts`, `use-coverage-drop-alerts.ts`
- `src/features/coverage-dashboard/components/locale-coverage-row.tsx`
- `src/features/coverage-dashboard/components/threshold-marker.tsx` — positioned from server-configured value
- `src/features/coverage-dashboard/components/coverage-drop-alert-panel.tsx`
- `src/features/coverage-dashboard/types/coverage.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `COVERAGE.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item under "Platform" group

## 10. NextJS Requirements
- `ThresholdMarker`: computes its visual position (e.g., `left: {threshold_percent}%`) directly from the coverage API response's server-configured threshold value — no fallback to a hardcoded default percentage anywhere in the component.
- `LocaleCoverageRow`: color-coded Missing/Draft/Approved segments; "Activate" action disabled with explanatory text when below threshold (deferring the actual gate check to N-04's activation detail screen, this row is a summary/navigation entry point).
- `CoverageDropAlertPanel`: lists already-active locales whose coverage has dropped, with copy explicitly framed as "flagged for follow-up," never implying automatic correction or deactivation.

## 11. Required API
**Admin API** — B-03: `GET /v1/admin/locales/coverage?locale=`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="localization_manager"`.

## 13. Loading / Empty / Error States
Dashboard loading skeleton; brand-new-locale "Import strings to begin" empty state (0% coverage, §1.12); "No coverage drops" calm empty state for the alert monitor.

## 14. Responsive UI / Accessibility
Progress bar segments and the threshold marker both convey their meaning via accessible text labels in addition to color/position.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
The threshold marker's server-sourced positioning is this screen's defining guarantee — mandatory test confirms the marker's rendered position changes correctly when the mocked API response's threshold value changes, proving no hardcoded fallback exists.

## 17. Testing
Unit: threshold-marker position-from-server-value computation. UI: **mandatory** — marker position reflects the server-configured value across multiple fixture threshold values, never a hardcoded percentage. Integration: full dashboard-load → per-locale-coverage-display flow; coverage-drop alert correctly surfaces without implying auto-correction.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `coverage.ts` schema. Files: `types/coverage.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `CoverageRepositoryImpl`**
Objective: Repository for B-03's coverage endpoint. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `ThresholdMarker` with Server-Sourced Positioning**
Objective: Zero hardcoded fallback. Dependencies: Task 02. Tests: **mandatory** — position-changes-with-server-value test across multiple fixtures. Definition of Done: test passes.

**Task 04 — Implement `LocaleCoverageRow`**
Objective: Color-coded segments, disabled-with-explanation Activate summary action. Dependencies: Task 03. Tests: below-threshold-disabled-state test. Definition of Done: test passes.

**Task 05 — Implement `CoverageDropAlertPanel`**
Objective: Flagged-not-auto-corrected framing. Dependencies: Task 02. Tests: copy-content test confirming no auto-correction implication. Definition of Done: test passes.

**Task 06 — Implement the Dashboard and Alert Pages**
Objective: Compose all components with loading/empty/error states. Dependencies: Tasks 03–05. Tests: full-page smoke tests. Definition of Done: tests pass.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §17, including the mandatory threshold-positioning test. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm zero hardcoded threshold value exists anywhere in this module. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Threshold marker position sourced exclusively from the server's configured value — mandatory test passing across multiple fixtures
- [ ] Coverage-drop alert copy never implies automatic correction or deactivation
- [ ] Brand-new-locale empty state uses the "Import strings to begin" framing
- [ ] `localization_manager` scope enforced

## 20. Definition of Done
Localization managers have an accurate, server-truth-driven readiness dashboard and an honest coverage-drop monitor that flags regressions on active locales without ever overstating the system's automatic remediation.
