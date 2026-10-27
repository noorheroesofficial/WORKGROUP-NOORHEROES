# K-01 — Settings & Privacy Navigation Hub

## 1. Feature Context
Part of Feature C.26 — Privacy, Consent, Account Security & Data Rights (Settings). The entry shell every other C.26 sub-feature is reached through, from C.20's Parent Dashboard.

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**K-01 — Settings & Privacy Navigation Hub**

## 4. Objective
Build `SettingsScreen` and `PrivacySupportScreen` as lightweight navigation shells routing into every other C.26 KMP sub-feature, with zero business logic of their own.

## 5. Business Requirements
- §1.18 Screen Inventory #1–2: Settings (landing) and Privacy & Support (landing).
- §1.19: `settings_viewed`, `privacy_support_viewed` events.
- §2.3 Tab Structure: reached from the Parent Dashboard, not a standalone tab.

## 6. Existing Architecture
New module `:feature:parent-settings` (per PRD §6.1), depends on `:core:auth` (C.19), `:core:design-system`, `:core:network`, `:core:offline-cache`. Navigation composed via the platform's existing Compose Navigation graph (`CORE_NAVIGATION_INSTRUCTIONS.md`), entered from `:feature:parent-dashboard`'s (C.20) existing navigation graph.

## 7. Existing Code to Reuse
- `:core:design-system` — standard settings-list row components (reuse whatever list-item composable C.20/C.21 already use for their own settings-style rows, do not create a new one).
- C.20's Parent Dashboard navigation entry point.
- `ParentSettingsAnalytics` (new, but follows the exact per-feature analytics-wrapper convention established by `ChildManagementAnalytics`/equivalent in sibling features).

## 8. Files to Create
- `feature/parent-settings/src/commonMain/kotlin/.../SettingsScreen.kt`
- `feature/parent-settings/src/commonMain/kotlin/.../PrivacySupportScreen.kt`
- `feature/parent-settings/src/commonMain/kotlin/.../ParentSettingsNavGraph.kt`
- `feature/parent-settings/src/commonMain/kotlin/.../analytics/ParentSettingsAnalytics.kt`

## 9. Files to Modify
- `:feature:parent-dashboard`'s navigation graph — add the entry route into `:feature:parent-settings`.
- App-level nav graph registration (wherever feature graphs are composed together, per `CORE_NAVIGATION_INSTRUCTIONS.md`'s documented pattern).

## 10. Backend Requirements
None directly — this screen makes no network calls itself.

## 11. KMP Requirements
- `SettingsScreen` renders entry rows: Security, Consent Log, AI Interaction History, Language, Privacy & Support — each a simple `NavigationListItem` routing to the corresponding sub-feature's screen (K-02 through K-06).
- `PrivacySupportScreen` renders entry rows: Consent Log, AI Interaction History, Data Export, Account Deletion entry — a sub-section reachable both from `SettingsScreen` and directly from the Parent Dashboard.
- No ViewModel-level state beyond navigation — this is intentionally a static shell, not a data-driven screen.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
None — no network calls originate from this sub-feature.

## 14. Database Requirements
None.

## 15. Validation
None.

## 16. Authentication
Standard parent session required to reach Settings at all (inherited from the Parent Dashboard's own gating, not re-implemented here).

## 17. Authorization
None beyond standard parent-session access — individual sensitive actions are gated downstream in their own sub-features (K-02, K-04, K-06, K-07), not here.

## 18. Error Handling
None — a static navigation shell has no failure modes of its own.

## 19. Offline First
Fully available offline — pure navigation, no data dependency.

## 20. Local Data
None.

## 21. Localization
All row labels sourced via string resources (English, Hindi, Arabic, Urdu) — no hardcoded strings.

## 22. RTL
Full RTL mirroring of list rows and navigation icons.

## 23. Analytics
`settings_viewed`, `privacy_support_viewed` fired on screen composition via `ParentSettingsAnalytics`.

## 24. Performance
Trivial — static composable tree, no recomposition risk beyond standard navigation state.

## 25. Security
None beyond the inherited parent-session gate at the Dashboard entry point.

## 26. Library Requirements
No new libraries — standard Compose Navigation.

## 27. Testing
- UI test: `SettingsScreen` renders all 5 entry rows and each navigates to the correct destination.
- UI test: `PrivacySupportScreen` renders all 4 entry rows and each navigates correctly.
- Analytics test: `settings_viewed`/`privacy_support_viewed` fire exactly once per screen composition, not on every recomposition.

## 28. Documentation
KDoc noting this module is a pure navigation shell — any business logic added here in the future should instead live in the relevant sub-feature's own screen/ViewModel.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `:feature:parent-settings` Module Skeleton**
- **Objective:** Module scaffold with correct dependencies (`:core:auth`, `:core:design-system`, `:core:network`, `:core:offline-cache`).
- **Definition of Done:** Module builds, dependencies resolve, no circular dependency introduced.

**Task 02 — Build `SettingsScreen` and `PrivacySupportScreen`**
- **Files to Create:** both screen composables.
- **Definition of Done:** All entry rows render and route correctly (destinations may be placeholder routes until K-02–K-06 exist).

**Task 03 — Wire Navigation Graph & Dashboard Entry Point**
- **Files to Create:** `ParentSettingsNavGraph.kt`.
- **Files to Modify:** `:feature:parent-dashboard`'s nav graph.
- **Definition of Done:** Navigating from C.20's Dashboard reaches `SettingsScreen`.

**Task 04 — Implement `ParentSettingsAnalytics` and Wire Events**
- **Files to Create:** `analytics/ParentSettingsAnalytics.kt`.
- **Definition of Done:** Events fire once per composition, verified by test.

**Task 05 — Localization & RTL Pass**
- **Definition of Done:** All strings externalized; RTL layout verified in both screens.

**Task 06 — Full Test Suite**

## 30. Definition of Done
Both navigation shells are live, fully localized/RTL-correct, analytics-instrumented, and route correctly into every downstream C.26 sub-feature's screen.

## 31. Final Verification Checklist
- [ ] All entry rows present and correctly routed
- [ ] No business logic leaked into this shell module
- [ ] `settings_viewed`/`privacy_support_viewed` fire exactly once per view
- [ ] Full localization and RTL verified
- [ ] Reachable both from C.20 Dashboard and internally between Settings/Privacy & Support
