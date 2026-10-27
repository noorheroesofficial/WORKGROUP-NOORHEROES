# K-02 — Resumable Chunked Download Engine

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). The actual chunked-transfer engine underlying every download — resumable across app kills and reboots, checksum-validated, and the single shared entry point every offline-capable feature module calls to start a transfer.

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
K-02 — Resumable Chunked Download Engine

## 4. Objective
Extend the existing `core-database` `DownloadEntity`/DAO and `core-network` manifest DTOs with a `DownloadController` built on Media3 `DownloadManager`, providing checksum-validated, resumable chunked transfer that survives process death and device reboot, with exponential-backoff retry on interruption.

## 5. Business Requirements
- FR-2 items 3–4: resumable chunked download with checksums; encrypt/sandbox local media where the platform supports it (encryption itself is K-05's scope; this blueprint owns the transfer mechanics it protects).
- FR-6: interrupted/failed downloads resume with exponential backoff rather than restarting from zero.
- Integrity NFR: checksums validated on every downloaded chunk; a corrupted/incomplete download must never be presented as successfully complete.
- Edge Case 2: two simultaneous downloads pause/resume independently on connectivity loss, never cross-contaminating each other's progress.
- Edge Case 5: a signed manifest URL expiring mid-download is transparently re-requested and resumed from the last successfully-downloaded chunk.
- Edge Case 9: device runs out of storage mid-download → fails gracefully with a distinct "not enough storage" message.
- §5 Android AI Prompt item 1: `DownloadController.startDownload()` is the sole entry point; instrumented test kills the process mid-transfer and verifies correct resume.

## 6. Existing Architecture
Extends `core-database`'s existing `DownloadEntity` (already present per `CORE_DATABASE_INSTRUCTIONS.md` §4) and `core-network`'s `ConnectivityObserver`/`safeCall` — this blueprint does **not** introduce a new `:core:download-manager` module as the PRD's generic AI prompt suggests; it adds a `DownloadController` class within the existing `core-data` layer (alongside `SyncQueue`, per `CORE_DATA_INSTRUCTIONS.md`'s established pattern of housing coordination logic there), backed by Media3 `DownloadManager` as the underlying transfer engine on Android, with an equivalent platform-appropriate transfer mechanism on iOS via `expect`/`actual`.

## 7. Existing Code to Reuse
- `core-database`'s `DownloadEntity`, `SafeDatabaseHelper.withTransaction()` for atomic progress persistence.
- `core-network`'s `ConnectivityObserver` — pause/resume trigger on connectivity change.
- `core-network`'s `SyncOperation`/idempotency plugin conventions (for consistency, though downloads themselves aren't sync-queue operations).
- `common/utils/retry.py`-equivalent client-side backoff policy — implemented via WorkManager's built-in `BackoffPolicy.EXPONENTIAL`, not a bespoke retry loop.
- K-01's `DownloadRepository` — supplies the manifest this engine consumes.

## 8. Files to Create
- `core-data/src/commonMain/kotlin/.../download/DownloadController.kt`.
- `core-data/src/androidMain/kotlin/.../download/AndroidDownloadEngine.kt` (Media3 `DownloadManager` wrapper).
- `core-data/src/iosMain/kotlin/.../download/IosDownloadEngine.kt` (platform-appropriate transfer implementation).
- `core-database/src/commonMain/kotlin/.../dao/DownloadDao.kt` (if not already fully covering resumable-chunk state — extend as needed).
- `core-data/src/commonMain/kotlin/.../download/ChunkChecksumValidator.kt`.
- `core-data/src/androidAndroidTest/kotlin/.../download/ProcessKillResumeTest.kt` (instrumented).
- `core-data/src/commonTest/kotlin/.../download/ChecksumValidationTest.kt`.
- `core-data/src/commonTest/kotlin/.../download/PerChildIsolationTest.kt`.

