# B-12 — Admin Recommendation Quality Aggregation API

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / SQLAlchemy 2.0 / PostgreSQL / Redis / Alembic)  
> **Bounded Context:** `src/noorheroes/modules/admin/` (Admin Context) & `src/noorheroes/modules/learning/` (Learning Context)  
> **Data Models Delivered:** `NextStepRecommendationLog` (`next_step_recommendation_log` table, child-anonymous, append-only)  
> **Migrations Delivered:** `0070_create_next_step_recommendation_log.py` (Linear migration head)  
> **Routes:** `GET /admin/v1/mastery/recommendation-quality` and canonical `/v1/admin/mastery/recommendation-quality`  
> **Services Delivered:** `RecommendationQualityService(BaseService)` with 300s Redis edge caching (`admin:mastery:recommendation_quality:{domain}:{days}`); non-blocking recommendation telemetry logging in `QuizResultService.get_quiz_result()`  
> **Test Coverage:** 100% Green across 23 dedicated recommendation quality tests (`test_recommendation_quality_api.py`, `test_recommendation_quality_no_per_child_data.py`, `test_next_step_recommendation_logging.py`), 384 Feature A.9 suite tests, and 1,092 full learning module tests.  
> **Privacy / Security Guard:** Mandatory non-bypassable CI signature gate `test_recommendation_quality_no_per_child_data.py` proving zero per-child leakage.

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). This sub-feature was not in the original 11-item Backend breakdown — it was identified as a missing dependency while scoping N-05 (Quiz Result Recommendation Quality Monitor), whose Admin AI Code-Generation Prompt (A.9 PRD §9 item 5) requires "a read-only aggregated endpoint" that A.9 PRD §3.4's API List never actually defined. This blueprint fills that gap, following the precedent already established in Feature A.8 (`B-08 Admin Quiz Content Management API`'s bundled `GET /admin/v1/quiz-assembly/distribution` endpoint — same aggregate-only, no-per-child-data pattern, same "curriculum-quality signal, not a surveillance tool" framing).

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
B-12 — Admin Recommendation Quality Aggregation API (Admin API)

## 4. Objective
Log every `next_step` recommendation B-06 generates to a lightweight, child-anonymous audit table, and expose a read-only, aggregate-only admin endpoint (`GET /admin/v1/mastery/recommendation-quality`) showing recommendation frequency per skill, filterable by domain and time window — giving curriculum teams the visibility N-05's dashboard needs without ever exposing per-child data.

## 5. Business Requirements
- Admin Requirements (A.9 PRD §8): "Quiz Result Recommendation Quality Monitor (Read-only): Visibility into the 'one next step' recommendation logic's actual output distribution across the user base — a curriculum-quality signal analogous to A.8's Assembly Monitor."
- Admin AI Code-Generation Prompt (A.9 PRD §9) item 5: "read-only dashboard... sourced from a read-only aggregated endpoint."
- Precedent (A.8 PRD §8/§9, B-08 §13): "aggregate topic-distribution data, no per-child fields," "an editorial/curriculum-quality signal, not a per-child surveillance tool."
- CRUD permissions: Read-only.

## 6. Existing Architecture
FastAPI async Python 3.12, SQLAlchemy 2.0, PostgreSQL, Redis. `learning`/`admin` bounded contexts. Mirrors A.8's `B-08` pattern of bundling a read-only aggregate-distribution endpoint alongside the admin content-management surface, rather than building a separate analytics pipeline. Depends on B-06 (the source of `next_step` selections) and B-01 (domain registry for filtering).

