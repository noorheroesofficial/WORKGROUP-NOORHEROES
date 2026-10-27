# K-10 — Ramadan Mode Checklist Variant & Ethical Messaging Safeguards

## 1. Feature Context
NoorHeroes KMP app. Seasonal checklist variant plus the two core empty states establishing the feature's warm, non-alarming first-touch experience.

## 2. Parent Feature
A.7 Habit Tracker — KMP App (Android/iOS)

## 3. Sub-feature
K-10 Ramadan Mode Checklist Variant & Ethical Messaging Safeguards

## 4. Objective
Render the Ramadan Mode Checklist Variant when seasonal mode is active, plus the "No Habits Configured" and "No Streak History" empty states, with correct reversion when Ramadan ends without streak discontinuity (FR-18, Edge Case 9).

## 5. Business Requirements
- When Ramadan mode is active, checklist reflects fasting, charity, Quran, dua, and family iftar reflection habits (FR-18).
- Reverts to standard checklist post-Ramadan without streak discontinuity purely from the seasonal switch (Edge Case 9).
- Empty state (zero habits): friendly "ask a grown-up" prompt with parent deep link.
- Empty state (zero streak history): warm "Let's start your first day!" framing, never a stark "0".

## 6. Existing Architecture
Extends `feature-habits` (K-01). Ramadan-mode status sourced from the existing F.36 Ramadan Mode feature's shared state/service — reuse F.36's existing seasonal-mode detection mechanism rather than re-implementing date-based Ramadan detection in this feature.

## 7. Existing Code to Reuse
- F.36 Ramadan Mode's shared seasonal-state provider (exact class/service TBD — verify against F.36's KMP implementation before coding; do not re-derive Ramadan dates independently)
- `HabitChecklistUiState` (K-01), extended with a Ramadan-variant rendering path

## 8. Files to Create
- `feature-habits/src/commonMain/kotlin/.../checklist/RamadanChecklistVariant.kt`
- `feature-habits/src/commonMain/kotlin/.../checklist/HabitEmptyStates.kt` (zero-habits, zero-streak-history)
- `feature-habits/src/commonTest/kotlin/.../RamadanModeTransitionTest.kt`

## 9. Files to Modify
- `HabitBuilderScreen.kt` (K-01) — branch to `RamadanChecklistVariant` based on `ramadan_mode_active` flag from B-01
- `HabitChecklistViewModel.kt` (K-01) — subscribe to F.36's seasonal-state provider

## 10. Backend Requirements
Consumes `ramadan_mode_active` flag from `GET /v1/habits` (B-01).

## 11. KMP Requirements
- Ramadan checklist variant swaps in seasonal habit rows without discarding the underlying streak state.
- Reversion to standard checklist post-Ramadan is a pure UI/data-source swap, not a streak reset.
- Empty states per §5, both using warm, non-stark framing consistent with the feature's anti-shaming design language.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`GET /v1/habits` (B-01) `ramadan_mode_active` flag.

## 14. Database Requirements (Local)
None beyond the existing catalog cache (K-01), which already includes the flag.

## 15. Validation
Test simulating Ramadan-mode activation mid-cycle with an active non-Ramadan streak, asserting no streak discontinuity occurs purely from the mode switch (Edge Case 9, mirrors B-03's server-side guarantee).

## 16. Authentication
N/A (UI-layer rendering only).

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Ramadan-mode state fails to load | Default to standard checklist, not a blocked/error state |
| Zero habits configured | Friendly setup-prompt empty state with parent deep link |
| Zero streak history | "Let's start your first day!" framing, never a bare "0" |

## 19. Offline First
Ramadan-mode flag cached alongside the habit catalog (K-01); works offline from last-known state.

## 20. Local Data
Shared with K-01's catalog cache; no additional local storage required.

## 21. Localization
Ramadan-specific habit labels and empty-state copy fully localized, culturally reviewed per PRD NFR Localization requirement (mercy/encouragement language must land appropriately across cultures, not just literal translation).

## 22. RTL
Ramadan checklist variant and empty-state illustrations verified for RTL.

## 23. Analytics
`ramadan_mode_checklist_activated`, `ramadan_mode_checklist_deactivated` via `AnalyticsTracker`.

## 24. Performance
Seasonal-mode check is a lightweight state read, no additional network round-trip beyond the existing catalog fetch.

## 25. Security
No elevated risk.

## 26. Library Requirements
Compose Multiplatform, Koin.

## 27. Testing
- Unit: Ramadan-transition no-discontinuity test (mandatory, mirrors Edge Case 9).
- UI: both empty states render with correct warm framing.
- Unit: reversion post-Ramadan correctly restores standard checklist.

## 28. Documentation
KDoc noting the Ramadan-mode swap must never trigger a streak reset — a pure content-source change only.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Integrate F.36 Seasonal-State Provider**
- Objective: Subscribe to existing Ramadan-mode detection rather than re-deriving it.
- Files to Modify: `HabitChecklistViewModel.kt`
- Existing Files to Reuse: F.36's shared seasonal-state provider (verify exact API before implementation).
- Definition of Done: checklist correctly reflects live Ramadan-mode state.

**Task 02 — Build Ramadan Checklist Variant**
- Files to Create: `RamadanChecklistVariant.kt`
- Business Rules: FR-18.
- Tests: mandatory no-discontinuity transition test.
- Definition of Done: variant renders correctly and reverts cleanly post-Ramadan.

**Task 03 — Build Empty States**
- Files to Create: `HabitEmptyStates.kt`
- Business Rules: warm, non-stark framing per §5.
- Tests: UI tests for both states.
- Definition of Done: both empty states render correctly with parent deep link (zero-habits case).

**Task 04 — Wire into Habit Builder**
- Files to Modify: `HabitBuilderScreen.kt`
- Definition of Done: correct branching based on `ramadan_mode_active` and habit/streak-history presence.

**Task 05 — Final Code Review**
- Do Not Change: F.36's underlying Ramadan-date-detection logic (only consume it).
- Expected Result: PR merge-ready.

## 30. Definition of Done
Ramadan checklist variant and both empty states live, with verified no-streak-discontinuity behavior across the seasonal transition.

## 31. Final Verification Checklist
- [ ] Ramadan-mode activation/deactivation causes no streak discontinuity (mandatory test)
- [ ] Ramadan checklist correctly reflects seasonal habit set
- [ ] Zero-habits empty state includes parent deep link
- [ ] Zero-streak-history empty state uses warm framing, never a bare "0"
- [ ] F.36's existing seasonal-state provider reused, not re-derived
- [ ] Localization and RTL verified
- [ ] Analytics events wired
