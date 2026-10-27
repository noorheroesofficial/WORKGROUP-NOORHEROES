# B-03 — Translation Coverage & Dual-Gate Locale Activation Service

## 1. Feature Context
The service that turns locale activation into a genuinely enforced publishing gate rather than a manual checklist item — requiring both sufficient coverage percentage AND full review-stage completeness, neither alone sufficient, so a locale that merely looks complete by raw percentage can never be activated if its covered strings haven't actually finished review.

## 2. Parent Feature
E.34 — Localization Management

## 3. Sub-feature
1.3 Translation Coverage & Dual-Gate Locale Activation Service (ID: **B-03**)

## 4. Objective
Build `GET /v1/admin/locales/coverage`, `POST /v1/admin/locales/{code}/activate`, and `POST /v1/admin/locales/{code}/deactivate`, with activation enforcing a dual gate and deactivation triggering a graceful existing-user fallback rather than an abrupt cutoff.

## 5. Business Requirements
- FR-4: a locale cannot be activated below a configurable translation-coverage threshold, enforced at the service layer.
- FR-5 (dual-gate, Edge Case 7): coverage percentage AND review-stage completeness both required — a locale with 95% raw coverage but several required strings still in draft must still be rejected.
- Edge Case 1: coverage dropping below threshold on an already-active locale does NOT trigger auto-deactivation — only a dashboard flag/alert.
- Edge Case 5: deactivating a locale triggers a graceful existing-user fallback (e.g., to English), not an abrupt cutoff.

## 6. Existing Architecture
`localization` bounded context, `app/localization/routers/locale_activation_router.py`.

## 7. Existing Code to Reuse
- B-01's `locale_string_version` schema (read for coverage computation)
- E.28's `AuditLogService.log_action()`
- Cross-ref E.28's general job-failure/alerting pattern for the coverage-drop alert

## 8. Files to Create
- `app/localization/routers/locale_activation_router.py`
- `app/localization/services/locale_activation_service.py`
- `app/localization/repositories/coverage_repository.py`
- `app/localization/schemas/locale_activation_schema.py`
- `app/localization/monitoring/coverage_drop_monitor.py` — scheduled check for already-active locales dropping below threshold

## 9. Files to Modify
- `app/localization/routers/__init__.py` — register router

## 10. Backend Requirements
- `CoverageRepository.compute()`: counts total/missing/draft/approved keys per locale, returns `coverage_percent`.
- `LocaleActivationService.activate()`: evaluates BOTH gates independently — `coverage_percent >= threshold` AND every in-scope string's current best version is `status='published'` — rejects with `409 COVERAGE_BELOW_THRESHOLD` or a distinct `409 REVIEW_INCOMPLETE` (or a combined structured response identifying which gate(s) failed) if either fails; activates only when both pass.
- `LocaleActivationService.deactivate()`: sets `locale.active=false` and triggers a graceful existing-user fallback transition — this is a distinct, more careful code path than routine string-level fallback (B-02), since it affects users currently mid-session on that locale, not just a missing individual key.
- `CoverageDropMonitor`: scheduled job flagging (never auto-deactivating) an already-active locale whose coverage has dropped below threshold, per Edge Case 1.

## 11. Required API / API Contract
`GET /v1/admin/locales/coverage?locale=` → `200 { "locale", "total_keys", "missing", "draft", "approved", "coverage_percent" }`.
`POST /v1/admin/locales/{code}/activate` → `200` or `409` (gate-specific rejection).
`POST /v1/admin/locales/{code}/deactivate` → `200`.

## 12. Database Requirements
Reads `locale_string`/`locale_string_version` (B-01); writes `locale.active`, `locale.activated_at`.

## 13. Validation
`threshold` sourced from configuration (per-locale or global, confirm against PRD — default to a configurable global threshold with optional per-locale override).

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`require_admin_scope("localization_manager")` for activate/deactivate; coverage read may extend to broader read visibility if needed (default to `localization_manager`+).

