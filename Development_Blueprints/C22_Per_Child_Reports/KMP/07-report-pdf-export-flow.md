# Blueprint: Report PDF Export Flow

## 1. Feature Context
Platform: NoorHeroes KMP App. Module: `:feature:reports`. Delivers `PdfExportFlow`, triggered from the "Export PDF" action on `PerChildReportScreen` (K-01).

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
K-07 — Report PDF Export Flow.

## 4. Objective
Implement a connectivity-first export flow that blocks immediately when offline (no attempted network call), shows a clear generating-progress state, and hands off to the OS share/save sheet on success.

## 5. Business Requirements
Source: PRD §1.7 FR-11, §1.10 Edge Case #9, §1.13 Loading States, §2.3, §6.9.
- Export PDF action → "Generating your report..." progress indicator → OS share/save sheet.
- Offline → blocked with a clear "needs internet" message, since the action requires a fresh, server-validated report payload — never operates on a potentially-stale local cache (Edge Case #9).
- p95 < 3s generation time (server-side NFR; client shows progress accordingly).

## 6. Existing Architecture
Calls Backend B-07's `POST /v1/parent/reports/{child_id}/export`. Uses `ConnectivityObserver` (`core-data`/`core-common`) — the platform's confirmed, single abstraction for online/offline state (established and named in C.20 K-07; never poll platform APIs directly) — for the connectivity-first check, and the OS share-sheet integration pattern (platform-specific `expect`/`actual` implementation, the same unnamed-but-established per-platform pattern A.11 K-05 already uses for its own share flow — reuse that mechanism, do not reinvent it).

## 7. Existing Code to Reuse
- `ConnectivityObserver` (`core-data`/`core-common`).
- Platform's existing OS share/save sheet integration (`expect`/`actual`), if one exists elsewhere (e.g., for media sharing) — reuse the same mechanism.
- `BaseViewModel`, `NoorResult<T>`, `DispatcherProvider`.

## 8. Files to Create
- `feature/reports/src/commonMain/kotlin/.../PdfExportFlow.kt`
- `feature/reports/src/commonMain/kotlin/.../PdfExportViewModel.kt`
- `feature/reports/src/commonMain/kotlin/.../PdfExportUiState.kt`
- `feature/reports/src/commonTest/kotlin/.../PdfExportFlowOfflineBlockTest.kt`
- `feature/reports/src/commonTest/kotlin/.../PdfExportViewModelTest.kt`

## 9. Files to Modify
- `ReportRepository.kt` — add `exportPdf(childId): NoorResult<PdfExportResult>`
- `PerChildReportScreen.kt` (K-01) — wire the "Export PDF" button to trigger `PdfExportFlow`

## 10. KMP Requirements
- `PdfExportUiState`: `sealed interface { object Idle; object CheckingConnectivity; object OfflineBlocked; object Generating; data class Success(val pdfUrl: String); data class Error(val error: AppError) }`.
- `PdfExportViewModel.startExport(childId)`:
  1. Check connectivity **first**, before any network call.
  2. If offline: emit `OfflineBlocked` immediately, **do not attempt** the export network call.
  3. If online: emit `Generating`, call `reportRepository.exportPdf(childId)`.
  4. On success: emit `Success(pdfUrl)`, trigger the OS share/save sheet with the PDF.
  5. On failure: emit `Error`.
- The connectivity check must be synchronous/fast enough to feel instantaneous — no network round-trip used merely to determine online/offline status (use the platform's existing reachability signal, not a probe request).

## 11. Files to Create — continued
`PdfExportFlow` composable: renders `Generating` as a progress overlay with "Generating your report..." copy; renders `OfflineBlocked` as an inline message, not a full-screen error; triggers the platform share sheet on `Success`.

## 12. NextJS Requirements
N/A.

## 13. API Mapping
`ReportRepository.exportPdf(childId)` → `POST /v1/parent/reports/{child_id}/export` (Backend B-07).

## 14. Database Requirements (Local)
N/A — this flow always requires a live network call by design (Edge Case #9); no local persistence of export state beyond the in-memory `PdfExportUiState`.

## 15. Validation
`childId` required.

## 16. Authentication
Inherits Parent Gate requirement (only reachable from within the gated `PerChildReportScreen`).

## 17. Authorization
Server-enforced (Backend B-07); client reflects `403`/`404` as `Error`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Offline at flow start | `OfflineBlocked` immediately, no network call attempted |
| Generation failure/timeout server-side | `Error` with retry |
| Share sheet unavailable/cancelled by user | Returns to `Idle`, not treated as an error |

## 19. Offline First
Deliberately **not** offline-first — this write/export action requires a live connection by design (Edge Case #9), documented explicitly to avoid future accidental "helpful" offline-caching additions that would violate the PRD's freshness requirement.

## 20. Local Data
N/A.

## 21. Localization
"Generating your report..." and the offline-blocked message are locale-resolved string resources (English/Hindi/Arabic/Urdu).

## 22. RTL
Progress overlay and offline-blocked message layout mirror correctly for Arabic/Urdu.

## 23. Analytics
`report_pdf_export_initiated` fired when the export call begins (after the connectivity check passes); `report_pdf_export_completed` fired on `Success`.

## 24. Performance
Connectivity check must not introduce perceptible delay; `Generating` state must appear within one frame of the button tap.

## 25. Security
No sensitive data handled client-side beyond the signed, short-TTL `pdf_url` already scoped by the backend to the authenticated parent.

## 26. Library Requirements
No new dependencies; reuses existing platform share-sheet integration.

## 27. Testing
1. **Offline-block test:** simulate airplane mode/no connectivity, assert `OfflineBlocked` renders immediately and no network call is attempted (verified via a mocked repository call-count assertion of zero).
2. Unit test: successful export transitions `Idle → Generating → Success`.
3. Unit test: generation failure transitions to `Error`.
4. UI test: `Generating` shows the correct progress copy.
5. Integration test: full export flow through the gate, including share-sheet hand-off.

## 28. Documentation
KDoc explicitly citing Edge Case #9 and the "connectivity check before any network call" contract.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define PdfExportUiState and Repository Method**
- Task ID: K07-T01
- Objective: State model with a distinct `OfflineBlocked` variant reachable without any network call.
- Why This Is Required: Edge Case #9's core enforcement point.
- Existing Architecture to Follow: `NoorResult<T>` pattern.
- Existing Files to Reuse: `ReportRepository` (extend).
- Files to Create: `PdfExportUiState.kt`.
- Files to Modify: `ReportRepository.kt`.
- Implementation Details: Per §10.
- Business Rules: Edge Case #9.
- Validation: N/A.
- Error Handling: `OfflineBlocked`/`Error` distinct.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 03.
- Documentation: KDoc.
- Dependencies: Backend B-07 live.
- Do Not Change: N/A.
- Expected Result: State model compiles.
- Definition of Done: Matches Backend B-07's contract.

**Task 02 — Implement PdfExportViewModel with Connectivity-First Check**
- Task ID: K07-T02
- Objective: Check connectivity before attempting any network call.
- Why This Is Required: Direct implementation of Edge Case #9.
- Existing Architecture to Follow: `ConnectivityObserver` (`core-data`/`core-common`), per C.20 K-07's established usage.
- Existing Files to Reuse: `:core:network` reachability signal.
- Files to Create: `PdfExportViewModel.kt`, `PdfExportFlow.kt`.
- Files to Modify: `PerChildReportScreen.kt`.
- Implementation Details: Per §10.
- Business Rules: Edge Case #9, FR-11.
- Validation: N/A.
- Error Handling: Per §18.
- Security: N/A.
- Performance: Fast/instantaneous connectivity check.
- Localization: Full string-resource coverage.
- RTL: Verified mirroring.
- Analytics: `report_pdf_export_initiated`/`report_pdf_export_completed`.
- Tests: Covered in Task 03.
- Documentation: KDoc citing Edge Case #9.
- Dependencies: Task 01.
- Do Not Change: Platform's existing share-sheet integration internals.
- Expected Result: Flow correctly blocks offline attempts before any network call.
- Definition of Done: Task 03's offline-block test passes with zero network calls verified.

**Task 03 — Write Test Suite Including Offline-Block Test**
- Task ID: K07-T03
- Objective: Cover §27, with the offline-block test as the defining verification.
- Why This Is Required: Edge Case #9 is a hard requirement with a specific "no attempted call" clause.
- Existing Architecture to Follow: Kotlin test with mocked connectivity/repository.
- Existing Files to Reuse: none new.
- Files to Create: `PdfExportViewModelTest.kt`, `PdfExportFlowOfflineBlockTest.kt`.
- Files to Modify: none.
- Implementation Details: 5 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact states.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test KDoc citing Edge Case #9.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green, offline-block test verifies zero network calls.

## 30. Definition of Done
`PdfExportFlow` live, connectivity checked before any network call, offline attempts blocked immediately, successful exports hand off to the OS share sheet, all tests green.

## 31. Final Verification Checklist
- [ ] Offline-block test confirms zero network calls attempted when offline (Edge Case #9)
- [ ] "Generating your report..." progress state renders promptly
- [ ] Successful export correctly triggers the OS share/save sheet
- [ ] Localization and RTL mirroring verified
- [ ] Reachable only from within the gated `PerChildReportScreen`
