# N-05 — Billing-Content Safety Audit Log Viewer

## 1. Feature Context
NoorHeroes Admin Portal (NextJS). Read-only visibility for Trust & Safety into the continuous verification of FR-9 (zero billing content ever reaches a child) — surfaces both CI-run results and production-sampling audit results from B-08.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
3.5 Billing-Content Safety Audit Log Viewer (ID: N-05)

## 4. Objective
Build a read-only, paginated table of content-safety-audit run results (pass/fail, timestamp, commit SHA, failing blocklist terms, sample size, override metadata) sourced from B-08's `safety_audit_run` table, restricted to the `trust_safety` RBAC role.

## 5. Business Requirements
Per PRD §8, §9 item 5, §12.5:
- Read-only paginated table of CI test run results (pass/fail, timestamp, commit SHA, any failing blocklist terms found).
- Restricted to the `trust_safety` RBAC role.
- Also surfaces production-sampling audit runs (per B-08 §10), not just CI runs.

## 6. Existing Architecture
Follow `NEXT-JS-INSTRUCTIONS.md` conventions; consumes B-08's `GET /admin/v1/home/safety-audit-runs` endpoint (B-08 §13).

## 7. Existing Code to Reuse
Existing Admin Portal RBAC route-guard pattern (shared with N-03's `trust_safety` gating — consider extracting a shared `TrustSafetyGuard` component if N-03 hasn't already established one, to avoid duplicating the same RBAC logic twice).

## 8. Files to Create
- `app/(admin)/safety-audit-log/page.tsx`
- `components/safety-audit-log/AuditRunTable.tsx`
- `components/safety-audit-log/AuditRunDetailModal.tsx`
- `lib/api/safetyAuditLog.ts`
- `types/safetyAuditLog.ts`

## 9. Files to Modify
- Admin navigation/sidebar config (visible only to `trust_safety` role)

## 10. Backend Requirements
Consumes `GET /admin/v1/home/safety-audit-runs` (owned by B-08). No backend code written here.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Paginated table: `run_type` (CI/production_sample), `pass`/`fail` status badge, `timestamp`, `commit_sha`, `sample_size`, and an expandable detail view showing `failing_terms` when `pass=false`.
- Filter by date range and pass/fail status.
- Detail modal/expansion showing override metadata (`override_by`, `override_reason`) when present, making any emergency bypass fully visible/auditable to Trust & Safety.
- Strictly read-only — no action buttons beyond viewing/filtering/paginating.
- Route restricted to `trust_safety` role, including direct-URL-access blocking.

## 13. API Contract
**Admin API (read-only):**
`GET /admin/v1/home/safety-audit-runs?from=...&to=...&pass=...&page=...` — Auth: Admin Bearer, `trust_safety` role required — Response: paginated `safety_audit_run` records per B-08 §14 schema.

