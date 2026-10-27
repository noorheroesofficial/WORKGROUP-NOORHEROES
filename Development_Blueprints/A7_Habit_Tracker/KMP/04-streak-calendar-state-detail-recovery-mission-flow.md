# K-04 — Streak Calendar, State Detail & Recovery Mission Flow

## 1. Feature Context
NoorHeroes KMP app. Renders streak history and the non-shaming Broken/AtRisk/Recovery messaging that is central to the feature's ethical design commitment.

## 2. Parent Feature
A.7 Habit Tracker — KMP App (Android/iOS)

## 3. Sub-feature
K-04 Streak Calendar, State Detail & Recovery Mission Flow

## 4. Objective
Build the Streak Calendar, Streak State Detail (AtRisk/Broken/Recovery), Recovery Mission, and Mercy Suggestion Prompt screens, with a mandatory shame-word blocklist test across all locales (FR-13, FR-14).

## 5. Business Requirements
- Warm, non-alarming iconography for AtRisk/Broken states — never red/alarming (PRD §2.1).
- Client-side display only mirrors server-computed streak state (B-03); never independently computes transitions.
- The internal `broken` state name must never be surfaced as raw user-facing text — always translated into supportive copy.
- Mercy Suggestion Prompt offers a smaller target/alternate time/family reminder, never implies failure (FR-14).
- Recovery Mission completion returns streak to Active; window expiry returns to Inactive — both communicated without shame framing.

## 6. Existing Architecture
Extends `feature-habits`/`feature-habits-domain` (K-01). Uses `core-navigation` for Streak Calendar/State Detail/Recovery Mission as sibling destinations off Habit Builder.

## 7. Existing Code to Reuse
- `HabitRepository` extended with `GetStreakUseCase` (K-01 pattern)
- `core-design-system` non-alarming iconography tokens (streak-risk amber, moon-phase motif, shield-glow for Protected)

## 8. Files to Create
- `feature-habits/src/commonMain/kotlin/.../streak/StreakCalendarScreen.kt`
- `feature-habits/src/commonMain/kotlin/.../streak/StreakStateDetailScreen.kt`
- `feature-habits/src/commonMain/kotlin/.../streak/RecoveryMissionScreen.kt`
- `feature-habits/src/commonMain/kotlin/.../streak/MercySuggestionPrompt.kt`
- `feature-habits-domain/src/commonMain/kotlin/.../GetStreakUseCase.kt`
- `feature-habits/src/androidInstrumentedTest/kotlin/.../ShameWordBlocklistUiTest.kt` (scans all locale string resources)

## 9. Files to Modify
- `HabitBuilderScreen.kt` (K-01) — "View Streak History" navigation entry, AtRisk/Broken banner

## 10. Backend Requirements
Consumes `GET /v1/habits/streaks/{child_id}` (B-03), `PATCH /v1/habits/{habit_id}/target` (not applicable here; mercy-suggestion "accept" calls the same target-adjustment endpoint per PRD §2.3 click-mapping when applicable to the affected habit).

## 11. KMP Requirements
- Streak Calendar with skeleton loading state.
- Streak State Detail with warm illustration (softly glowing garden at dusk, not a wilted plant), AtRisk-warning/Broken-transition/Recovery-active/Recovery-closing-soon states.
- Recovery Mission screen; completing it navigates back to Habit Builder with streak restored to Active.
- Mercy Suggestion Prompt: Accept (adjusts target inline) / Dismiss.
- Compose UI test utility scanning all rendered `Text` composables on these screens against a case-insensitive blocklist: "fail", "failed", "broke", "broken", "lost", "didn't" — run against every locale's string resources, not just default.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`GET /v1/habits/streaks/{child_id}` (B-03).

## 14. Database Requirements (Local)
Room cache of last-fetched streak state for offline/degraded-mode display, mirroring B-03's server-side cached-fallback behavior.

## 15. Validation
Mandatory: shame-word blocklist Compose UI test across every locale's string resources (PRD §7 Android prompt item 5).

## 16. Authentication
Shared `core-network` Bearer token attachment.

## 17. Authorization
N/A at UI layer.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Streak Service degraded (B-03 cached fallback) | Client shows last-known cached state with a calm "reconnecting" indicator, never a zero-reset flash |
| Recovery window expiring | Gentle nudge, not a countdown-pressure timer |

