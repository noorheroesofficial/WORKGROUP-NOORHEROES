# K-07 — Parent Download Cap & Policy Configuration Screen

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). Screen Inventory item #13 in the B.15 PRD's own "Complete — Zero Missing" table: the Parent Area screen where a parent sets/updates their child's per-download cap and downloads-enabled/disabled flag — the human control surface for the policy B-03 enforces server-side. The underlying storage/write API is owned by C.23 (Parental Controls), per B.15's explicit "Depends on: C.23" relationship; this blueprint owns only the B.15-specific screen and its read-side context (current usage), not a new backend endpoint.

## 2. Parent Feature
B.15 — Offline Downloads & Sync (cap/policy write ownership: C.23 — Parental Controls)

## 3. Sub-feature
K-07 — Parent Download Cap & Policy Configuration Screen

## 4. Objective
Build the Parent Area screen for setting a child's download cap and downloads-enabled/disabled toggle, showing current storage usage for context, delegating the actual write to C.23's existing parental-controls API, and reflecting FR-3/Edge Case 4/Edge Case 11's non-destructive, next-download-only enforcement semantics in the UI copy.

## 5. Business Requirements
- §1.18 Screen Inventory #13: Parent Download Cap/Policy Configuration — Screen (Parent Area), entry point "Parent Controls," exit "Saves configuration."
- FR-3: per-child download cap set by parent; exceeding it blocks new downloads with a clear message (enforced by B-01/B-03; this screen is where the parent sets the value).
- Acceptance Criteria §1.9: given a parent changes a download cap, the change is reflected the next time the child attempts a new download — never retroactive to an in-flight or already-issued manifest.
- Edge Case 4: a parent reducing the cap below current usage does not forcibly delete existing downloads — only blocks new ones until usage drops under the new cap; this screen's copy must not imply existing downloads will be removed.
- Edge Case 11: parental controls disabling downloads entirely is a distinct control from the cap — existing downloads remain playable, only new attempts blocked; this screen exposes both controls independently, never conflated into one toggle.
- §1.19 Events: `parent_download_cap_configured`.