## 14. Database Requirements
Reads `safety_audit_run` (owned by B-08's migration). No writes from this sub-feature.

## 15. Validation
Date-range/status filter inputs validated client-side before constructing the API request.

## 16. Authentication
Existing Admin Portal Bearer-session auth.

## 17. Authorization
Strictly `trust_safety` role, matching B-08's endpoint restriction and N-03's pattern — reuse the same RBAC guard component if one was established in N-03 for consistency.

## 18. Error Handling
Empty state (no runs yet — distinct message from an error); error state (API failure, retry-capable, no raw stack trace); a highlighted/urgent visual treatment for any `pass=false` row, especially production-sample failures (these represent the most severe possible finding for the entire A.2 feature).

## 19. Offline First
Not applicable (admin web portal).

## 20. Local Data
Not applicable.

## 21. Localization
Admin Portal UI chrome localized per existing convention; `failing_terms`/audit data displayed as-is (raw investigative/compliance data).

## 22. RTL
Per existing Admin Portal RTL support convention.

## 23. Analytics
Not specified as required; skip unless existing admin-tooling convention requires internal usage instrumentation. Note: viewing this log is itself somewhat sensitive (compliance data) — confirm whether the platform's audit-logging convention (as applied in N-03) should also apply here; if B-08/platform conventions require it, add the same view-audit-logging pattern established in N-03 rather than skip it silently.

## 24. Performance
Server-side pagination for the audit-run table as history accumulates (especially with a nightly production-sampling job continuously adding rows per B-08).

## 25. Security
Strict `trust_safety`-only access; this page is the visibility layer for the platform's single highest-severity risk control (FR-9) — any bug here that hides a failing run from visibility would undermine the entire audit system's value, so error states must never silently swallow/hide failing-run data.

## 26. Library Requirements
Next.js, existing Admin Portal table/pagination libraries.

## 27. Testing
- Component test: table renders CI and production-sample runs correctly, with clear visual distinction for `pass=false` rows.
- Component test: detail view correctly surfaces `failing_terms` and override metadata when present.
- Integration test: direct URL access blocked for non-`trust_safety` roles.
- Integration test: filter (date range, pass/fail) correctly narrows results via the API.
- Component test: confirms zero action/mutation buttons exist anywhere on this page.

## 28. Documentation
Page-level documentation stating this is the visibility layer for B-08's zero-tolerance billing-content-safety guarantee, and that any bug hiding a failing run here is a P0-severity issue in its own right.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Types & API Client (Read-Only)**
- Objective: Typed contract for the safety-audit-run read API.
- Why Required: Foundation for the table/detail components.
- Existing Architecture to Follow: Existing admin-portal API-client conventions; reuse N-03's read-only-client pattern as a template if useful.
- Existing Files to Reuse: Existing typed-fetch wrapper.
- Files to Create: `types/safetyAuditLog.ts`, `lib/api/safetyAuditLog.ts`
- Files to Modify: none
- Implementation Details: `SafetyAuditRun { runId, timestamp, commitSha, runType, pass, failingTerms, sampleSize, overrideBy, overrideReason }`; `getSafetyAuditRuns(filters, page)`.
- Business Rules: Read-only client, no mutation methods.
- Validation: Filter param validation.
- Error Handling: Typed error results.
- Security: No mutation capability by design.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Unit tests for the API client (mocked fetch).
- Documentation: TSDoc.
- Dependencies: B-08's `GET /admin/v1/home/safety-audit-runs` endpoint.
- Do Not Change: N/A.
- Expected Result: Typed read-only client.
- Definition of Done: Unit tests pass.

**Task 02 — Build `AuditRunTable` with Pass/Fail Visual Treatment**
- Objective: Primary paginated, filterable table.
- Why Required: Core deliverable.
- Existing Architecture to Follow: Existing admin table/pagination conventions.
- Existing Files to Reuse: Existing generic table component if present.
- Files to Create: `components/safety-audit-log/AuditRunTable.tsx`
- Files to Modify: none
- Implementation Details: Server-side pagination; status badge (pass=green, fail=red/urgent); filter controls for date range and pass/fail.
- Business Rules: Failing rows must be visually unmistakable, especially production-sample failures.
- Validation: Filter input validation.
- Error Handling: Empty/error states distinct.
- Security: N/A.
- Performance: Server-side pagination.
- Localization: Column headers localized.
- RTL: Per §22.
- Analytics: N/A.
- Tests: Component tests for rendering, filtering, pagination, and pass/fail visual distinction.
- Documentation: TSDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working table.
- Definition of Done: Component tests pass.

**Task 03 — Build `AuditRunDetailModal` + Page Assembly with RBAC Guard**
- Objective: Detail view for failing_terms/override metadata, and full page with strict role gating.
- Why Required: Complete investigative detail + PRD's `trust_safety`-restriction requirement.
- Existing Architecture to Follow: Existing Admin Portal RBAC route-guard (reuse N-03's guard component if established).
- Existing Files to Reuse: RBAC guard, Task 01/02 outputs.
- Files to Create: `components/safety-audit-log/AuditRunDetailModal.tsx`, `app/(admin)/safety-audit-log/page.tsx`
- Files to Modify: Admin navigation config (visible to `trust_safety` only)
- Implementation Details: Modal/expansion shows `failing_terms` list and `override_by`/`override_reason` when present, making bypass usage fully visible; page composes table + filters + modal, wrapped in the `trust_safety`-only route guard.
- Business Rules: Strictly read-only, zero action buttons.
- Validation: N/A.
- Error Handling: Per §18, with emphasis on never silently hiding failing-run data on error.
- Security: `trust_safety`-only gate; this is the core requirement.
- Performance: N/A.
- Localization: Labels localized.
- RTL: Per §22.
- Analytics: Confirm/apply view-audit-logging per §23 if platform convention requires it (following N-03's precedent).
- Tests: Component test confirming zero mutation controls exist; integration test for RBAC route-guard blocking non-`trust_safety` roles via direct URL; integration test for override-metadata visibility.
- Documentation: Page comment per §28.
- Dependencies: Tasks 01, 02.
- Do Not Change: Never add mutation capability to this page.
- Expected Result: Complete, strictly read-only, `trust_safety`-gated audit log viewer.
- Definition of Done: All tests pass, including the RBAC-bypass-attempt test.

## 30. Definition of Done
Trust & Safety staff can view, filter, and paginate through the complete history of CI and production-sampling safety-audit runs, with failing runs and any bypass usage fully visible, under strict `trust_safety`-only access; all tests green.

## 31. Final Verification Checklist
- [ ] Table correctly renders both CI and production-sample run types
- [ ] Failing runs are visually unmistakable, especially production-sample failures
- [ ] Override (`override_by`/`override_reason`) metadata fully visible when present
- [ ] Direct URL access blocked for non-`trust_safety` roles
- [ ] Zero mutation/action controls exist anywhere on this page
- [ ] Pagination and filters (date range, pass/fail) function correctly
- [ ] All tests pass

---

**All 21 development blueprints for Feature A.2 (Child Home Dashboard & AI Personalization) are now complete:**
Backend B-01–B-08, KMP K-01–K-08, NextJS Admin N-01–N-05, saved under
`Development_Blueprints/A2_Home_Dashboard_AI_Personalization/{Backend,KMP,NextJS_Admin}/`.
