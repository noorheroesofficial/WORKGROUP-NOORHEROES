# K-01 — Download Initiation & Entitlement Gate

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). The shared entry point every content-detail screen (Story, Surah Learning, Bedtime Audio, Quiz, etc.) calls to start a download — the client-side gate in front of B-01's manifest issuance.

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
K-01 — Download Initiation & Entitlement Gate

## 4. Objective
Implement the shared `Download` control and its cap/entitlement-gated initiation logic, rendering distinct, non-alarming messaging for cap-reached vs. downloads-disabled vs. insufficient-storage, and treating an already-downloaded item as a no-op rather than a re-download.

## 5. Business Requirements
- FR-2: verify entitlement and parent download policy before any download begins.
- FR-3: cap-reached shows a clear message, no download begins.
- Edge Case 3: already-fully-downloaded content is a no-op/"already downloaded" confirmation, not a re-download or duplicate manifest.
- Edge Case 9: insufficient device storage fails gracefully with a distinct message from generic retry messaging.
- §2.1 UX: cap-reached/insufficient-storage messaging is supportive, non-alarming, actionable — never a harsh red error block.
- §1.19 Events: `download_initiated`, `download_cap_reached_shown`, `download_failed_insufficient_storage`.

## 6. Existing Architecture
New shared composable/control living in a `feature-downloads` module, invoked from each content-detail screen's existing UI (Story Detail, Surah Learning, etc.) — this blueprint does not modify those screens' own domain logic, only adds the shared `DownloadInitiationControl` they each embed. Built on the existing `core-data`/`core-network` repository pattern (Koin-injected), not a new DI graph.

## 7. Existing Code to Reuse
- `core-network`'s `HttpClient`/`safeCall` — for the manifest request itself.
- `core-data`'s `NoorResult<T>` error-handling pattern.
- `core-database`'s `DownloadEntity`/DAO — to check "already downloaded" state locally before ever calling the server.
- `core-network`'s `ConnectivityObserver` — to short-circuit with an offline-appropriate message rather than attempting a doomed network call.
- Existing content-detail screens' entry points (A.3/A.5/A.6/etc.) — this control is embedded into them, not a replacement screen.

