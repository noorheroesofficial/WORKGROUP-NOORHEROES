# K-02 — Consent Log & Withdrawal Flow

## 1. Feature Context
Part of Feature C.26. Gives parents a genuine, individually-actionable view of every consent they gave — the client-side half of B-01's read/write veneer over A.1's consent ledger.

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**K-02 — Consent Log & Withdrawal Flow**

## 4. Objective
Render the 6-item Consent Log from B-01, enforce that required consents never expose an interactive withdraw control, and implement the `voice_ai` shared-state integration with C.23's AI Permissions module correctly — including surfacing B-01's documented family-vs-per-child scope conflict rather than presenting false confidence of sync.

## 5. Business Requirements
- FR-8: required consents render info-icon-only, routing to account-deletion explanation.
- FR-9: `voice_ai` withdrawal here and C.23's AI toggle reflect the same state (subject to B-01's flagged interim mitigation, not a guaranteed structural single-value share).
- Edge Case 1: re-grant flow.
- §2.2 Screen: Consent Log — per-consent row, required/optional tag, tap-through to full text.
- §6.10 Testing Strategy: UI test asserting no interactive withdraw control on required-consent rows.

## 6. Existing Architecture
Within `:feature:parent-settings`, consumes B-01's endpoints via a new `ConsentRepository`. The `voice_ai` toggle path must call the **same shared repository method** `:feature:parental-controls` (C.23) uses — confirm the exact existing method name/location in C.23's KMP module (likely `FamilySettingsRepository.updateAiSettings()`, per C.23's own documented convention) before wiring this, per rule 30; do not invent a second AI-settings write path.

## 7. Existing Code to Reuse
- `ParentGateLauncher.requireParentAuth(triggerContext = Settings)` (`:core:auth`, C.19) — step-up for withdrawal.
- `FamilySettingsRepository` (confirm exact class/method from C.23's `:feature:parental-controls` module) — shared AI-settings write path for `voice_ai`.
- `:core:design-system`'s status-pill/tag components (reused from C.19's "Required" label precedent style, or the design system's general tag component).

## 8. Files to Create
- `feature/parent-settings/src/commonMain/kotlin/.../ConsentLogScreen.kt`
- `feature/parent-settings/src/commonMain/kotlin/.../ConsentDetailScreen.kt`
- `feature/parent-settings/src/commonMain/kotlin/.../WithdrawConfirmationDialog.kt`
- `feature/parent-settings/src/commonMain/kotlin/.../RequiredConsentRedirectScreen.kt`
- `feature/parent-settings/src/commonMain/kotlin/.../ConsentLogViewModel.kt`
- `core-data/.../ConsentRepository.kt` (interface) + `ConsentRepositoryImpl.kt`

## 9. Files to Modify
- `ParentSettingsNavGraph.kt` (K-01) — wire the 4 new routes.

## 10. Backend Requirements
Consumes B-01 exclusively (`GET /v1/parent/consents`, `POST /v1/parent/consents/{id}/withdraw`).

## 11. KMP Requirements
- `ConsentLogScreen`: renders 6 rows from `ConsentRepository.getConsents()`; each row shows name, status pill, last-changed date, required/optional tag.
- Rows where `required == true` render **only** an info icon (tap → `RequiredConsentRedirectScreen`, which links into C.21's account-deletion flow) — **no withdraw/toggle control exists on these rows at all**, enforced by conditional composition, not a disabled-but-present control.
- Rows where `required == false` render a withdraw action, gated by `ParentGateLauncher.requireParentAuth()`.
- On successful `voice_ai` withdrawal: call the shared `FamilySettingsRepository` method (§6/§7) so C.23's AI Permissions screen reflects the change on next load — **do not** maintain a locally-cached duplicate of this value in `ConsentLogViewModel` beyond what's needed for this screen's own immediate re-render.
- Re-grant: same withdraw endpoint's inverse — toggling an already-withdrawn optional consent back on, per Edge Case 1.
- Explicitly surface (in a code comment and, if product agrees, a subtle UI note) that `voice_ai`'s family-level vs. per-child sync is an interim mitigation per B-01 §23 — do not silently assume perfect sync in tests or UI copy.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes B-01's contract as documented in that blueprint.

## 14. Database Requirements
No local persistence beyond standard short-lived in-memory ViewModel state and the existing offline-cache read-through for the list (per §19).

## 15. Validation
None client-side beyond disabling the withdraw button during an in-flight request (prevent double-submit).

## 16. Authentication
Parent session; withdrawal additionally requires step-up.

## 17. Authorization
Step-up gate before any withdraw call; required-consent rows have no authorization path to bypass since no control exists to trigger it.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Network failure on list load | Retry affordance, last-cached list shown if available |
| Withdrawal API failure | Inline error, row state unchanged, no optimistic update reverted awkwardly |
| Step-up cancelled | Return to Consent Log, no withdrawal attempted |
| `404 UNKNOWN_CONSENT_ID` (should be unreachable from UI) | Logged as a client bug, generic error shown |

## 19. Offline First
List renders from last-cached response offline; withdrawal/re-grant require connectivity, clearly indicated if attempted offline.

## 20. Local Data
Cached consent list in `:core:offline-cache`, invalidated on successful withdrawal/re-grant.

## 21. Localization
Consent names, status labels, required/optional tags, and full consent text (linked from Consent Detail) all sourced via string resources / the existing legal-content localization system — never hardcoded.

## 22. RTL
Full RTL layout for rows, tags, and the detail screen; required/optional tag position mirrors correctly.

## 23. Analytics
`consent_log_viewed`, `consent_detail_viewed`, `consent_withdrawn` (with `consent_type`), `consent_regranted`, `required_consent_withdrawal_attempt_redirected`.

## 24. Performance
Lightweight list (6 items, fixed) — no pagination or lazy-loading complexity needed; stable state to avoid unnecessary recomposition on unrelated ViewModel updates.

## 25. Security
- **Signature UI test:** a required-consent row never renders any interactive withdraw/toggle control, only the info icon — this is the client-side enforcement of FR-8, mirrored from B-01's server-side rejection.
- Step-up required before any withdrawal call reaches B-01.

## 26. Library Requirements
No new libraries — Hilt, Retrofit+OkHttp (via `:core:network`), Compose.

## 27. Testing
- **Highest-priority UI test:** required-consent rows render zero interactive withdraw controls (only info icon) — grep/composition-tree assertion, not just a visual check.
- Integration test: withdraw an optional consent, confirm row updates to "Withdrawn" status.
- Integration test: `voice_ai` withdrawal reflected in a mocked/fixture `FamilySettingsRepository` shared with C.23's module — confirm the shared-call-site claim, and confirm the test also documents the family-vs-per-child scope caveat rather than asserting perfect symmetry it cannot guarantee.
- Integration test: re-grant flow (Edge Case 1).
- UI test: step-up cancellation returns to Consent Log with no state change.
- Offline test: list renders from cache; withdraw action disabled/clearly blocked offline.

## 28. Documentation
KDoc on `ConsentLogViewModel` cross-referencing B-01's flagged `voice_ai` scope conflict explicitly, so a future maintainer doesn't assume the sync guarantee is airtight.

## 29. AI Coding Agent Implementation Steps

**Task 01 — `ConsentRepository`**
- **Files to Create:** interface + impl, wrapping B-01's two endpoints.
- **Definition of Done:** Repository has no business logic beyond network mapping.

**Task 02 — `ConsentLogScreen` with Required/Optional Conditional Rendering**
- **Files to Create:** `ConsentLogScreen.kt`.
- **Tests:** the highest-priority signature UI test from §27.
- **Definition of Done:** Zero interactive controls on required rows, verified by test.

**Task 03 — Withdraw/Re-grant Flow with Step-Up**
- **Files to Create:** `WithdrawConfirmationDialog.kt`, ViewModel logic.
- **Dependencies:** Task 01, 02.

**Task 04 — Shared `voice_ai` Repository Integration**
- **Objective:** Confirm and call C.23's actual shared repository method.
- **Definition of Done:** Integration test confirms the call site is shared, not a local duplicate write.

**Task 05 — Required-Consent Redirect Screen**
- **Files to Create:** `RequiredConsentRedirectScreen.kt`, linking to C.21.

**Task 06 — Localization, RTL, Analytics, Offline Caching**

**Task 07 — Full Test Suite**

## 30. Definition of Done
Consent Log is fully functional, required-consent rows are structurally incapable of exposing a withdraw control, `voice_ai` correctly integrates with C.23's shared repository method (with its known scope caveat documented, not hidden), and the full withdraw/re-grant/redirect flows are tested end to end.

## 31. Final Verification Checklist
- [ ] Required-consent rows render zero interactive controls (signature test passes)
- [ ] Withdraw/re-grant flows both tested end to end
- [ ] `voice_ai` shared-repository call confirmed against C.23's actual implementation, not guessed
- [ ] Family-vs-per-child scope caveat documented in code, not silently assumed resolved
- [ ] Full localization and RTL verified
- [ ] Offline list-cache and connectivity-required mutation states verified
