# Blueprint: AI Report Generation Service

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI + Celery). Module: `src/noorheroes/modules/dashboard/`. Asynchronous background service producing weekly, monthly, AI-insight, and safety reports consumed by B-03.

## 2. Parent Feature
C.20 — Parent Dashboard.

## 3. Sub-feature
B-04 — AI Report Generation Service.

## 4. Objective
Asynchronously generate the 4 report types on their respective cadences, persist them with a `content_safety_passed` audit flag (validated by B-05 before eligibility), and guarantee `monthly_family_report`'s schema structurally cannot hold a per-child comparison field.

## 5. Business Requirements
Source: PRD §1.7 FR-8, FR-15, §3.1, §3.3, §4, §5 (Backend AI Code-Gen Prompt items 2, 3, 5), §10 DevOps.
- Weekly child report: stories completed, Quran progress, duas learned, habit streaks, quiz scores, recommended next step — weekly cadence.
- Monthly family report: cross-child progress summary, family streaks, content favorites, learning consistency — monthly cadence, **aggregate-only, no per-child-array field**.
- AI insight report: strengths, weak areas, suggested next content, healthy-usage notes — premium, weekly.
- Safety report: AI usage history, blocked requests, content flags, profile-setting changes — on demand.
- Every row carries `generated_at` and `content_safety_passed`.

## 6. Existing Architecture
Per `FAST-API-INSTRUCTIONS.md` §4 Infrastructure: Celery workers already exist for `modules/localization/tasks.py` (`translate_content_task`, `batch_translate_task`, `retry_failed_translations_task`) — this is the established pattern for async background jobs in this codebase. `infrastructure/ai/` already provides `AIProviderFactory.get_provider()` with `OpenAIProvider`, `ClaudeProvider`, `GeminiProvider`, `DeepSeekProvider` — reuse this factory rather than building a new AI client integration.

