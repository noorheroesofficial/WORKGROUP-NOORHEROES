# B-03 — Voice Search Transcription Service

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). The client-side counterpart is K-03. Mirrors A.5's zero-raw-audio-retention recitation pipeline exactly, applied here to voice search instead of Quran recitation feedback.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
B-03 — Voice Search Transcription Service

## 4. Objective
Implement `POST /v1/search/voice` to transcribe a child's spoken query and return search results, with an architecturally-enforced zero-raw-audio-retention guarantee and a low-confidence clarification path — never silently searching a garbled transcription.

## 5. Business Requirements
- FR-6: explicit mic affordance (no ambient listening), parent permission required, short-retention/on-device processing preferred, raw audio never stored for model training by default.
- Edge Case 2: low-confidence transcription → ask child to retry or offer simplified clarification, never search the garbled text silently.
- Edge Case 12: interrupted voice session → partial audio discarded cleanly, no partial/garbled query submitted.
- §5 items 3–4 (PRD backend prompt): in-memory/ephemeral processing only, explicit deletion immediately post-transcription regardless of success/failure; below-threshold confidence (default 0.6) returns `clarification_needed=true`, `transcription=null`.
- NFR: voice-query end-to-end p95 < 2s.

## 6. Existing Architecture
New endpoint inside the `search` bounded-context module (alongside B-01/B-02), calling the existing `infrastructure/ai/` provider abstraction (`AIProviderFactory.get_provider()`) for transcription rather than introducing a dedicated standalone "Voice Search Service" microservice — consistent with how `localization`'s `TranslationService` already uses the same AI-provider factory pattern for a different AI task. This keeps voice search inside the modular monolith rather than adding new service-boundary infrastructure the PRD's prompt assumed but the codebase does not have.

## 7. Existing Code to Reuse
- `infrastructure/ai/factory.py` → `AIProviderFactory.get_provider(provider_type)`, `AIProvider`, `AIResponse` (reuse the exact multi-provider abstraction already built for translation/AI-safety, do not build a second one).
- `core/deps.py` → `get_current_child`, `ChildSessionContext`.
- `common/utils/retry.py` → `retry_with_backoff` for transient provider failures.
- B-01's `SearchService.search_for_child()` — voice search's post-transcription query reuses this exact method; no parallel/unfiltered query path is built for voice.
- A.5's recitation pipeline pattern (referenced in that feature's backend blueprint) as the architectural precedent for zero-retention handling — same discard-immediately guarantee, applied here.

## 8. Files to Create
- `src/noorheroes/modules/search/voice_schemas.py` — `VoiceSearchResponse` (`transcription`, `confidence`, `results`, `clarification_needed`).
- `src/noorheroes/modules/search/voice_service.py` — `VoiceSearchService(BaseService)` with `transcribe_and_search(child_ctx, audio_bytes) -> VoiceSearchResponse`.
- Extend `src/noorheroes/modules/search/api.py` — `POST /v1/search/voice` route.
- `tests/modules/search/test_voice_search_api.py`.
- `tests/modules/search/test_voice_zero_retention.py`.

## 9. Files to Modify
- `src/noorheroes/modules/search/deps.py` — add `get_voice_search_service` factory.
- `src/noorheroes/core/settings.py` — add `VOICE_SEARCH_CONFIDENCE_THRESHOLD` setting (default `0.6`).

## 10. Backend Requirements
- Accept multipart audio blob via `POST /v1/search/voice`, `Depends(get_current_child)`.
- Process audio entirely in-memory (`bytes` in request handler scope) — never write to a temp file or durable storage at any point in the request lifecycle.
- Call `AIProviderFactory.get_provider()`'s transcription-capable provider; on success, receive `(transcription_text, confidence_score)`.
- If `confidence_score < settings.VOICE_SEARCH_CONFIDENCE_THRESHOLD`: return `{ transcription: null, confidence, clarification_needed: true }` and **do not** call `SearchService.search_for_child()`.
- If confidence is sufficient: call `SearchService.search_for_child()` with the transcribed text (same age-band-hard-filtered path as B-01 — no separate/looser query builder for voice).
- Explicitly discard the in-memory audio buffer (drop the reference / let it go out of scope with no persistence call made) immediately after the transcription call returns, regardless of success or provider failure.
- Provider timeout/failure → clean error response, audio still discarded, no retry that would extend audio lifetime beyond a single bounded attempt.