## 9. Files to Modify
- `core-database`'s `DownloadEntity` — confirm/extend fields for `localFilePath`, per-chunk progress tracking, `checksumVerified`.
- `DataModule.kt` (Koin) — register `DownloadController`.

## 10. Backend Requirements
Consumes B-01's manifest response (`chunks[]` with `url`/`checksum`) and re-requests a fresh manifest via K-01's `DownloadRepository` when a signed URL expires mid-transfer.

## 11. KMP Requirements
- `DownloadController.startDownload(contentId, contentType)` is the **sole** entry point for starting a download — no feature module calls Media3 `DownloadManager` directly.
- Each chunk downloaded and validated against its `checksum` before being marked persisted; a checksum mismatch triggers a re-download of that chunk only, never silently accepting corrupted data.
- Progress persisted to `DownloadEntity` via `SafeDatabaseHelper.withTransaction()` after each validated chunk — so an app kill/reboot resumes from the last **validated** chunk, not merely the last attempted one.
- On resume (app restart, reconnect), scan `DownloadEntity` rows with `status='in_progress'` and continue each from its last validated chunk.
- Exponential backoff via WorkManager's `BackoffPolicy.EXPONENTIAL` on transfer interruption, rather than an immediate tight-loop retry.
- Two simultaneous downloads tracked independently — per-download state keyed by `downloadId`, no shared mutable state that could cross-contaminate progress between them (Edge Case 2).
- On a `410`/expired-URL response mid-transfer, transparently call back into K-01's `DownloadRepository.requestManifest()` for a fresh manifest and resume from the last validated chunk (Edge Case 5) — never restart from zero.
- Pre-transfer and mid-transfer available-storage checks; on exhaustion, fail with a distinct storage-error state (surfaced by K-01's initiation control and K-03's tab) rather than a generic failure.
- On full-download completion (all chunks validated), mark `DownloadEntity.status = 'complete'`, fire a local "download complete" notification (owned by this module, not the server Notification Service).

## 12. NextJS Requirements
N/A.

## 13. API Contract
Re-requests `POST /v1/downloads/manifest` (B-01) on expired-URL mid-transfer; otherwise downloads directly from the signed CDN chunk URLs returned by the original manifest call.

## 14. Database Requirements
Extends `core-database`'s existing `DownloadEntity` — no new Room table introduced, consistent with the existing architecture already anticipating this entity (per `CORE_DATABASE_INSTRUCTIONS.md`'s "Models" table listing `DownloadEntity` with `localFilePath`).

## 15. Validation
Every chunk's SHA-256 checksum verified against the manifest-supplied value before being accepted as persisted; the overall download is never marked `complete` until all chunks pass validation.

## 16. Authentication
Relies on the child-session bearer token already attached to the manifest request; chunk URLs themselves are pre-signed and don't require a bearer token (per B-01's CDN signing).

## 17. Authorization
N/A beyond the manifest-issuance authorization already enforced server-side (B-01/B-03).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Chunk checksum mismatch | Chunk re-downloaded, never accepted; overall download not marked complete |
| Process killed mid-transfer | Resumes from last validated chunk on next app launch (instrumented test, §27) |
| Connectivity lost mid-transfer | Pauses cleanly, resumes independently of any other in-flight download |
| Signed URL expires mid-transfer | Fresh manifest requested transparently, resumes from last validated chunk |
| Device storage exhausted | Distinct "not enough storage" failure state, not generic retry messaging |
| Persistent transfer failure | Exponential backoff via WorkManager, eventually surfaced as a retriable "failed" state in K-03 |

## 19. Offline First
This module **is** the offline-support infrastructure — once chunks are downloaded and validated, content is fully usable with zero network dependency.

## 20. Local Data
`DownloadEntity` (extended) is the local source of truth for download status, progress, and file location.

## 21. Localization
Local "download complete" notification text localized (English/Hindi/Arabic/Urdu).

## 22. RTL
N/A directly (notification/progress UI RTL handled by K-03).

## 23. Analytics
`download_progress_updated` (throttled to avoid excessive event volume), `download_interrupted`, `download_resumed`, `download_completed`, `download_failed_other`.

