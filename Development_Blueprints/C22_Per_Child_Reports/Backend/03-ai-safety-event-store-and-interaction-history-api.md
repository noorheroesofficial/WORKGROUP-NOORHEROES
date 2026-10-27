# Blueprint: AI Safety Event Store & Interaction History API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/ai_safety/` (existing bounded context per `FAST-API-INSTRUCTIONS.md` §5.3) plus a `dashboard`-facing read endpoint. Delivers the `ai_safety_event` table, its Kafka ingestion consumer, and `GET /v1/children/{id}/ai-history?from=&to=` — the single most trust-critical component of C.22.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
B-03 — AI Safety Event Store & Interaction History API.

## 4. Objective
Build a structurally redacted event store — no column capable of holding a raw prompt/response transcript — that is the exclusive data source for the parent-facing AI Interaction History, enforcing FR-5/FR-13 at the data-architecture level rather than as a display-layer choice.

## 5. Business Requirements
Source: PRD §1.7 FR-5, FR-13, FR-14, §1.9 Acceptance Criteria, §1.10 Edge Case #8, §3.3, §4.1, §4.2, §5 item 1.
- Reports never include raw AI chat transcripts, only flags (FR-5) — a hard, zero-exception rule.
- AI Interaction History entries are derived exclusively from safety-event/flag records, never from raw prompt/response logs (FR-13) — architectural, not display-layer.
- If AI is disabled mid-period, history shows activity only up to the disable point, no further entries implied (Edge Case 8).
- Consistent with A.5 §1.7 FR-10's zero-retention recitation pipeline principle, extended to the broader AI-interaction-logging surface.

## 6. Existing Architecture
Per `FAST-API-INSTRUCTIONS.md` §5.3, `ai_safety` is already one of the platform's 10 bounded contexts (`src/noorheroes/modules/ai_safety/`), implying safety-event infrastructure (categories, flagging) already exists for at least the child-facing AI guardrail system (A.5). This blueprint extends that existing context with the `ai_safety_event` table (if not already present) and exposes a new parent-facing read endpoint, consumed by the `dashboard` module's aggregation layer (B-01) for the summary view and directly by K-03 for the full history screen.

## 7. Existing Code to Reuse
- `require_parent_session_only` (C.20 B-01) for the parent-facing endpoint.
- `ChildRepository.get_child_by_id_and_family()` for family-ownership validation.
- The category taxonomy is owned by this feature's own B-09 (`AiSafetyCategoryDefinition`, `src/noorheroes/modules/ai_safety/`) — the ingestion consumer must resolve incoming events' categories against that table (or its cached enum), not a separate/duplicate taxonomy.
- Existing Kafka consumer infrastructure/base class used elsewhere in the platform for event ingestion, if present.

## 8. Files to Create
- `src/noorheroes/modules/ai_safety/models.py` — `AiSafetyEvent` SQLAlchemy model (or extend if a partial model exists)
- `src/noorheroes/modules/ai_safety/ai_safety_event_consumer.py` — Kafka consumer for AI safety event ingestion, following the same base class/framework as `modules/notifications/trigger_consumer.py` and A.6's `dua_marked_learned_consumer.py`
- `alembic/versions/xxxx_create_ai_safety_event.py`
- `tests/modules/ai_safety/test_ai_safety_event_schema_structural.py`
- `tests/modules/ai_safety/test_ai_interaction_history_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/ai_safety/schemas.py` — add `AiInteractionHistoryResponse`, `AiSafetyEventEntry`
- `src/noorheroes/modules/ai_safety/service.py` — add `get_interaction_history(parent_ctx, child_id, date_from, date_to)`
- `src/noorheroes/modules/ai_safety/api.py` — add `GET /v1/children/{id}/ai-history`
- `src/noorheroes/modules/dashboard/service.py` — wire `ai_interaction_summary` fan-out call (B-01) to this module's repository

