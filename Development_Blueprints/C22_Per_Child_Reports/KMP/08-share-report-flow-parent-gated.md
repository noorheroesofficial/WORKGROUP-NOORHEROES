# Blueprint: Share Report Flow — Parent-Gated

## 1. Feature Context
Platform: NoorHeroes KMP App. Module: `:feature:reports`, integrating `:core:auth`'s `ParentGateLauncher` (C.19). Delivers `ShareReportFlow`: Parent Gate → Card Preview → OS Share Sheet.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
K-08 — Share Report Flow (Parent-Gated).

## 4. Objective
Implement the WhatsApp achievement-sharing flow requiring a fresh Parent PIN/biometric step-up before any share-card API call is reachable, rendering a PII-free Achievement Share Card Preview, verified structurally via a reflection-based test on the UI state model.

## 5. Business Requirements
Source: PRD §1.7 FR-10, §1.10 Edge Case #2, #9, §1.18 Screen Inventory #13/#14, §6.5, §7 item 4/5.
- Share flow: Parent Gate → Card Preview → OS Share Sheet.
- `ParentGateLauncher.requireParentAuth(AchievementShare)` (C.19) must succeed **before** the share-card API is ever called.
- Card contains nickname/initial + badge only — no PII.
- Offline → blocked with a clear "needs internet" message (Edge Case #9).
- A shared card remains valid even if the underlying badge is later revoked (Edge Case #2) — this is a backend guarantee (B-08); the client simply displays what the server returns without re-validating badge status client-side.

## 6. Existing Architecture
Reuses C.19's `ParentGateLauncher` (established in the Parent Gate architecture referenced throughout C.19/C.20/A.11) and calls Backend B-08's `POST /v1/parent/reports/{child_id}/share-card`.

## 7. Existing Code to Reuse
- `ParentGateLauncher.requireParentAuth(TriggerContext.AchievementShare)` (C.19) — reused exactly as A.11 already uses it for badge sharing, applied here to report-originated sharing.
- Platform's existing OS share-sheet integration (reused from K-07/A.11).
- `ConnectivityObserver` (`core-data`/`core-common`, reused from K-07).
- `BaseViewModel`, `NoorResult<T>`.

## 8. Files to Create
- `feature/reports/src/commonMain/kotlin/.../ShareReportFlow.kt`
- `feature/reports/src/commonMain/kotlin/.../ShareCardPreviewScreen.kt`
- `feature/reports/src/commonMain/kotlin/.../ShareReportViewModel.kt`
- `feature/reports/src/commonMain/kotlin/.../ShareCardUiState.kt`
- `feature/reports/src/commonTest/kotlin/.../ShareCardUiStateNoPiiStructuralTest.kt`
- `feature/reports/src/commonTest/kotlin/.../ShareReportFlowGateEnforcementTest.kt`

## 9. Files to Modify
- `ReportRepository.kt` — add `getShareCard(childId, stepUpToken): NoorResult<ShareCardResult>`
- `PerChildReportScreen.kt` (K-01) — wire the "Share via WhatsApp" action to trigger `ShareReportFlow`

## 10. KMP Requirements
- `ShareCardUiState`: `data class Content(val cardImageUrl: String, val nicknameOrInitial: String, val badgeLabel: String)` — **no `childId`, `dob`, or `location` field declared anywhere in this class or any type it references.**
- `ShareReportViewModel.startShare(childId)`:
  1. Check connectivity first; if offline, emit `OfflineBlocked` (Edge Case #9), no API call attempted.
  2. Call `ParentGateLauncher.requireParentAuth(TriggerContext.AchievementShare)`.
  3. **Only if** step 2 succeeds, call `reportRepository.getShareCard(childId, stepUpToken)` — the API call must be structurally unreachable from any code path that skips step 2.
  4. On success, navigate to `ShareCardPreviewScreen` showing the card.
  5. From the preview, "Share" triggers the OS share sheet with the card image.
- `ShareCardPreviewScreen` renders **only** `nicknameOrInitial` and `badgeLabel` — no other child-identifying UI element.

## 11. Files to Create — continued
`ShareReportFlow`: orchestrates the gate → preview → share-sheet sequence as a single flow instance, ensuring the gate cannot be bypassed by re-entering the flow at the preview step directly (no direct navigation route to `ShareCardPreviewScreen` exists outside this flow's internal state machine).

## 12. NextJS Requirements
N/A.

## 13. API Mapping
`ReportRepository.getShareCard(childId, stepUpToken)` → `POST /v1/parent/reports/{child_id}/share-card` (Backend B-08).

## 14. Database Requirements (Local)
N/A — this write/share action requires a live connection and a fresh step-up token by design; no local persistence of share state.

## 15. Validation
`childId` required; step-up token must be present and fresh before the API call (enforced by `ParentGateLauncher`, not re-validated client-side beyond that call's own result).

## 16. Authentication
Inherits Parent Gate requirement for the base screen, **plus** the additional fresh step-up requirement specific to this action (two-factor within an already-gated context, mirroring A.11's pattern).

## 17. Authorization
Server-enforced (Backend B-08); client's `ParentGateLauncher` call is the client-side half of this two-sided guarantee.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Offline at flow start | `OfflineBlocked` immediately, no API call attempted |
| Parent Gate step-up fails/cancelled | Flow returns to `Idle`, no API call ever made |
| Share-card generation failure | `Error` with retry |
| Share sheet unavailable/cancelled by user | Returns to `Idle`, not treated as an error |

## 19. Offline First
Deliberately not offline-first, identical rationale to K-07 (Edge Case #9).

## 20. Local Data
N/A.

## 21. Localization
Badge labels locale-resolved (reused from A.11's existing localization); "needs internet" and gate-related copy locale-resolved.

## 22. RTL
Card preview layout and share-sheet trigger mirror correctly for Arabic/Urdu.

## 23. Analytics
`report_share_gate_opened` when the Parent Gate step begins; `report_share_completed` on successful share-sheet hand-off; `report_export_share_blocked_offline` when blocked per Edge Case #9.

## 24. Performance
Standard flow-level performance; no special concerns.

## 25. Security
The share-card API call must be **structurally unreachable** without a prior successful `ParentGateLauncher.requireParentAuth()` call in the same flow instance — verified by a test that attempts to invoke the repository call directly and confirms it requires a valid step-up token parameter that only the gate flow can produce. The `ShareCardUiState`'s field-absence (no `childId`/`dob`/`location`) is verified by a reflection-based structural test, mirroring Backend B-08's own PII-absence guarantee on the client side.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. **PII field-absence structural test:** reflection scan of `ShareCardUiState` confirms no field matching `childId`/`dob`/`location`/`address`.
2. **Gate-enforcement test:** confirm the share-card repository call is never reachable without a successful `ParentGateLauncher` result preceding it in the same flow instance.
3. Unit test: offline block prevents both the gate call and the API call.
4. Unit test: gate cancellation returns to `Idle` without an API call.
5. UI test: `ShareCardPreviewScreen` renders only nickname/initial and badge, no other identifying content.
6. Integration test: full gate → preview → share-sheet flow.

## 28. Documentation
KDoc explicitly citing FR-10 and the "gate before API call" structural guarantee, mirroring A.11's established pattern documentation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define ShareCardUiState with Structural PII-Absence Guarantee**
- Task ID: K08-T01
- Objective: Data model with no PII field possible.
- Why This Is Required: FR-10's client-side enforcement point, mirroring Backend B-08.
- Existing Architecture to Follow: A.11's existing reflection-test pattern for share-card PII absence.
- Existing Files to Reuse: A.11's field-absence test utility if present.
- Files to Create: `ShareCardUiState.kt`, `ShareCardUiStateNoPiiStructuralTest.kt`.
- Files to Modify: none.
- Implementation Details: Per §10.
- Business Rules: FR-10.
- Validation: N/A.
- Error Handling: N/A at this layer.
- Security: This IS the security control.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task's structural test is itself a deliverable.
- Documentation: KDoc citing FR-10.
- Dependencies: none.
- Do Not Change: A.11's existing share-card model.
- Expected Result: State model compiles, structural test passes.
- Definition of Done: Reflection test green and CI-wired.

**Task 02 — Implement ShareReportViewModel with Gate-Before-API-Call Enforcement**
- Task ID: K08-T02
- Objective: Structurally require `ParentGateLauncher` success before any API call.
- Why This Is Required: FR-10's mandatory sequencing requirement.
- Existing Architecture to Follow: `ParentGateLauncher.requireParentAuth()` (C.19), reused exactly as A.11 uses it.
- Existing Files to Reuse: `core-auth::ParentGateLauncher`, `ConnectivityObserver`.
- Files to Create: `ShareReportViewModel.kt`, `ShareReportFlow.kt`.
- Files to Modify: `ReportRepository.kt`, `PerChildReportScreen.kt`.
- Implementation Details: Per §10.
- Business Rules: FR-10, Edge Case #9.
- Validation: N/A.
- Error Handling: Per §18.
- Security: Gate-before-call sequencing is the primary control.
- Performance: N/A.
- Localization: Full string-resource coverage.
- RTL: Verified mirroring.
- Analytics: `report_share_gate_opened`/`report_share_completed`/`report_export_share_blocked_offline`.
- Tests: Covered in Task 04.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: `ParentGateLauncher` internals.
- Expected Result: Flow correctly sequences gate then API call, never the reverse.
- Definition of Done: Task 04's gate-enforcement test passes.

**Task 03 — Implement ShareCardPreviewScreen**
- Task ID: K08-T03
- Objective: PII-free preview screen with the share-sheet trigger.
- Why This Is Required: User-facing delivery of this sub-feature.
- Existing Architecture to Follow: A.11's existing badge/card preview pattern.
- Existing Files to Reuse: A.11's card preview composable, if reusable directly.
- Files to Create: `ShareCardPreviewScreen.kt`.
- Files to Modify: Navigation graph (internal to `ShareReportFlow`, no standalone external route).
- Implementation Details: Per §11.
- Business Rules: FR-10.
- Validation: N/A.
- Error Handling: Per §18.
- Security: Only nickname/initial + badge rendered.
- Performance: N/A.
- Localization: Full string-resource coverage.
- RTL: Verified mirroring.
- Analytics: N/A (ViewModel-level).
- Tests: Covered in Task 04.
- Documentation: KDoc.
- Dependencies: Task 02.
- Do Not Change: N/A.
- Expected Result: Preview renders correctly.
- Definition of Done: Matches §2.2/§6.2-equivalent PRD requirements.

**Task 04 — Write Test Suite Including PII and Gate-Enforcement Structural Tests**
- Task ID: K08-T04
- Objective: Cover §27, with both structural tests as the highest-priority guarantees for this sub-feature.
- Why This Is Required: PRD §7 item 4/5 explicitly name these as top-priority for the Android/KMP module.
- Existing Architecture to Follow: Kotlin test + Compose UI test, reflection-based scanning.
- Existing Files to Reuse: A.11's structural test utilities if present.
- Files to Create: `ShareReportFlowGateEnforcementTest.kt` (PII test created in Task 01).
- Files to Modify: none.
- Implementation Details: 6 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact states.
- Security: Both structural tests are critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test KDoc citing FR-10.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green, both structural tests CI-blocking.

## 30. Definition of Done
`ShareReportFlow` live, share-card API call structurally unreachable without a prior successful Parent Gate step-up, `ShareCardUiState` verified PII-free, offline block enforced, all tests green.

## 31. Final Verification Checklist
- [ ] Gate-enforcement test confirms the API call is never reachable without a prior successful `ParentGateLauncher` result in the same flow instance
- [ ] PII field-absence structural test confirms no `childId`/`dob`/`location`/`address` field in `ShareCardUiState`
- [ ] Offline block prevents both the gate call and the API call (Edge Case #9)
- [ ] Card preview renders only nickname/initial and badge
- [ ] Localization and RTL mirroring verified
