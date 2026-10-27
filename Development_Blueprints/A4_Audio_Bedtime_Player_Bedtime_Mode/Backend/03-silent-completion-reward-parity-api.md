# B-03 — Silent Completion & Quiet Reward Parity API

> **Status:** Implemented & Verified (100% Green, 34/34 Parity Tests Passing, 495 Module Tests Passing, 0 Regressions)  
> **Parent Feature:** Feature A.4 — Audio Bedtime Player & Bedtime Mode  
> **Sub-feature ID:** B-03 (1.3 Silent Completion & Quiet Reward Parity API)  
> **Authoritative Specification:** `FAST-API-INSTRUCTIONS.md` §5.4 & `MASTER-README.md` §11.29  
> **Last Verified:** 2026-09-06  

## 1. Feature Context
Lets the client signal that a completion event happened during Bedtime/Calm Mode so the Reward Service records the identical ledger entry it always would, while telling the client not to render the celebratory completion UI. This is the backend half of the "reward recorded quietly, not celebrated" rule (FR-10) — the single highest-risk piece of this sub-feature is guaranteeing zero divergence between silent and standard reward-ledger entries.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
1.3 Silent Completion & Quiet Reward Parity API (ID: **B-03**)

## 4. Objective
Extend A.3's existing `POST /v1/content/{id}/complete` endpoint with an optional `silent_completion: bool` field. When `true`, the Reward Service writes the byte-for-byte-identical ledger entry as a standard completion (same idempotency-key behavior, same XP/Noor Heroes Points amount); the only observable difference is the response's `celebratory_ui_hint` field.

## 5. Business Requirements
- FR-10: on Bedtime completion, reward is recorded quietly in the background but not visually celebrated.
- §3.3: Reward Service accepts a `silent: true` flag on completion calls originating from Bedtime Mode.
- §3.4: request addition `silent_completion: true`; response's `celebratory_ui_hint` set to `false`.
- §10 DevOps: changes to this logic require A.3's shared reward-ledger regression suite to pass before promotion — this feature must never cause a reward-ledger discrepancy in the shared system.

## 6. Existing Architecture
A.3's `POST /v1/content/{id}/complete` endpoint already exists on the `content`/`reward` module boundary, calling into a shared `RewardService.record_completion()` (or equivalently named method — confirm exact signature in the A.3 codebase before extending) with existing idempotency-key handling keyed on `client_event_id`. This sub-feature adds one optional field to the request schema and threads it through unchanged to the ledger-write call, adding only a response-shaping branch.

## 7. Existing Code to Reuse
- A.3's completion endpoint router method (`content` or `playback` module — confirm exact file)
- A.3's `RewardService` ledger-write method and its existing idempotency-key logic (`client_event_id` dedup)
- A.3's completion request/response Pydantic schemas (extend, do not fork)