## 8. Files to Create
- `feature-downloads/src/commonMain/kotlin/.../downloads/DownloadInitiationControl.kt` (Composable).
- `feature-downloads/src/commonMain/kotlin/.../downloads/DownloadInitiationViewModel.kt` (or a reusable state-holder consumed by each hosting screen's ViewModel).
- `feature-downloads/src/commonMain/kotlin/.../downloads/DownloadRepository.kt` (interface) + `DownloadRepositoryImpl.kt` in `core-data`.
- `core-network/src/commonMain/kotlin/.../api/DownloadsApi.kt` (Ktor client for `POST /v1/downloads/manifest`).
- `feature-downloads/src/commonTest/kotlin/.../CapVsDisabledMessagingTest.kt`.
- `feature-downloads/src/commonTest/kotlin/.../AlreadyDownloadedNoOpTest.kt`.

## 9. Files to Modify
- Each hosting content-detail screen (Story Detail, Surah Learning, etc.) — embed `DownloadInitiationControl`, wiring `contentId`/`contentType`.
- `DownloadsModule.kt` (Koin) — register `DownloadsApi`, `DownloadRepositoryImpl`.

## 10. Backend Requirements
Consumes B-01 exclusively: `POST /v1/downloads/manifest`.

## 11. KMP Requirements
- Before calling the server, check `core-database`'s `DownloadEntity` for an existing `status='complete'` row for `(childId, contentId)` — if found, render the "already downloaded" state (tap opens offline playback, per Edge Case 3) without a network call.
- On tap with no local record: perform a fast client-side cap-check mirror against a locally cached usage/limit figure **purely for responsive UX** — but always still issue the real `POST /v1/downloads/manifest` request, since the server's check is authoritative (never trust the client mirror as the actual gate).
- Render `403 DOWNLOAD_CAP_REACHED` and `403 DOWNLOADS_DISABLED_BY_PARENT` as two **visually and textually distinct** messages — never collapsed into one generic "can't download" string.
- Pre-flight device-storage check (platform API) before initiating the download transfer; insufficient storage renders a distinct message, never the generic retry-failure copy.
- On successful manifest response, hand off to K-02's `DownloadController.startDownload()` to begin the actual chunked transfer.
- Offline state: if `ConnectivityObserver` reports offline, show an appropriately-worded "connect to the internet to download" message rather than attempting and failing the request.
- Analytics: `download_initiated` on tap, `download_cap_reached_shown` on the cap-reached response, `download_failed_insufficient_storage` on the storage-check failure.

## 12. NextJS Requirements
N/A.

## 13. API Contract
`POST /v1/downloads/manifest` → per B-01 §13. Client sends `content_id`, `content_type`, `quality`; auth token carries child identity (no client-suppliable cap-override field exists in the request DTO).

## 14. Database Requirements
Reads `core-database`'s existing `DownloadEntity` table (owned by K-02) to determine already-downloaded state; writes nothing new here.

## 15. Validation
Client-side existence check only (already-downloaded, offline, storage) — all authoritative validation (cap, entitlement) happens server-side per B-01/B-03; this control never implements its own cap-enforcement logic beyond the explicitly-labeled "UX mirror."

## 16. Authentication
Relies on the app-wide child-session bearer token attached by `core-network`'s HTTP client interceptor.

## 17. Authorization
N/A beyond standard child session.

## 18. Error Handling
- `DOWNLOAD_CAP_REACHED` and `DOWNLOADS_DISABLED_BY_PARENT` render as two distinct copy blocks (UI test asserts they differ, §27).
- `ENTITLEMENT_REQUIRED` renders a standard entitlement-upsell message consistent with the platform's existing entitlement-gate pattern (reused, not reinvented).
- Insufficient device storage: distinct "not enough storage" message, never conflated with a generic network/retry error.
- Network failure (not a 403, a genuine transport error): standard retry-capable error state.

## 19. Offline First
This control itself requires connectivity to initiate a **new** download (by definition); it correctly distinguishes "offline, can't start a new download" from any of the 403 policy rejections.

## 20. Local Data
Reads `DownloadEntity` (K-02-owned) for already-downloaded/in-progress state.

## 21. Localization
All messaging (cap-reached, disabled, insufficient-storage, already-downloaded, offline) localized (English/Hindi/Arabic/Urdu), no hardcoded strings, non-alarming supportive tone per §2.1.

## 22. RTL
Control mirrors correctly in RTL layouts, consistent with `core-designsystem` conventions.

## 23. Analytics
`download_initiated`, `download_cap_reached_shown`, `download_failed_insufficient_storage` per §1.19, fired from this control.

## 24. Performance
- Local `DownloadEntity` existence check is a fast indexed Room query, never blocking the UI thread.
- Client-side cap mirror read is from an already-cached local value (updated opportunistically from K-03's inventory fetch), not a fresh network call on every tap.

## 25. Security
No new security surface — cap/entitlement enforcement is server-authoritative (B-01/B-03); this control's client-side mirror is explicitly documented as UX-only and never treated as a trust boundary.

## 26. Library Requirements
Jetpack Compose, Ktor (via `core-network`), Koin, Room (via `core-database`, read-only here). No Retrofit/OkHttp (existing platform convention).

## 27. Testing
- **Messaging distinction test (mandatory):** UI test asserting `DOWNLOAD_CAP_REACHED` and `DOWNLOADS_DISABLED_BY_PARENT` render visually/textually different copy.
- Unit: already-downloaded local-check short-circuits without a network call.
- Unit: insufficient-storage pre-flight check produces the distinct message, not the generic error.
- UI test: offline-state tap shows the offline-appropriate message, no failed network attempt.

## 28. Documentation
KDoc on `DownloadRepository.requestManifest()` explicitly noting the client-side cap mirror is UX-only and the server call is always made regardless of the mirror's result.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Implement DownloadsApi (Ktor)**
Objective: `POST /v1/downloads/manifest` client.
Files to create: `DownloadsApi.kt`.

**Task 02 — Implement DownloadRepository**
Objective: interface + impl, including the already-downloaded local-check short-circuit.
Files to create: `DownloadRepository.kt`, `DownloadRepositoryImpl.kt`.

**Task 03 — Build DownloadInitiationControl Composable**
Objective: tap handling, state rendering (default/already-downloaded/loading/cap-reached/disabled/insufficient-storage/offline).
Files to create: `DownloadInitiationControl.kt`.

**Task 04 — Implement Cap-Reached vs. Disabled Distinct Messaging**
Files to modify: `DownloadInitiationControl.kt`.
Tests: `CapVsDisabledMessagingTest.kt`.

**Task 05 — Implement Storage Pre-Flight Check**
Objective: platform-specific available-storage query before transfer handoff.

**Task 06 — Wire Into Content-Detail Screens**
Files to modify: Story Detail, Surah Learning, and other consuming screens.

**Task 07 — Wire Analytics Events**

**Task 08 — Final Review**
Objective: confirm the client-side cap mirror never blocks the actual server request from firing.

## 30. Definition of Done
- Shared control embedded in all offline-capable content-detail screens.
- Cap-reached vs. disabled messaging verified distinct.
- Already-downloaded state is a true no-op (no network call).
- Insufficient-storage message verified distinct from generic errors.

## 31. Final Verification Checklist
- [ ] Server manifest request always fires regardless of client-side cap mirror result.
- [ ] Cap-reached and disabled-by-parent render distinct messages — verified by test.
- [ ] Already-downloaded content produces no network call.
- [ ] Insufficient-storage message distinct from generic retry messaging.
- [ ] Offline tap shows an offline-appropriate message, not a failed request.
- [ ] Localization and RTL verified, no hardcoded strings.
