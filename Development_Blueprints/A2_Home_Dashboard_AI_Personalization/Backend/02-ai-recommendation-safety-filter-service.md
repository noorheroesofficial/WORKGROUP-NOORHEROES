# B-02 — AI Recommendation Engine & Safety Filter Service

## 1. Feature Context
NoorHeroes Child App, Feature A.2. Provides the "Recommended Next Step" section and personalizes greeting variants for the Home Aggregation Service (B-01). Carries the feature's second most critical safety guarantee: no AI-sourced content reaches a child without passing a synchronous, fail-closed safety filter.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
1.2 AI Recommendation Engine & Safety Filter Service (ID: B-02)

## 4. Objective
Implement a ranking service that scores candidate content using age band, locale, parental restrictions, mastery/skill-gap, incomplete activity, variety/fatigue, recent dislikes/skips, time-of-day/bedtime state, and offline availability — and gate every AI-sourced item/greeting through a synchronous AI Safety Filter call before it becomes eligible for Home, failing closed (excluding, never showing unfiltered) on any filter error.

## 5. Business Requirements
Per PRD FR-5, FR-6, FR-18, Edge Case 2, §3.3, §5 items 2–3:
- Ranking inputs listed in FR-5 must all be accepted signals.
- Every AI-sourced recommendation and every AI-generated greeting variant must pass the Safety Filter synchronously before inclusion.
- Filter failure/timeout → exclude the item silently (fail closed); never show a "blocked" placeholder.
- Zero eligible items post-filter → fall back to scholar-curated evergreen content set, never render empty (Edge Case 2).
- Greeting phrasing must vary across sessions (non-repetitive script pool) within scholar-approved bounds — no freeform AI text shown unfiltered (FR-18).

## 6. Existing Architecture
Follow the FastAPI service-layer pattern from Core-Architecture docs. This service is called by B-01's Home Aggregation Service as one of the 7 fan-out dependencies — its public interface must conform to the `RecommendationClient` contract defined in B-01 Task 02.

## 7. Existing Code to Reuse
- httpx-based service client pattern established in B-01.
- Content Catalog client (read-only content metadata lookups) — reuse rather than duplicate if B-01/B-05 already implement it.
- Existing structured-logging utility.

## 8. Files to Create
- `app/services/recommendation_service.py`
- `app/services/ai_safety_filter_client.py`
- `app/services/ranking/signals.py` (signal extraction/normalization)
- `app/services/ranking/fallback_evergreen.py`
- `app/services/greeting_service.py` (phrasing-pool + occasion composition, safety-filtered)
- `tests/unit/test_recommendation_service.py`
- `tests/unit/test_ai_safety_filter_fail_closed.py`
- `tests/integration/test_recommendation_fallback_evergreen.py`

## 9. Files to Modify
- `app/core/config.py` — feature flag `home_ai_ranking_enabled`, Safety Filter timeout setting

## 10. Backend Requirements
- Ranking function accepts a typed `RankingContext` (age_band, locale, parent_restrictions, mastery_gaps, incomplete_activity_ids, recent_dislikes, time_of_day, bedtime_state, offline_available_ids) and returns a ranked candidate list with `reason_tag` per item.
- Every candidate + every greeting variant routed through `ai_safety_filter_client.check(item)` synchronously; on exception/timeout, drop the item from the candidate list (fail closed).
- If post-filter candidate list is empty, return the evergreen fallback set instead (never propagate an empty list upward as "no recommendations").
- Respect `home_ai_ranking_enabled` feature flag — when `false`, skip the ML ranking model entirely and serve only the deterministic rule-based/evergreen feed.
- Input sanitization: bound/validate all ranking-context fields server-side (e.g., `recent_dislikes` capped at N entries, type-checked) to prevent injection into the ranking pipeline.

## 11. KMP Requirements
Not applicable — consumed indirectly via B-01's `recommended` and `greeting` sections. No client code here.

## 12. NextJS Requirements
Not applicable directly. Filter-pass/candidate-set decisions must be logged in a queryable form for N-03 (Recommendation Explainability Viewer) to read by masked `child_id` + timestamp.

## 13. API Contract
Internal service contract (not directly client-facing):
- `RecommendationService.get_recommendations(ranking_context) -> list[RecommendedItem]`
- `AISafetyFilterClient.check(candidate) -> FilterResult(passed: bool, reason: str|None)`
- `GreetingService.compose_greeting(child_id, locale, occasion) -> GreetingModel`

No new public HTTP endpoint is added by this sub-feature; it is invoked in-process/via internal call by B-01.