## 10. Backend Requirements
- **Table `ai_safety_event`:** `event_id` (PK), `child_id` (FK), `category` (enum: `topic_blocked`, `question_redirected`, `question_approved`, extensible via B-09's taxonomy manager), `summary_text` (short, pre-templated categorical description — **not free-form user-generated text**), `concerning` (boolean), `occurred_at` (timestamptz), `source_event_id` (unique, the upstream Kafka event's own ID, for redelivery idempotency — mirrors A.12 B-02's idempotent-grant pattern). **No column named or capable of holding `raw_prompt`, `raw_response`, or `transcript`.**
- Indexes: `(child_id, occurred_at DESC)`, `(child_id, concerning)`, unique index on `source_event_id`.
- Kafka consumer ingests events from the Child-Safe AI Layer's flagging pipeline (A.5), mapping each flagged/categorized interaction to an `ai_safety_event` row — the consumer's mapping function must only ever write to the categorical/summary fields, never accept or forward a raw text payload into a persisted column.
- `GET /v1/children/{id}/ai-history?from=&to=`: validate family-ownership, apply date range consistently with B-01's range resolution, return entries ordered by `occurred_at DESC`.
- If AI was disabled for the child partway through the range, entries simply stop at the disable timestamp — this falls out naturally from the event-sourced design (no synthetic "AI disabled" filler needed) as long as the ingestion consumer stops receiving events post-disable, which is enforced upstream in A.5/C.23's AI-disable flow, not duplicated here.

## 11. KMP Requirements
Consumed directly by K-03 (`AiInteractionHistoryScreen`) and indirectly via B-01's `ai_interaction_summary`. Response must map cleanly to a flat list-row UI model — no nested conversational structure that could imply a transcript exists.

## 12. NextJS Requirements
N/A for the parent-facing endpoint. B-09 (admin taxonomy manager) governs the `category`/`summary_text` template library consumed here.

## 13. API Contract
- **HTTP Method:** GET
- **Endpoint:** `/v1/children/{id}/ai-history?from=&to=`
- **Auth:** Bearer, parent session only
- **Request:** path `id: str` (child_id); query `from: date`, `to: date`
- **Response 200:**
```json
{
  "entries": [
    { "date": "ISO-8601", "category": "topic_blocked", "summary": "A question about {topic} was redirected to approved content", "concerning": false }
  ]
}
```
- **Authentication:** Bearer parent session
- **Authorization:** Family-ownership on `id`
- **Validation:** `from`/`to` required
- **Error Responses:** `403`/`404` `ChildScopeViolationError`, `401` invalid session

## 14. Database Requirements
`ai_safety_event`: FK `child_id`; `CHECK category IN (...)`; append-only (no soft delete — historical record); indexes per §10. Retention per platform's compliance-relevant policy (PRD §4.5) — carries none of the heightened sensitivity a raw-transcript retention policy would, precisely because no such column exists.

## 15. Validation
- `child_id`/`id` required, family-owned.
- `category` constrained to the enum/taxonomy managed by B-09.
- `summary_text` at write time must originate only from the pre-templated library (enforced by B-09's admin-side validation and by the ingestion consumer never accepting free-form text).

## 16. Authentication
Bearer parent session.

## 17. Authorization
Family-ownership check on `child_id`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Cross-family `child_id` | `403`/`404` `ChildScopeViolationError` |
| Zero events in range | `200` with `entries: []` — client renders "No AI interactions recorded" |
| Kafka consumer ingestion failure | Dead-letter queue + alert; does not block API read path |

## 19. Offline First
N/A server-side; K-09 handles client-side caching.

## 20. Local Data
N/A (backend).

## 21. Localization
`summary_text` templates are locale-aware at the template layer (B-09), resolved server-side before serialization so the client never needs to translate categorical codes itself.

## 22. RTL
N/A (backend).

## 23. Analytics
`ai_interaction_history_viewed` / `ai_interaction_concerning_flag_acted_on` fired client-side (K-03).

## 24. Performance
Indexed `(child_id, occurred_at DESC)` lookup, p95 within Report load NFR; Kafka consumer processes ingestion asynchronously, decoupled from the read path's latency.

## 25. Security
The structural absence of a raw-transcript-capable column is this endpoint's — and arguably this entire feature's — single most important security control. `summary_text`'s placeholder-only template constraint (enforced in B-09) prevents it from ever becoming an indirect free-form-text injection vector.

## 26. Library Requirements
Kafka consumer client — reuse the platform's existing consumer framework, confirmed in use by A.6 B-05 (`dua_marked_learned_consumer.py`), B17 B-02 (`modules/notifications/trigger_consumer.py`), and A.12 B-02's avatar-unlock consumer — each bounded context owns its own consumer file following this same base class/framework, so this feature's consumer belongs at `src/noorheroes/modules/ai_safety/ai_safety_event_consumer.py` (rename from the generic `consumers.py` in §8), registered at consumer startup alongside the others.

## 27. Testing
1. **Schema-introspection test (CI-blocking, highest priority):** assert `ai_safety_event` has no column matching `/prompt|response|transcript|raw_text/i`.
2. Unit test: entries correctly filtered by date range.
3. Unit test: zero events returns empty list, not an error.
4. Unit test: cross-family `child_id` rejected.
5. Unit test: `concerning` flag correctly surfaced per entry.
6. Integration test: Kafka consumer correctly maps a fixture flagged interaction to a row without ever touching a raw-text field.
7. Integration test: full read request through the gate.
8. Test per category (`topic_blocked`, `question_redirected`, `question_approved`).

## 28. Documentation
OpenAPI docstring stating the structural no-transcript guarantee explicitly; module README documenting the ingestion consumer's mapping contract (categorical fields only).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create AiSafetyEvent Model, Migration, and Structural Schema Test**
- Task ID: B03-T01
- Objective: Define the table with no raw-transcript-capable column and prove it via an automated test.
- Why This Is Required: FR-5/FR-13's foundational structural guarantee.
- Existing Architecture to Follow: SQLAlchemy 2.0 model conventions, Alembic migration pattern used elsewhere in `ai_safety`/other modules.
- Existing Files to Reuse: `common/base_repository.py` pattern if applicable.
- Files to Create: `models.py` (or extend), migration, `tests/modules/ai_safety/test_ai_safety_event_schema_structural.py`.
- Files to Modify: none beyond model file.
- Implementation Details: Columns per §10; `CHECK category IN (...)`; indexes per §10.
- Business Rules: FR-5, FR-13.
- Validation: N/A (schema-level).
- Error Handling: N/A.
- Security: This task's test IS the primary security control for the whole feature.
- Performance: Indexes as specified.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Schema-introspection test asserting no `/prompt|response|transcript|raw_text/i` column, made CI-blocking.
- Documentation: Table docstring/comment stating the design intent.
- Dependencies: none.
- Do Not Change: Existing `ai_safety` module tables unrelated to this feature.
- Expected Result: Table exists, migration applies, structural test passes.
- Definition of Done: Structural test is green and wired into CI as a blocking gate.

**Task 02 — Implement Kafka Ingestion Consumer**
- Task ID: B03-T02
- Objective: Ingest categorized safety events from the Child-Safe AI Layer.
- Why This Is Required: This is how `ai_safety_event` rows are populated in production.
- Existing Architecture to Follow: Platform's existing Kafka consumer base class/framework, the same one used by `modules/notifications/trigger_consumer.py` (B17 B-02) and A.6's `dua_marked_learned_consumer.py` — offset commit occurs only after the DB insert succeeds (at-least-once semantics), with idempotency enforced at the DB layer, mirroring A.12 B-02's unlock-evaluation-engine pattern for duplicate-redelivery safety.
- Existing Files to Reuse: Existing Kafka client configuration; existing consumer registry/startup wiring where other modules' consumers are registered.
- Files to Create: `ai_safety_event_consumer.py`.
- Files to Modify: Consumer registry/startup wiring.
- Implementation Details: Consumer function accepts only categorical/summary fields from the upstream message schema; explicitly rejects/drops (with alerting) any message containing an unexpected free-form-text-shaped field rather than silently persisting it. Include a unique `source_event_id` constraint on `ai_safety_event` (or an equivalent idempotency key) so redelivery of the same upstream event cannot create a duplicate row.
- Business Rules: FR-13.
- Validation: Message schema validation at consumption time.
- Error Handling: Dead-letter queue for malformed messages; does not crash the consumer loop.
- Security: Defense-in-depth rejection of unexpected raw-text-shaped fields.
- Performance: Async consumption, no blocking of the read API.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Consumer contract documented in module README.
- Dependencies: Task 01.
- Do Not Change: Upstream A.5 Child-Safe AI Layer internals.
- Expected Result: Events flow from Kafka into `ai_safety_event`.
- Definition of Done: Fixture message correctly ingested; malformed/unexpected-field message correctly dead-lettered.

**Task 03 — Implement get_interaction_history Service Method and Route**
- Task ID: B03-T03
- Objective: Expose `GET /v1/children/{id}/ai-history`.
- Why This Is Required: Public contract for AI Interaction History.
- Existing Architecture to Follow: Router → Service → Repository layering; `require_parent_session_only`.
- Existing Files to Reuse: `ChildRepository`.
- Files to Create: none.
- Files to Modify: `schemas.py`, `service.py`, `api.py`.
- Implementation Details: Per §10 read-path requirements.
- Business Rules: FR-5, FR-13, FR-14.
- Validation: Family-ownership, date-range required.
- Error Handling: Per §18.
- Security: No raw content ever queryable through this path (schema guarantees this).
- Performance: Indexed query.
- Localization: `summary_text` resolved server-side.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: OpenAPI summary.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Endpoint live.
- Definition of Done: Matches §13.

**Task 04 — Write Full Test Suite**
- Task ID: B03-T04
- Objective: Cover §27 including the structural test and ingestion mapping test.
- Why This Is Required: This blueprint carries the feature's single highest-priority guarantee.
- Existing Architecture to Follow: pytest + fixture factories.
- Existing Files to Reuse: Family/child/session fixtures.
- Files to Create: `tests/modules/ai_safety/test_ai_interaction_history_api.py`.
- Files to Modify: none.
- Implementation Details: 8 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact responses.
- Security: All tests here are security-critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings citing FR-5/FR-13.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green; structural test is a non-bypassable CI gate.

## 30. Definition of Done
`ai_safety_event` table exists with no raw-transcript-capable column (proven by CI-blocking test), Kafka consumer ingests categorized events only, `GET /v1/children/{id}/ai-history` live and gated, all tests green.

## 31. Final Verification Checklist
- [ ] Schema-introspection test asserting no `/prompt|response|transcript|raw_text/i` column, CI-blocking
- [ ] Kafka consumer never persists a free-form-text-shaped field
- [ ] Family-ownership check verified
- [ ] Date-range filtering consistent with B-01's resolved range
- [ ] Zero-events clean state verified
- [ ] `summary_text` sourced only from B-09's pre-templated library
- [ ] OpenAPI docs state the structural guarantee explicitly
