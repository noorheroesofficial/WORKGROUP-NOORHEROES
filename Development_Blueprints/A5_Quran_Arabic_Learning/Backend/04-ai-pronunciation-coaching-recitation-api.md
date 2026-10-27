# B-04 — AI Pronunciation Coaching & Zero-Retention Recitation API

> [!NOTE]
> **Status**: ✅ **COMPLETED & VERIFIED** (100% Tested & Verified, All Invariants Preserved)
> - **Models & Migration**: `RecitationFeedbackLog` in `src/noorheroes/modules/learning/recitation_models.py`, Alembic migration `alembic/versions/0046_add_recitation_feedback_log.py`.
> - **Zero-Retention & Privacy Invariants**: `EphemeralAudioBuffer` with explicit post-inference memory wiping (`explicit_delete()`), raw audio never written to persistent disk, database, or logs; zero audio/blob columns in `recitation_feedback_logs`; server-side parent AI/microphone toggle re-validation (`403 AI_DISABLED_FOR_CHILD`) before audio ingestion.
> - **Content-Safety & Theological Protection**: CI-blocking template blocklist validator rejecting all religious-judgment language; non-bypassable CI gates.
> - **Unified Confidence Gating & Fallback**: Unified single fallback path for low-confidence (<0.70 threshold) and external inference timeouts/errors (`fallback_to_reference=True`); internal anomaly flagging (Edge Case 4) without altering child-facing response; safe network drop retry handling without retention loopholes.
> - **Localization & Security**: 4-language i18n localization (`en`, `hi`, `ur`, `ar`); safe child ownership authorization (`CHILD_SCOPE_VIOLATION` / `403`).
> - **API Endpoints**: Canonical `POST /v1/learning/recitation` and direct alias `POST /v1/recitation` accepting multipart audio (`audio`, `ayah_id`, `child_id`); programmatic interface `submit_recitation(...)`.
> - **Test Suite**: 97 dedicated tests across `test_recitation_models.py` (17 tests), `test_ephemeral_audio_buffer.py` (7 tests), `test_feedback_template_blocklist.py` (24 tests), `test_recitation_zero_retention.py` (5 tests), `test_recitation_parent_toggle_enforcement.py` (4 tests), `test_pronunciation_coaching_service.py` (15 tests), `test_recitation_feedback_log_repository.py` (6 tests), and `test_recitation_api.py` (19 tests) with 100% pass rate (325 passing tests across learning module).

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). This is the single most privacy- and theology-safety-sensitive endpoint in the entire NoorHeroes system. It processes a child's recorded recitation attempt and returns coaching feedback while architecturally guaranteeing the raw audio is never durably persisted anywhere, and that feedback never implies religious/worship judgment.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
B-04 — AI Pronunciation Coaching & Zero-Retention Recitation API (User API)

## 4. Objective
Implement `POST /v1/learning/recitation` such that: (1) raw audio is never written to any durable storage under any code path; (2) the parent's per-child AI/microphone toggle is server-side re-validated before any audio is touched; (3) low-confidence or failed inference falls back to a safe reference-comparison mode; (4) feedback language is guaranteed, via automated CI-blocking test, to never contain religious-judgment language.

## 5. Business Requirements
- FR-9: mic-denied/parent-disabled state falls back to listen-only — enforced server-side as defense in depth, not just client-side.
- FR-10: AI pronunciation feedback is advisory/pedagogical only — never "accepted"/"rejected" or implying religious/spiritual validity. Hard, non-negotiable rule.
- FR-11: raw child voice recordings not retained after processing by default; only derived, non-reversible signals may be retained.
- FR-12: low-confidence results fall back to "compare against recorded reference" self-assessment rather than presenting an unreliable score as authoritative.
- FR-13: parent can disable microphone/AI per child; when disabled, no UI path bypasses this — and per this blueprint, no *server* path processes audio either.
- Edge Case 2: parent disabling mid-session must not leave a dangling broken record control.
- Edge Case 4: anomalously high-confidence result inconsistent with history is flagged internally, never second-guessed to the child.
- Edge Case 10: network-drop mid-upload retry is allowed, but raw audio is still deleted post-processing even after retry — no extended-retention loophole.
- Non-Functional: AI feedback round-trip p95 < 3s; service degrades gracefully to self-assessment mode on outage, never blocking lesson progression.