## 8. Files to Create
- `tests/modules/content/test_silent_completion_parity.py` — dedicated parity test suite (structural, not full end-to-end duplication of A.3's existing completion tests)

## 9. Files to Modify
- A.3's completion request schema — add `silent_completion: bool = False`
- A.3's completion response schema — add `celebratory_ui_hint: bool`
- A.3's completion service method — branch only on the response-shaping step; the ledger-write call itself receives no `silent`-specific arguments beyond what's needed for the (optional) internal audit flag, if the Reward Service's ledger schema already has a place for it — otherwise no ledger-schema change at all, since the requirement is "identical ledger entry"

## 10. Backend Requirements
- `silent_completion` defaults to `false`, fully backward-compatible with existing non-bedtime callers (A.3's standard Story Player, K-03/K-06).
- When `true`: the ledger write path is invoked with the exact same parameters (content_id, child_id, client_event_id, xp_amount, points_amount) as a standard completion — no conditional amount/logic branch based on `silent_completion` anywhere in the ledger-write call.
- Response: `celebratory_ui_hint = not silent_completion` (or equivalent explicit mapping) — this is the ONLY field whose value depends on `silent_completion`.
- Idempotency: `client_event_id` dedup behavior is completely unaffected — a retried silent completion with the same `client_event_id` is deduped identically to a retried standard completion.

## 11. API Contract

### `POST /v1/content/{id}/complete` (extension of A.3's existing endpoint)
- Auth: unchanged (Bearer, child-mode).
- Request addition: `{ "...": "...", "silent_completion": false }` (optional, default `false`).
- Response addition: `{ "...": "...", "celebratory_ui_hint": true }`.
- Errors: unchanged from A.3's existing contract.

## 12. Database Requirements
No schema change to the Reward Ledger table required — the ledger entry itself carries no `silent`/`celebratory` flag (that is purely a response-shaping concern, not a persisted fact about the reward). If A.3's ledger schema already has an analogous "context"/"source" column used for other completion-context distinctions, confirm whether it's appropriate to also record `silent` there for analytics purposes — do not add a new column unless this confirmation is made and the parity test still passes with it populated identically in structure (only the value differs, never the presence/absence of other fields).

## 13. Validation
- `silent_completion` is a plain boolean; no additional validation needed beyond standard Pydantic type coercion.
- Existing completion payload validation (content_id existence, child entitlement, etc.) is entirely unchanged.

## 14. Authentication
Unchanged from A.3's existing completion endpoint (Bearer, child-mode).

## 15. Authorization
Unchanged — no new authorization surface; `silent_completion` is a presentation hint, not a privileged operation.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| `silent_completion` omitted | Defaults to `false`, behaves exactly as today |
| Duplicate completion call (same `client_event_id`) with `silent_completion: true` | Deduped identically to a standard duplicate — no double reward |
| Reward Service ledger-write failure | Unchanged existing error handling (`5xx`, retried per existing client retry policy) — `silent_completion` has no bearing on failure handling |

## 17. Security
No new security surface. `silent_completion` cannot be used to bypass or alter reward amounts — it is explicitly excluded from any amount-calculation logic (verified by the parity test in Task 02).

## 18. Analytics
Emit via `OutboxWriter` (in addition to A.3's existing `story_completed` event, unaffected): `bedtime_reward_recorded_silently` when `silent_completion: true`.

## 19. Performance
No additional queries or latency — this is a single boolean threaded through an existing call path plus one response field.

## 20. Library Requirements
No new third-party libraries.

## 21. Testing
- Unit: **ledger-row structural parity test** — assert that a silent completion and a standard completion of the same content produce ledger rows identical in every field except (if applicable) the optional context/source column; the reward `xp_amount`/`points_amount` must be bit-for-bit equal.
- Unit: `celebratory_ui_hint` correctly maps to `false`/`true`.
- Integration: idempotency — duplicate `client_event_id` with `silent_completion: true` produces exactly one ledger row.
- Regression: full run against A.3's shared reward-ledger regression suite before this change is considered mergeable.

## 22. Documentation
Update OpenAPI schema for the completion endpoint's two new fields; run `classify_openapi_diff.py` to confirm additive/non-breaking status.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Extend Completion Request/Response Schemas [COMPLETED & VERIFIED]**
Objective: Add `silent_completion: bool = False` to the request schema, `celebratory_ui_hint: bool` to the response schema. Files modified: `src/noorheroes/modules/content/completion_schemas.py`. Business Rules: fully backward-compatible default. Tests: verified schema defaults correctly when field omitted; all existing A.3 completion tests pass unmodified.

**Task 02 — Thread `silent_completion` Through the Service Layer Without Altering the Ledger-Write Call [COMPLETED & VERIFIED]**
Objective: The ledger-write call receives identical parameters regardless of `silent_completion`; only the response-shaping step branches. Files modified: `src/noorheroes/modules/content/completion_service.py`. Dependencies: Task 01. Business Rules: zero conditional logic on `silent_completion` inside the reward-amount calculation or ledger-write call itself; truthiness check on 0 XP / 0 points daily cap preserved via `is not None`. Tests: mock identity test `test_reward_service_receives_identical_parameters_regardless_of_silent_flag` passed.

**Task 03 — Wire `celebratory_ui_hint` into the Response [COMPLETED & VERIFIED]**
Objective: Response field correctly reflects `not silent_completion`. Dependencies: Task 01. Tests: mapping tests for both `true`/`false` inputs, idempotent replay inversion, and concurrent race loser handling passed.

**Task 04 — Write the Reward-Ledger Structural Parity Test [COMPLETED & VERIFIED]**
Objective: The signature test for this entire sub-feature — assert byte-for-byte identical ledger-row structure between a silent and non-silent completion of the same content, differing only in the response hint field. Files created: `tests/modules/content/test_silent_completion_parity.py`. Dependencies: Task 02. Definition of Done: `test_reward_ledger_structural_parity_between_standard_and_silent_completion` executed on real SQLite schema and passed with 100% field equality.

**Task 05 — Add Idempotency and Analytics Tests [COMPLETED & VERIFIED]**
Objective: Duplicate-`client_event_id` dedup test with `silent_completion: true`; `bedtime_reward_recorded_silently` emission test. Dependencies: Task 02–03. Definition of Done: tests pass; `BedtimeRewardRecordedSilently` registered in `events.py:EVENT_TYPE_REGISTRY` and `outbox_relay.py:DISPATCH_TABLE`.

**Task 06 — Run A.3's Shared Reward-Ledger Regression Suite [COMPLETED & VERIFIED]**
Objective: Confirm this change introduces zero regression to the shared Reward Service used by all of A.3. Dependencies: Task 02. Definition of Done: shared rewards regression suite (`tests/modules/rewards/ -k "ledger or award or wallet"`) executed with 68/68 passed (100%).

**Task 07 — Update OpenAPI Documentation [COMPLETED & VERIFIED]**
Objective: Regenerate and diff-classify. Definition of Done: regenerated `artifacts/openapi.json` via `scripts/export_openapi_schema.py`; diff classified as `MINOR` (additive/non-breaking) with 0 breaking changes via `scripts/classify_openapi_diff.py`.

**Task 08 — Final Code Review [COMPLETED & VERIFIED]**
Objective: Confirm the ledger-write call path contains zero `silent_completion`-conditional logic; confirm `celebratory_ui_hint` is the sole observable difference. Definition of Done: checklist in §24 fully checked; 34 parity tests passing; 495 content module tests passing; 0 regressions.

## 24. Final Verification Checklist
- [x] `silent_completion` defaults to `false`, fully backward-compatible with all existing A.3 completion callers
- [x] Ledger-write call path contains zero conditional logic based on `silent_completion` — reward amount/idempotency identical either way
- [x] Structural parity test passes: silent vs. standard ledger rows differ only in an optional context field, never in reward amounts
- [x] `celebratory_ui_hint` correctly maps to the inverse of `silent_completion`
- [x] Duplicate `client_event_id` with `silent_completion: true` produces exactly one ledger row
- [x] A.3's shared reward-ledger regression suite passes
- [x] `bedtime_reward_recorded_silently` analytics event emitted correctly
- [x] OpenAPI diff confirmed additive/non-breaking

## 25. Definition of Done
**Status: Complete & Verified**  
Bedtime completions record an identical reward ledger entry to standard completions, with the client instructed via `celebratory_ui_hint` alone to suppress celebratory UI — zero risk of reward-ledger discrepancy, verified by 34 dedicated structural-parity tests in `tests/modules/content/test_silent_completion_parity.py` and gated by A.3's shared regression suite (68 tests) and the full content fleet (495 tests, 100% green). All documentation in `MASTER-README.md` §11.29, `FAST-API-INSTRUCTIONS.md` §5.4, `src/noorheroes/modules/content/README.md`, and `00_GAP_ANALYSIS_AND_CONFLICT_RESOLUTION_REGISTER.md` (Gap 11) is fully synchronized.