## 14. Database Requirements
No new tables owned by this sub-feature. Reads Content Catalog and Progress data (owned by B-05/Content Catalog). Writes a lightweight `recommendation_decision_log` record (candidate set before/after filter, signals used, filter-pass status) keyed by masked `child_id` + timestamp — required for N-03 Explainability Viewer. Add migration: `recommendation_decision_log(log_id PK, child_id_hash, generated_at, candidate_set_before jsonb, candidate_set_after jsonb, signals jsonb, filter_pass boolean)`; retention aligned with existing analytics-log retention policy (confirm with platform data-retention policy rather than inventing a new one).

## 15. Validation
Ranking-context fields validated/bounded before use; Safety Filter response validated against expected schema before trusting `passed: true`.

## 16. Authentication
Internal service-to-service call; not directly client-authenticated. Uses whatever internal service-auth mechanism (mTLS/service token) is already established between backend services in this codebase — reuse, do not invent a new one.

## 17. Authorization
N/A directly (internal call scoped by the `child_id` passed from the already-authorized B-01 caller).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Safety Filter call fails/times out | Exclude item (fail closed) |
| Zero eligible items post-filter | Serve evergreen fallback set |
| ML ranking model unavailable | Serve rule-based/evergreen feed (feature-flag-controlled fallback) |
| Ranking-context malformed | Reject malformed fields defensively, proceed with sanitized subset rather than failing the whole call |

## 19. Offline First
Not applicable (backend). Offline availability is one of the *inputs* to ranking (only recommend downloadable/available content when relevant), not a state this service itself manages.

## 20. Local Data
Not applicable.

## 21. Localization
Greeting phrasing pool must have entries per supported locale (English, Hindi, Arabic, Urdu); occasion phrases sourced from Islamic Calendar Service (B-07) already localized.

## 22. RTL
N/A (backend text generation only; rendering is client-side).

## 23. Analytics
Emits internal `recommendation_ai_filtered_count` aggregate metric (not per-user-visible) for product/ML iteration, per PRD §1.19.

## 24. Performance
Safety Filter call budget: 400ms per call, synchronous and blocking for AI-sourced fields specifically (per PRD §5 item 3) — do not relax this to async-fire-and-forget, as that would reintroduce the bypass risk this design prevents.

## 25. Security
- Fail-closed design is the primary security control (prevents filter-outage from becoming filter-bypass).
- Input sanitization at the ranking-context boundary prevents recommendation-poisoning via malformed client-influenced signals (e.g., recent dislikes).

## 26. Library Requirements
httpx (Safety Filter + ML model calls), existing ranking/ML SDK if the platform already has one (do not introduce a new ML framework without confirming none exists).

## 27. Testing
- Unit: fail-closed behavior on Safety Filter exception/timeout.
- Unit: evergreen fallback triggers when post-filter candidate list is empty.
- Integration: chaos test — kill Safety Filter service, confirm zero unfiltered content in `RecommendationService` output.
- Integration: feature-flag `home_ai_ranking_enabled=false` serves deterministic feed only.

## 28. Documentation
Document the fail-closed contract explicitly in the service docstring and in the shared architecture note referenced by B-01 (so future maintainers understand this is a deliberate security property, not a bug to "fix" by making it more lenient).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Ranking Context & Recommendation Models**
- Objective: Typed models for ranking input/output.
- Why Required: Type-safety and a stable internal contract for B-01.
- Existing Architecture to Follow: Pydantic model conventions from B-01.
- Existing Files to Reuse: none.
- Files to Create: `app/services/ranking/models.py` (`RankingContext`, `RecommendedItem`, `FilterResult`)
- Files to Modify: none
- Implementation Details: `RankingContext` includes all FR-5 signal fields with bounded/typed validation (e.g., `recent_dislikes: list[str] = Field(max_length=20)`).
- Business Rules: All fields optional except `child_id`/`age_band`; missing signals degrade ranking quality but never error.
- Validation: Field-level bounds per above.
- Error Handling: N/A.
- Security: Bounding fields prevents payload-size-based abuse.
- Performance: Lightweight models, no heavy computation here.
- Localization: `locale` field drives downstream phrasing.
- RTL: N/A.
- Analytics: N/A.
- Tests: Unit tests for field bound rejection/clamping.
- Documentation: Docstrings.
- Dependencies: None.
- Do Not Change: N/A.
- Expected Result: `models.py` with typed contract.
- Definition of Done: Models compile, unit tests pass.