## 16. Error Handling
`409 COVERAGE_BELOW_THRESHOLD`, `409 REVIEW_INCOMPLETE` (or combined) — both must be independently testable failure modes.

## 17. Security
The dual-gate requirement is this sub-feature's defining guarantee — mandatory tests confirm each gate fails independently (coverage-sufficient-but-review-incomplete rejected; review-complete-but-coverage-insufficient rejected) and a third test confirms activation succeeds only when both pass simultaneously.

## 18. Analytics
`locale_activation_attempted`, `locale_activation_blocked_coverage` (internal), `locale_activated`, `locale_deactivated`, `coverage_drop_alert_shown` per §1.19.

## 19. Performance
Coverage computation indexed on `(locale_code)`; cached with a short TTL if computation cost warrants (confirm against expected string-table size).

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async. No new libraries.

## 21. Testing
Unit: coverage-percent computation. Integration: **mandatory** — coverage-sufficient-but-review-incomplete rejected independently; **mandatory** — review-complete-but-coverage-insufficient rejected independently; **mandatory** — activation succeeds only when both gates pass; coverage-drop-on-active-locale flags without auto-deactivating (Edge Case 1); deactivation triggers graceful fallback, not abrupt cutoff.

## 22. Documentation
OpenAPI docstring explaining the dual-gate rationale (coverage percentage alone is insufficient if covered strings haven't completed review).

## 23. AI Coding Agent Implementation Steps

**Task 01 — Implement `CoverageRepository`**
Objective: Per-locale missing/draft/approved/percent computation. Files: `repositories/coverage_repository.py`. Dependencies: B-01. Tests: coverage-computation tests. Definition of Done: tests pass.

**Task 02 — Define Schemas**
Objective: `CoverageSummary`, `ActivationResult` (structured gate-failure detail). Files: `schemas/locale_activation_schema.py`. Dependencies: Task 01. Tests: schema tests. Definition of Done: tests pass.

**Task 03 — Implement `LocaleActivationService` with Dual-Gate Logic**
Objective: Independent evaluation of both gates. Files: `services/locale_activation_service.py`. Dependencies: Task 01, Task 02. Tests: **mandatory** — three dual-gate tests (each gate failing independently, both passing). Definition of Done: tests pass.

**Task 04 — Implement Deactivation with Graceful Fallback**
Objective: Distinct, careful existing-user-fallback transition logic. Dependencies: Task 03. Tests: **mandatory** — graceful-fallback-not-abrupt-cutoff test. Definition of Done: test passes.

**Task 05 — Implement Router Endpoints**
Objective: Wire all three endpoints, scope-gated. Files: `routers/locale_activation_router.py`. Dependencies: Task 03, Task 04. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 06 — Implement `CoverageDropMonitor`**
Objective: Scheduled flag-not-deactivate check for already-active locales. Files: `monitoring/coverage_drop_monitor.py`. Dependencies: Task 01. Tests: **mandatory** — coverage-drop-flags-without-deactivating test. Definition of Done: test passes.

**Task 07 — Wire Audit Logging**
Objective: Log activate/deactivate/coverage-drop-alert events. Dependencies: Task 05. Tests: audit-entry tests. Definition of Done: tests pass.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §21, all mandatory tests included. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm neither gate can be bypassed and confirm coverage-drop never triggers auto-deactivation anywhere in the codebase. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] Both activation gates evaluated independently, neither sufficient alone — three mandatory tests passing
- [ ] Coverage drop on an active locale only flags, never auto-deactivates — mandatory test passing
- [ ] Deactivation triggers a graceful existing-user fallback, not an abrupt cutoff
- [ ] `localization_manager` scope enforced

## 25. Definition of Done
Locale activation is a genuinely, structurally enforced dual-gate publishing decision, and coverage regressions on live locales are caught and flagged without ever silently degrading an already-active locale's availability.
