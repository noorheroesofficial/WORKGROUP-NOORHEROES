# B-02 — AI Interaction History Read API

## 1. Feature Context
Part of Feature C.26 — Privacy, Consent, Account Security & Data Rights (Settings). Intended as "the richer, still-redacted-at-write-time log" distinct from C.22's flags-only Safety Report (C.26 scope note). This sub-feature carries a **route/schema collision with an already-built endpoint that must be resolved before implementation, not silently duplicated.**

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**B-02 — AI Interaction History Read API** (`GET /v1/children/{id}/ai-history?date_from=&date_to=`)

## 4. Objective
Give parents a fuller (but still structurally redacted-at-write-time) AI interaction record, without creating a second, parallel AI-event table/endpoint alongside the one C.22 B-03 already built at the identical route.

## 5. Business Requirements
- FR-6: entries redacted at write time — no unredacted column exists anywhere, structurally.
- FR-7: each entry carries `model_version` and `policy_result` (allowed/blocked/redirected) alongside redacted input/output summaries and `expires_at`.
- Edge Case 4/8: "no interactions this period" vs. "AI always off" empty states.
- Edge Case 3: entries subject to the same cascade-deletion/retention rules as other family data.

## 6. Existing Architecture — Resolved, Conflict Flagged (read before implementing)
**Conflict:** C.22 B-03 ("AI Safety Event Store & Interaction History API") already implements `GET /v1/children/{id}/ai-history?from=&to=` — the **exact same route** this sub-feature's own PRD (§3.4) specifies (`?date_from=&date_to=` vs. C.22's `?from=&to=` — even the query param names nearly collide). C.22's table (`ai_safety_event`: `event_id`, `child_id`, `category` enum, `summary_text` templated string, `concerning` boolean, `occurred_at`) is deliberately **flags-only** — it has no `model_version`, `input_redacted`, `output_redacted`, or `policy_result` columns, because C.22 FR-13 requires history to be derived exclusively from categorical safety-event records, never richer content.

C.26's own FR-6/FR-7 require a genuinely richer shape (`model_version`, `input_redacted`, `output_redacted`, `policy_result`) that C.22's table cannot serve without modification. **Building a second, separate `ai_interactions` table plus a second Kafka consumer against the same upstream AI Moderation Service, at a colliding route, would create two independently-drifting AI-interaction records for the same underlying interactions — precisely the kind of duplicated, un-reused architecture rule 23/2 prohibit.**