## 6. Existing Architecture
New screen within the existing Parent Area / Parental Controls navigation flow (C.23's screen shell), added as a B.15-specific settings section rather than a standalone new parent-area entry point — consistent with C.23's existing per-child settings pattern (per C.21 Multi-Child Management's established per-child settings screen convention). The mutating API call is **not** built here: this screen calls C.23's existing parent-facing download-policy endpoint (owned and specified by C.23's own blueprint set) — this blueprint treats that endpoint as an existing dependency, per Rule 30 ("do not invent API endpoints"); if C.23's blueprint for this endpoint has not yet been generated, Task 03 below is blocked pending it (see §9 Dependencies).

## 7. Existing Code to Reuse
- C.23's existing per-child settings screen shell/navigation (Parent Controls entry point).
- C.23's parent-facing download-cap/policy repository (read/write) — **reused, not reimplemented** in this blueprint.
- B-02's `GET /v1/children/{id}/downloads` (`storage_used_bytes`) — reused here purely for display context, via K-03's existing `DownloadRepository.getDownloads()`, so the parent sees current usage while setting a new cap.
- `core-designsystem`'s existing form/slider/toggle components (reuse, not reinvent) — same primitives used by other Parent Area settings screens (e.g., C.23's other policy toggles).
- `useElevatedSession`-equivalent parent-PIN/biometric gate (C.19) already guarding entry into the Parent Area, inherited by this screen without re-implementation.

## 8. Files to Create
- `feature-parental-controls/src/commonMain/kotlin/.../downloads/DownloadCapConfigScreen.kt`.
- `feature-parental-controls/src/commonMain/kotlin/.../downloads/DownloadCapConfigViewModel.kt`.
- `feature-parental-controls/src/commonMain/kotlin/.../downloads/components/CapSliderInput.kt`.
- `feature-parental-controls/src/commonMain/kotlin/.../downloads/components/DownloadsEnabledToggle.kt`.
- `feature-parental-controls/src/commonMain/kotlin/.../downloads/components/CurrentUsageContextCard.kt`.
- `feature-parental-controls/src/commonTest/kotlin/.../DownloadCapConfigViewModelTest.kt`.
- `feature-parental-controls/src/commonTest/kotlin/.../CapVsDisabledIndependentTogglesTest.kt`.

## 9. Files to Modify
- C.23's Parent Controls settings list/navigation — add a "Downloads" entry routing to `DownloadCapConfigScreen`.
- **Dependency note:** if C.23's blueprint for the parent-facing download-cap/policy write endpoint has not yet been generated/implemented, this screen's save action (Task 03) is blocked on it — call `Generate: <C.23 sub-feature ID>` first if that endpoint doesn't yet exist in code.

## 10. Backend Requirements
Consumes C.23's existing parent-facing download-policy endpoint (read current cap/disabled-flag, write updates) — **not defined by this blueprint**; also reads B-02's `GET /v1/children/{id}/downloads` for the current-usage display context.

## 11. KMP Requirements
- `DownloadCapConfigScreen`: per-child settings screen reached via Parent Controls → Downloads.
- `CapSliderInput`: sets the per-child cap (e.g., in GB increments), pre-filled with the current value; on change, shows a live preview of the new cap against `CurrentUsageContextCard`'s displayed usage.
- `DownloadsEnabledToggle`: independent on/off control for "allow downloads for this child at all" — rendered and behaves as a **separate** control from the cap slider, never combined into one widget (Edge Case 11).
- `CurrentUsageContextCard`: read-only display of the child's current `storage_used_bytes` (from B-02, reused via K-03's repository), giving the parent context while adjusting the cap.
- Explicit, persistent UI copy near the cap slider: "Lowering this won't delete anything already downloaded — it just stops new downloads until usage drops below the new limit," directly reflecting Edge Case 4's non-destructive guarantee.
- Explicit UI copy near the disabled toggle: "Turning this off stops new downloads. Anything already downloaded stays available unless you remove it from the Downloads tab," reflecting Edge Case 11's distinction from a full revoke.
- Save action calls C.23's existing update endpoint with the new cap/flag values; on success, shows a confirmation and the change is understood to apply on the child's *next* download attempt (Acceptance Criteria), not retroactively to any in-flight download.
- Multi-child: this screen is entered per-child (from C.21's existing per-child settings navigation), never a single global cap across all children.
- Loading/empty/error states consistent with other Parent Area settings screens.

## 12. NextJS Requirements
N/A — this is the in-app Parent Area screen; the equivalent admin-side control (plan-level defaults, not per-child) is N-03.

## 13. API Contract
**Reused (not defined here):** C.23's parent-facing download-cap/policy read/write endpoint — exact contract (method, path, request/response shape) to be taken from C.23's own blueprint/API contract when generated; this blueprint does not invent one.
**Reused:** `GET /v1/children/{id}/downloads` (B-02 §13) for `storage_used_bytes` display context only.

## 14. Database Requirements
N/A directly — the parent-cap/disabled-flag table is owned and migrated by C.23, not this blueprint.

## 15. Validation
- Cap slider bounded to a sane min/max range (mirroring whatever server-side bound C.23's endpoint enforces — this screen's client-side bound is a UX guard, not the authoritative limit).
- No validation blocks setting a cap below current usage (Edge Case 4 explicitly permits this) — the UI instead shows the non-destructive-guarantee copy rather than rejecting the input.

## 16. Authentication
Inherits the Parent Area's existing parent-session + elevated-PIN/biometric gate (C.19) — no additional authentication logic introduced by this screen.

## 17. Authorization
Inherits C.23's existing parent-owns-this-child authorization check on the underlying endpoint; this screen adds no independent authorization logic.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Save fails (network/server error) | Standard retriable error state, cap/toggle values not silently reverted without explanation |
| Current-usage fetch fails | `CurrentUsageContextCard` shows a graceful "usage unavailable" fallback rather than blocking the cap-setting controls entirely |
| Cap set below current usage | Not an error — informational copy shown (Edge Case 4), save proceeds normally |

## 19. Offline First
This screen requires connectivity to save changes (delegates to C.23's endpoint); the current-usage context card may render a locally-cached last-known value (from K-03's local `DownloadEntity` sum) when offline, clearly labeled as potentially stale.

## 20. Local Data
Reads K-02/K-03's local `DownloadEntity` sum as a fallback usage figure when the live B-02 fetch is unavailable.

## 21. Localization
All copy (slider labels, toggle labels, the non-destructive-guarantee explanatory text, the disabled-vs-revoke distinction text) localized (English/Hindi/Arabic/Urdu), no hardcoded strings.

## 22. RTL
Slider direction, toggle placement, and card layout mirror correctly per `core-designsystem` RTL convention.

## 23. Analytics
`parent_download_cap_configured` (per §1.19), fired on successful save with the new cap value and disabled-flag state.

## 24. Performance
Lightweight settings screen; current-usage fetch reuses K-03's already-cached data path where possible rather than issuing a redundant network call on every screen open.

## 25. Security
No new security surface — this screen is a UI layer over C.23's already-authorized parent-session-gated endpoint; enforcement of the cap itself remains entirely server-side (B-01/B-03), consistent with the platform-wide principle that client-side settings screens are never themselves the enforcement boundary.

## 26. Library Requirements
Jetpack Compose, Koin. No new libraries.

## 27. Testing
- Unit: cap slider and disabled toggle behave as fully independent controls — changing one never implicitly changes the other (Edge Case 11, dedicated test).
- Unit: setting a cap below current usage does not block save and shows the correct non-destructive-guarantee copy (Edge Case 4).
- UI test: current-usage context card gracefully falls back to a cached/unavailable state without blocking the cap controls.
- UI test: save confirmation copy does not imply retroactive effect on in-flight downloads.

## 28. Documentation
KDoc explicitly noting this screen delegates its write action to C.23's existing endpoint and does not own the underlying policy storage — cross-referenced to B-03 §5 (the server-side enforcement this screen's values feed into) and to C.23's blueprint for the actual endpoint contract.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Confirm C.23 Dependency Availability**
Objective: verify C.23's parent-facing download-cap/policy endpoint exists (implemented or at least blueprinted); if not, this task blocks further implementation pending `Generate`/`Execute` on that C.23 sub-feature.
Expected result: confirmed endpoint contract (method, path, request/response) to build against.

**Task 02 — Build CapSliderInput & DownloadsEnabledToggle Components**
Files to create: `CapSliderInput.kt`, `DownloadsEnabledToggle.kt`.
Business rules: two fully independent controls, never combined.

**Task 03 — Build CurrentUsageContextCard**
Objective: reuse K-03's `DownloadRepository.getDownloads()`/local `DownloadEntity` sum for the usage display.
Files to create: `CurrentUsageContextCard.kt`.

**Task 04 — Implement DownloadCapConfigViewModel**
Objective: load current cap/flag (from C.23's endpoint), local-edit state, save action calling C.23's update endpoint.
Files to create: `DownloadCapConfigViewModel.kt`.

**Task 05 — Assemble DownloadCapConfigScreen & Wire Navigation**
Files to create: `DownloadCapConfigScreen.kt`.
Files to modify: C.23's Parent Controls settings navigation.

**Task 06 — Add Independent-Controls & Non-Destructive-Copy Tests (highest priority)**
Tests: `CapVsDisabledIndependentTogglesTest.kt`, plus cap-below-usage test in `DownloadCapConfigViewModelTest.kt`.

**Task 07 — Wire Analytics & Final Review**
Objective: confirm no duplicate/parallel write path to the cap/policy data was introduced (single source of truth remains C.23's endpoint).

## 30. Definition of Done
- Screen live within Parent Controls → Downloads, per-child.
- Cap and disabled-toggle confirmed fully independent controls.
- Non-destructive/next-download-only semantics correctly communicated in UI copy.
- Current-usage context displayed with graceful fallback.

## 31. Final Verification Checklist
- [ ] Cap slider and disabled toggle are independent — verified by test.
- [ ] Setting cap below current usage does not block save or imply deletion.
- [ ] Save confirmation copy does not imply retroactive effect on in-flight downloads.
- [ ] No duplicate write path introduced — C.23's endpoint remains the single source of truth.
- [ ] Current-usage display gracefully handles fetch failure/offline.
- [ ] Localization and RTL verified, no hardcoded strings.