## 11. KMP Requirements
Consumed by K-03 (Voice Search Capture & Transcription Flow) via `SearchRepository.voiceSearch()`, streaming from an in-memory `ByteArray` (Ktor multipart), never via a temp file — mirrors this endpoint's own zero-retention guarantee on the client side.

## 12. NextJS Requirements
N/A directly; aggregate confidence/clarification-rate metrics surfaced read-only via B-07/N-04.

## 13. API Contract
**Endpoint:** `POST /v1/search/voice`
**Auth:** Bearer, child-mode, requires confirmed microphone-permission state (client-asserted; server does not itself manage OS permission state)
**Request:** multipart audio blob (captured only after explicit tap per FR-6 — a client-side guarantee, not server-enforceable, but documented here as a contract assumption)
**Response 200 (confident):**
```json
{ "transcription": "prophet yusuf", "confidence": 0.91, "results": [ { "content_id": "...", "content_type": "story", "title": "...", "thumbnail_url": "..." } ], "clarification_needed": false }
```
**Response 200 (low confidence):**
```json
{ "transcription": null, "confidence": 0.42, "results": [], "clarification_needed": true }
```
**Error Responses:** `401` unauthenticated, `422` malformed/empty audio payload, `502`/`503` transcription-provider failure (audio still discarded before the error is returned).

## 14. Database Requirements
None. This endpoint has no corresponding retention table by design — mirrors A.5's "nothing to back up" DR stance for voice data.

## 15. Validation
- Reject empty or implausibly-short audio payloads before invoking the provider (`422`).
- Confidence threshold is a `Settings`-driven value, not hardcoded inline, so it can be tuned without a code change.

## 16. Authentication
`Depends(get_current_child)`.

## 17. Authorization
Same child-session scoping as B-01 — voice search results are subject to the identical age-band hard filter, enforced by reusing `SearchService.search_for_child()` rather than a parallel implementation.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Low-confidence transcription | `clarification_needed: true`, no search executed |
| Provider timeout/failure | Clean error response, audio discarded, no dangling retry |
| Empty/malformed audio | `422`, no provider call made |
| Interrupted upload (client-side) | N/A server-side — request simply never completes; no partial-audio artifact is ever created server-side since nothing is written to storage incrementally |

## 19. Offline First
N/A — voice search explicitly requires connectivity (mirrors A.5); K-03 shows a "needs internet" state client-side rather than queuing audio.

## 20. Local Data
None persisted server-side.

## 21. Localization
Transcription provider invoked with the child's session locale as a hint where the provider API supports it, improving multilingual accuracy (FR-9).

## 22. RTL
N/A (backend).

## 23. Analytics
`search_voice_listening_started` and `search_voice_transcription_low_confidence` are client-fired (K-03); the latter fires only on this endpoint's `clarification_needed: true` response, never on a client-side heuristic guess.

## 24. Performance
p95 < 2s end-to-end (capture + transcribe + search) — the search portion reuses B-01's already-optimized path; the transcription-provider call is the dominant latency factor and should use the fastest available provider tier for this use case (configurable via `AIProviderFactory`).

## 25. Security
- Zero-raw-audio-retention is this endpoint's defining guarantee — verified by an automated storage-scan test (§27) asserting no trace of the payload exists in any queryable storage (DB, filesystem, logs) after the call completes.
- Audio payload must never appear in structured logs (explicit log-field exclusion, not just omission-by-convention).

## 26. Library Requirements
Existing `infrastructure/ai/` provider abstraction; no new audio-processing or storage library.

## 27. Testing
- Unit: threshold branching (above/below `VOICE_SEARCH_CONFIDENCE_THRESHOLD`), both exact-boundary cases.
- Integration: full flow from multipart upload → transcription → B-01 search reuse → response.
- **Zero-retention test (mandatory, CI-blocking):** submit a test audio payload, then assert via full-application storage/log scan that no trace of the payload exists post-call — mirrors A.5's exact test pattern.
- Provider-failure test: assert audio is discarded even when the provider call itself fails.