**Proposed resolution (requires cross-feature architecture sign-off with C.22's owner before implementation — do not proceed silently):**
1. Extend C.22's existing `ai_safety_event` table (in `modules/ai_safety`) with three additional nullable columns: `model_version`, `input_redacted`, `output_redacted` — populated by the same upstream ingestion consumer (`ai_safety_event_consumer.py`), which already only ever writes categorical/redacted fields and already rejects any raw-text-shaped field. `policy_result` is a **new derived value**, not a new column: map C.22's existing `category` enum (`topic_blocked`, `question_redirected`, `question_approved`) to `policy_result` (`blocked`, `redirected`, `allowed`) via a pure mapping function — no schema duplication needed for that field.
2. Retire the C.26 PRD's separate `ai_interactions`/`data_request`-adjacent ER diagram entry for this specific table (§4.1 in the C.26 PRD) as superseded by this extension — **do not create it.**
3. Route ownership stays with C.22 B-03's existing `GET /v1/children/{id}/ai-history` endpoint; this sub-feature (B-02) becomes a **thin extension task** against that endpoint (add `model_version`/`input_redacted`/`output_redacted`/`policy_result` to its response schema) rather than a net-new endpoint — the two features' "flags-only" vs. "fuller" distinction becomes a **response-verbosity difference on one shared endpoint** (e.g., an optional `?detail=full` query flag, or simply always returning the richer shape since flags-only was never a hard privacy requirement, only a design choice) — confirm the exact mechanism with C.22's owner.
4. **Until this cross-feature confirmation happens, this blueprint should not be executed as a net-new build** — flag as blocked in project tracking.

## 7. Existing Code to Reuse
- `modules/ai_safety/models.py::AiSafetyEvent` (C.22 B-03) — extend, do not duplicate.
- `modules/ai_safety/ai_safety_event_consumer.py` (C.22 B-03) — extend the ingestion mapping, do not create a second consumer.
- `modules/ai_safety/service.py::get_interaction_history()` (C.22 B-03) — extend response shape.
- `require_parent_session_only` (C.20 B-01).
- `ChildRepository.get_child_by_id_and_family()`.

## 8. Files to Create
- `tests/modules/ai_safety/test_ai_history_extended_fields_schema_structural.py` — schema-introspection test confirming the new columns still contain no raw-transcript-capable field name/type.

## 9. Files to Modify (pending cross-feature sign-off per §6)
- `src/noorheroes/modules/ai_safety/models.py` — add `model_version VARCHAR NULL`, `input_redacted VARCHAR(max-length) NULL`, `output_redacted VARCHAR(max-length) NULL` to `AiSafetyEvent`.
- `alembic/versions/xxxx_extend_ai_safety_event_redacted_fields.py`.
- `src/noorheroes/modules/ai_safety/ai_safety_event_consumer.py` — populate the three new fields from the same upstream message, still rejecting any raw-text-shaped field.
- `src/noorheroes/modules/ai_safety/schemas.py` — extend `AiInteractionHistoryResponse`/`AiSafetyEventEntry` with the new fields and a derived `policy_result`.
- `src/noorheroes/modules/ai_safety/service.py` — add the `category` → `policy_result` mapping function.

## 10. Backend Requirements
- `policy_result` is **derived**, never independently stored: `topic_blocked → "blocked"`, `question_redirected → "redirected"`, `question_approved → "allowed"` (pure mapping function, unit-testable in isolation).
- New redacted columns carry the same max-length constraint discipline as `summary_text` — bounded, never unbounded free text.
- **Signature test (inherited from C.22 B-03, re-run against the extended schema):** no column across the table is named/typed consistent with raw content storage.
- **Signature test:** the read endpoint performs no string-manipulation/filtering on `input_redacted`/`output_redacted` before returning them — redaction is complete at write time, this endpoint is a pure read.
- Empty states: "AI always off" (child never had AI enabled — check `ChildProfile.ai_enabled` history, or absence of any row) vs. "no interactions this period" (rows exist outside the queried range) — both already partially supported by C.22 B-03's design; confirm the "AI always off" distinction is actually implemented there or add it here if missing.

## 11. API Contract

### `GET /v1/children/{id}/ai-history?date_from=&date_to=` (extends C.22 B-03's existing endpoint — confirm final param naming with that owner, `from`/`to` vs. `date_from`/`date_to`)
- **Response 200:**
```json
{ "entries": [ { "id": "...", "model_version": "...", "input_redacted": "...", "output_redacted": "...", "policy_result": "allowed|blocked|redirected", "occurred_at": "..." } ] }
```
- **Error Responses:** `403`/`404` `ChildScopeViolationError`, `401` invalid session.

## 12. Database Requirements
Extends `ai_safety_event` (owned by C.22 B-03) with 3 new nullable columns. **No new table** — building a separate `ai_interactions` table is explicitly out of scope per §6's resolution.

## 13. Validation
`date_from`/`date_to` required; family-ownership of `id` (child_id) enforced.

## 14. Authentication
Bearer parent session (`require_parent_session_only`).

## 15. Authorization
Family-ownership check on `child_id`.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Cross-family `child_id` | `403`/`404` |
| Zero events in range | `200`, `entries: []` |
| AI never enabled for child | `200`, `entries: []` with a distinct `ai_never_enabled: true` response flag (client renders the dedicated empty state) |
| Kafka ingestion failure | Dead-letter queue + alert, does not block reads |

## 17. Offline First
N/A server-side.

## 18. Local Data
N/A (backend).

## 19. Localization
N/A — this endpoint returns redacted summaries and codes, not display copy needing server-side translation beyond what C.22 B-03 already resolves for `summary_text`.

## 20. RTL
N/A (backend).

## 21. Analytics
Backing source for K-03's `ai_interaction_history_viewed`, `ai_interaction_detail_viewed`, `ai_history_empty_state_shown`.

## 22. Performance
Same indexed `(child_id, occurred_at DESC)` lookup C.22 B-03 already established — no new index needed for the additional nullable columns.

## 23. Security
The structural absence of a raw-transcript-capable column remains the defining guarantee, inherited entirely from C.22 B-03's existing design — this sub-feature's only responsibility is to extend it correctly, not to re-derive the guarantee independently (re-deriving it independently is exactly the risk a second parallel table would introduce).

## 24. Library Requirements
No new libraries — reuses C.22 B-03's Kafka consumer framework.

## 25. Testing
- **Blocking precondition:** confirm with C.22's owner that extending `ai_safety_event` (vs. building a new table) is the agreed resolution before writing any test against a net-new table.
- Schema-introspection test re-run against the extended table (no raw-content-capable column).
- Unit: `category` → `policy_result` mapping covers all 3 known categories; unmapped/future categories fail loudly rather than silently defaulting.
- Unit: read endpoint performs zero string manipulation on the redacted fields.
- Integration: "AI always off" vs. "no interactions this period" empty states are distinguishable in the response.
- Integration: extended ingestion consumer still rejects any raw-text-shaped upstream field.

## 26. Documentation
OpenAPI description must state explicitly that this is the same underlying table/route as C.22's Safety Report, extended with additional redacted fields for C.26's fuller view — cross-reference both blueprints from each other's docs to prevent future duplication.

## 27. AI Coding Agent Implementation Steps

**Task 00 — Cross-Feature Architecture Sign-Off (blocking)**
- **Objective:** Confirm the §6 resolution (extend C.22's table, do not build a new one) with C.22's feature owner before any code is written.
- **Definition of Done:** Written confirmation obtained; final query-param naming (`from`/`to` vs `date_from`/`date_to`) and response-verbosity mechanism (`?detail=full` vs. always-full) decided.

**Task 01 — Extend `AiSafetyEvent` Model & Migration**
- **Files to Modify:** `models.py`; **Files to Create:** migration.
- **Dependencies:** Task 00.
- **Definition of Done:** 3 new nullable columns added; structural schema test still passes.

**Task 02 — Extend Ingestion Consumer**
- **Files to Modify:** `ai_safety_event_consumer.py`.
- **Definition of Done:** New fields populated from upstream message; raw-text-shaped fields still rejected/dead-lettered.

**Task 03 — Implement `category` → `policy_result` Mapping**
- **Files to Modify:** `service.py`.
- **Tests:** All 3 categories mapped correctly; unknown category raises rather than silently defaulting.

**Task 04 — Extend Response Schema & Empty States**
- **Files to Modify:** `schemas.py`, `service.py`, `api.py`.
- **Definition of Done:** Response includes new fields; `ai_never_enabled` empty-state flag implemented.

**Task 05 — Full Test Suite & Documentation**
- **Definition of Done:** All §25 tests green; OpenAPI cross-references C.22.

## 28. Definition of Done
AI Interaction History's richer fields are served from the same, single, already-redacted-at-write-time table C.22 owns — with explicit cross-feature sign-off obtained, zero duplicate tables/consumers/routes created, and the structural no-raw-content guarantee re-verified after extension.

## 29. Final Verification Checklist
- [ ] Cross-feature sign-off obtained before implementation (Task 00)
- [ ] No new `ai_interactions` table created; `ai_safety_event` extended instead
- [ ] No second Kafka consumer created
- [ ] `policy_result` is derived, not independently stored
- [ ] Schema-introspection test passes on the extended table
- [ ] "AI always off" and "no interactions this period" empty states distinguishable
- [ ] Both this blueprint and C.22 B-03's blueprint cross-reference each other
