# Blueprint: AI Insight Report Entitlement Enforcement

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/dashboard/`, integrating `src/noorheroes/modules/subscriptions/`. Extends C.20's existing `GET /v1/parent/reports/{child_id}/ai-insight` (premium-gated) endpoint with serve-time entitlement re-checking.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
B-06 — AI Insight Report Entitlement Enforcement.

## 4. Objective
Close the entitlement race condition where a family's premium status lapses between an async report-generation request and its completion, ensuring the AI Insight Report always reflects the entitlement state actually in effect at serve time, never at request time.

## 5. Business Requirements
Source: PRD §1.7 FR-6 (AI insight report — premium, weekly), FR-8, §1.10 Edge Case #4, §3.4.
- AI Insight Report content: strengths, weak areas, suggested next stories/duas/Quran practice, healthy-usage notes — premium-gated, weekly cadence.
- If entitlement lapses mid-generation (a race between the async report job and a billing-state change), the delivered report must respect the entitlement state **actually in effect when served**, not the state at request time (Edge Case #4).
- Content Safety Validator gate applies identically to this report type (FR-8).

## 6. Existing Architecture
This endpoint already exists per C.20 §3.4 ("reused from C.20 §3.4"). This blueprint's scope is narrowly the entitlement re-check fix plus any C.22-specific drill-down linkage (e.g., routing to B-02's skill detail from a "weak area" mention) — it does not rebuild AI Insight Report generation from scratch.

## 7. Existing Code to Reuse
- `SubscriptionService.get_entitlement()` (`modules/subscriptions/`) — existing entitlement check.
- `AIReportGenerationService` / `ContentSafetyValidator` (C.20).
- `require_parent_session_only` (C.20 B-01).
- The existing `GET /v1/parent/reports/{child_id}/ai-insight` route (C.20) — modify, do not duplicate.

## 8. Files to Create
- `tests/modules/dashboard/test_ai_insight_report_entitlement_race.py`

## 9. Files to Modify
- `src/noorheroes/modules/dashboard/service.py` — modify the AI Insight Report generation job/serve path to re-check entitlement at completion/serve time
- `src/noorheroes/modules/dashboard/api.py` — ensure the `ai-insight` route always calls the serve-time entitlement check before returning content

## 10. Backend Requirements
- The async AI Insight Report generation job (existing from C.20) must, upon completion, re-check `SubscriptionService.get_entitlement()` before marking the report deliverable — if entitlement has lapsed since the job started, the job still completes and persists the generated report (do not discard the compute work), but the **serve path** treats it as locked/upsell content rather than delivering it.
- The `GET /v1/parent/reports/{child_id}/ai-insight` route re-checks entitlement on every request independently of generation-time state — entitlement is evaluated at request/serve time, always, never cached from a stale generation-time flag.
- If non-premium: return the locked/upsell response shape (routes client to C.24).
- Content Safety Validator gate applies to the underlying report content exactly as in C.20.

## 11. KMP Requirements
Consumed by K-06 (`AI Insight Report Screen`), which renders the locked/upsell state when `entitled: false`.

## 12. NextJS Requirements
N/A.

## 13. API Contract
- **HTTP Method:** GET
- **Endpoint:** `/v1/parent/reports/{child_id}/ai-insight` (existing route, modified)
- **Auth:** Bearer, parent session only
- **Request:** path `child_id: str`
- **Response 200 (entitled):** existing C.20 AI Insight Report shape, unmodified.
- **Response 200 (not entitled):**
```json
{ "entitled": false, "upsell_context": { "plan_required": "premium" } }
```
- **Authentication:** Bearer parent session
- **Authorization:** Family-ownership on `child_id`; premium entitlement checked at serve time
- **Validation:** `child_id` required
- **Error Responses:** `403`/`404` `ChildScopeViolationError`, `401` invalid session

## 14. Database Requirements
No new tables; reuses `ai_insight_report` (C.20 §4.1) and `subscriptions` module's entitlement tables, read-only from this blueprint.

## 15. Validation
`child_id` required, family-owned; entitlement checked as a business rule at serve time, not a request-body validation concern.

## 16. Authentication
Bearer parent session.

## 17. Authorization
Family-ownership on `child_id` plus serve-time premium entitlement check (two independent, additive gates).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Entitlement lapses between generation-job start and completion | Report still generated/persisted; serve path returns locked/upsell state, not the generated content |
| Entitlement lapses between two separate GET requests | Second request returns locked/upsell even if the first succeeded (serve-time, not cached) |
| Non-premium family requests directly | Locked/upsell state, routes to C.24 |

## 19. Offline First
N/A server-side; cached client-side content must itself be re-validated against a fresh entitlement check on next online access — K-06's responsibility, informed by this endpoint always re-checking server-side.

## 20. Local Data
N/A (backend).

## 21. Localization
`upsell_context` copy pre-localized.

## 22. RTL
N/A (backend).

## 23. Analytics
`ai_insight_report_viewed` / `ai_insight_locked_state_shown` fired client-side (K-06).

## 24. Performance
Entitlement check adds one indexed lookup per request; negligible against the p95 < 700ms NFR.

## 25. Security
Prevents an entitlement-race exploit where a family could retain premium report access after cancellation by timing a request during the generation window.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: entitled family receives full report content.
2. Unit test: non-premium family receives locked/upsell state.
3. **Race test:** simulate entitlement lapsing after job start but before completion — assert serve path returns locked state despite a successfully generated report existing.
4. Unit test: entitlement re-checked independently on each of two sequential requests.
5. Integration test: full request through the gate with entitlement lapse simulated mid-flow.

## 28. Documentation
OpenAPI docstring updated to state the serve-time (not request-time) entitlement contract explicitly, referencing Edge Case #4.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Add Serve-Time Entitlement Re-Check to the Generation Job**
- Task ID: B06-T01
- Objective: Ensure the async job marks completion state without assuming entitlement remains valid.
- Why This Is Required: Root cause of the race condition described in Edge Case #4.
- Existing Architecture to Follow: C.20's existing async report-generation job pattern.
- Existing Files to Reuse: `AIReportGenerationService`.
- Files to Create: none.
- Files to Modify: `service.py` (job completion path).
- Implementation Details: Job persists the generated report regardless of entitlement state at completion; does not gate persistence on entitlement (only the serve path does).
- Business Rules: Edge Case #4.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: No added latency to the job itself.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 03.
- Documentation: Comment explaining why persistence and serving are decoupled from entitlement.
- Dependencies: none.
- Do Not Change: `ContentSafetyValidator` gate on generation content.
- Expected Result: Job behavior unchanged except entitlement is no longer checked at this stage.
- Definition of Done: Job persists reports regardless of entitlement state.

**Task 02 — Add Serve-Time Entitlement Check to the Route**
- Task ID: B06-T02
- Objective: Every GET request independently re-checks entitlement before returning content.
- Why This Is Required: Direct fix for the race — this is where the guarantee is actually enforced.
- Existing Architecture to Follow: `SubscriptionService.get_entitlement()`.
- Existing Files to Reuse: `SubscriptionService`.
- Files to Create: none.
- Files to Modify: `api.py`/`service.py` (serve path).
- Implementation Details: Per §10.
- Business Rules: Edge Case #4.
- Validation: Family-ownership first, entitlement second.
- Error Handling: Locked/upsell response per §13.
- Security: Prevents stale-entitlement exploitation.
- Performance: One additional indexed lookup.
- Localization: `upsell_context` pre-localized.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 03.
- Documentation: OpenAPI note.
- Dependencies: Task 01.
- Do Not Change: `SubscriptionService` internals.
- Expected Result: Serve path always reflects current entitlement.
- Definition of Done: Race test (Task 03) passes.

**Task 03 — Write Test Suite Including Entitlement Race Simulation**
- Task ID: B06-T03
- Objective: Cover §27, with the race-condition test as the defining verification.
- Why This Is Required: Edge Case #4 is explicitly called out as a race condition requiring targeted testing.
- Existing Architecture to Follow: pytest + fixture-based entitlement toggling.
- Existing Files to Reuse: Family/child/session/subscription fixtures.
- Files to Create: `test_ai_insight_report_entitlement_race.py`.
- Files to Modify: none.
- Implementation Details: 5 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact responses.
- Security: Race test is security-critical (prevents entitlement bypass).
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings citing Edge Case #4.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green, race test included and green.

## 30. Definition of Done
AI Insight Report serve path re-checks entitlement independently on every request, generation job no longer conflates persistence with entitlement, race-condition test passes, all tests green.

## 31. Final Verification Checklist
- [ ] Entitlement checked at serve time on every request, not cached from generation time
- [ ] Race-condition test simulating mid-generation entitlement lapse passes
- [ ] Non-premium families receive locked/upsell state routing to C.24
- [ ] Content Safety Validator gate still applies to underlying content
- [ ] OpenAPI docs state the serve-time entitlement contract
