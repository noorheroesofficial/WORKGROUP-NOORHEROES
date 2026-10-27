# K-07 — Offline Downloads & Sync for Dua Content

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. `B15_Offline_Downloads_Sync/Backend/01`'s real `download_record.content_type` enum already includes `dua` (`'story|surah|dua|quiz|audio'`), and its KMP counterparts (`B15_Offline_Downloads_Sync/KMP/01-download-initiation-entitlement-gate.md`, `02-resumable-chunked-download-engine.md`, `06-offline-progress-sync-outbox-integration.md`) already implement a generic, content-type-parameterized download/outbox engine. This file integrates with that engine rather than building a parallel one.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
K-07 — Offline Downloads & Sync for Dua Content (integration with B.15's shared download engine)

## 4. Objective
Make dua content downloadable and offline-playable via B.15's existing download-initiation/chunked-download/outbox-sync engine, scoped to `content_type=dua`, and ensure B-02's mark-as-learned/B-04's favorite-toggle actions route through B.15's real `SyncQueueDao`/`SyncQueueEntity`-based outbox (per `06-offline-progress-sync-outbox-integration.md`) rather than a dua-specific one.

## 5. Business Requirements
FR-12; Edge Case 4 (offline quiz for a downloaded-and-learned dua — depends on `:core:quiz-engine`'s own offline bundling, A8-KMP/06, not something this file separately implements); Edge Case 5 (download-permission revocation doesn't remove existing downloads — B.15's existing policy, `B15_Offline_Downloads_Sync/Backend/03-entitlement-download-policy-enforcement-service.md`).

## 6. Existing Architecture
B.15's real chunked-download engine + outbox-sync integration, already generic across content types. `SyncQueueDao`/`SyncQueueEntity` (per `CORE_DATABASE_INSTRUCTIONS.md`) is the real local outbox table, not an invented dua-specific one.

## 7. Existing Code to Reuse
- B15-KMP/01's download-initiation flow, B15-KMP/02's chunked download engine, B15-KMP/06's outbox-sync integration
- `SyncQueueDao`/`SyncQueueEntity` (`core/database`)
- `DownloadRepository` (`core/kmpplayer`, per `CORE_KMP_PLAYER_INSTRUCTIONS.md` — confirm whether this is the same repository B.15's engine uses, or a distinct media-download-specific one; the platform may have two related-but-distinct download concerns: media-file caching (`core/kmpplayer`'s `DownloadRepository`) vs. B.15's content-download-manifest/entitlement layer — clarify before wiring)

## 8. Files to Create
- `feature/dua/src/commonTest/kotlin/.../DuaDownloadScopeTest.kt` — confirms `content_type=dua` downloads correctly initiate and complete through B.15's real engine
- `feature/dua/src/androidUiTest/kotlin/.../DuaOfflineFullFlowTest.kt`

## 9. Files to Modify
- `DuaRepository`/`DuaRepositoryImpl` (K-01/K-02) — route mark-learned/favorite writes through B.15's real outbox mechanism when offline (or confirm B.15's outbox is content-type-agnostic enough to just work without dua-specific wiring)

## 10. Backend Requirements
Consumes B15-B01's real `POST /v1/downloads/manifest` (`content_type: "dua"`).

## 11. KMP Requirements
- Download initiation for dua content uses B.15's existing entitlement-gated flow (K-01) — no dua-specific download-permission logic
- Downloaded dua fully functional offline: full card render + audio playback + bundled quiz (if `:core:quiz-engine`'s own offline mechanism includes it)
- Offline mark-as-learned/favorite queue via the real `SyncQueueDao`/`SyncQueueEntity`, synced on reconnect per B15-KMP/06's existing pattern

## 12. NextJS Requirements
N/A.

## 13. API Contract
Per B15-B01 §13 (confirm exact request/response shape from that real file rather than the placeholder shown here): `POST /v1/downloads/manifest`, `{content_id, content_type: "dua", quality}`.

## 14. Database Requirements
Reuses B.15's shared download-record local schema and `SyncQueueEntity` — no dua-specific tables.

## 15. Validation
N/A directly — inherited from B.15's engine.

## 16. Authentication / 17. Authorization
Inherited from B.15's entitlement-gated download flow (`B15_Offline_Downloads_Sync/Backend/03`).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Download failure | B.15's existing retry/backoff and failed-state UI |
| Non-downloaded dua accessed offline | "Connect to internet or download" affordance, consistent with B.15's existing pattern for other content types |
| Outbox sync failure | B.15's existing retry/backoff |

## 19. Offline First
Entirely delegated to B.15's real engine; this file's only job is correct `content_type=dua` scoping.

## 20. Local Data
B.15's shared local schema.

## 21. Localization / 22. RTL
Inherited from B.15's Downloads Manager UI, if a shared one exists (per `B15_Offline_Downloads_Sync/KMP/03-downloads-tab-inventory-management-ui.md`) — dua downloads should appear in that shared inventory UI, not a dua-specific downloads screen.

## 23. Analytics
`dua_download_started`/`dua_download_completed` — confirm whether B.15's engine already emits generic, content-type-parameterized download analytics that supersede dua-specific event names.

## 24. Performance
Inherited from B.15's chunked-download engine.

## 25. Security
Inherited from B.15's entitlement-gated flow.

## 26. Library Requirements
B.15's shared download engine dependency only.

## 27. Testing
- Integration: `content_type=dua` download initiates, downloads, and completes correctly through B.15's real engine
- Integration: offline mark-as-learned (B-02) queues via the real `SyncQueueEntity` and syncs exactly-once on reconnect via `client_request_id`
- Integration: download-permission revocation → existing dua downloads remain playable (B.15's existing policy, verified here as a dua-specific regression)

## 28. Documentation
Record whether dua downloads appear in B.15's shared Downloads Manager UI (likely) or need a dua-specific entry point, and the resolution of the `DownloadRepository` (kmpplayer) vs. B.15-engine question from §7.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Resolve `DownloadRepository` vs. B.15 Engine Relationship**
Task ID: K-07-T01. Objective: clarify whether `core/kmpplayer`'s `DownloadRepository` (media-file caching) and B.15's download-manifest engine are the same system or two layers that compose, before wiring dua content into either. Definition of Done: documented finding.

**Task 02 — Verify Dua Content-Type Scoping in B.15's Engine**
Task ID: K-07-T02. Definition of Done: `content_type=dua` downloads verified working end-to-end against the real engine, no dua-specific download code needed beyond parameter passing.

**Task 03 — Wire Offline Outbox for Mark-Learned/Favorite**
Task ID: K-07-T03. Files to Modify: `DuaRepositoryImpl.kt`. Existing Files to Reuse: `SyncQueueDao`/`SyncQueueEntity`, B15-KMP/06's sync integration. Definition of Done: exactly-once sync verified via `client_request_id`.

**Task 04 — Verify Downloads Manager UI Integration**
Task ID: K-07-T04. Objective: confirm dua downloads appear correctly in B.15's shared inventory UI (KMP/03) if one exists. Definition of Done: verified or a minimal dua-specific entry point added if genuinely needed.

**Task 05 — Add Tests**
Task ID: K-07-T05. Definition of Done: all §27 scenarios green.

**Task 06 — Add Documentation**
Task ID: K-07-T06. Definition of Done: §28's open items resolved and recorded.

**Task 07 — Final Code Review**
Task ID: K-07-T07. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
Dua content downloadable and offline-functional entirely through B.15's real, shared download/outbox engine, with no parallel dua-specific download pipeline built.

## 31. Final Verification Checklist
- [ ] No dua-specific download engine/outbox built — B.15's real engine reused
- [ ] `SyncQueueDao`/`SyncQueueEntity` used for offline mark-learned/favorite queuing, not an invented outbox
- [ ] `DownloadRepository` (kmpplayer) vs. B.15-engine relationship clarified, not assumed
- [ ] Download-permission revocation behavior verified against B.15's real policy

## 32. Addendum — What Changed From the Original Draft
The original draft built a dua-specific download manifest client, offline outbox, and sync worker, duplicating what `B15_Offline_Downloads_Sync` already provides generically (and which already lists `dua` in its real `content_type` enum). This file's scope is now correct scoping/integration with that existing engine, plus resolving one genuine ambiguity: whether `core/kmpplayer`'s `DownloadRepository` and B.15's engine are the same system.