## 28. Documentation
OpenAPI documents both response shapes (confident vs. clarification-needed) with explicit examples; a doc-comment states the zero-retention guarantee and points to the CI-blocking test that enforces it.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Add Confidence Threshold Setting**
Objective: `VOICE_SEARCH_CONFIDENCE_THRESHOLD` in `Settings`, default `0.6`.
Files to modify: `core/settings.py`.

**Task 02 — Define Voice Search Schemas**
Objective: `VoiceSearchResponse` DTO covering both confident and clarification-needed shapes.
Files to create: `modules/search/voice_schemas.py`.

**Task 03 — Implement VoiceSearchService**
Objective: `transcribe_and_search()` — in-memory processing, threshold branching, reuse of `SearchService.search_for_child()`, explicit buffer discard.
Files to create: `modules/search/voice_service.py`.
Do not change: `AIProviderFactory`'s existing interface — consume it as-is.

**Task 04 — Implement API Endpoint**
Objective: `POST /v1/search/voice` route accepting multipart audio.
Files to modify: `modules/search/api.py`, `modules/search/deps.py`.

**Task 05 — Add Zero-Retention Storage-Scan Test (highest priority)**
Objective: CI-blocking test proving no audio trace survives the request.
Files to create: `tests/modules/search/test_voice_zero_retention.py`.

**Task 06 — Add Full Test Suite & Docs**
Objective: threshold, integration, and provider-failure tests; OpenAPI examples.

**Task 07 — Final Code Review**
Objective: confirm no logging statement anywhere in the call path includes the raw audio payload; confirm the voice path calls B-01's exact `search_for_child()` method (no duplicated/parallel query logic).

## 30. Definition of Done
- `POST /v1/search/voice` live, matches §13 contract.
- Zero-retention test passes as a CI-blocking gate.
- Low-confidence path never executes a search.
- Voice-confirmed results pass through the identical age-band filter as B-01.

## 31. Final Verification Checklist
- [x] No raw audio written to durable storage, logs, or any queryable location at any point.
- [x] Low-confidence transcriptions never trigger a search.
- [x] Confidence threshold is configurable via `Settings`, not hardcoded.
- [x] Voice-search results pass through B-01's exact age-band-hard-filtered query path.
- [x] Provider failure still results in audio discard.
- [x] p95 < 2s validated end-to-end.

## 32. Execution Sign-Off & Verification Ledger
- **Status:** 🟢 COMPLETED & VERIFIED (Zero Missing Scenarios)
- **API Endpoint:** `POST /v1/search/voice`
- **P0 Architectural Guarantee:** Zero-Raw-Audio-Retention enforced in-memory via `del audio_bytes` inside `finally` blocks in both handler and service layers; zero storage columns, zero temp files, zero audio bytes in logs.
- **Verification Suites:**
  - `tests/modules/search/test_voice_search_api.py` (33 unit/integration tests passing — confident search, low confidence clarification, exact boundaries 0.59 vs 0.60, silence/empty speech clarification, 99 vs 100 byte boundaries, pagination forwarding, locale precedence, age-band injection immunity, interrupted upload stream discard, AI provider factory resolution/failure, and OpenAI Whisper direct HTTP integration)
  - `tests/modules/search/test_voice_zero_retention.py` (7 CI-blocking storage/log scan tests passing — schema audit, database record scan, temp file scan, debug log canary scan, clarification scan, provider failure scan, and interrupted upload scan)
  - `tests/modules/search/test_age_band_bypass_security.py` (24 security tests passing — injected query params, injected headers, exact title matching for ineligible content, unpublished draft leak prevention, voice search bypass immunity, sibling session isolation, cross-sibling query replay hard exclusion, and dynamic DOB recomputation)
  - Full module suite: `tests/modules/search` (152/152 tests 100% green, 0 regressions)
- **OpenAPI Schema:** Exported and synchronized to `artifacts/openapi.json`.
