# B-03 — Manual-Activation Structural-Absence Guardrail

## 1. Feature Context
The single highest-priority guarantee in this entire module: nowhere in the admin API surface does a capability exist to directly write `subscription.state=active_paid` without an accompanying `billing_event_id` or `comp_grant_id` reference. This is not a validated-and-rejected request — it is a capability that was never built, verified continuously by an OpenAPI-schema-scanning test that fails the build if it is ever introduced.

## 2. Parent Feature
E.33 — Subscription Management & Billing Ops

## 3. Sub-feature
1.3 Manual-Activation Structural-Absence Guardrail (ID: **B-03**)

## 4. Objective
Build a CI-blocking OpenAPI-schema-scanning test suite that inspects the full generated API schema for any endpoint/field combination capable of setting subscription state without a billing-event or comp-grant reference, plus a defense-in-depth runtime canary alert.

## 5. Business Requirements
- FR-3 (the module's central hard rule): store webhook/receipt is always the entitlement source of truth; no admin path exists to manually flip a subscription to active.
- §5 Backend AI prompt item 1: this must be the single highest-priority test in the entire deliverable — a structural absence (no matching field/endpoint exists at all), not a validated-rejected field.
- Acceptance Criteria: attempting to set state to `active_paid` without a billing-event/comp-grant reference — including via a direct API call — is rejected because the capability does not exist.

## 6. Existing Architecture
`subscriptions` bounded context, a dedicated test module (not a runtime service — this sub-feature is primarily a CI-gate and a monitoring canary) plus a shared static-analysis utility consumed by CI.

## 7. Existing Code to Reuse
- FastAPI's own OpenAPI schema generation (`app.openapi()`) as the scan target — no external tooling needed
- E.28's alerting/monitoring hook pattern for the P0 canary alert

## 8. Files to Create
- `tests/security/test_no_manual_activation_path.py` — the mandatory OpenAPI-schema-scanning test
- `app/subscriptions/monitoring/manual_activation_canary.py` — a defense-in-depth runtime check (e.g., a periodic query for any `subscription` row whose `state='active_paid'` transition has no corresponding `billing_event`/`comp_grant` reference in its transition history) that pages on any hit, since the schema-level guarantee should make this query permanently empty
- `docs/security/manual-activation-guardrail.md` — rationale documentation, referenced by every other sub-feature in this module

## 9. Files to Modify
None — by design, this sub-feature does not add or modify a mutation endpoint; it only adds tests and a monitoring canary confirming the absence.

## 10. Backend Requirements
- The schema-scanning test parses `app.openapi()`'s full path/schema tree and asserts: no request-body schema for any endpoint under `/v1/admin/subscriptions*` or `/v1/admin/plans*` contains a `state` field accepting the literal `active_paid` without the same schema also requiring one of `billing_event_id`/`comp_grant_id`.
- The runtime canary (`manual_activation_canary.py`) is a scheduled job (reuses the platform's existing job-scheduling infrastructure) that queries the `subscription_state_transition` audit trail (if one exists — else `billing_event`/`comp_grant` tables) for any `active_paid` transition lacking a valid reference, alerting P0 on any match. This is intentionally redundant with the schema-level guarantee — a canary that should permanently find nothing.

## 11. Required API / API Contract
No new endpoint. This sub-feature is purely a test-suite and monitoring addition.

## 12. Database Requirements
None new — the canary reads existing `subscription`/`billing_event`/`comp_grant` tables (comp_grant owned by B-04).

## 13. Validation
N/A (no request path).

## 14. Authentication
N/A.

## 15. Authorization
N/A.

## 16. Error Handling
The schema-scanning test fails the CI build (not a runtime error) if the guarantee is ever violated by a future code change.

## 17. Security
This sub-feature IS the security control. Its own test failing is the alarm. The runtime canary is the second, independent layer — confirming the guarantee holds in production data, not just in the API schema, given a schema-correct-but-buggy-implementation could theoretically still write bad data through some other path (e.g., a direct DB migration mistake).

## 18. Analytics
`plan_manual_activation_attempt_blocked` (internal/security signal) per §1.19 — logged if the canary or the (structurally absent) endpoint ever registers an attempt.

## 19. Performance
Schema scan runs once per CI build (fast, in-memory). Canary runs on a low-frequency schedule (e.g., hourly), lightweight query.

## 20. Library Requirements
FastAPI (schema introspection), pytest. No new libraries.

## 21. Testing
**Mandatory, CI-blocking:** the OpenAPI-schema-scanning test itself — this sub-feature's entire deliverable is this test plus its canary counterpart. Additional test: canary correctly identifies a deliberately-injected fixture violation in a non-production test database (to prove the canary itself works, since a canary that can't detect a known-bad fixture provides false confidence).

## 22. Documentation
`docs/security/manual-activation-guardrail.md` explains why this guarantee is structural rather than validation-based, and instructs future engineers modifying any subscription-related endpoint to re-run this test suite explicitly before merging.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Write the OpenAPI-Schema-Scanning Test**
Objective: Parse `app.openapi()`, assert no endpoint accepts `state=active_paid` without a `billing_event_id`/`comp_grant_id` requirement. Files: `tests/security/test_no_manual_activation_path.py`. Tests: this IS the test. Definition of Done: test passes against the current schema, and is proven to fail against a deliberately-reintroduced violation (write a throwaway broken-fixture branch locally to confirm the test actually catches it, then revert).

**Task 02 — Implement the Runtime Canary**
Objective: Scheduled query detecting any unattributed `active_paid` transition. Files: `monitoring/manual_activation_canary.py`. Dependencies: existing job-scheduling infra. Tests: canary detects a deliberately-injected fixture violation in a test DB. Definition of Done: test passes.

**Task 03 — Wire P0 Alerting**
Objective: Canary hit pages the on-call/security channel immediately. Dependencies: Task 02, E.28's alerting hook. Tests: alert-fired-on-detection test. Definition of Done: test passes.

**Task 04 — Write Guardrail Documentation**
Objective: `docs/security/manual-activation-guardrail.md`. Dependencies: Task 01. Definition of Done: doc references this test explicitly as a required pre-merge check for any subscription-endpoint change.

**Task 05 — Register as a CI-Blocking Gate**
Objective: Ensure `test_no_manual_activation_path.py` cannot be skipped/marked-xfail in the CI pipeline configuration. Dependencies: Task 01. Definition of Done: CI config confirmed to treat this test as non-bypassable.

**Task 06 — Final Code Review**
Objective: Confirm the test suite actually inspects the full, currently-generated schema (not a stale/cached snapshot) on every run. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] Schema-scanning test is CI-blocking and non-bypassable — the single highest-priority test in this deliverable
- [ ] Test proven to actually catch a deliberately-reintroduced violation (not just pass trivially)
- [ ] Runtime canary independently confirms the guarantee against live data
- [ ] P0 alert wired for any canary hit
- [ ] Guardrail rationale documented and referenced by other sub-features in this module

## 25. Definition of Done
The platform has two independent, continuously-verified layers of proof — one at the API-schema level, one at the production-data level — that no path exists anywhere to manually fabricate an active subscription outside a real billing event or an audited comp grant.
