# K-05 — Cross-Domain Mastery Analytics Integration

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). Defines the single shared `MasteryAnalytics` interface every domain feature module fires mastery-related events through, so event definitions, parameter shapes, and domain-tagging stay consistent across Quran, Arabic, Tajweed, and any future domain.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
K-05 — Cross-Domain Mastery Analytics Integration (Shared Analytics Interface)

## 4. Objective
Implement `MasteryAnalytics` in `:core:mastery-engine`, firing every event from A.9 PRD §1.19 with correct parameters and `domain` tagging, consumed by K-02/K-03/K-06 and any domain feature module — replacing any risk of each domain defining a parallel, inconsistent analytics interface.

## 5. Business Requirements
- A.9 PRD §1.19: full event list — `quiz_result_screen_shown`, `quiz_result_review_mistakes_selected`, `quiz_result_try_again_selected`, `quiz_result_continue_selected`, `mastery_score_recomputed`, `skill_state_transitioned`, `mastery_single_session_block_applied`, `spaced_review_due_cross_domain_capped`, `cross_domain_mastery_summary_viewed`, `mastery_formula_version_applied`.
- §6.6 Analytics Mapping: "`MasteryAnalytics` fires `quiz_result_screen_shown` and the three selection events; domain feature modules (A.5) consume the same shared analytics interface rather than each defining a parallel one."
- §11.1 Event Taxonomy: all events tagged with `domain` where relevant, enabling cross-domain comparison.

## 6. Existing Architecture
Kotlin, KMP. Reference `CORE_ANALYTICS_INSTRUCTIONS.md` for the platform's existing analytics-SDK wrapper conventions (event-firing interface pattern, parameter typing, batching/offline-queueing behavior already built into `:core:analytics` or equivalent).

## 7. Existing Code to Reuse
- `:core:analytics`'s existing event-firing infrastructure (SDK wrapper, offline-queueing, batching) — `MasteryAnalytics` is a typed, domain-specific facade over that existing infrastructure, not a new analytics pipeline.
- A.8's analytics-interface pattern (if A.8 established a similar per-feature analytics facade, mirror its structure).

## 8. Files to Create
- `core/mastery-engine/src/commonMain/kotlin/.../analytics/MasteryAnalytics.kt` — interface + default implementation.
- `core/mastery-engine/src/commonTest/kotlin/.../analytics/MasteryAnalyticsTest.kt`

## 9. Files to Modify
- K-02's `QuizCompletionResultScreen`/`MasteryResultViewModel` — wire event firing via `MasteryAnalytics` (if not already stubbed during K-02's implementation).
- B-04-consuming client code / B-07's client-facing due-skills flow — wire `spaced_review_due_cross_domain_capped` firing where the client observes a capped due-skills response.
- A.5's `:feature:learn` — replace any existing ad-hoc analytics calls for mastery-related events with calls through this shared interface.

## 10. Backend Requirements
N/A (client-side).

## 11. KMP Requirements
- **`MasteryAnalytics` interface:** one method per event in §1.19's list, strongly typed parameters (e.g., `fun onQuizResultScreenShown(strengthsCount: Int, nextStepSkillId: String)`), always accepting/tagging `domain` where the event is domain-scoped.
- **Default implementation:** delegates to `:core:analytics`'s underlying SDK wrapper, mapping each typed method call to the correct event name/parameter payload.
- **Internal/aggregate events** (`mastery_score_recomputed`, `mastery_single_session_block_applied`, `spaced_review_due_cross_domain_capped`, `mastery_formula_version_applied`): fired without raw score values in their parameters (consistent with the platform-wide no-raw-score principle) — these are transition/occurrence signals, not score-value carriers.
- **Consumption contract:** any domain feature module (current or future) fires mastery-related analytics ONLY through this interface — never directly through the raw `:core:analytics` SDK for these specific event types, to prevent drift/inconsistency.

## 12. NextJS Requirements
N/A (events consumed downstream by the analytics pipeline/dashboards, not by NextJS directly in this sub-feature).

## 13. API Contract
N/A (client-side SDK event firing, not an HTTP API).

## 14. Database Requirements
N/A.

## 15. Validation
Parameter types enforced at compile time via the typed interface (e.g., `strengthsCount: Int`, not a loosely-typed `Map<String, Any>`) — reduces the risk of malformed event payloads reaching the analytics pipeline.