## 7. Existing Code to Reuse
- `AIProviderFactory.get_provider(provider_type)` and the `AIProvider` interface (`infrastructure/ai/`) — **verify these classes actually exist in `backend/src/noorheroes/infrastructure/ai/` before relying on them**; a direct filesystem check during this research pass found only an `ai/__init__.py` stub, meaning the AI-provider factory described in `FAST-API-INSTRUCTIONS.md` is, like several other "existing" services referenced there, not yet implemented — this generation service may need to build the provider integration itself rather than purely reusing one, or coordinate with whichever feature is first to need it.
- Celery task registration pattern from `modules/localization/tasks.py` (periodic + on-demand task structure) — **also not directly verified as implemented**; confirm `modules/localization/tasks.py` exists in `backend/src` before assuming this pattern is available to copy (the `localization` module directory does exist per the module listing, but its internal file contents were not individually verified in this research pass).
- `OutboxWriter` (`common/outbox.py`) if report generation should emit a domain event (e.g., for notification triggers owned by C.25 — "weekly report ready" push).
- Source data via `HabitRepository` (`modules/habits/`, confirmed real per C.22 B-01 — see B-02 §6/§7 for the full confirmed/unconfirmed service inventory) and the not-yet-implemented `LearningService`/`RewardService`/Restriction-Engine equivalents (same caveats as B-02's fan-out sources).

## 8. Files to Create
- `src/noorheroes/modules/dashboard/models.py` — `WeeklyReportOrm`, `MonthlyFamilyReportOrm`, `AiInsightReportOrm`, `SafetyReportOrm`
- `alembic/versions/xxxx_create_dashboard_report_tables.py`
- `src/noorheroes/modules/dashboard/tasks.py` — `generate_weekly_report_task`, `generate_monthly_family_report_task`, `generate_ai_insight_report_task`, `generate_safety_report_task`
- `tests/modules/dashboard/test_ai_report_generation_service.py`
- `tests/modules/dashboard/test_monthly_family_report_schema_structural.py`

## 9. Files to Modify
- `src/noorheroes/modules/dashboard/service.py` — add `ReportGenerationService(BaseService)`
- Celery beat schedule config (wherever periodic tasks are registered, per `translate_content_task`'s pattern) — add weekly/monthly cadence entries

## 10. Backend Requirements
- `ReportGenerationService.generate_weekly_report(child_id)`: gathers source data (stories, Quran, duas, habits, quizzes) via existing domain services, builds a prompt via an AI provider (reuse `PromptBuilder`-equivalent pattern from `modules/localization/service.py` if generalizable, or a new dashboard-scoped prompt builder), calls `AIProviderFactory.get_provider(...)`, and produces `summary_json`.
- `ReportGenerationService.generate_monthly_family_report(family_id)`: aggregates across all children in the family; `aggregate_summary_json` schema MUST NOT contain any field capable of holding a per-child breakdown array intended for comparison rendering (structurally enforced, see Task 04).
- `ReportGenerationService.generate_ai_insight_report(child_id)`: premium-gated content (generation still occurs; gating happens at read-time in B-03), produces `insight_json` (strengths, weak areas, suggestions, healthy-usage notes).
- `ReportGenerationService.generate_safety_report(child_id)`: on-demand (not scheduled), aggregates AI usage history/blocked requests/content flags/setting changes from `ai_safety` context (`modules/ai_safety/`) and identity/settings-change logs.
- Every generated row passed through B-05's Content Safety Validator BEFORE `content_safety_passed` can be set `true`; on failure, still insert the row with `content_safety_passed = false` for audit (never delete/discard).
- Celery periodic tasks: weekly cadence for `weekly_report`/`ai_insight_report`, monthly cadence for `monthly_family_report`; `safety_report` generation triggered on-demand (via B-03 request or explicit parent action, not scheduled).

## 11. KMP Requirements
N/A directly — KMP consumes generated reports via B-03, never triggers generation directly.

## 12. NextJS Requirements
N/A for generation itself; failed-validation rows become visible via B-06/N-01's read-only audit log.

## 13. API Contract
No public-facing endpoint in this blueprint (internal service + Celery tasks only). Internal contract: `ReportGenerationService` methods return the persisted ORM row (or raise on generation failure, which Celery's retry policy handles per existing `retry_with_backoff` utility in `common/utils/retry.py`).

## 14. Database Requirements
Per PRD §4.1/§4.2 ER diagram:
- `weekly_report(report_id PK, child_id FK, period_start, period_end, summary_json, generated_at, content_safety_passed)`, index `(child_id, period_end DESC)`.
- `monthly_family_report(report_id PK, family_id FK, period_start, period_end, aggregate_summary_json, generated_at)`, index `(family_id, period_end DESC)`. Schema constraint: no per-child-array field.
- `ai_insight_report(report_id PK, child_id FK, insight_json, generated_at, content_safety_passed)`, index `(child_id, generated_at DESC)`.
- `safety_report(report_id PK, child_id FK, ai_usage_summary, blocked_requests, generated_at)`, index `(child_id, generated_at DESC)`.
- Retention: weekly/monthly reports retained ~12 months rolling; safety reports retained per platform compliance-audit retention tier (PRD §4.5).
- No soft-delete lifecycle — reports are immutable historical artifacts (PRD §4.4).

## 15. Validation
- `aggregate_summary_json` schema validated at write time to contain no field shaped as a per-child array (structural test, Task 04).
- Generated content validated by B-05 before `content_safety_passed = true` is permitted.

## 16. Authentication
N/A — internal Celery task, not directly HTTP-exposed; triggered by scheduler or internal service call authenticated via the standard service-to-service context (no external caller).

## 17. Authorization
N/A directly; `safety_report` on-demand trigger (if exposed via an internal call from B-03) inherits the caller's already-validated parent-session/family-ownership context.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| AI provider call fails/times out | Celery retry with backoff (`retry_with_backoff` utility); on exhaustion, previous report remains the servable "last known good" via B-03 |
| Content safety validation fails | Row persisted with `content_safety_passed = false`, audit-visible via B-06, never served |
| Partial source-data unavailability (e.g., Habit service down during generation) | Generation deferred/retried rather than producing an incomplete report silently |

## 19. Offline First
N/A (backend async service).

## 20. Local Data
N/A (backend).

## 21. Localization
Generated narrative content (`summary_json.next_step_recommendation`, `insight_json.suggestions`, etc.) should be generated in the family's active locale (English/Hindi/Arabic/Urdu) where the platform's AI/localization pipeline supports locale-aware generation — reuse `modules/localization/` patterns (`PromptBuilder`, `TranslationValidator`) rather than inventing a parallel localization mechanism.

## 22. RTL
N/A (backend; content is plain text/JSON, RTL rendering is a KMP concern).

## 23. Analytics
N/A directly (internal service); report-generation-delay rate is a DevOps monitoring signal (§10), tracked via the gap between expected and actual `generated_at` timestamps.

## 24. Performance
Async/Celery-based, off the request path entirely; no impact on B-02/B-03 read-path latency except through the caching layer they already implement.

## 25. Security
Content Safety Validator (B-05) is a mandatory write-time gate — this service must call it synchronously before ever marking `content_safety_passed = true`; it must be structurally impossible to bypass (no code path inserts a row with `true` without validator invocation).

## 26. Library Requirements
No new dependencies — reuses existing Celery, `infrastructure/ai/` providers, SQLAlchemy async, Alembic.

## 27. Testing
1. Unit test: weekly report generation produces expected `summary_json` shape from mocked source-service data.
2. Unit test: monthly family report aggregation across multiple children produces `aggregate_summary_json` with no per-child-array field.
3. **Structural test (mandatory, PRD §5 item 5):** assert `monthly_family_report`'s JSON schema/model has no field capable of holding a per-child breakdown intended for comparison rendering.
4. Unit test: ai_insight report generation.
5. Unit test: safety report generation on-demand.
6. Unit test: content-safety-validator integration — failing content stored with `content_safety_passed=false`, never marked eligible.
7. Integration test: Celery task retry-on-failure behavior via `retry_with_backoff`.
8. Integration test: periodic schedule triggers weekly/monthly tasks correctly.

## 28. Documentation
Update Celery beat schedule documentation; add module docstring describing the 4 report types and cadences, citing PRD §1.8 (FR-8).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create ORM Models and Migration**
- Task ID: B04-T01
- Objective: Persist the 4 report tables.
- Why This Is Required: Foundation for all report generation/retrieval.
- Existing Architecture to Follow: `infrastructure/db/base.py` `Base`/`TimestampMixin` pattern.
- Existing Files to Reuse: `Base`, `TimestampMixin`.
- Files to Create: `src/noorheroes/modules/dashboard/models.py`, Alembic migration.
- Files to Modify: none.
- Implementation Details: Per §14 schema exactly, including indexes.
- Business Rules: PRD §4.
- Validation: FK constraints to `child`/`family`.
- Error Handling: N/A.
- Security: No new PII fields beyond `summary_json`/`insight_json` content, which mirrors existing service data.
- Performance: Indexes per §14.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Migration up/down tested in Task 06 (via CI migration check if the project has one) — otherwise implicit in integration tests.
- Documentation: Docstrings on ORM classes.
- Dependencies: none.
- Do Not Change: Do not modify PostgreSQL credentials/connection config.
- Expected Result: Tables exist post-migration.
- Definition of Done: Migration applies cleanly, matches ER diagram.

**Task 02 — Build ReportGenerationService Core Logic**
- Task ID: B04-T02
- Objective: Implement generation methods for all 4 types.
- Why This Is Required: Core deliverable of this blueprint.
- Existing Architecture to Follow: `BaseService`, `AIProviderFactory`.
- Existing Files to Reuse: `LearningService`, `RewardService`, Habit/Restriction services, `AIProviderFactory.get_provider()`.
- Files to Create: none.
- Files to Modify: `src/noorheroes/modules/dashboard/service.py`.
- Implementation Details: Per §10.
- Business Rules: FR-8.
- Validation: N/A (validation happens via B-05 before persistence eligibility).
- Error Handling: Per §18.
- Security: N/A here (enforced in Task 03).
- Performance: N/A (async, off request path).
- Localization: Locale-aware generation per §21.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 06.
- Documentation: Docstrings citing PRD §1.8.
- Dependencies: Task 01.
- Do Not Change: Do not modify `AIProviderFactory` or existing provider implementations.
- Expected Result: 4 generation methods functional against mocked/live AI providers.
- Definition of Done: Each method produces schema-conformant output.

**Task 03 — Integrate Content Safety Validator as Mandatory Write-Time Gate**
- Task ID: B04-T03
- Objective: Ensure no row is ever marked `content_safety_passed=true` without passing B-05.
- Why This Is Required: PRD's single highest-priority guarantee alongside B-01 (§5 "item 4... treated as the two highest-priority guarantees").
- Existing Architecture to Follow: New `ContentSafetyValidator` from B-05.
- Existing Files to Reuse: B-05's validator interface.
- Files to Create: none.
- Files to Modify: `src/noorheroes/modules/dashboard/service.py`.
- Implementation Details: Every insert path for `weekly_report`/`ai_insight_report` calls `content_safety_validator.validate(generated_content)` synchronously before setting the flag; `monthly_family_report`/`safety_report` are non-narrative/structural data and validated instead via the structural schema test (Task 05 in B-05, and Task 04 here for monthly).
- Business Rules: FR-13.
- Validation: N/A (this IS the validation gate integration).
- Error Handling: Failing validation → row persisted with flag `false`, generation pipeline logs the failure for B-06 audit visibility.
- Security: This is a P0 security control.
- Performance: Synchronous validator call within the async Celery task — acceptable since this is off the request path.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 06.
- Documentation: Comment citing PRD §5 item 4 priority.
- Dependencies: B-05 must exist (or be implemented in tandem).
- Do Not Change: Do not create any alternate insert path that bypasses this gate.
- Expected Result: Structurally impossible to persist `true` without validation.
- Definition of Done: Test 6 in §27 passes.

**Task 04 — Enforce Monthly Family Report No-Comparison Schema**
- Task ID: B04-T04
- Objective: Guarantee `aggregate_summary_json` has no per-child-array field.
- Why This Is Required: PRD's platform-wide no-sibling-ranking guarantee, explicitly mandated as a structural test (§5 item 5).
- Existing Architecture to Follow: A.7/A.11's established structural no-comparison pattern (per PRD cross-reference).
- Existing Files to Reuse: N/A (new schema, but same design principle as A.7/A.11 — confirm exact prior implementation location if reusing a shared validator utility; otherwise implement independently per this table's own schema).
- Files to Create: none.
- Files to Modify: `src/noorheroes/modules/dashboard/schemas.py` (Pydantic schema for `aggregate_summary_json`), `models.py` (JSONB column with an application-layer schema, not DB-level JSON schema constraint, consistent with `jsonb` column type in PRD ER diagram).
- Implementation Details: Define `AggregateSummaryJson` as a Pydantic model with only scalar/aggregate fields (e.g., `family_streak_count: int`, `top_content_favorites: list[str]` — content titles, not per-child breakdowns, `consistency_score: float`); explicitly no field like `per_child_breakdown: list[ChildSummary]`.
- Business Rules: FR-15.
- Validation: Structural test (Task 05).
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Comment explicitly stating the no-comparison design constraint and citing FR-15.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Schema structurally incapable of comparison rendering.
- Definition of Done: Structural test passes.

**Task 05 — Write Structural Test for Monthly Report Schema**
- Task ID: B04-T05
- Objective: Automated proof of Task 04's guarantee.
- Why This Is Required: PRD §5 item 5 mandates this exact test.
- Existing Architecture to Follow: Reflection-based structural test pattern (mirrors platform's established approach, e.g., B.16/C.19 reflection tests referenced elsewhere in this PRD).
- Existing Files to Reuse: none.
- Files to Create: `tests/modules/dashboard/test_monthly_family_report_schema_structural.py`.
- Files to Modify: none.
- Implementation Details: Iterate `AggregateSummaryJson.model_fields`, assert no field's type is `list[SomeChildScopedModel]` or similarly comparison-shaped.
- Business Rules: FR-15.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A (this IS a safety/trust guarantee test).
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the test.
- Documentation: Docstring citing FR-15 and PRD §5 item 5.
- Dependencies: Task 04.
- Do Not Change: N/A.
- Expected Result: Test passes and would fail if a future developer adds a comparison-shaped field.
- Definition of Done: CI-enforced per DevOps §10 (mandatory, non-bypassable gate alongside B-01's and B-05's tests).

**Task 06 — Register Celery Tasks and Schedule**
- Task ID: B04-T06
- Objective: Wire generation into periodic/on-demand execution.
- Why This Is Required: Reports must actually run on cadence.
- Existing Architecture to Follow: `modules/localization/tasks.py` pattern (`translate_content_task`, periodic `retry_failed_translations_task`).
- Existing Files to Reuse: Celery app/beat configuration location (wherever `translate_content_task` is scheduled).
- Files to Create: `src/noorheroes/modules/dashboard/tasks.py`.
- Files to Modify: Celery beat schedule config.
- Implementation Details: `generate_weekly_report_task.delay(child_id)` scheduled weekly per family/child; `generate_monthly_family_report_task.delay(family_id)` scheduled monthly; `generate_ai_insight_report_task` weekly (only for premium families, or generated for all and gated at read-time per B-03 — follow the simpler "generate for all, gate at read" approach consistent with B-03's design); `generate_safety_report_task` NOT scheduled, invoked on-demand only.
- Business Rules: FR-8 cadences.
- Validation: N/A.
- Error Handling: `retry_with_backoff` on transient failures.
- Security: N/A.
- Performance: Batched/staggered scheduling to avoid thundering-herd on the AI provider.
- Localization: N/A.
- RTL: N/A.
- Analytics: Report-generation-delay is monitored (DevOps §10).
- Tests: Covered in Task 06's own test (#7, #8 in §27).
- Documentation: Beat schedule comment.
- Dependencies: Tasks 01–04.
- Do Not Change: Do not modify existing localization Celery tasks/schedule.
- Expected Result: Tasks run on correct cadence.
- Definition of Done: Schedule verified in staging.

## 30. Definition of Done
All 4 report types generate correctly on their cadences, content-safety-gated at write time, monthly report structurally incapable of sibling comparison, all tests green including the two mandatory structural/signature tests.

## 31. Final Verification Checklist
- [ ] `content_safety_passed` cannot be set `true` without validator invocation (code-path audit)
- [ ] Monthly report schema structural test passing
- [ ] Celery retry/backoff configured for AI provider failures
- [ ] Safety report generation is on-demand only, not scheduled
- [ ] Locale-aware generation reuses existing localization pipeline, no parallel mechanism invented
- [ ] Alembic migration reviewed, no destructive changes to unrelated tables