## 19. Offline First
Streak display works from local cache when offline; recovery-mission completion requires connectivity (delegates to K-06 outbox if the completion action itself is a check-in-equivalent).

## 20. Local Data
```
GET /v1/habits/streaks/{child_id}
   ↓
GetStreakUseCase
   ↓
Room streak_cache
   ↓
StreakCalendarScreen / StreakStateDetailScreen (cached fallback)
```

## 21. Localization
All streak-state and mercy-suggestion copy fully localized and culturally reviewed (not just translated) per B-11's review workflow — consume only `status='published'` copy.

## 22. RTL
Calendar grid, state-detail illustration layout, and prompt buttons verified for RTL mirroring.

## 23. Analytics
`streak_state_changed`, `streak_shield_applied`, `streak_broken_shown`, `recovery_mission_started`, `recovery_mission_completed`, `recovery_window_expired`, `mercy_suggestion_shown`, `mercy_suggestion_accepted` via `AnalyticsTracker`.

## 24. Performance
Streak state read is lightweight; illustration assets lazy-loaded to avoid blocking screen entry.

## 25. Security
No elevated risk; the mandatory blocklist test is a content-safety control, not a security control per se, but treated with equivalent CI-gate rigor.

## 26. Library Requirements
Compose Multiplatform, Koin, Ktor, Room.

## 27. Testing
- Mandatory: shame-word blocklist test across all locales (CI-blocking).
- Unit: client never independently computes state transitions (render-only verification).
- UI: all documented streak-state visual variants render correctly with correct iconography.

## 28. Documentation
KDoc explicitly noting: "broken" is a valid internal state name but must never appear as user-facing text — always translate to supportive copy.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `GetStreakUseCase` with Cached Fallback**
- Files to Create: `GetStreakUseCase.kt`, Room cache entity/DAO.
- Existing Architecture to Follow: `core-database` Room conventions.
- Tests: cached-fallback unit test on service degradation.
- Definition of Done: use case never surfaces a zero-reset on degraded fetch.

**Task 02 — Build Streak Calendar Screen**
- Files to Create: `StreakCalendarScreen.kt`
- Implementation Details: skeleton loading, calendar grid history rendering.
- Tests: Compose UI test.
- Definition of Done: calendar renders correctly with cached-fallback support.

**Task 03 — Build Streak State Detail, Recovery Mission, Mercy Suggestion Screens**
- Files to Create: `StreakStateDetailScreen.kt`, `RecoveryMissionScreen.kt`, `MercySuggestionPrompt.kt`
- Existing Files to Reuse: `core-design-system` non-alarming iconography.
- Business Rules: FR-13, FR-14.
- Tests: Compose UI tests per documented state variant.
- Definition of Done: all states render with correct warm, non-punitive framing.

**Task 04 — Implement Mandatory Shame-Word Blocklist Test**
- Files to Create: `ShameWordBlocklistUiTest.kt`
- Implementation Details: scan all rendered `Text` nodes on these screens against the blocklist, across every locale's string resources.
- Do Not Change: do not weaken the blocklist or exempt any locale without explicit content-safety sign-off.
- Definition of Done: test passes for all locales; registered as a CI-blocking gate.

**Task 05 — Wire Navigation & Analytics**
- Files to Modify: `HabitBuilderScreen.kt`
- Definition of Done: navigation entries correct; all events wired.

**Task 06 — Final Code Review**
- Do Not Change: internal `broken` state must never be surfaced as raw text.
- Expected Result: PR merge-ready, blocklist test green across all locales.

## 30. Definition of Done
Streak Calendar/State Detail/Recovery/Mercy Suggestion flows live, all locales pass the mandatory shame-word blocklist test, client never independently computes streak transitions.

## 31. Final Verification Checklist
- [ ] Shame-word blocklist test passes across every locale (mandatory CI gate)
- [ ] Internal `broken` state name never surfaced as raw text
- [ ] Client mirrors server state only, never independently computes transitions
- [ ] Cached-fallback display never zero-resets on service degradation
- [ ] All documented state variants render with warm, non-punitive iconography
- [ ] Localization and RTL verified
- [ ] Analytics events wired