## 16. Authentication
N/A.

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Underlying analytics SDK call fails/throws | Caught and logged via `:core:logger`, never propagates to crash the user-facing flow (analytics failures must be non-blocking, per standard platform convention) |
| Event fired with a `domain` value not yet known to analytics tooling (e.g., a brand-new domain) | Fired as-is; analytics dashboards are expected to handle new domain tags gracefully (no client-side allowlist blocking new domains, which would undermine FR-9's extensibility goal) |

## 19. Offline First
Relies on `:core:analytics`'s existing offline-queueing/batching behavior (events fired while offline are queued and flushed on reconnect) — not reimplemented here.

## 20. Local Data
N/A beyond what `:core:analytics`'s existing queueing already handles.

## 21. Localization
N/A (event names/parameters are not user-facing text).

## 22. RTL
N/A.

## 23. Analytics
This sub-feature IS the analytics integration layer; see §11 for the full event contract.

## 24. Performance
Event firing must be fire-and-forget from the caller's perspective (non-blocking, dispatched off the main thread by the underlying SDK) — no UI jank from analytics calls.

## 25. Security
No PII beyond what the existing analytics pipeline already handles for other event types; `skill_id`/`domain` are non-sensitive metadata, never raw score values.

## 26. Library Requirements
No new libraries — wraps existing `:core:analytics`.

## 27. Testing
- Unit: each `MasteryAnalytics` method correctly maps to the expected underlying event name and parameter shape (mock the underlying SDK, assert call arguments).
- Unit: analytics failures are caught and don't propagate.

## 28. Documentation
KDoc on the interface stating it is the MANDATORY single entry point for all mastery-related analytics across every domain — direct SDK calls for these event types elsewhere in the codebase should be treated as a code-review flag.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define MasteryAnalytics Interface**
- Task ID: K-05-T01
- Objective: Typed interface covering every event in A.9 PRD §1.19.
- Why This Is Required: The single shared contract every domain consumes.
- Existing Architecture to Follow: `:core:analytics`'s existing facade-interface pattern (mirror A.8's if one exists).
- Existing Files to Reuse: `:core:analytics` SDK wrapper.
- Files to Create: `analytics/MasteryAnalytics.kt`.
- Files to Modify: None.
- Implementation Details: One method per event, strongly typed parameters, `domain` parameter on every domain-scoped event.
- Business Rules: No raw score values in any parameter.
- Validation: Compile-time typing.
- Error Handling: Implementation (not interface) catches SDK failures.
- Security: No PII beyond existing norms.
- Performance: Non-blocking dispatch (delegated to SDK).
- Localization: N/A. RTL: N/A.
- Analytics: This task IS the analytics layer.
- Tests: `MasteryAnalyticsTest.kt`.
- Documentation: KDoc per §28.
- Dependencies: `:core:analytics` (existing).
- Do Not Change: `:core:analytics`'s core SDK wrapper.
- Expected Result: Complete interface + default implementation.
- Definition of Done: Unit tests verifying correct event-name/parameter mapping for all 10 events.

**Task 02 — Wire K-02/K-03/K-06 and A.5 to Consume This Interface**
- Task ID: K-05-T02
- Objective: Replace any ad-hoc or stubbed analytics calls with real `MasteryAnalytics` usage.
- Why This Is Required: Without this wiring, the interface exists but nothing actually fires through it.
- Existing Architecture to Follow: Hilt-injected dependency, consistent with other shared interfaces in `:core:mastery-engine`.
- Existing Files to Reuse: K-02's ViewModel/screen, K-03's renderer (if it fires tap-through events at the consumer level), K-06's screen, A.5's `:feature:learn`.
- Files to Create: None.
- Files to Modify: `MasteryResultViewModel.kt` (K-02), any A.5 mastery-related analytics call sites.
- Implementation Details: Inject `MasteryAnalytics` via Hilt; call the appropriate method at each event trigger point (screen shown, button selections, etc.).
- Business Rules: No direct `:core:analytics` SDK calls remain for these specific event types outside this interface.
- Validation/Error Handling/Security/Performance: N/A beyond Task 01's coverage.
- Localization: N/A. RTL: N/A.
- Analytics: This task completes the wiring.
- Tests: Verify (via existing K-02 tests, extended) that the correct events fire at the correct trigger points.
- Documentation: N/A (wiring task).
- Dependencies: Task 01, K-02, K-03, K-06.
- Do Not Change: Event semantics defined in Task 01.
- Expected Result: All 10 events firing correctly from real user flows.
- Definition of Done: Event-firing verified end-to-end for at least the Quiz Completion Result flow (K-02) and one spaced-review/cap scenario (B-07 client consumption).

## 30. Definition of Done
`MasteryAnalytics` interface live, covering all 10 events from A.9 PRD §1.19 with correct typed parameters and `domain` tagging, consumed consistently by K-02/K-03/K-06 and A.5's `:feature:learn`, with no parallel/duplicate analytics interface anywhere in the mastery-consuming codebase.

## 31. Final Verification Checklist
- [ ] All 10 events from §1.19 implemented with correct parameter shapes
- [ ] `domain` tagging present on every domain-scoped event
- [ ] No raw score value in any event parameter
- [ ] Analytics SDK failures caught, non-blocking to user flows
- [ ] K-02, K-03 (if applicable), K-06, and A.5's `:feature:learn` all wired to this shared interface
- [ ] No remaining direct `:core:analytics` calls for these event types outside this interface