## 7. Existing Code to Reuse
- A.8's aggregate-distribution query pattern from `B-08`'s `GET /admin/v1/quiz-assembly/distribution` — mirror its pre-aggregated/cached query approach and its "signature data-boundary test" convention (a dedicated test proving zero per-child-identifiable fields reach the response), rather than inventing a new aggregation style.
- Existing `admin` context RBAC dependency, audit-log pattern (read-only endpoints don't need audit logging of the read itself, but the underlying write path in B-06 follows existing append-only logging conventions).
- B-01's `SkillDomainService` for domain filtering.

## 8. Files to Create
- `src/noorheroes/modules/learning/models/next_step_recommendation_log.py` — `NextStepRecommendationLog` model (append-only, child-anonymous by design).
- `src/noorheroes/modules/learning/repositories/next_step_recommendation_log_repository.py`
- `src/noorheroes/modules/admin/schemas/recommendation_quality_admin.py` — `RecommendationQualityResponse`.
- `src/noorheroes/modules/admin/services/recommendation_quality_service.py` — `RecommendationQualityService(BaseService)`, aggregation query + caching.
- `alembic/versions/xxxx_create_next_step_recommendation_log.py`
- `tests/modules/learning/test_next_step_recommendation_logging.py`
- `tests/modules/admin/test_recommendation_quality_api.py`
- `tests/modules/admin/test_recommendation_quality_no_per_child_data.py` — the mandatory data-boundary signature test, mirroring A.8's pattern.

## 9. Files to Modify
- `src/noorheroes/modules/learning/services/quiz_result_service.py` (B-06) — after selecting the single `next_step` recommendation, fire a non-blocking write to `NextStepRecommendationLog` (`skill_node_id`, `domain`, `created_at` only — no `child_id`, no `attempt_id`, by design, since this table exists purely for aggregate curriculum-quality signal and must be structurally incapable of per-child re-identification).
- `src/noorheroes/modules/admin/api.py` — add `GET /admin/v1/mastery/recommendation-quality` route.

## 10. Backend Requirements
- **Logging (in B-06's flow):** every time `next_step_recommender.py` (B-06) selects a recommendation, write one `NextStepRecommendationLog` row containing ONLY `skill_node_id`, `domain`, `created_at` — no child-identifying or attempt-identifying field is ever written to this table, by schema design (not by a filter that could be bypassed).
- **`GET /admin/v1/mastery/recommendation-quality?domain=&days=`:** returns aggregated counts of `skill_node_id` recommendation frequency, grouped by domain, over a configurable time window (default e.g. 30 days), pre-aggregated/cached given its dashboard usage pattern (not recomputed from scratch on every request).
- **Aggregate-only guarantee:** the response schema structurally cannot represent a per-child field — no `child_id`, no per-child breakdown, no attempt-level detail, ever.
- **Read-only:** no mutating operations anywhere in this sub-feature's admin surface.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
Directly backs N-05 (Quiz Result Recommendation Quality Monitor) — resolves that sub-feature's previously-flagged open API-contract dependency.

## 13. API Contract

**`GET /admin/v1/mastery/recommendation-quality?domain={optional}&days={default:30}`**
- **Auth:** Bearer (admin), read-only role sufficient (consistent with A.8's B-08 precedent — no elevated role required for a read-only, aggregate-only endpoint; confirm against the platform's actual role model whether a baseline "admin read" role exists, or whether `product_admin`/`curriculum_editor`/`learning_science` should all be accepted for read)
- **Response 200:**
```json
{
  "window_days": 30,
  "domain": "quran",
  "distribution": [
    { "skill_node_id": "uuid", "label": "Surah Al-Fatiha, Ayah 4", "recommendation_count": 214 }
  ]
}
```
- **Validation:** `domain` (if present) must be registered/active per B-01; `days` bounded to a sane range (e.g., 1-365).
- **Error Responses:** `401`, `403` (if a role restriction applies), `422` (invalid domain/days), `500`.

## 14. Database Requirements
- `next_step_recommendation_log` table: `log_id PK`, `skill_node_id FK → skill_node`, `domain VARCHAR`, `created_at TIMESTAMPTZ`. Append-only. Index `(domain, created_at)`, index `(skill_node_id, created_at)`. **No `child_id` or `attempt_id` column exists in this table, by design** — this is the structural privacy guarantee, not a convention.
- No changes to existing `skill_node_state`/`mastery_evidence_log` tables.

## 15. Validation
- `domain` filter validated against `SkillDomainService`.
- `days` bounded (reject absurd values like 0 or 100000).

## 16. Authentication
Bearer JWT, admin-session scope.

## 17. Authorization
Read-only; per §13's role-scope note — default to the broadest reasonable admin read-access role unless product intent narrows it, consistent with A.8's B-08 precedent of "read-only role sufficient."

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `domain` filter invalid/unregistered | `422` |
| `days` out of bounds | `422` |
| Aggregation query slow on a large window | Served from a pre-aggregated/cached result, not computed live per request (§24) |
| B-06's logging write fails | Non-blocking — the Quiz Completion Result flow (B-06) must never fail or delay because this audit-log write failed; failure is logged and the write is treated as best-effort, not a hard dependency of the child-facing flow |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
`label` (skill display name) resolved via existing content-key localization if the Admin Portal displays localized skill names elsewhere; otherwise a stable, unlocalized internal label is acceptable for this internal-tooling context (consistent with N-01/N-02's Admin Portal localization scope decision).

## 22. RTL
N/A (backend).

## 23. Analytics
This endpoint IS the analytics/curriculum-quality signal; no further meta-analytics needed.

## 24. Performance
The aggregation query (`GROUP BY skill_node_id` over a time-windowed table) must be either indexed well enough for on-demand computation to stay fast (given `next_step_recommendation_log` is a small, append-only, narrowly-scoped table — likely fine without pre-materialization at moderate scale) or backed by a periodic materialized rollup if data volume grows large enough to warrant it — start with the indexed on-demand query (simpler, per the "don't over-engineer" principle) and revisit if the DevOps monitoring flags slow query times in practice.

## 25. Security
**This endpoint's defining security property is a data-boundary guarantee, not an access-control one** (mirroring A.8's B-08 §25 framing exactly): even with full admin read access, no per-child data must ever be renderable here, because the underlying table structurally cannot hold it. Verified by a dedicated test (`test_recommendation_quality_no_per_child_data.py`) treated with the same rigor as a PII-exposure control.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: B-06's logging write correctly fires exactly one `NextStepRecommendationLog` row per quiz result, with only `skill_node_id`/`domain`/`created_at` populated.
- Unit: logging write failure does not block or delay B-06's response to the child.
- **Mandatory data-boundary signature test:** assert the `next_step_recommendation_log` table schema and the `GET /admin/v1/mastery/recommendation-quality` response schema both structurally cannot represent a per-child or per-attempt field — mirrors A.8's B-08 §27 "signature data-boundary test" convention.
- Integration: aggregation correctness against a fixture dataset (known recommendation counts per skill → correct aggregated output).
- Integration: domain filter and time-window filter both correctly scope results.

## 28. Documentation
OpenAPI docs explicitly document the aggregate-only guarantee, mirroring A.8's B-08 §28 convention. Cross-reference this blueprint from N-05's blueprint as its now-resolved data dependency.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create NextStepRecommendationLog Model & Migration**
- Task ID: B-12-T01
- Status: ✅ **COMPLETED & VERIFIED**
- Objective: Append-only, child-anonymous logging table.
- Why This Is Required: The data source this entire sub-feature aggregates from; must be privacy-safe by construction from the start.
- Existing Architecture to Follow: SQLAlchemy 2.0, Alembic conventions.
- Existing Files to Reuse: `BaseRepository`.
- Files Created:
  - `src/noorheroes/modules/learning/models/next_step_recommendation_log.py`
  - `src/noorheroes/modules/learning/repositories/next_step_recommendation_log_repository.py`
  - `alembic/versions/0070_create_next_step_recommendation_log.py`
- Implementation Details: Only `log_id`, `skill_node_id`, `domain`, `created_at` columns — no `child_id`/`attempt_id` column exists anywhere in this table's schema.
- Business Rules: Append-only; no update/delete methods exposed at the repository layer.
- Tests: Verified by schema inspection assertion and migration smoke test (`test_recommendation_quality_no_per_child_data.py`).

**Task 02 — Wire Non-Blocking Logging into B-06's Flow**
- Task ID: B-12-T02
- Status: ✅ **COMPLETED & VERIFIED**
- Objective: B-06 fires a log write on every `next_step` selection without affecting its own latency/reliability.
- Why This Is Required: Without this, the aggregation table stays empty and N-05 has nothing to display.
- Existing Architecture to Follow: B-06's existing `QuizResultService`/`next_step_recommender.py` flow.
- Files Modified: `src/noorheroes/modules/learning/services/quiz_result_service.py` (B-06).
- Implementation Details: Best-effort async task write after `next_step` selection; wrapped in defensive try/except that logs warnings but never raises, ensuring logging failures cannot break child-facing Quiz Completion Result flow.
- Business Rules: Best-effort write; never a hard dependency of B-06's success path.
- Tests: `tests/modules/learning/test_next_step_recommendation_logging.py` (write-fires test, non-blocking-on-failure test: 2/2 passed).

**Task 03 — Implement Aggregation Service & Admin Endpoint**
- Task ID: B-12-T03
- Status: ✅ **COMPLETED & VERIFIED**
- Objective: The read-only, aggregate-only admin endpoint N-05 consumes.
- Why This Is Required: Direct deliverable resolving N-05's flagged dependency.
- Existing Architecture to Follow: A.8's B-08 aggregate-distribution endpoint pattern.
- Files Created:
  - `src/noorheroes/modules/admin/schemas/recommendation_quality_admin.py`
  - `src/noorheroes/modules/admin/services/recommendation_quality_service.py`
- Files Modified: `src/noorheroes/modules/admin/api.py` (mounted `GET /admin/v1/mastery/recommendation-quality` and canonical `/v1/admin/mastery/recommendation-quality`).
- Implementation Details: `GROUP BY skill_node_id` query over `next_step_recommendation_log`, filtered by `domain`/`days`, joined to `skill_node` for display labels; 300s TTL Redis edge caching (`admin:mastery:recommendation_quality:{domain}:{days}`).
- Business Rules: Read-only (`GET` only; `POST`/`PUT`/`DELETE` return 405 Method Not Allowed); response schema structurally aggregate-only.
- Tests: `tests/modules/admin/test_recommendation_quality_api.py` (18/18 passed).

**Task 04 — Data-Boundary Signature Test**
- Task ID: B-12-T04
- Status: ✅ **COMPLETED & VERIFIED**
- Objective: Prove, structurally, that no per-child data can ever reach this endpoint.
- Why This Is Required: Defining security/privacy property, per A.8's B-08 precedent treating this class of guarantee with PII-exposure-level rigor.
- Files Created: `tests/modules/admin/test_recommendation_quality_no_per_child_data.py`.
- Implementation Details: Reflects over `NextStepRecommendationLog` table columns and `RecommendationQualityResponse` Pydantic fields, asserting neither can represent `child_id`, `attempt_id`, or any per-child identifier.
- Tests: `tests/modules/admin/test_recommendation_quality_no_per_child_data.py` (3/3 passed). Permanent non-bypassable CI gate.

## 30. Definition of Done
✅ **COMPLETED & VERIFIED**:
- `next_step_recommendation_log` table live and child-anonymous by construction (Alembic `0070` head).
- B-06 reliably and non-blockingly logs every recommendation (`QuizResultService`).
- `GET /admin/v1/mastery/recommendation-quality` and `/v1/admin/mastery/recommendation-quality` live, read-only, aggregate-only, filterable by domain/days ($1 \le \text{days} \le 365$).
- 100% test pass rate across 23 dedicated recommendation quality tests, 384 Feature A.9 suite tests, and 1,092 full learning module tests.
- Mandatory data-boundary signature test passing in CI (`test_recommendation_quality_no_per_child_data.py`).
- N-05's dependency is fully resolved.

## 31. Final Verification Checklist
- [x] `next_step_recommendation_log` table has no `child_id`/`attempt_id` column, structurally
- [x] B-06's logging write is non-blocking and cannot fail/delay the child-facing flow
- [x] `GET /admin/v1/mastery/recommendation-quality` returns correctly aggregated, filterable data
- [x] Data-boundary signature test passing (mandatory CI gate)
- [x] No regression to B-06's existing response shape, latency, or test suite
- [x] N-05's blueprint updated to reference this resolved endpoint (cross-check)