**Task 02 — Implement Safety Filter Client (Fail-Closed)**
- Objective: Synchronous, fail-closed wrapper around the AI Safety Filter service.
- Why Required: Core safety guarantee of this sub-feature.
- Existing Architecture to Follow: httpx client pattern from B-01.
- Existing Files to Reuse: none.
- Files to Create: `app/services/ai_safety_filter_client.py`
- Files to Modify: none
- Implementation Details: `async def check(candidate) -> FilterResult`; wraps call in `try/except` + `asyncio.wait_for(timeout=0.4)`; any exception/timeout returns `FilterResult(passed=False, reason="filter_unavailable")` — never raises up to caller as a hard failure that could accidentally short-circuit into "show anyway."
- Business Rules: Fail closed, no exceptions.
- Validation: Response schema validated before trusting `passed=True`.
- Error Handling: All failure modes converge to `passed=False`.
- Security: This task is the security control.
- Performance: 400ms timeout budget.
- Localization: N/A.
- RTL: N/A.
- Analytics: Log filter-pass/reject decisions for Task 05's decision log.
- Tests: Unit tests — timeout returns `passed=False`; 5xx returns `passed=False`; malformed response returns `passed=False`; only a well-formed `passed=True` response passes through.
- Documentation: Explicit "fail closed, always" docstring warning against future refactors weakening this.
- Dependencies: Task 01.
- Do Not Change: Never change the default failure branch to `passed=True`.
- Expected Result: Fail-closed client.
- Definition of Done: All fail-mode unit tests pass.

**Task 03 — Implement Ranking Signal Extraction & Scoring**
- Objective: Score/rank candidate content from Content Catalog using `RankingContext`.
- Why Required: Core personalization logic (FR-5).
- Existing Architecture to Follow: Existing ranking/ML integration pattern if one exists on the platform; otherwise implement a documented rule-based scoring baseline first, ML model as a pluggable strategy.
- Existing Files to Reuse: Content Catalog client.
- Files to Create: `app/services/ranking/signals.py`, `app/services/ranking/scorer.py`
- Files to Modify: none
- Implementation Details: Pure functions mapping `RankingContext` + candidate pool → scored/ordered list with `reason_tag` derived from the dominant signal (e.g., `because_you_liked_prophet_stories`).
- Business Rules: Exclude content already completed or explicitly disliked recently; respect parent restrictions as a hard filter before scoring.
- Validation: Candidate pool pre-filtered by age-band/entitlement before scoring.
- Error Handling: Empty pool after hard filters → return empty list (Task 04 handles evergreen fallback).
- Security: Parent-restriction filter is a hard, non-bypassable pre-filter.
- Performance: Vectorized/batched scoring, not per-candidate synchronous DB round-trips.
- Localization: Content filtered/ranked respecting `locale`.
- RTL: N/A.
- Analytics: N/A here (logged in Task 05).
- Tests: Unit tests for scoring order given fixture signals; parent-restriction hard-filter test.
- Documentation: Docstring explaining `reason_tag` derivation logic.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working scorer.
- Definition of Done: Unit tests pass.

**Task 04 — Wire Safety Filter Into Recommendation Pipeline + Evergreen Fallback**
- Objective: End-to-end `RecommendationService.get_recommendations()`.
- Why Required: Combines Tasks 02+03 into the safe, complete pipeline.
- Existing Architecture to Follow: Service composition pattern.
- Existing Files to Reuse: Tasks 01–03 outputs.
- Files to Create: `app/services/recommendation_service.py`, `app/services/ranking/fallback_evergreen.py`
- Files to Modify: none
- Implementation Details: Score candidates (Task 03) → filter each through Safety Filter (Task 02) concurrently (`asyncio.gather`) → if resulting list empty, call `fallback_evergreen.get_evergreen_set(age_band, locale)`.
- Business Rules: Evergreen set is scholar-curated and does not require Safety Filter re-check (already pre-approved) — confirm this assumption against existing evergreen-content curation process; if evergreen content is not pre-vetted in this codebase, route it through the filter too rather than assuming.
- Validation: Final list validated against `RecommendedItem` schema.
- Error Handling: Handles Task 03 empty results and Task 02 mass-failure gracefully.
- Security: End-to-end fail-closed guarantee.
- Performance: Concurrent filtering, not sequential.
- Localization: Evergreen set filtered by locale.
- RTL: N/A.
- Analytics: N/A here.
- Tests: Integration test — chaos-kill Safety Filter, assert output is either empty-safe or evergreen, never unfiltered.
- Documentation: Full pipeline docstring/diagram reference.
- Dependencies: Tasks 02, 03.
- Do Not Change: N/A.
- Expected Result: Complete recommendation pipeline.
- Definition of Done: Chaos test passes.

