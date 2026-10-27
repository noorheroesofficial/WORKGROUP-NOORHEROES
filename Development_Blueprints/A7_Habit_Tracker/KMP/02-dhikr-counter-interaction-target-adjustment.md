# K-02 — Dhikr Counter Interaction & Target Adjustment

## 1. Feature Context
NoorHeroes KMP app. Distinct, meditative tap-counter interaction for the Dhikr habit type, with mid-day target adjustment.

## 2. Parent Feature
A.7 Habit Tracker — KMP App (Android/iOS)

## 3. Sub-feature
K-02 Dhikr Counter Interaction & Target Adjustment

## 4. Objective
Build the Dhikr Counter screen with a large tap target, gentle haptic pulse, batched/throttled submission, audio pronunciation support, and proportional target-change recalculation (Edge Case 6).

## 5. Business Requirements
- Large tap-target (≥72dp), gentle haptic pulse where platform supports it, meditative not game-like interaction (PRD §2.1).
- Non-gesture accessibility alternative (decrement/reset reachable via standard navigation).
- Batch/throttle count submission — not a network call per tap (PRD §2.3 click-mapping table).
- Audio pronunciation support with graceful silent fallback if the asset fails to load.
- Target change mid-day preserves progress proportionally, capping at new target if smaller (Edge Case 6).

## 6. Existing Architecture
Extends `feature-habits`/`feature-habits-domain` (K-01). Uses `core-network` Ktor client, `core-database` Room for local progress persistence, Koin DI, `core-navigation` for entry from Habit Builder.

## 7. Existing Code to Reuse
- `HabitRepository` (K-01, extended with Dhikr-specific methods)
- `core-design-system` haptic/tactile interaction tokens if present, otherwise platform-native haptic APIs behind a `core-common` `expect/actual` abstraction

## 8. Files to Create
- `feature-habits/src/commonMain/kotlin/.../dhikr/DhikrCounterScreen.kt`
- `feature-habits/src/commonMain/kotlin/.../dhikr/DhikrCounterViewModel.kt`
- `feature-habits/src/commonMain/kotlin/.../dhikr/DhikrCounterUiState.kt`
- `feature-habits-domain/src/commonMain/kotlin/.../AdjustDhikrTargetUseCase.kt`
- `feature-habits/src/commonTest/kotlin/.../DhikrTargetRecalculationTest.kt`

## 9. Files to Modify
- `HabitBuilderScreen.kt` (K-01) — render Dhikr as a visually distinct larger card, not a standard checklist row

## 10. Backend Requirements
Consumes `POST /v1/habits/check-ins` (B-02, batched) and `PATCH /v1/habits/{habit_id}/target` (B-05).

## 11. KMP Requirements
- Large circular tap button with count display, haptic pulse per tap.
- Local count accumulation; batched submission to backend (throttled, not per-tap network call).
- Audio pronunciation asset load with silent tactile fallback on failure, background retry.
- Non-gesture accessible decrement/reset control.
- Target-change proportional recalculation matching B-05's server formula exactly, applied optimistically client-side.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`POST /v1/habits/check-ins` (batched Dhikr submissions), `PATCH /v1/habits/{habit_id}/target` (B-05).

## 14. Database Requirements (Local)
Room table `dhikr_progress_cache(habit_id PK, current_count, target, last_updated)` for offline-tolerant local accumulation between batched syncs.

## 15. Validation
Unit test for proportional recalculation: 50/100 → target 150 → 50/150 (unchanged); 80/100 → target 50 → capped at 50/50 "target reached" (mandatory boundary case per PRD §7 Android prompt item 6).

## 16. Authentication
Shared `core-network` Bearer token attachment.

## 17. Authorization
N/A at UI layer.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Audio asset fails to load | Counter remains fully functional (silent tactile counting); background retry |
| Batched sync fails | Local count preserved; retried via K-06's outbox pattern |
| Target change fails to sync | Local optimistic recalculation stands; retried in background |

## 19. Offline First
Fully offline-capable — local count accumulation and target-change math work without connectivity; sync is opportunistic/batched.

## 20. Local Data
```
Local tap accumulation
   ↓
Room dhikr_progress_cache
   ↓
Batched POST /v1/habits/check-ins (throttled)
```

## 21. Localization
Dhikr text/audio pronunciation assets localized per supported language; count display uses locale-correct number formatting.

## 22. RTL
Large tap target and count display mirror correctly; decrement/reset control position verified for RTL.

## 23. Analytics
`dhikr_counter_opened`, `dhikr_target_reached`, `dhikr_target_changed_midday` via `AnalyticsTracker`.

## 24. Performance
Batched/throttled network calls avoid per-tap request overhead; haptic feedback must not introduce perceptible tap-to-feedback latency.

## 25. Security
No elevated risk; standard local-cache handling.

## 26. Library Requirements
Compose Multiplatform, Koin, Ktor, Room, platform haptic APIs via `expect/actual`.

## 27. Testing
- Unit: proportional recalculation formula, both directions (mandatory).
- UI: large-tap-target accessibility test, non-gesture alternative control test.
- Integration: audio-fallback behavior, batched-sync-failure retry behavior.

## 28. Documentation
KDoc on the recalculation formula referencing Edge Case 6 explicitly, including the smaller-target boundary case example.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Local Progress Cache & Batched Submission Logic**
- Objective: Room-backed accumulation with throttled sync.
- Existing Architecture to Follow: `core-database` Room conventions.
- Files to Create: Room entity/DAO for `dhikr_progress_cache`, batching logic in `HabitRepository`.
- Tests: unit tests for accumulation and batching thresholds.
- Definition of Done: local counting works fully offline with correct batched sync behavior.

**Task 02 — Implement `AdjustDhikrTargetUseCase` with Proportional Recalculation**
- Files to Create: `AdjustDhikrTargetUseCase.kt`
- Business Rules: Edge Case 6 formula, matching B-05 exactly.
- Tests: mandatory boundary-case unit tests (both directions).
- Definition of Done: recalculation matches server-side formula exactly.

**Task 03 — Build `DhikrCounterScreen` Composable**
- Files to Create: `DhikrCounterScreen.kt`, `DhikrCounterViewModel.kt`, `DhikrCounterUiState.kt`
- Implementation Details: large tap target, haptic pulse, audio pronunciation with fallback, non-gesture accessible controls.
- Localization/RTL: per §21/§22.
- Analytics: events per §23.
- Tests: Compose UI tests.
- Definition of Done: screen fully functional and accessible.

**Task 04 — Integrate into Habit Builder as a Distinct Card**
- Files to Modify: `HabitBuilderScreen.kt`
- Definition of Done: Dhikr renders visually distinct from standard checklist rows.

**Task 05 — Final Code Review**
- Do Not Change: batching/throttling behavior must not regress to per-tap network calls.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Dhikr Counter fully functional offline with correct batched sync, proportional target recalculation in both directions, and full accessibility support.

## 31. Final Verification Checklist
- [ ] Large tap target (≥72dp) with haptic pulse implemented
- [ ] Non-gesture accessible decrement/reset control present
- [ ] Batched/throttled submission, not per-tap network calls
- [ ] Audio pronunciation fallback verified
- [ ] Proportional target recalculation correct in both directions (mandatory test)
- [ ] Fully offline-capable local counting
- [ ] Localization and RTL verified
- [ ] Analytics events wired
