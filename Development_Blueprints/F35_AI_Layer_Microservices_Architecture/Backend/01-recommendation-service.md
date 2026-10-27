# B-01 — Recommendation Service

## 1. Feature Context
The ranking service behind Home's next-best-action suggestions — deliberately scoped to a small, curated corpus rather than a general LLM tutor, and re-verifying every candidate's actual current availability at the moment of serving rather than trusting a potentially-stale ranking index.

## 2. Parent Feature
F.35 — AI Layer & Microservices Architecture

## 3. Sub-feature
1.1 Recommendation Service (ID: **B-01**)

## 4. Objective
Build `POST /v1/ai/recommendations`, ranking candidates by age/language/progress/parent-preferences/safety-tags, re-verifying each candidate's current (not-withdrawn) content availability at serve time.

## 5. Business Requirements
- FR-1: ranks stories, lessons, habits, missions, next-best actions; controls: age, language, progress, parent preferences, safety tags.
- FR-11: deliberately small, curated corpus, not a general LLM tutor.
- §5 Backend AI prompt item 1: re-verify each candidate's current availability at SERVE TIME, never trusting a stale index — mandatory test.
- Edge Case 1: the citation/safety verifier checks current content availability at serve-time, not merely at indexing time.
- §1.12: thin-corpus locale/age-bands fall back to a sensible, clearly-non-personalized default set, never an empty result.

## 6. Existing Architecture
Logical `ai` module within the modular monolith (per FR-10, not a separate deployed service), `app/ai/services/recommendation_service.py`, reading E.29's approved `content_version` table read-only.

## 7. Existing Code to Reuse
- E.29's `content_version` schema (read-only, approved-corpus-only query)
- E.30's Citation/Safety Verifier and six-stage pipeline (this service's output passes through it, not duplicated here)
- A.2's existing graceful-degradation default-set pattern (reused for the thin-corpus fallback)

## 8. Files to Create
- `app/ai/routers/recommendation_router.py`
- `app/ai/services/recommendation_service.py`
- `app/ai/repositories/recommendation_repository.py`
- `app/ai/schemas/recommendation_schema.py`
- `alembic/versions/xxxx_create_ai_recommendation_log_table.py`

## 9. Files to Modify
- `app/ai/routers/__init__.py` — register router (new `ai` module if not yet present, per `FAST-API-INSTRUCTIONS.md`'s bounded-context conventions)

## 10. Backend Requirements
- `RecommendationService.rank()`: builds a candidate set from the approved corpus filtered by age/language/progress/safety-tags, ranks by `rank_score`.
- `RecommendationService.serve()`: for each ranked candidate, re-queries E.29's `content_version` table for current `status`/`withdrawn` state immediately before returning the response — this re-check is unconditional and cannot be skipped even if the ranking index was refreshed moments ago; any candidate found withdrawn is excluded from the response, never merely deprioritized.
- Thin-corpus fallback: when the filtered candidate set falls below a minimum viable size, the service returns a fixed, clearly-non-personalized default set rather than an empty or partial result.
- Logs every serve to `ai_recommendation_log`.

## 11. Required API / API Contract
`POST /v1/ai/recommendations` `{child_id, context}` → `200 { "items": [ { "content_id", "rank_score", "reason_tags" } ] }`.

## 12. Database Requirements
`ai_recommendation_log(log_id PK, child_id FK, content_version_id FK, rank_score, served_at)`. Index `(child_id, served_at DESC)`. Reads E.29's `content_version` read-only.

## 13. Validation
`child_id`/`context` required; `context` enum-validated (e.g., `home_feed`).

## 14. Authentication
Internal service-to-service auth (called by A.2's Home feed assembly, not directly by an external client).

## 15. Authorization
Internal call scope only — not admin-gated, not directly client-exposed.

## 16. Error Handling
Thin-corpus scenario returns the default set (`200`), never an error; internal-service-auth failure `401`.

## 17. Security
Serve-time re-verification is this sub-feature's defining guarantee — mandatory test confirms a fixture content item marked withdrawn in E.29's table AFTER being indexed by the ranking process is still correctly excluded from the response, proving the check happens at serve time, not index time.

## 18. Analytics
`ai_recommendation_served` (with `service: recommendation`, `corpus_size`) per §1.19.

## 19. Performance
Indexed candidate queries; re-verification query batched (single query for all candidate IDs, not N+1) to avoid serve-time latency regression from the mandatory re-check.

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Redis (candidate-index caching, re-verification always bypasses this cache). No new libraries.

## 21. Testing
Unit: ranking-score computation, thin-corpus fallback trigger threshold. Integration: **mandatory** — a content item withdrawn after index-time is excluded from results despite remaining in the ranking index; default-set fallback returns a non-empty, clearly-non-personalized result for a thin-corpus fixture; batched re-verification query count test (no N+1).

## 22. Documentation
OpenAPI docstring noting the mandatory serve-time re-verification and its unconditional nature.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Write Migration for `ai_recommendation_log`**
Objective: Table with FK/index. Files: `alembic/versions/xxxx_create_ai_recommendation_log_table.py`. Tests: migration test. Definition of Done: schema created.

**Task 02 — Define Schemas**
Objective: `RecommendationRequest`, `RecommendationResponse`. Files: `schemas/recommendation_schema.py`. Dependencies: Task 01. Tests: schema validation. Definition of Done: tests pass.

**Task 03 — Implement `RecommendationRepository`**
Objective: Candidate-set query against E.29's approved corpus, batched re-verification query. Files: `repositories/recommendation_repository.py`. Dependencies: Task 01. Tests: repository tests. Definition of Done: tests pass.

**Task 04 — Implement `RecommendationService` with Mandatory Serve-Time Re-Verification**
Objective: Rank + unconditional re-check before response assembly. Files: `services/recommendation_service.py`. Dependencies: Task 03. Tests: **mandatory** — withdrawn-after-index-time exclusion test. Definition of Done: test passes.

**Task 05 — Implement Thin-Corpus Fallback**
Objective: Default-set logic below minimum-viable-candidate threshold. Dependencies: Task 04. Tests: fallback-triggers-correctly test. Definition of Done: test passes.

**Task 06 — Implement the Router Endpoint**
Objective: `POST /v1/ai/recommendations`. Files: `routers/recommendation_router.py`. Dependencies: Task 05. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 07 — Wire Logging**
Objective: `ai_recommendation_log` entry per serve. Dependencies: Task 06. Tests: log-entry test. Definition of Done: test passes.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §21, mandatory test included. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm the re-verification query cannot be bypassed or skipped under any code path, including cache-hit scenarios. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] Serve-time re-verification unconditionally excludes withdrawn content — mandatory test passing
- [ ] Re-verification is batched, not N+1
- [ ] Thin-corpus scenario returns a non-empty, clearly-non-personalized default set
- [ ] Every serve logged to `ai_recommendation_log`

## 25. Definition of Done
The Recommendation Service provably never serves withdrawn content regardless of index staleness, and gracefully degrades to a sensible default when the curated corpus is too thin for genuine personalization.
