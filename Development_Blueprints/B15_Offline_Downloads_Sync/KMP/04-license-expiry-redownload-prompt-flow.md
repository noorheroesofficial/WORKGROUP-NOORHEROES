# K-04 — License Expiry & Re-Download Prompt Flow

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). The client-side reaction to B-06's periodic entitlement refresh — ensures a child never hits a silent failure or crash when opening content whose offline license has expired.

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
K-04 — License Expiry & Re-Download Prompt Flow

## 4. Objective
Detect `license_expired`/withdrawn state on attempted offline-content open and show a clear, actionable re-download prompt, routing confirm back into K-01/K-02 for a fresh manifest and download.

## 5. Business Requirements
- FR-7: license-expired downloads show a clear re-download prompt instead of silently failing.
- Acceptance Criteria §1.9: given a downloaded item's entitlement/license has expired, when the child attempts to open it, a clear re-download prompt is shown — never a silent failure or crash.
- Edge Case 8: a withdrawn quiz/question-bank package's response is still recorded on sync but excluded from mastery/reward — this flow's job is correct prompting, not the withdrawal-exclusion business logic itself.

## 6. Existing Architecture
Extends `feature-downloads`' existing screens/components (K-02/K-03), adding a shared `LicenseExpiredPrompt` composable invoked from any content-open entry point (Story Player, Surah Learning, Bedtime Audio, etc.) when the local `DownloadEntity.status == 'license_expired'`.

## 7. Existing Code to Reuse
- `core-database`'s `DownloadEntity` (`status` field, extended per K-02) as the trigger source — this flow reads local state only, no dedicated network call needed to detect expiry (B-06's server-side job already set the state, surfaced via K-03's periodic B-02 refresh or the entity's locally-cached value).
- K-01's `DownloadInitiationControl`/`DownloadRepository.requestManifest()` for the re-download action itself.
- `core-designsystem`'s existing modal/prompt components (reuse, not reinvent).

## 8. Files to Create
- `feature-downloads/src/commonMain/kotlin/.../downloads/components/LicenseExpiredPrompt.kt`.
- `feature-downloads/src/commonTest/kotlin/.../LicenseExpiredPromptTriggerTest.kt`.

## 9. Files to Modify
- Each offline-content-open entry point (Story Player, Surah Learning, Bedtime Audio) — check `DownloadEntity.status` before attempting local playback; if `license_expired`, show `LicenseExpiredPrompt` instead of attempting to play a stale/inaccessible file.

## 10. Backend Requirements
Re-download action re-invokes B-01 (`POST /v1/downloads/manifest`) via K-01's existing repository.

## 11. KMP Requirements
- On any offline-content-open attempt, check the local `DownloadEntity.status` first: `complete` → proceed to normal offline playback; `license_expired` → show `LicenseExpiredPrompt` instead of attempting playback (never a silent failure or crash, per Acceptance Criteria).
- `LicenseExpiredPrompt`: clear, non-alarming copy explaining the offline access needs refreshing, with a single primary "Re-download" action.
- Confirm → re-invokes K-01's initiation flow (fresh manifest request → K-02's download engine), replacing the expired local copy on successful re-download.
- Dismiss → returns to the previous screen without attempting playback (no crash path).
- Withdrawn-content variant: if the underlying content is also flagged `withdrawn` (per B-06), the prompt's copy is adjusted to indicate the content may no longer be available rather than promising a successful re-download (routing/copy distinction only — the actual availability decision is server-side, delegated to B-01's response on re-download attempt).

## 12. NextJS Requirements
N/A.

## 13. API Contract
Re-download action: `POST /v1/downloads/manifest` per B-01 §13.

## 14. Database Requirements
Reads `DownloadEntity.status` (K-02-owned); on successful re-download, K-02's normal completion flow updates the same row back to `complete`.

## 15. Validation
N/A (UI/flow layer) — this blueprint contains no independent validation logic beyond checking local `status`.

## 16. Authentication
Relies on the standard child-session context already active for content-open actions.

## 17. Authorization
N/A beyond standard child-session scoping.

## 18. Error Handling
- Content-open attempt on `license_expired` status: always shows the prompt, never attempts a doomed playback call and never crashes.
- Re-download attempt itself fails (e.g., now genuinely unentitled): standard entitlement-upsell messaging (reused from K-01), not a repeat of the expired-license copy.
- Prompt dismissed without action: content remains in `license_expired` state, re-triggerable on next open attempt.

## 19. Offline First
Expiry detection is fully local (reads `DownloadEntity.status`); only the re-download action itself requires connectivity.

## 20. Local Data
`DownloadEntity.status` (K-02-owned) is the sole trigger source.

## 21. Localization
Prompt copy (including the withdrawn-content variant) fully localized (English/Hindi/Arabic/Urdu).

## 22. RTL
Modal/prompt mirrors correctly per `core-designsystem` convention.

## 23. Analytics
`download_license_expired_shown`, `download_redownload_initiated`.

## 24. Performance
Local status check is a single indexed Room read, negligible overhead added to any content-open path.

## 25. Security
No new security surface — re-download re-runs through B-01/B-03's full server-side entitlement/cap enforcement, exactly as a fresh download would.

## 26. Library Requirements
Jetpack Compose, Koin. No new libraries.

## 27. Testing
- **Trigger test (mandatory):** attempting to open `license_expired` content always shows the prompt, never attempts playback, never crashes (§27, matching the explicit Acceptance Criterion).
- Unit: confirm action re-invokes K-01's manifest request correctly.
- Unit: dismiss leaves local state unchanged, re-triggerable.
- UI test: withdrawn-content variant renders distinct copy from the standard expiry copy.

## 28. Documentation
KDoc noting this is the mandatory guard against the "silent failure or crash on expired-license open" acceptance criterion, and why the check must precede every offline-playback entry point.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Build LicenseExpiredPrompt Component**
Files to create: `LicenseExpiredPrompt.kt`.

**Task 02 — Wire Status Check into Content-Open Entry Points**
Files to modify: Story Player, Surah Learning, Bedtime Audio content-open logic.

**Task 03 — Wire Re-Download Confirm Action**
Objective: delegates to K-01's existing initiation flow.

**Task 04 — Implement Withdrawn-Content Copy Variant**

**Task 05 — Add Trigger Test (highest priority)**
Tests: `LicenseExpiredPromptTriggerTest.kt`.

**Task 06 — Wire Analytics & Final Review**
Objective: confirm every offline-content-open entry point checks status before attempting playback (code-search verification).

## 30. Definition of Done
- Prompt shown on every `license_expired` open attempt, across all offline-capable content types.
- Re-download confirm correctly triggers a fresh manifest request.
- No crash/silent-failure path exists for expired content.

## 31. Final Verification Checklist
- [ ] Every offline-content-open entry point checks `DownloadEntity.status` before playback.
- [ ] `license_expired` always shows the prompt, never a silent failure or crash — verified by test.
- [ ] Re-download confirm correctly re-invokes K-01/B-01.
- [ ] Withdrawn-content variant copy distinct from standard expiry copy.
- [ ] Localization and RTL verified.