## 24. Performance
- Chunked, resumable transfer avoids re-downloading already-validated bytes on any interruption.
- Progress-update throttling (e.g., max once per 1–2 seconds per download) to avoid excessive DB writes/analytics volume during active transfer.
- Concurrency-limited parallel chunk/download processing (reasonable limit, e.g., 2–3 concurrent downloads) to avoid saturating device network/CPU resources.
- No main-thread blocking — all transfer/checksum work on background dispatchers via the injected `DispatcherProvider`.

## 25. Security
Checksum validation is the integrity guarantee this module owns; local encryption/sandboxing of the validated bytes is K-05's responsibility, applied immediately after this module marks a chunk as validated-and-persisted.

## 26. Library Requirements
Media3 `DownloadManager` (Android), platform-appropriate transfer API (iOS), WorkManager (Android background scheduling + backoff), Room (via `core-database`). No new bespoke HTTP client — reuses `core-network`'s existing engine where the transfer isn't handled by Media3 directly.

## 27. Testing
- **Instrumented process-kill-resume test (mandatory):** kill the process mid-transfer, relaunch, assert resume from the last validated chunk, not from zero.
- Unit: checksum-mismatch triggers re-download of only that chunk.
- Unit: two concurrent downloads' progress never cross-contaminate (Edge Case 2, dedicated test).
- Unit: expired-URL-mid-transfer triggers a fresh manifest request and resumes correctly (Edge Case 5).
- Unit: storage-exhaustion produces the distinct failure state.
- Unit: exponential backoff policy applied on repeated transfer failure (verified via WorkManager test harness).

## 28. Documentation
KDoc on `DownloadController.startDownload()` explicitly stating it is the sole entry point; architecture note explaining why this extends existing `core-data`/`core-database` rather than introducing a new `:core:download-manager` module.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Extend DownloadEntity/DAO for Chunk-Level Progress**
Files to modify: `core-database`'s `DownloadEntity`, `DownloadDao.kt`.

**Task 02 — Implement ChunkChecksumValidator**
Files to create: `ChunkChecksumValidator.kt`.

**Task 03 — Implement AndroidDownloadEngine (Media3 DownloadManager wrapper)**
Files to create: `AndroidDownloadEngine.kt`.

**Task 04 — Implement IosDownloadEngine**
Files to create: `IosDownloadEngine.kt`.

**Task 05 — Implement DownloadController (commonMain)**
Objective: sole entry point, orchestrating engine + checksum validator + `DownloadEntity` persistence.
Files to create: `DownloadController.kt`.

**Task 06 — Wire Exponential Backoff via WorkManager**

**Task 07 — Add Process-Kill-Resume Instrumented Test (highest priority)**
Tests: `ProcessKillResumeTest.kt`.

**Task 08 — Add Checksum & Isolation Tests**
Tests: `ChecksumValidationTest.kt`, `PerChildIsolationTest.kt`.

**Task 09 — Wire Local "Download Complete" Notification**

**Task 10 — Final Review**
Objective: confirm no feature module calls Media3 `DownloadManager` directly, bypassing `DownloadController`.

## 30. Definition of Done
- `DownloadController` is the sole, verified entry point for all downloads.
- Process-kill-resume instrumented test passes.
- Checksum validation verified non-bypassable.
- Two concurrent downloads verified non-cross-contaminating.
- Exponential backoff verified on interruption.

## 31. Final Verification Checklist
- [ ] `DownloadController.startDownload()` is the sole entry point — verified by code search for direct Media3 usage elsewhere.
- [ ] Process-kill mid-transfer resumes from last validated chunk — verified by instrumented test.
- [ ] Corrupted chunks never accepted as complete.
- [ ] Two concurrent downloads never cross-contaminate progress.
- [ ] Expired signed URL handled transparently, resumes without restart.
- [ ] Storage exhaustion produces a distinct, non-generic failure state.
