# K-04 — Account Security — Device Session Management

## 1. Feature Context
Part of Feature C.26. Surfaces C.19/C.23's existing device-session infrastructure within the Settings surface — this sub-feature builds zero new session/PIN logic of its own.

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**K-04 — Account Security — Device Session Management**

## 4. Objective
Render a Device List screen and PIN reset entry point within Settings, calling C.23 B-06's existing `GET /v1/sessions`/`DELETE /v1/sessions/{id}` and A.1/C.19's existing PIN reset screen — introducing no parallel session or PIN implementation.

## 5. Business Requirements
- FR-11: PIN reset and device revocation reuse C.19's exact mechanisms — no parallel implementation.
- Edge Case 5: a device revoked mid-in-flight-poll — in-flight read completes, subsequent requests from that device fail immediately (inherited from C.23 B-06's server-side behavior; this screen must not attempt to mask or retry around that failure incorrectly).
- §1.18 Screen Inventory #3–5: Security — PIN Reset (shared screen), Security — Device List, Device Revocation Confirmation.

## 6. Existing Architecture
Within `:feature:parent-settings`, this sub-feature's Device List screen is **new UI** (not present in C.19/C.23's own KMP modules per the reviewed blueprints) but calls **C.23 B-06's existing repository/API** (`GET /v1/sessions`, `DELETE /v1/sessions/{id}`, per C.23 K-06 §5 "device revocation calls `DELETE /v1/sessions/{id}` through `:core:auth`'s shared session repository, not a parallel client"). Confirm the exact existing repository class/location (likely in `:core:auth`, per C.23 K-06's own citation) before wiring — do not create a second `SessionRepository`.

## 7. Existing Code to Reuse
- `:core:auth`'s existing session repository (confirm exact class name against C.23 K-06's actual implementation before use).
- A.1/C.19's existing PIN Reset screen Composable — reused by navigation, not reimplemented.
- `ParentGateLauncher.requireParentAuth()` for step-up before revocation.

## 8. Files to Create
- `feature/parent-settings/src/commonMain/kotlin/.../DeviceListScreen.kt`
- `feature/parent-settings/src/commonMain/kotlin/.../DeviceRevocationConfirmationDialog.kt`
- `feature/parent-settings/src/commonMain/kotlin/.../SecuritySectionViewModel.kt`

## 9. Files to Modify
- `ParentSettingsNavGraph.kt` (K-01) — wire Device List route and the existing PIN Reset screen's route into this navigation graph (not a new PIN screen).

## 10. Backend Requirements
Consumes C.23 B-06's existing `GET /v1/sessions`/`DELETE /v1/sessions/{id}` and C.19 B-03's `POST /v1/auth/pin/verify` (via the existing PIN reset screen) exclusively — zero new backend endpoints from this sub-feature.

## 11. KMP Requirements
- `DeviceListScreen` sources data from the confirmed existing session repository — no new network client.
- Revoke action gated by `ParentGateLauncher.requireParentAuth()`, then calls the existing repository's revoke method.
- Handle Edge Case 5 by simply letting the existing repository's standard error handling surface a clear "session expired/revoked" state on the next request from a revoked device — do not add feature-local retry logic that could mask this expected behavior.
- "Reset PIN" entry navigates to A.1/C.19's existing PIN Reset screen — this sub-feature adds a navigation entry point only, zero PIN logic.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes C.19 B-03 and C.23 B-06's contracts exactly as documented in those blueprints.

## 14. Database Requirements
No local persistence beyond the existing session repository's own caching behavior (owned by `:core:auth`, not duplicated here).

## 15. Validation
None client-side beyond standard confirm-before-destructive-action UX for revocation.

## 16. Authentication
Parent session; revocation requires step-up (reused C.19 mechanism).

## 17. Authorization
Step-up gate before any revocation call.

## 18. Error Handling
Standard C.19/C.23 error handling reused verbatim — no separate error path introduced by this screen (per FR-11).

## 19. Offline First
Device list renders from last-cached state offline (via the existing session repository's own cache); revocation requires connectivity.

## 20. Local Data
Owned entirely by `:core:auth`'s existing session repository — this screen holds no independent local device-list cache.

## 21. Localization
Device names (user-facing labels, if any) and screen chrome fully localized.

## 22. RTL
Full RTL layout for the device list and confirmation dialog.

## 23. Analytics
`pin_reset_initiated`, `device_list_viewed`, `device_revoked` — cross-referenced with C.19/C.23's existing analytics wrappers, not a duplicate event source.

## 24. Performance
Trivial list rendering; no special performance concerns beyond what the existing session repository already handles.

## 25. Security
Zero new session/PIN logic — the entirety of this sub-feature's security posture is inherited from C.19/C.23's already-reviewed implementations; the only new risk surface is this screen's own navigation wiring, which introduces no new capability.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Integration test: `DeviceListScreen` correctly renders data from the confirmed existing repository (using that repository's own test fixtures, not new ones).
- Integration test: revocation calls the existing repository's revoke method, gated by step-up.
- Integration test: zero parallel session/PIN implementation exists anywhere in this sub-feature's files (a code-review-level check, backed by confirming imports point to `:core:auth`, not a local reimplementation).
- UI test: PIN Reset navigation entry correctly routes to the existing shared screen.

## 28. Documentation
KDoc explicitly stating this sub-feature adds UI only, zero new session/PIN business logic, and naming the exact existing repository/screen classes it depends on.

## 29. AI Coding Agent Implementation Steps

**Task 00 — Confirm Existing Session Repository Class/Location**
- **Objective:** Identify the exact class C.23 K-06 already uses before writing any new code against a guessed name.
- **Definition of Done:** Confirmed class name and package.

**Task 01 — `DeviceListScreen` Wired to Existing Repository**
- **Files to Create:** `DeviceListScreen.kt`.
- **Dependencies:** Task 00.

**Task 02 — Revocation Flow with Step-Up**
- **Files to Create:** `DeviceRevocationConfirmationDialog.kt`.
- **Definition of Done:** Revocation gated correctly, uses the existing repository's revoke method only.

**Task 03 — Wire PIN Reset Navigation Entry**
- **Files to Modify:** `ParentSettingsNavGraph.kt`.
- **Definition of Done:** Routes to A.1/C.19's existing screen, no new PIN screen created.

**Task 04 — Localization, RTL, Analytics**

**Task 05 — Full Test Suite**

## 30. Definition of Done
Device List and PIN Reset are both reachable from Settings, calling exclusively C.19/C.23's existing, already-reviewed session/PIN infrastructure — with zero new backend logic and zero parallel client implementation introduced.

## 31. Final Verification Checklist
- [ ] Existing session repository class confirmed before implementation, not guessed
- [ ] Zero new PIN logic — navigates to the existing shared screen only
- [ ] Revocation gated by step-up, uses existing repository's method only
- [ ] Edge Case 5 (mid-poll revocation) handled by existing error surfacing, no masking retry logic added
- [ ] Full localization and RTL verified
