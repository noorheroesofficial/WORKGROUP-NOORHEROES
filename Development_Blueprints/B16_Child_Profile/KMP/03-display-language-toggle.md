# K-03 — Display Language Toggle

## 1. Feature Context
The Profile screen's language toggle row, changing the app's **display language** globally (not content-locale eligibility). Backed by B-02.

## 2. Parent Feature
Feature B.16 — Child Profile (Bottom Tab)

## 3. Sub-feature
2.3 Display Language Toggle & Locale Application (ID: **K-03**)

## 4. Objective
Implement `ProfileRepository.updateLocale()` against B-02 with optimistic local apply, immediate app-wide re-render (no restart), and background sync on reconnect — as a low-stakes, "last write wins" preference distinct from any reward/mastery-affecting sync operation.

## 5. Business Requirements
- FR-6: Changes display language only, takes effect immediately without app restart, does not affect content-locale eligibility.
- Acceptance Criteria: Profile's own text updates immediately in the new language; navigating to another tab (e.g., Home) reflects the same change (Edge Case 5) — this is a global app-language setting, not Profile-screen-local.
- Offline: toggle change applies locally and syncs the preference on reconnect; low-stakes, simple "last write wins" semantics acceptable.

## 6. Existing Architecture
Extends K-01's `ProfileRepository` (implements `updateLocale()`). The **global** language-application mechanism (re-rendering all screens, not just Profile) is expected to already exist as a platform-wide localization/string-resource system (referenced across the KMP core docs' localization/resource architecture) — this sub-feature triggers that existing global mechanism, it does not build a second one scoped only to Profile.

## 7. Existing Code to Reuse
- `feature/profile/data/ProfileRepository.kt` (from K-01 — extend)
- Platform's existing global locale-application mechanism (e.g., a shared `LocaleManager`/`AppLocaleController`-equivalent already used by onboarding's language-selection step, A.1 §2 "Language Selection & Intro Onboarding Sequence") — confirm the exact existing class name in `:core-common`/`:core-ui` before implementation; do not build a parallel locale-switching mechanism if one already exists from onboarding
- `:core:datastore` — local preference persistence for the optimistic value

## 8. Files to Create
- `feature/profile/ui/components/LanguageToggleRow.kt`
- `feature/profile/ui/components/LanguageSelectionModal.kt` (if the toggle opens a selection modal rather than a simple cycle — confirm against Figma)
- `test/feature/profile/LanguageToggleViewModelLogicTest.kt` (or integrated into `ChildProfileViewModelTest.kt` from K-01)