**Task 05 — Implement Greeting Service + Decision Logging**
- Objective: Compose localized, non-repetitive greeting text (safety-filtered) and persist `recommendation_decision_log` rows.
- Why Required: FR-2, FR-18, and N-03 Explainability Viewer dependency.
- Existing Architecture to Follow: Migration pattern (Alembic) from platform conventions.
- Existing Files to Reuse: Islamic Calendar client (B-07).
- Files to Create: `app/services/greeting_service.py`, migration for `recommendation_decision_log`
- Files to Modify: none
- Implementation Details: Phrasing pool per locale; select non-repeating variant (track last-used per child, e.g., via Redis or a small history table); pass composed greeting through Safety Filter before returning; write decision-log row (candidate set before/after, signals, filter-pass) with `child_id` hashed for the masked-search requirement of N-03.
- Business Rules: Occasion omitted silently if Islamic Calendar Service fails (Edge Case 8).
- Validation: N/A beyond schema.
- Error Handling: Calendar failure → omit occasion only, greeting still renders.
- Security: `child_id` hashed in the decision log per N-03's "masked identifier" requirement.
- Performance: Greeting composition must not add meaningfully to the 400ms budget shared with other B-01 fan-out calls.
- Localization: Phrasing pool covers EN/HI/AR/UR.
- RTL: N/A (backend).
- Analytics: `greeting_occasion_shown` is client-fired; this service just supplies the data.
- Tests: Unit tests for non-repetition logic and calendar-failure graceful omission.
- Documentation: Note the hashing scheme used for `child_id` in the decision log so N-03 implementers know how to correlate a masked identifier back (via the same hash function) during investigation.
- Dependencies: Tasks 02, 04.
- Do Not Change: Do not store greeting decision logs with raw unhashed `child_id`.
- Expected Result: Greeting service + decision log table.
- Definition of Done: Migration applied, unit tests pass.

## 30. Definition of Done
Recommendation and greeting pipelines never surface unfiltered AI content under any failure mode; evergreen fallback always available; decision logs support N-03 investigation; all tests green.

## 31. Final Verification Checklist
- [x] Safety Filter fail-closed behavior verified via chaos test
- [x] Evergreen fallback triggers correctly on empty post-filter candidate list
- [x] `home_ai_ranking_enabled` feature flag correctly bypasses ML ranking when off
- [x] Parent-restriction hard-filter cannot be bypassed by ranking signals
- [x] `recommendation_decision_log` stores hashed `child_id`, never raw
- [x] Greeting phrasing varies across sessions, filtered before display
- [x] Islamic Calendar Service failure omits occasion without breaking greeting
- [x] All unit/integration tests pass

## 32. Architectural & Implementation Specification Reference (Zero Missing Scenarios)

### 32.1 Non-Bypassable Fail-Closed AI Safety Filter Contract
- **Core Security Rule**: No AI-generated or AI-recommended content may reach a child client without passing a synchronous safety inspection.
- **SLA & Budget**: Strict 400ms SLA enforced via `asyncio.wait_for(timeout=0.4)`.
- **Fail-Closed Semantics**:
  - Socket timeout → `FilterResult(passed=False, reason="safety_filter_timeout")`
  - HTTP 5xx / 4xx error → `FilterResult(passed=False, reason="safety_filter_5xx")`
  - Connection drop / DNS failure → `FilterResult(passed=False, reason="network_error")`
  - Malformed response JSON → `FilterResult(passed=False, reason="invalid_schema")`
  - The client **never** raises unhandled exceptions to callers and **never** defaults to `passed=True`.
- **Anti-Billing & Commercial Token Pre-Flight Scan**:
  - Deterministic pre-flight regex filter rejects any payload containing billing, subscription, upgrade, price, or payment tokens (`subscribe`, `subscription`, `billing`, `premium`, `upgrade`, `usd`, `tier`, `payment`, `renew`, `paywall`, etc.) across English, Arabic, Urdu, and Hindi.
- **Chaos Testing**:
  - Hook `AISafetyFilterClient.simulate_outage = True` enables testing catastrophic upstream failure; output immediately drops candidate items and falls back safely to scholar-curated evergreen content.

### 32.2 Scholar-Curated Evergreen Fallback Guarantee (PRD Edge Case 2)
- **Trigger Conditions**:
  1. Feature flag `home_ai_ranking_enabled` is set to `False`.
  2. All scored candidates are filtered out by the AI Safety Filter.
  3. Candidate pool is empty after applying non-bypassable parent restrictions or recent dislikes.
  4. Content catalog or ranking service is completely unreachable.
