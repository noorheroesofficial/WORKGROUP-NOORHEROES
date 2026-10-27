# Blueprint: Content Safety Validator (Write-Time Gate)

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/dashboard/` (or `modules/ai_safety/` if the team prefers centralizing all content-safety validation there — see Task 01 decision note). Mandatory write-time gate protecting every AI-generated report from ever surfacing diagnosis, sibling-comparison, or false-certainty language.

## 2. Parent Feature
C.20 — Parent Dashboard.

## 3. Sub-feature
B-05 — Content Safety Validator.

## 4. Objective
Validate AI-generated report content against three hard rules before it is ever eligible to be marked `content_safety_passed = true`: no developmental/behavioral/religious diagnosis language, no sibling-comparison language, no uncertain-conclusion-presented-as-fact pattern.

## 5. Business Requirements
Source: PRD §1.7 FR-13, §3.3 (Content Safety Validator service), §3.5, §4.3, §5 (Backend AI Code-Gen Prompt item 4), §12.7, Edge Case #9.
- "AI-generated parent insights must never diagnose developmental, behavioral, or religious conditions; must never compare siblings; must never present uncertain conclusions as settled facts" — governs every AI-derived surface on this Dashboard and its linked reports.
- Must be a write-time gate (validated before persistence eligibility), not a read-time filter that could be bypassed by a caching/query-logic change.
- On failure: row stored with `content_safety_passed = false` for audit purposes, never served via read API.

## 6. Existing Architecture — CORRECTED AFTER DIRECT CODE VERIFICATION
`FAST-API-INSTRUCTIONS.md` §5.3 describes an aspirational `AISafetyService.evaluate_content()`/`POST /v1/ai-safety/evaluate` general-purpose content-moderation service. **This does not exist.** Direct inspection of `backend/src/noorheroes/modules/ai_safety/` found the real, implemented contents to be entirely different: `service.py` defines `AiHistoryService` — a pure READ-ONLY query service over the `AiSafetyEvent` table (pre-redacted AI chat logs), exposing exactly one method, `get_interaction_history(family_id, child_id, date_from, date_to)`, consumed by exactly one route, `GET /v1/children/{child_id}/ai-history`. There is no evaluation/classification/moderation logic anywhere in this module — `input_redacted`/`output_redacted` fields are explicitly documented as "redaction is complete at write time (upstream ingestion consumer, out of scope here)". **Conclusion: this blueprint's `ContentSafetyValidator` must be built as new, standalone logic — there is nothing existing to extend or reuse for the 3-rule (diagnosis / sibling-comparison / false-certainty) evaluation this feature needs.** Task 01 below is corrected accordingly (the "decide reuse strategy" investigation is resolved: build standalone).

## 7. Existing Code to Reuse
- `AiSafetyEvent` model / `AiHistoryService` pattern (`modules/ai_safety/`) as a STRUCTURAL reference only (how a read-only, family-scoped safety-data service is shaped in this codebase) — not as reusable evaluation logic, since none exists.
- `infrastructure/ai/` — also verified to be an empty stub (`__init__.py` only, no `AIProviderFactory`/provider classes implemented). If this validator's diagnosis/sibling-comparison/false-certainty checks require an LLM classifier pass (rather than pure rule/pattern matching), the AI-provider integration itself must be built here for the first time — coordinate with whichever other feature (e.g., B-04's report generation, which also needs an LLM call) builds it first to avoid two parallel provider integrations.
- `core/exceptions.py`'s `DomainError` pattern if a dedicated exception type is useful for validator-level failures (optional — this validator mostly returns a result object rather than raising).

## 8. Files to Create
- `src/noorheroes/modules/dashboard/content_safety.py` — `ContentSafetyValidator` class with `validate(content: dict) -> ContentSafetyResult`
- `tests/modules/dashboard/test_content_safety_validator.py`

## 9. Files to Modify
- `src/noorheroes/modules/dashboard/service.py` (`ReportGenerationService`, from B-04) — invoke validator before every insert of `weekly_report`/`ai_insight_report`

## 10. Backend Requirements
- `ContentSafetyValidator.validate(content: str | dict) -> ContentSafetyResult` where `ContentSafetyResult` has `passed: bool`, `failure_reasons: list[str]` (e.g., `"possible_diagnosis_language"`, `"possible_sibling_comparison"`, `"possible_false_certainty"`).
- Three checks, each independently evaluable:
  1. **Diagnosis check:** pattern/classifier detecting developmental, behavioral, or religious diagnostic language (e.g., clinical terms applied to the child as a conclusion rather than descriptive progress language).
  2. **Sibling-comparison check:** detects comparative language referencing another child/sibling by name or relative ranking terms ("better than", "unlike his brother", etc.).
  3. **False-certainty check:** detects hedged-uncertainty content being presented as settled fact (e.g., AI-inferred emotional states stated without appropriate qualification).
- Built standalone (confirmed via §6 — no existing evaluation service to extend). Recommended implementation shape given `infrastructure/ai/` is also an empty stub: start with deterministic rule/pattern matching (regex/keyword lists per rule, cheap and testable, no external dependency) as the baseline, with an LLM-classifier pass as an optional stronger layer added later once an AI-provider integration exists elsewhere in the codebase — do not block this validator's delivery on building a new provider integration from scratch if a simpler pattern-based v1 satisfies the 7 test cases in §27.
- MUST be invoked synchronously by `ReportGenerationService` (B-04 Task 03) before any insert can set `content_safety_passed = true`.
- On failure: `ReportGenerationService` persists the row with `content_safety_passed = false` and the validator's `failure_reasons` stored in an auditable location (either a new column or via `SafetyAuditLog`) for B-06's audit log tag display.

## 11. KMP Requirements
N/A directly — client never calls this validator; it only ever sees the effect (a failed report simply never appears, replaced transparently by the previous passing report per B-03).

## 12. NextJS Requirements
Failure reasons feed B-06/N-01's read-only audit log (`validator-failure-reason tag`).

## 13. API Contract
No public HTTP endpoint — internal service class, invoked in-process by `ReportGenerationService`. If the team decides to centralize in `ai_safety` context, it may be exposed as an internal call to the existing `POST /v1/ai-safety/evaluate` endpoint pattern, but this must remain an internal/service-to-service call, never parent- or child-facing.

## 14. Database Requirements
Adds no new tables of its own if reusing `SafetyAuditLog`; otherwise, PRD's `content_safety_passed` boolean column already covers pass/fail per report row (B-04's migration). If failure-reason tags need persistence beyond `SafetyAuditLog`, add a `validation_failure_reasons` JSONB/array column to `weekly_report` and `ai_insight_report` — confirm exact approach against B-04's migration before implementation to avoid two migrations touching the same tables inconsistently (implement both B-04 and B-05 migrations together as a single coordinated PR).

## 15. Validation
This service IS the validation layer for AI-generated report content — see §10 checks 1–3.

## 16. Authentication
N/A — internal service call, no external auth surface.

## 17. Authorization
N/A — invoked only by `ReportGenerationService` (B-04) in-process; not independently callable by any external actor.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Content fails any of the 3 checks | Row persisted with `content_safety_passed=false`, failure reasons recorded, never returned by read API |
| Validator itself errors (e.g., underlying AI classifier call fails) | Treated as a failure (fail-closed, not fail-open) — content_safety_passed remains `false` rather than defaulting to `true` on validator error |
| All 3 checks pass | `content_safety_passed=true` |

## 19. Offline First
N/A (backend).

## 20. Local Data
N/A (backend).

## 21. Localization
Validator must operate correctly across the report content's active locale (English/Hindi/Arabic/Urdu) — diagnosis/comparison/false-certainty language patterns are not English-only concerns; if using an LLM-based classifier pass, ensure the prompt instructs multilingual evaluation rather than assuming English input.

## 22. RTL
N/A (backend).

## 23. Analytics
Content Safety Validator failure-rate spike is a DevOps P0-adjacent monitoring signal (§10: "Alert on Content Safety Validator failure-rate spikes — a model-quality signal worth investigating").

## 24. Performance
Synchronous call within the async Celery report-generation task (B-04) — acceptable since generation is already off the request path; should not introduce unbounded latency (apply a reasonable timeout with fail-closed behavior on timeout).

## 25. Security
This is one of the two highest-priority guarantees in the entire C.20 feature (alongside B-01), per PRD §5. Fail-closed design is mandatory: any ambiguity or validator error must result in `content_safety_passed=false`, never `true` by default.

## 26. Library Requirements
No new dependencies if reusing `AISafetyService`/`AIProviderFactory`; otherwise, whatever text-classification/pattern-matching library is already used by `ai_safety` context.

## 27. Testing
1. Unit test: diagnosis-language content correctly flagged and fails.
2. Unit test: sibling-comparison content correctly flagged and fails.
3. Unit test: false-certainty content correctly flagged and fails.
4. Unit test: clean content (calm, trend-oriented, non-comparative) passes all 3 checks.
5. Unit test: validator error/timeout results in fail-closed (`passed=false`), not fail-open.
6. **Mandatory integration test (PRD §5 item 4):** a report failing validation is never returned by `GET /v1/parent/dashboard/reports/weekly`, while the read API correctly falls back to the previous passing report instead.
7. Unit test: failure reasons correctly recorded and retrievable for B-06's audit display.

## 28. Documentation
Module docstring explicitly stating the fail-closed design principle and citing FR-13 and PRD §5 item 4's priority designation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Re-Confirm Standalone Build (Decision Already Resolved by Direct Code Verification)**
- Task ID: B05-T01
- Objective: Re-verify `modules/ai_safety/` still has no content-evaluation logic before starting Task 02's standalone build.
- Why This Is Required: A direct filesystem/code check already confirmed `modules/ai_safety/service.py` implements only `AiHistoryService.get_interaction_history()` (a read-only query over pre-redacted `AiSafetyEvent` rows, exposed via one route, `GET /v1/children/{child_id}/ai-history`) — no `evaluate_content()`, no `SafetyAuditLog`, no moderation logic of any kind exists to reuse. This task is a final freshness guard against codebase drift, not an open investigation.
- Existing Architecture to Follow: `modules/ai_safety/` bounded context (structural reference only — same "family-scoped read service" shape, not reusable logic).
- Existing Files to Reuse: none for evaluation logic.
- Files to Create: none (confirmation task).
- Files to Modify: none.
- Implementation Details: Re-run a search for `evaluate`/`classif`/`moderat` across `modules/ai_safety/` immediately before Task 02; if still nothing found (expected), proceed directly to the standalone build.
- Business Rules: FR-13.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: N/A.
- Documentation: Record the re-check result in the module docstring.
- Dependencies: none.
- Do Not Change: Do not modify `modules/ai_safety/`'s existing `AiHistoryService`/`GET /v1/children/{child_id}/ai-history` — this validator is fully independent of it.
- Expected Result: Standalone build path confirmed.
- Definition of Done: Re-check performed before Task 02 begins.

**Task 02 — Implement ContentSafetyValidator**
- Task ID: B05-T02
- Objective: Build the 3-rule validation logic.
- Why This Is Required: Core deliverable.
- Existing Architecture to Follow: Per Task 01's decision.
- Existing Files to Reuse: `AISafetyService`/`AIProviderFactory` as decided.
- Files to Create: `src/noorheroes/modules/dashboard/content_safety.py`.
- Files to Modify: none.
- Implementation Details: Per §10.
- Business Rules: FR-13.
- Validation: This IS the validation logic.
- Error Handling: Fail-closed per §18.
- Security: Core P0 guarantee.
- Performance: Timeout-bounded, fail-closed on timeout.
- Localization: Multilingual-aware per §21.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstring per §28.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: `ContentSafetyValidator.validate()` functional.
- Definition of Done: All 3 rule checks independently testable and correct.

**Task 03 — Wire Validator into ReportGenerationService as Mandatory Gate**
- Task ID: B05-T03
- Objective: Connect B-05 to B-04's insert path.
- Why This Is Required: The validator is meaningless unless it's actually the gate.
- Existing Architecture to Follow: B-04's `ReportGenerationService`.
- Existing Files to Reuse: `ReportGenerationService`.
- Files to Create: none.
- Files to Modify: `src/noorheroes/modules/dashboard/service.py`.
- Implementation Details: Every `weekly_report`/`ai_insight_report` insert calls `content_safety_validator.validate()` synchronously first.
- Business Rules: FR-13.
- Validation: N/A.
- Error Handling: Per §18.
- Security: This IS the wiring for the P0 guarantee — must be structurally impossible to bypass (single insert code path, not multiple).
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04 (integration test #6).
- Documentation: Comment citing PRD §5 item 4.
- Dependencies: Task 02, B-04.
- Do Not Change: Do not create a second insert path for these tables that skips this call.
- Expected Result: No row can be marked `true` without validation.
- Definition of Done: Integration test #6 passes.

**Task 04 — Write Test Suite**
- Task ID: B05-T04
- Objective: Cover §27, especially the mandatory integration test.
- Why This Is Required: PRD explicitly requires this exact end-to-end proof.
- Existing Architecture to Follow: pytest fixtures.
- Existing Files to Reuse: B-03's and B-04's test fixtures.
- Files to Create: `tests/modules/dashboard/test_content_safety_validator.py`.
- Files to Modify: none.
- Implementation Details: 7 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: N/A.
- Security: Test #6 is the CI-blocking security-critical test alongside B-01's structural test.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings citing PRD §5 item 4.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: CI treats test #6 (and B-01's structural test) as the two mandatory, non-bypassable gates per DevOps §10.

## 30. Definition of Done
Validator correctly flags diagnosis/sibling-comparison/false-certainty content, fails closed on error/timeout, is wired as the sole insert-time gate for `weekly_report`/`ai_insight_report`, and a failing report is provably never servable via B-03's read API.

## 31. Final Verification Checklist
- [ ] Fail-closed behavior verified (validator error ≠ pass)
- [ ] All 3 rule categories independently tested
- [ ] Mandatory end-to-end "failed report never served" test passing
- [ ] No alternate insert path bypasses the validator
- [ ] Multilingual content evaluated correctly, not English-only
- [ ] Failure reasons recorded and available for B-06 audit display