## 6. Existing Architecture
Modular monolith; this logic lives in a new/extended `ai_safety`-adjacent flow inside the `learning` context (per architecture doc, `ai_safety` context already exists at `src/noorheroes/modules/ai_safety/` with an `evaluate` pattern for child-safety guideline checks — this endpoint's content-safety blocklist validation follows that established pattern). Uses the async request-scoped `AsyncSession`, Redis pool, and `get_current_child` dependency, consistent with B-01–B-03.

## 7. Existing Code to Reuse
- `ai_safety` context's evaluation pattern (`AISafetyRouter`/service) as the template for the content-safety blocklist test approach — mirrors Feature A.2's billing-content audit pattern referenced in the PRD.
- `SkillNodeStateRepository`/`compute_next_state()`/`invalidate_skill_tree_cache()` from B-01 (a successful recitation still contributes to mastery-affecting progress via a non-audio-bearing pathway, e.g., "ayah marked practiced").
- `get_current_child` dependency.
- Parental Controls service/table (existing, referenced in PRD as the source of the per-child AI/mic toggle — reuse its existing read API/table, do not duplicate the toggle state).

## 8. Files to Create
- `src/noorheroes/modules/learning/schemas/recitation.py`
- `src/noorheroes/modules/learning/services/pronunciation_coaching_service.py`
- `src/noorheroes/modules/learning/services/feedback_template_library.py` (in-memory/DB-backed template selector, read-only consumer of B-10's admin-managed templates)
- `src/noorheroes/modules/learning/models/recitation_feedback_log.py`
- `src/noorheroes/modules/learning/repositories/recitation_feedback_log_repository.py`
- `src/noorheroes/modules/learning/infra/ephemeral_audio_buffer.py` (in-memory/short-TTL encrypted buffer handler with explicit-delete)
- `src/noorheroes/modules/learning/infra/pronunciation_inference_client.py` (external inference service adapter)
- `tests/modules/learning/test_recitation_zero_retention.py` (CI-blocking signature test)
- `tests/modules/learning/test_recitation_parent_toggle_enforcement.py` (CI-blocking)
- `tests/modules/ai_safety/test_feedback_template_blocklist.py` (CI-blocking, mirrors A.2 billing-content audit)
- `tests/modules/learning/test_pronunciation_coaching_service.py`
- `tests/modules/learning/test_recitation_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/learning/api.py` — add `POST /v1/learning/recitation`.
- CI pipeline config — mark the zero-retention and blocklist tests as mandatory, non-bypassable gates on any PR touching this service (DevOps requirement, cross-ref B-04's CI wiring here).

## 10. Backend Requirements
- **Router**: `POST /v1/learning/recitation`, multipart form (`audio` file field + `ayah_id`, `child_id` fields), `get_current_child`.
- **Step 1 — Server-side toggle re-validation (before touching audio)**: query the Parental Controls service/table for `child_id`; if AI/mic is disabled, return `403 AI_DISABLED_FOR_CHILD` immediately — the multipart body must not be read/buffered into memory beyond what's unavoidable to reject the request; the inference client must never be invoked on this path (verified via mock/spy test).
- **Step 2 — Ephemeral capture**: accept the audio into an in-memory buffer or an ephemeral, encrypted, short-TTL (max 5 min) temp store; issue an **explicit delete call** immediately after the inference call returns, success or failure — never rely on TTL expiry alone.
- **Step 3 — Inference call**: call `PronunciationInferenceClient` (external service treated as a black-box async call) with the ephemeral audio reference; the raw audio bytes must never be written to PostgreSQL, a permanent object store, or any log output (including debug level) — this must be true across the entire request path, not just the "happy path."
- **Step 4 — Confidence gating**: if the returned confidence < configurable threshold (`ai_ops`-managed via B-11) OR the inference call times out/errors, route to the identical `fallback_to_reference=true` path — this is one code path handling both conditions, not two branches that could diverge.
- **Step 5 — Template selection**: on a high-confidence result, select a `feedback_template_id` from `FeedbackLibrary` (managed by B-10) filtered by `confidence_band`; the library must have passed the blocklist content-safety test before any template can be marked active/selectable.
- **Step 6 — Persist categorical log only**: write `recitation_feedback_log` (`child_id`, `ayah_id`, `confidence_band`, `feedback_template_id`, `fallback_used`, `created_at`) — no audio/blob column exists in this table by design.
- **Step 7 — Explicit deletion**: delete the ephemeral audio buffer/object, success or failure, before returning the response.
- **Anomaly handling (Edge Case 4)**: if confidence is high but wildly inconsistent with the child's historical trend (compare against `learning_attempt`/`recitation_feedback_log` history), flag internally (e.g., write to an ops-monitoring table/metric) but still return the positive feedback to the child — do not second-guess a too-good-to-be-true score to the child's face; true uncertainty is handled entirely by Step 4's confidence gate, not by this anomaly flag.

## 11. KMP Requirements
N/A directly at this layer; the contract this endpoint exposes is consumed by `K-04 Recitation Recorder & Zero-Retention Audio Capture`, which has matching client-side zero-retention guarantees.

## 12. NextJS Requirements
N/A directly; the `feedback_template_id` values this service selects from are managed via `N-03 Coaching Feedback Template Library Manager`, and the confidence threshold via `N-04 Learning Configuration Panel`.

## 13. API Contract

**`POST /v1/learning/recitation`**
- **Auth:** Bearer (child-mode) — requires both OS-mic-permission-implied client state AND server-side re-validation that AI/mic is not disabled for `child_id`.
- **Request:** `multipart/form-data` — audio blob + `{ "ayah_id": "uuid", "child_id": "uuid" }`
- **Response 200:**
```json
{ "feedback_template_id": "coach_023", "confidence_band": "high|medium|low", "fallback_to_reference": false }
```
- **Authentication:** Bearer JWT, child-mode
- **Authorization:** `child_id` family-scoped; additionally gated by the Parental Controls AI/mic toggle
- **Validation:** `ayah_id` must reference an existing, active ayah; audio content-type/size limits enforced
- **Error Responses:** `403 AI_DISABLED_FOR_CHILD` (parent toggle off — audio never processed), `422` (malformed request/unsupported audio format), `504`/graceful-fallback (inference timeout → still `200` with `fallback_to_reference=true`, not a hard error), `500` (unexpected failure — still must guarantee ephemeral cleanup ran)

## 14. Database Requirements
- `recitation_feedback_log` table exactly per B-01's ER diagram: `log_id PK`, `child_id FK`, `ayah_id FK`, `confidence_band`, `feedback_template_id`, `fallback_used BOOLEAN`, `created_at`. Index `(child_id, created_at DESC)`. **No audio/blob column exists in this table by design** — this is a schema-level enforcement of the zero-retention guarantee, not merely an application convention.
- No other durable storage is used for audio at any point — this is the defining architectural property of this sub-feature and must be documented as intentional in the DR/retention runbook, not left implicit.

## 15. Validation
- `ayah_id` exists and is active.
- Audio content-type/size validated before buffering (reject oversized/malformed uploads early, before full buffering).
- `child_id` matches session family scope.

## 16. Authentication
Bearer JWT, `get_current_child`.

## 17. Authorization
Two-layer gate: (1) standard family-scoped `child_id` check; (2) Parental Controls AI/mic toggle re-validated server-side on every single request — never cached client-side trust, never a one-time check.

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Parent AI/mic disabled for child | `403 AI_DISABLED_FOR_CHILD`, audio never read/processed |
| Inference service unavailable/timeout | `fallback_to_reference=true`, `200`, no error surfaced to child, logged for ops |
| Malformed/corrupt audio | `422` |
| Network drop mid-upload (client retry) | Server treats each attempt independently; once one attempt is fully processed, raw audio is deleted regardless of whether the client retries again |
| Anomalous high-confidence vs. history | Internal flag/metric only, `200` positive feedback still returned |

## 19. Offline First
N/A (backend requires connectivity by design — offline recitation is explicitly not supported per PRD §1.14, with self-assessment offered as the immediate client-side alternative).

## 20. Local Data
N/A (backend). Zero-retention is the entire point — there is no "local data" concept for audio at the server layer.

## 21. Localization
`feedback_template_id` resolves to locale-specific text at the template-library layer (B-10 manages `locale` per template); this endpoint returns only the ID, not localized text, keeping the response minimal and cache-friendly.

## 22. RTL
N/A at API layer.

## 23. Analytics
Only categorical fields (`confidence_band`, `fallback_used`, template IDs) may ever appear in any event schema derived from this endpoint — there must be no schema field anywhere capable of carrying raw audio, transcript text, or numeric confidence scores to the analytics warehouse, by architectural design, not policy alone.

## 24. Performance
p95 round-trip target < 3s (communicated client-side via a "Listening... checking..." state, not implying instant judgment). Ephemeral buffer operations must not block the event loop — use async I/O throughout.

## 25. Security
This is the highest-privacy-sensitivity endpoint in the app. Controls: (1) zero raw-audio persistence anywhere, enforced by CI-blocking tests; (2) server-side parent-toggle re-validation on every request, never trusting client state; (3) confidence-gated fallback preventing unreliable scores from being presented as authoritative; (4) content-safety blocklist on all selectable feedback templates, with zero bypass for any role at the template-management layer (B-10).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0, Pydantic v2, an async multipart-handling library (e.g., `python-multipart`, already standard for FastAPI), an encrypted ephemeral-storage mechanism (in-memory buffer preferred; if a temp object store is used, it must support explicit delete + short TTL — e.g., Redis with TTL as a defense-in-depth secondary, never the primary mechanism, or a tmpfs-backed object). No credentials for this infra are to be modified from existing values.

## 27. Testing
- **Signature test (CI-blocking)**: after calling this endpoint, assert no trace of the raw audio payload exists in any queryable storage the test can access — DB rows, object storage listing, and captured log output (including debug-level log capture).
- **CI-blocking**: assert a request with AI disabled for the child never reaches the inference-call code path (mock/spy assertion the inference function was never invoked), and that this holds even when the request includes a valid audio payload.
- **CI-blocking**: content-safety test loading the entire feedback template library and asserting zero templates match the blocklist (`accepted`, `rejected`, `valid prayer`, `invalid`, and the full maintained list).
- Unit: confidence-gating branch — both explicit low-confidence AND service-error/timeout route to the identical fallback path (test both, assert identical response shape/UX).
- Unit: anomaly-flagging logic (Edge Case 4) — high-confidence-but-inconsistent-with-history triggers an internal flag without altering the child-facing response.
- Integration: full happy path (high-confidence recitation → coaching feedback selected → categorical log persisted → ephemeral buffer confirmed deleted).
- Integration: `403 AI_DISABLED_FOR_CHILD` path — audio buffer never allocated/touched.

## 28. Documentation
OpenAPI docstring explicitly flags this as the app's highest-sensitivity endpoint, documents the zero-retention guarantee, the confidence-gating behavior, and the `403 AI_DISABLED_FOR_CHILD` contract. Internal architecture doc addendum: this endpoint's ephemeral-storage design should be referenced in the DR/retention runbook (owned by DevOps, cross-ref B-04's infra requirements).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `recitation_feedback_log` Model & Migration**
- Task ID: B-04-T01
- Task Name: Create Categorical-Only Feedback Log Table
- Objective: Persist non-audio recitation history for progress tracking.
- Why This Is Required: B-08's parent report and B-06's spaced-repetition scheduling need recitation history without ever touching audio.
- Files to Create: `models/recitation_feedback_log.py`, migration.
- Business Rules: No blob/audio column exists in the schema — this is a hard architectural constraint, not a convention.
- Dependencies: None.
- Do Not Change: Do not add any binary/blob column to this table under any future task.
- Definition of Done: Migration applies; schema review confirms no audio-capable column.

**Task 02 — Build Ephemeral Audio Buffer Handler**
- Task ID: B-04-T02
- Task Name: Implement `EphemeralAudioBuffer`
- Objective: Provide the single, audited code path for receiving and destroying raw audio.
- Why This Is Required: Centralizing this logic makes "never write audio to disk" enforceable in one place rather than scattered across handlers.
- Implementation Details: In-memory buffer preferred; if ephemeral object storage is used, encrypt at rest, set a max-5-minute TTL, and expose an `explicit_delete()` method that must be called by the caller in a `finally` block (success or failure) — do not rely on TTL expiry as the primary deletion mechanism.
- Security: Audit this module's entire code path to confirm no debug-level logging statement ever includes the buffer's contents.
- Dependencies: None.
- Do Not Change: N/A.
- Definition of Done: Unit test confirms `explicit_delete()` is invoked in both success and exception paths.

**Task 03 — Build `PronunciationInferenceClient` Adapter**
- Task ID: B-04-T03
- Task Name: Implement External Inference Service Adapter
- Objective: Encapsulate the transient call to the ASR/pronunciation model as an async external call.
- Implementation Details: Treat the model itself as external (not built here); adapter returns `{confidence: float, raw_signal: ...}` and must never persist its own copy of the request payload.
- Performance: Enforce a timeout consistent with the p95 < 3s target; timeout triggers the fallback path (Task 05).
- Dependencies: None (can be mocked for staging per DevOps environment-setup requirement).
- Definition of Done: Adapter unit-testable with a mocked backend returning deterministic confidence bands.

**Task 04 — Implement Server-Side Parent-Toggle Re-Validation**
- Task ID: B-04-T04
- Task Name: Enforce `AI_DISABLED_FOR_CHILD` Gate Before Any Audio Handling
- Objective: Defense-in-depth enforcement of the parent's per-child AI/mic setting, independent of client UI state.
- Existing Files to Reuse: Existing Parental Controls service/table (read-only query here — do not modify its schema or ownership).
- Implementation Details: Query the toggle BEFORE the multipart body is buffered into `EphemeralAudioBuffer`; return `403 AI_DISABLED_FOR_CHILD` immediately on disabled.
- Security: This is the second-most critical control in this blueprint after zero-retention — write the CI-blocking test (Task 09) confirming the inference function is never invoked on this path.
- Dependencies: B-04-T02.
- Definition of Done: Mock/spy test proves the inference client constructor/call is never reached when disabled.

**Task 05 — Implement Confidence Gating & Fallback Logic**
- Task ID: B-04-T05
- Task Name: Implement Unified Low-Confidence/Error Fallback Path
- Objective: Guarantee identical, safe behavior whether the AI genuinely returned low confidence or simply failed/timed out.
- Implementation Details: A single function `resolve_feedback(inference_result_or_error, threshold) -> FeedbackDecision` handling both branches identically — no separate error-handling code path that could diverge in behavior from the low-confidence path.
- Dependencies: B-04-T03.
- Definition of Done: Unit tests confirm identical `FeedbackDecision` shape for both trigger conditions.

**Task 06 — Implement Feedback Template Selection**
- Task ID: B-04-T06
- Task Name: Implement `FeedbackTemplateLibrary` Selector
- Objective: Select a `feedback_template_id` for high-confidence results from B-10's admin-managed, blocklist-validated template set.
- Existing Files to Reuse: B-10's template storage (read-only consumer here — do not duplicate template CRUD).
- Business Rules: Only templates that passed blocklist validation at save-time (B-10) are eligible for selection; this service does not re-validate content itself, it trusts B-10's write-time guarantee plus the periodic content-safety audit test (Task 10).
- Dependencies: B-04-T05, B-10 (template storage must exist; can stub with a seed set if built out of order).
- Definition of Done: Selector returns a valid `feedback_template_id` filtered by `confidence_band`.

**Task 07 — Implement `PronunciationCoachingService` Orchestration**
- Task ID: B-04-T07
- Task Name: Orchestrate Full Recitation Processing Flow
- Objective: Wire Tasks 02–06 into the end-to-end flow described in §10 Steps 1–7, including the Edge Case 4 anomaly-flagging check and the explicit ephemeral-buffer deletion guarantee.
- Implementation Details: Use a `try/finally` structure ensuring `explicit_delete()` (Task 02) is called regardless of outcome; persist `recitation_feedback_log` (Task 01) only after successful/fallback resolution; call B-01's `invalidate_skill_tree_cache()` if this recitation contributes to a "marked practiced" progress update.
- Dependencies: B-04-T01–T06, B-01-T06/T10.
- Definition of Done: Full orchestration unit-tested with mocked inference client across high/low/error scenarios.

**Task 08 — Wire Router Endpoint**
- Task ID: B-04-T08
- Task Name: Add `POST /v1/learning/recitation` to `LearningRouter`
- Files to Modify: `api.py`.
- Implementation Details: Multipart request parsing, `get_current_child`, calls `PronunciationCoachingService`.
- Dependencies: B-04-T07.
- Definition of Done: Endpoint reachable, manually verified against staging's mocked inference endpoint (per DevOps environment setup).

**Task 09 — Write Zero-Retention & Toggle-Enforcement CI-Blocking Tests**
- Task ID: B-04-T09
- Task Name: `test_recitation_zero_retention.py`, `test_recitation_parent_toggle_enforcement.py`
- Objective: Prove the two defining safety guarantees automatically, as mandatory CI gates.
- Implementation Details: File-system/object-storage-listing scan + log-output capture scan asserting zero audio trace; mock/spy assertion the inference function is never invoked when disabled.
- Dependencies: B-04-T04, B-04-T07, B-04-T08.
- Definition of Done: Both tests pass and are configured as non-bypassable CI gates on any PR touching this service (DevOps task, cross-referenced here).

**Task 10 — Write Content-Safety Blocklist Test**
- Task ID: B-04-T10
- Task Name: `test_feedback_template_blocklist.py` (mirrors A.2's billing-content audit)
- Objective: Guarantee no live-selectable template ever contains religious-judgment language.
- Implementation Details: Load full template library (from B-10's storage), assert none match the blocklist terms.
- Dependencies: B-04-T06, B-10.
- Definition of Done: Test passes against current library and is a mandatory CI gate.

**Task 11 — Full Test Suite & Confidence-Gating Coverage**
- Task ID: B-04-T11
- Objective: Complete remaining unit/integration coverage per §27.
- Dependencies: B-04-T01–T10.
- Definition of Done: All tests green in CI.

**Task 12 — API Documentation**
- Task ID: B-04-T12
- Objective: Finalize OpenAPI docstring per §28.
- Dependencies: B-04-T08.
- Definition of Done: `/docs` clearly documents the sensitivity, zero-retention guarantee, and `403 AI_DISABLED_FOR_CHILD` behavior.

## 30. Definition of Done
Endpoint live; zero-raw-audio-retention proven via CI-blocking automated test; parent-toggle server-side enforcement proven via CI-blocking automated test; feedback template blocklist proven via CI-blocking automated test; confidence-gating fallback unified and tested; Edge Case 2, 4, and 10 behaviors verified; full documentation complete.

## 31. Final Verification Checklist
- [x] Zero raw-audio-retention verified via automated file-system/storage-listing/log-capture scan (CI-blocking)
- [x] Server-side parent-AI-toggle re-validation verified — inference function never invoked when disabled (CI-blocking)
- [x] Feedback template blocklist validator verified to reject all known-bad phrases across the live library (CI-blocking)
- [x] Low-confidence AND service-error/timeout route to the identical fallback path
- [x] Anomalous high-confidence-vs-history flagged internally without altering child-facing response
- [x] Network-drop-mid-upload retry does not create an extended-retention loophole
- [x] `recitation_feedback_log` table has no audio/blob column
- [x] p95 round-trip < 3s target validated under load test
- [x] No PostgreSQL/Redis credentials modified
- [x] Full unit/integration/CI-blocking test suite green
- [x] OpenAPI documentation complete and flags this as the highest-sensitivity endpoint
