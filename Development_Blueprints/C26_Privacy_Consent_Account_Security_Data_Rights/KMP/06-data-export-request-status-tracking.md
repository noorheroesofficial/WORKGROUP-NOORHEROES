# K-06 — Data Export Request & Status Tracking

## 1. Feature Context
Part of Feature C.26. The client half of B-03's async, idempotent, cross-surface-consistent data export pipeline.

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**K-06 — Data Export Request & Status Tracking**

## 4. Objective
Implement the export request flow with client-side idempotent handling (never firing a duplicate request when one is already known in-flight) and a status-tracking screen reusing C.25's async-status-stage-indicator pattern.

## 5. Business Requirements
- FR-5: async, cross-surface status.
- Edge Case 2: duplicate request handling — client-side, never shows two conflicting "ready" states.
- Edge Case 7: large-family export — no special client handling beyond the existing "preparing" state.
- §7 Android AI Code-Generation Prompt item 4: idempotent client-side handling — tapping "Request Export" again shows existing status rather than firing a duplicate.

## 6. Existing Architecture
Within `:feature:parent-settings`, consumes B-03's endpoints. Status indicator reuses **C.25's existing async-status-stage-indicator component** (Requested → Preparing → Ready) — confirm the exact existing Composable from C.25's module before building a second one, per rule 2 ("do not invent a new architecture when the existing architecture already supports the requirement").

## 7. Existing Code to Reuse
- C.25's stage-indicator Composable (confirm exact location/class name in that feature's module).
- `ParentGateLauncher.requireParentAuth()` for step-up on request creation.
- Push-notification deep-link handling infrastructure (C.25 owns export-ready notifications; this screen is the deep-link destination, not the notification sender).

## 8. Files to Create
- `feature/parent-settings/src/commonMain/kotlin/.../DataExportRequestScreen.kt`
- `feature/parent-settings/src/commonMain/kotlin/.../ExportStatusTrackingScreen.kt`
- `feature/parent-settings/src/commonMain/kotlin/.../DataExportViewModel.kt`
- `core-data/.../DataExportRepository.kt` (interface) + impl

## 9. Files to Modify
- `ParentSettingsNavGraph.kt` (K-01) — wire routes, including the deep-link destination `noorheroes://parent/settings/export`.

## 10. Backend Requirements
Consumes B-03's `POST /v1/data-requests/exports`, `GET /v1/data-requests/{id}` exclusively.

## 11. KMP Requirements
- `DataExportViewModel` tracks last-known request state; before firing a new `POST`, check local state — if a request is already `preparing` per the last successful poll/response, show that existing status instead of calling the endpoint again (client-side idempotency, complementing B-03's server-side dedup, not replacing it — the server-side check per B-03 §10 remains the authoritative guard).
- `ExportStatusTrackingScreen` polls `GET /v1/data-requests/{id}` at a reasonable interval while `status == "preparing"`, stops polling on `ready`/`failed`.
- Handle the export-ready push notification (owned by C.25) as a deep link directly into this screen with the relevant `request_id`.
- Empty state: "Request your first export anytime" when no export history exists locally/server-side.

## 12. NextJS Requirements
Not applicable — but this screen's underlying data (`GET /v1/data-requests/{id}`) must remain byte-identical to what D.27's future web portal will show, per B-03's cross-surface guarantee; this screen must not add any mobile-only interpretation/transformation that the web portal wouldn't also apply.

## 13. API Contract
Consumes B-03's contract as documented in that blueprint.

## 14. Database Requirements
Local cache of the last-known `request_id`/status for client-side idempotency checks, invalidated on `ready`/`failed`.

## 15. Validation
None client-side beyond disabling the "Request Export" button during an in-flight request.

## 16. Authentication
Parent session; request creation requires step-up.

## 17. Authorization
Step-up gate before `POST /v1/data-requests/exports`.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Export start failure | Clear retry option, never silent |
| Poll failure (transient) | Retry poll silently a bounded number of times before surfacing an error |
| Duplicate tap while in-flight | Existing status shown, no new request fired (client-side idempotency test) |

## 19. Offline First
Status viewable from last-cached state offline; request creation requires connectivity.

## 20. Local Data
Last-known `request_id`/status cached locally for idempotent-tap handling and offline status viewing.

## 21. Localization
All screen chrome and stage-indicator labels localized.

## 22. RTL
Full RTL layout, including the stage-indicator's visual progression direction.

## 23. Analytics
`data_export_requested`, `data_export_status_viewed`, `data_export_completed`.

## 24. Performance
Bounded polling interval/backoff while `preparing`, stopped immediately on terminal state — no indefinite polling loop.

## 25. Security
Step-up required before requesting export, consistent with the sensitivity of the data being packaged.

## 26. Library Requirements
No new libraries — reuses C.25's stage-indicator component and existing push-notification deep-link infrastructure.

## 27. Testing
- **Highest-priority test:** re-tapping "Request Export" while a request is known in-flight shows existing status, fires zero duplicate network calls.
- Integration test: full request-to-ready flow, status polling stops on terminal state.
- Integration test: export-ready push notification correctly deep-links into this screen with the right `request_id`.
- Offline test: last-cached status renders correctly with no network.
- UI test: empty state renders correctly for a family with no export history.

## 28. Documentation
KDoc noting the client-side idempotency check is a UX complement to B-03's authoritative server-side dedup, not a replacement for it.

## 29. AI Coding Agent Implementation Steps

**Task 00 — Confirm C.25's Stage-Indicator Component**
- **Objective:** Locate the exact existing Composable before building a second one.

**Task 01 — `DataExportRepository`**
- **Files to Create:** interface + impl wrapping B-03's two endpoints.

**Task 02 — `DataExportRequestScreen` with Client-Side Idempotency**
- **Files to Create:** screen + ViewModel logic.
- **Tests:** the highest-priority idempotent-tap test.

**Task 03 — `ExportStatusTrackingScreen` with Bounded Polling**
- **Files to Create:** screen composable, reusing C.25's stage indicator.
- **Definition of Done:** Polling stops correctly on `ready`/`failed`.

**Task 04 — Deep-Link Wiring for Export-Ready Notifications**
- **Files to Modify:** `ParentSettingsNavGraph.kt`.
- **Dependencies:** Coordinate with C.25's notification-sending implementation.

**Task 05 — Localization, RTL, Analytics, Offline Caching, Full Test Suite**

## 30. Definition of Done
Data export request and status tracking are fully functional, client-side idempotent (complementing B-03's server-side guarantee), correctly reuse C.25's existing stage-indicator component, and correctly handle the export-ready deep link.

## 31. Final Verification Checklist
- [ ] Client-side idempotent-tap test passes, zero duplicate network calls
- [ ] Polling bounded and stops on terminal state
- [ ] Reuses C.25's existing stage-indicator component, not a duplicate
- [ ] Export-ready deep link correctly routes into this screen
- [ ] Full localization and RTL verified
- [ ] Offline last-cached status rendering verified
