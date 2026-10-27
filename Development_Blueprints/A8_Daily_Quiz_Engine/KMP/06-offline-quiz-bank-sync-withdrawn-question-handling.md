# K-06 — Offline Quiz Bank, Sync & Withdrawn-Question Handling

## 1. Feature Context
NoorHeroes — Feature A.8 Daily Quiz & Quiz Completion Engine. Source PRD §6.7, §7 item 6, FR-10, FR-11, Edge Cases 4/7, Screen Inventory item 14.

## 2. Parent Feature
A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
K-06 — Offline Quiz Bank, Sync & Withdrawn-Question Handling

## 4. Objective
Implement a source-agnostic `QuizRepository` backing (server vs. Room-cached bundled question set) so the entire question-rendering/answering/explanation code path (K-02–K-05) is identical regardless of source, with a sync outbox that correctly surfaces the server's withdrawn-question exclusion outcome without local error.

## 5. Business Requirements
FR-10 (offline attempts supported for downloaded question banks, idempotent sync), FR-11 (withdrawn-question exclusion applies even to late-syncing offline attempts), Edge Case 4 (stale client-side weak-skill framing doesn't cause incorrect double-counting — server is authoritative), Edge Case 7 (media-load-failure handling applies equally offline).

## 6. Existing Architecture
Built inside `:core:quiz-engine`, implementing K-02's `QuizRepository` interface against `:core:offline-cache` (Room) conventions (`CORE_DATABASE_INSTRUCTIONS.md`, `CORE_DATASTORE_INSTRUCTIONS.md`). Downloaded content packages (Stories/Learn/Dua) bundle pre-assembled question sets per each consuming feature's own offline spec — this module consumes that bundle format, does not define it.

## 7. Existing Code to Reuse
- `:core:offline-cache` Room database conventions
- Existing outbox/sync pattern (shared with A.3/A.5/A.6 offline flows, per their respective K-07/offline blueprints)
- K-02's `QuizRepository` interface (implemented, not redefined, here)

## 8. Files to Create
- `core/quiz-engine/src/commonMain/kotlin/.../offline/OfflineQuizRepository.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../offline/QuizResponseOutbox.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../offline/OfflineQuizIndicator.kt`
- `core/quiz-engine/src/androidMain/kotlin/.../offline/QuizRoomEntities.kt`
- `core/quiz-engine/src/commonTest/kotlin/.../OfflineSyncWithdrawnQuestionTest.kt`
- `core/quiz-engine/src/commonTest/kotlin/.../OfflineOutboxIdempotencyTest.kt`

## 9. Files to Modify
- `QuizSessionViewModel.kt` (K-02) — constructed with either `OfflineQuizRepository` or server-backed repository via the shared interface, ViewModel unaware of which is active

## 10. Backend Requirements
Consumes B-03 (server fetch when online), B-04 (response submission/sync), B-06 (server-side withdrawn-question exclusion outcome).

## 11. KMP Requirements
- `QuizRepository` implementable by either a server-backed or a locally-bundled (Room-cached) data source through the same interface — `QuizSessionViewModel` (K-02) is unaware of which is active
- Offline responses queue in a shared outbox keyed by `client_request_id`
- Local flow: Remote Data (B-03) → Repository → Local Storage (Room) → UI (K-03/K-04)
- Network-recovery listener triggers outbox flush automatically
- Sync-time handling: when a locally-answered question was withdrawn server-side in the interim, the client simply accepts the server's response (exclusion is server-authoritative per B-06) without local error or double-counting
- Stale client-side "weak skill" framing at download time never causes incorrect local double-counting — client trusts server's authoritative recalculation on sync (Edge Case 4)
- `OfflineQuizIndicator` component shown on any quiz screen while offline

## 12. NextJS Requirements
N/A.

## 13. API Contract
Per B-03/B-04 §13; sync path uses the same `client_request_id` idempotency contract.

## 14. Database Requirements
Room entities: bundled question cache table, response outbox table (keyed by `client_request_id`, sync-status flag).

## 15. Validation
Outbox entries validated for well-formed `answer_json` before local queueing (same per-type validation as K-03's renderers already enforce at submission time).

## 16. Authentication
Inherits existing child-mode session/token refresh handling.

## 17. Authorization
N/A at this layer (server-enforced on sync).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Offline with bundled question set | Quiz functions fully, results queue locally |
| Offline without a bundled set for the requested context | Entry point shows a "download to practice offline" affordance rather than a broken quiz attempt |
| Sync-time server response indicates a question was withdrawn and excluded | Client accepts the server's authoritative result silently, no error surfaced, no local recalculation attempted |
| Duplicate outbox flush attempt (e.g., app relaunch mid-sync) | Idempotent via `client_request_id`, safely re-flushable |
| Network recovery mid-flush | Outbox resumes from last unsynced entry, no duplicate submissions |

## 19. Offline First
This sub-feature **is** the offline-first implementation: Initial local load → remote refresh → offline read → offline action → retry → sync, per the platform's standard offline-first flow.

## 20. Local Data
Bundled question cache (Room), response outbox (Room, keyed by `client_request_id`).

## 21. Localization / 22. RTL
Bundled question payload retains the same localized fields as the server response — no re-fetch needed for locale changes mid-offline-session (locale is baked into the bundle at download time, consistent with each consuming feature's own offline-locale handling).

## 23. Analytics
`quiz_offline_attempted`, `quiz_offline_synced`, `quiz_withdrawn_question_excluded_on_sync` (client-observed confirmation of the server-side exclusion event).

## 24. Performance
No main-thread blocking on Room read/write for large offline bundles; outbox flush runs on a background dispatcher; deserialization of bundled question sets is lazy per-question, not eager for the entire bundle.

## 25. Security
No new sensitive data handling; offline-cached question content is standard learning-progress data under existing platform child-data handling policies (consistent with PRD §12.4).

## 26. Library Requirements
Room, `:core:offline-cache`, Kotlin Coroutines/Flow — existing dependencies only.

## 27. Testing
- Integration: **signature test** — offline attempt answers a question later withdrawn server-side; sync occurs; assert the client accepts the server's exclusion outcome without local error, crash, or incorrect recalculation (Edge Case 4/FR-11 client-side verification)
- Unit: outbox flush idempotency — duplicate flush attempt produces no duplicate server-side submissions
- Integration: full offline flow — download fixture bundle → offline → answer 5 questions → reconnect → verify exactly the expected number of sync calls, each with a unique `client_request_id`
- Unit: `OfflineQuizIndicator` visibility tied correctly to network state

## 28. Documentation
Repository interface doc explicitly states the "ViewModel is source-agnostic" architectural guarantee K-02 depends on, and the "server is authoritative on sync, client never re-derives mastery/exclusion locally" rule from Edge Case 4.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Room Entities**
Task ID: K-06-T01. Files to Create: `QuizRoomEntities.kt`. Definition of Done: bundled-question and outbox tables defined, migration-safe.

**Task 02 — Implement OfflineQuizRepository**
Task ID: K-06-T02. Files to Create: `OfflineQuizRepository.kt`. Implementation Details: implements K-02's `QuizRepository` interface. Definition of Done: ViewModel construction with this repository requires no ViewModel code changes.

**Task 03 — Implement Response Outbox**
Task ID: K-06-T03. Files to Create: `QuizResponseOutbox.kt`. Business Rules: `client_request_id`-keyed idempotent queueing. Tests: `OfflineOutboxIdempotencyTest.kt`. Definition of Done: idempotency test passes.

**Task 04 — Implement Network-Recovery Flush Trigger**
Task ID: K-06-T04. Definition of Done: outbox auto-flushes on reconnect, resumable mid-flush.

**Task 05 — Implement Withdrawn-Question Sync Handling**
Task ID: K-06-T05. Business Rules: Edge Case 4, FR-11 — client accepts server-authoritative result. Tests: `OfflineSyncWithdrawnQuestionTest.kt` (signature test). Definition of Done: signature test passes.

**Task 06 — Implement OfflineQuizIndicator Component**
Task ID: K-06-T06. Files to Create: `OfflineQuizIndicator.kt`. Definition of Done: correctly tied to network-state observation.

**Task 07 — Add Tests**
Task ID: K-06-T07. Definition of Done: full coverage per §27.

**Task 08 — Add Documentation**
Task ID: K-06-T08. Definition of Done: source-agnostic guarantee and server-authoritative-on-sync rule documented.

**Task 09 — Final Code Review**
Task ID: K-06-T09. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
`QuizRepository` fully implementable offline with zero ViewModel awareness of source; outbox idempotent and resumable; withdrawn-question sync outcome handled silently and correctly on the client, matching B-06's server-side guarantee.

## 31. Final Verification Checklist
- [ ] `QuizSessionViewModel` requires no code changes to function against either repository implementation
- [ ] Offline attempt on a since-withdrawn question syncs without local error, matching server's exclusion outcome (signature test passing)
- [ ] Outbox flush idempotent — no duplicate submissions on repeated/interrupted flush attempts
- [ ] `OfflineQuizIndicator` correctly reflects network state
- [ ] No main-thread blocking on offline bundle read/write