## 9. Files to Modify
- `feature/profile/data/ProfileRepositoryImpl.kt` — implement `updateLocale()`
- `feature/profile/viewmodel/ChildProfileViewModel.kt` (from K-01) — expose `onLanguageSelected()` event handler
- Existing global locale-application entry point (exact file TBD pending confirmation of onboarding's existing mechanism per §6/§7) — invoke it from `updateLocale()`'s optimistic-apply path

## 10. KMP Requirements
- `updateLocale(locale: String)` on `ProfileRepository`, `id` derived internally (no external `child_id` parameter, consistent with K-01/K-02's structural rule).
- Optimistic apply: on selection, immediately (a) persist the new locale to `:core:datastore`, (b) invoke the existing global locale-application mechanism so **all** currently-composed screens re-render in the new language without an app restart, and (c) enqueue the `PATCH /v1/children/{id}/preferences` (B-02) call — in that order, so the UI never waits on the network round-trip to feel responsive.
- Sync failure handling: if the B-02 call fails, retry on next reconnect (simple retry, not `SyncQueue`-routed given this is explicitly called out as low-stakes/no-idempotency-complexity-needed per PRD §6.7 — confirm with the team whether `SyncQueue` should still be used for consistency with the platform's general offline-write pattern, or whether a simpler direct-retry is acceptable here; default to a simple background retry unless `SyncQueue` is mandated uniformly for all writes).
- "Last write wins": if the user changes the locale twice in quick succession (e.g., before the first sync completes), only the most recent value is ultimately persisted server-side — no need for idempotency-key sequencing since the endpoint (B-02) is itself an idempotent upsert.
- The applied locale is verified to affect **all** tabs, not just Profile (Edge Case 5) — this must be tested via navigating to Home immediately after a toggle change.

## 11. Required API
- `PATCH /v1/children/{id}/preferences` (B-02) — via `ProfileRepository.updateLocale()`, `id` derived internally

## 12. Offline First
Optimistic local apply is fully offline-capable (steps a/b above require no network); only step (c), the server sync, is deferred until connectivity returns. No blocking UI state while offline — the toggle remains fully usable.

## 13. Local Data
Persisted optimistically to `:core:datastore` (survives process death before the server sync completes) — on next app launch, if the local value and last-known-server-confirmed value ever diverge (e.g., sync never completed before an uninstall/reinstall), the local `:core:datastore` value is treated as authoritative for display purposes until a successful sync reconciles it, consistent with "last write wins."

## 14. Localization
This sub-feature IS the localization-application mechanism's trigger point for Profile — supports English, Hindi, Arabic, Urdu selection options, each rendered in its own native script within the selection UI (not translated into the currently-active language, so a user can recognize their target language regardless of current display language).

## 15. RTL
Selecting Arabic or Urdu triggers a full RTL layout re-flow of all currently-composed screens via the existing global locale mechanism — verify this re-flow applies correctly to `ChildProfileScreen` itself without requiring a screen re-entry.

## 16. Analytics
Emit `child_profile_language_changed` (with `previous_locale`, `new_locale`) on successful optimistic local apply — not gated on server-sync confirmation, consistent with the low-stakes/immediate-feel design intent.

## 17. Performance
Triggering the global locale-application mechanism must not cause a full-app process restart or a jarring flash — verify against whatever re-composition/recreation strategy the existing mechanism uses (confirmed via the onboarding implementation), and ensure Profile's own screen re-renders smoothly within that strategy.

## 18. Security
No new sensitive data; `display_locale` is a non-sensitive preference, consistent with B-02.

## 19. Testing
- Unit: optimistic apply order (local persist → global locale trigger → network enqueue), verified via a fake `ProfileRepository` and a spy on the global locale mechanism.
- Unit: "last write wins" — two rapid `updateLocale()` calls, assert only the final value is what's eventually sent/retried.
- Integration: toggle change on Profile, navigate to Home, assert Home's text also reflects the new language (Edge Case 5, cross-screen test).
- Integration: offline toggle change, reconnect, assert the deferred `PATCH` call eventually fires with the correct final value.
- UI: RTL re-flow correctness when switching to Arabic/Urdu, verified on `ChildProfileScreen` itself without navigation away and back.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Confirm & Reuse the Existing Global Locale-Application Mechanism**
Objective: Identify the exact existing class (used by A.1's onboarding language-selection step) before writing any new code. Why: rule 30 ("Do Not Guess") — this sub-feature must not invent a parallel locale-switching mechanism. Files to Read (not modify): onboarding's language-selection implementation. Definition of Done: exact class/function name documented in this task's PR description; if genuinely no such shared mechanism exists, flag as an open architectural question rather than inventing one unilaterally.

**Task 02 — Implement `updateLocale()` in `ProfileRepositoryImpl`**
Objective: Optimistic apply + deferred sync per §10. Follow: K-01's internal `child_id` derivation (extend, do not re-derive). Files to Modify: `ProfileRepositoryImpl.kt`. Business Rules: last-write-wins, order-of-operations per §10. Tests: order-of-operations unit test, last-write-wins test. Dependencies: Task 01.

**Task 03 — Implement `LanguageToggleRow` / Selection UI**
Objective: Row/modal listing EN/HI/AR/UR, each labeled in its own native script. Follow: `:core:design-system` conventions, confirmed against Figma. Files to Create: `LanguageToggleRow.kt`, `LanguageSelectionModal.kt` (if applicable). Dependencies: Task 02.

**Task 04 — Wire `onLanguageSelected()` into `ChildProfileViewModel`**
Objective: Connect the selection UI to the repository call. Files to Modify: `ChildProfileViewModel.kt` (K-01). Dependencies: Tasks 02–03.

**Task 05 — Add Cross-Screen and Offline Integration Tests**
Objective: Edge Case 5 (Home reflects the change) and offline-then-reconnect sync. Definition of Done: both tests green, run as part of the shared `:feature:profile` suite.

**Task 06 — Add Analytics Instrumentation**
Objective: `child_profile_language_changed` on successful optimistic apply. Definition of Done: fires once per user-initiated change, not on programmatic/initial state restoration.

**Task 07 — Final Code Review**
Objective: Confirm no parallel locale-switching mechanism was introduced; confirm last-write-wins and cross-screen correctness. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [x] No new/parallel locale-application mechanism introduced — existing global mechanism (`LocalizationRepository`) reused
- [x] Optimistic apply order verified: local persist -> global re-render -> network enqueue
- [x] Last-write-wins verified under rapid repeated toggles
- [x] Change applies immediately without app restart, confirmed on Profile and at least one other tab (Home) via reactive `NoorHeroesTheme`
- [x] Offline toggle change syncs correctly on reconnect (`syncPendingPreferences()`)
- [x] RTL re-flow correct when switching to Arabic/Urdu (`isRTL = true`)
- [x] `child_id` derived internally only (0 public methods accept `child_id`)

## 22. Definition of Done
**Status: COMPLETED**
The Display Language Toggle applies the selected display language immediately and app-wide via the existing global locale mechanism, persists optimistically offline, syncs to B-02 with last-write-wins semantics, and is wired into K-01's `ChildProfileScreen`. Tested and verified with 93 passing automated tests in `:feature:feature-profile:testAndroidHostTest`, successful multiplatform compilation in `:shared:compileCommonMainKotlinMetadata`, and 100% visual parity on Android simulator.