- **Multi-Lingual Coverage**: Pre-approved, scholar-vetted feeds configured for all supported locales:
  - English (`en`): Prophetic manners, Quranic surahs, kindness to parents, morning dhikr.
  - Arabic (`ar`): قصص الأنبياء، سورة الفاتحة، بر الوالدين، أذكار الصباح.
  - Urdu (`ur`): انبیاء کے قصے، سورۃ الفاتحہ، والدین کی خدمت، صبح کے اذکار.
  - Hindi (`hi`): नबियों के क़िस्से, सूरह अल-फ़ातिहा, वालिदैन की खिदमत, सुबह के अज़कार.
- **Guarantee**: Recommendation section **never** renders empty and **never** displays an error/broken card.

### 32.3 Privacy-Preserving Child Identifier Hashing Scheme (N-03 Explainability Viewer)
- **Hash Function**: Standard SHA-256 (Secure Hash Algorithm 256-bit).
- **Format**: Lowercase 64-character hexadecimal string (`hashlib.sha256(child_id.encode('utf-8')).hexdigest()`).
- **Zero Raw PII Invariant**: Table `recommendation_decision_log` stores `child_id_hash`, `generated_at`, `candidate_set_before`, `candidate_set_after`, `signals`, and `filter_pass`. No raw `child_id`, child names, or parent identifiers are ever persisted.
- **Server-Side Anti-Drift Search Support**:
  - The Admin Explainability endpoints (`GET /admin/v1/recommendations/explain` and `GET /v1/admin/recommendations/explain`) accept `child_id_hash` as either:
    1. A pre-hashed 64-character SHA-256 hexadecimal string.
    2. A raw `child_id` string (the server automatically computes `sha256(raw_child_id)` server-side).
  - This eliminates client-side hashing implementation drift between NextJS Admin and Python Backend.

### 32.4 Admin Recommendation Explainability API Contract (N-03 Blueprint)
- **Endpoints**:
  - `GET /admin/v1/recommendations/explain`
  - `GET /v1/admin/recommendations/explain`
- **RBAC Authorization**:
  - Strictly restricted to `trust_safety` or `super_admin` scopes via `require_any_scope("trust_safety", "super_admin")`.
  - Non-trust-safety authenticated admins receive `403 Forbidden` (`{"detail": "Forbidden: Requires trust_safety or super_admin scope"}`).
  - Unauthenticated requests receive `401 Unauthorized`.
- **Query Parameters**:
  - `child_id_hash` (required, string): SHA-256 hex or raw child ID.
  - `from` (optional, ISO datetime string): Earliest decision timestamp filter.
  - `to` (optional, ISO datetime string): Latest decision timestamp filter.
  - `limit` (optional, int, default 20, range 1..100): Maximum records returned.
  - `offset` (optional, int, default 0, min 0): Pagination offset.
- **Response Format (Dual-Wire CamelCase Compatible)**:
  ```json
  {
    "total": 1,
    "items": [
      {
        "logId": "019488a0-...",
        "childIdHash": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
        "generatedAt": "2026-09-25T06:00:00Z",
        "candidateSetBefore": [...],
        "candidateSetAfter": [...],
        "signals": {
          "age_band": "6-8",
          "locale": "en",
          "incomplete_activity_ids": ["story_101"],
          "mastery_gaps": ["tajweed_noon"],
          "recent_dislikes": [],
          "parent_restrictions": []
        },
        "filterPass": true
      }
    ]
  }
  ```
- **Empty Search Behavior**:
  - An inquiry matching 0 records returns HTTP 200 with `{"total": 0, "items": []}`, clearly distinguished from an error or invalid query.
- **Immutable Server-Side Audit Logging**:
  - Every successful execution writes an immutable `AdminAuditRecord`:
    - `action`: `"recommendations.explain_view"`
    - `admin_id`: Subject ID extracted from admin JWT token.
    - `details`: `{"child_id_hash": "...", "record_count": N}`.
- **Strict Read-Only Enforcement**:
  - `POST`, `PUT`, `PATCH`, `DELETE` methods return `405 Method Not Allowed`.

### 32.5 Child Greeting Service Phrasing Pool & Calendar Degradation (FR-2, FR-18, Edge Case 8)
- **Dynamic Phrasing Rotation**:
  - Multi-lingual greeting pools in English, Arabic, Urdu, and Hindi.
  - Session-to-session script rotation prevents repetitive or robotic phrasing.
  - Greeting text is validated through the AI Safety Filter prior to presentation.
- **Graceful Islamic Calendar Degradation**:
  - If the Islamic Calendar Service (B-07) experiences latency, timeout, or 5xx outage, the occasion is silently omitted (`Assalamu Alaikum, {name}!`), and the request completes without failure.

