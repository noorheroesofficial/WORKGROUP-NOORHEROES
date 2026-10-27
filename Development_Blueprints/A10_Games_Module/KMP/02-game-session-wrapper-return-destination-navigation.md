# K-02 — Game Session Wrapper & Return-Destination Navigation

## 1. Feature Context
Part of **A.10 Games Module**. Covers `GameSessionWrapper`, the reusable composable/navigation host that wraps any individual game's play screen with generic loading/completion lifecycle and explicit return-destination routing (PRD §6.3, §7 item 2).

## 2. Parent Feature
A.10 Games Module — KMP App (Android/iOS)

## 3. Sub-feature
**2.2 Game Session Wrapper & Return-Destination Navigation** `[K-02]`

## 4. Objective
Build `GameSessionWrapper(gameId, returnDestination: ReturnDestination)` where `ReturnDestination` is a sealed class (`Home`, `Rewards`, `GamesHub`) captured at launch time and honored explicitly on completion via `Navigator.navigateTo()`, not a generic back-stack pop — correct even if intermediate screens were pushed during the session (PRD FR-7, §6.3, §7 item 2).

## 5. Business Requirements
- FR-7: on completion, return to the exact screen that launched the session — never an unrelated destination.
- FR-9: replaying a completed game is always available (no re-locking).
- FR-12: session has a clear natural end state; no auto-continuing without explicit child action.
- §2.1 Difficulty-Adaptive Feedback: in-session difficulty shifts must never be visually jarring (no "Level Up!" interruption).
- §2.2 Session Completion Screen: celebratory-but-calm treatment, XP reveal, optional strengths/next-step block, "Play Again"/"Done" actions.

## 6. Existing Architecture
Per `CORE_NAVIGATION_INSTRUCTIONS.md` §4, `Route` implementations must avoid passing large objects — pass IDs, let the target screen fetch data. `ReturnDestination` is therefore modeled as a lightweight sealed class carrying only an enum-like discriminant (and, for `GamesHub`, no extra data; for `Home`/`Rewards`, no extra data either — these are fixed destinations, not parameterized ones), not a full `Route` object serialized through navigation args, to stay consistent with this rule while still being "typed" per the PRD's requirement.

**Resolved (previously implicit reuse gap):** `Feature_A9_Skill_Tree_Mastery_Engine.md` §6.2–§6.4 confirms `:core:mastery-engine` already ships a reusable `QuizCompletionResultScreen` Composable plus `MasteryResultViewModel` that fetches `GET /v1/mastery/result/{attempt_id}` and exposes a sealed `ResultAction` (`ReviewMistakes`, `TryAgain`, `Continue`) — this is the exact component the PRD (§2.3 of A.10) means by "reuses A.9's Strengths + one next step framing." `GameSessionWrapper` must invoke this existing composable directly for the strengths+next-step variant (passing `game_session.session_id` as the `attempt_id` argument, consistent with B-03's confirmed idempotency mapping), not build a parallel result-fetching screen. `SessionCompletionScreen` (§8 below) is therefore narrowed to only the simpler, free-form "Nice work! 🌟 [XP earned]" variant for games where a strengths/next-step breakdown doesn't apply — the per-game-configurable choice PRD §2.1 describes.

## 7. Existing Code to Reuse
- `Navigator` / `Route` (`core-navigation`) — `navigator.navigateTo(route, popUpTo, inclusive)`.
- `NoorResult<T>` / `AppError` (`core-common`).
- A.5's existing Quran Game / Arabic Letters game-play composables (`:feature:learn`) — invoked from within `GameSessionWrapper`, not reimplemented (PRD §7 item 5).
- `GamesRepository` (K-01, extended here with `getManifest()`).
- Design-system celebratory/result-screen components (`core-ui`) — reuse A.8/A.9's existing result-screen visual pattern per PRD §2.4.

## 8. Files to Create
```
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/session/GameSessionWrapper.kt
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/session/ReturnDestination.kt
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/session/GameSessionViewModel.kt
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/session/GameSessionRoute.kt
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/ui/SessionCompletionScreen.kt
feature/games/src/commonTest/kotlin/com/noorheroes/feature/games/session/GameSessionWrapperNavigationTest.kt
```

## 9. Files to Modify
```
core/data/src/commonMain/kotlin/com/noorheroes/core/data/repository/GamesRepository.kt      # add getManifest()
core/data/src/commonMain/kotlin/com/noorheroes/core/data/repository/GamesRepositoryImpl.kt  # implement getManifest()
core/navigation/src/commonMain/kotlin/com/noorheroes/core/navigation/Route.kt               # register GameSessionRoute
```
**Do Not Change:** `:feature:learn` (A.5) game-play composable internals — invoke their existing public composables only.

## 10. Backend Requirements
None implemented here; consumes B-02 (`GET /v1/games/{game_id}/manifest`) exactly as documented.

## 11. KMP Requirements
- `GameSessionRoute(gameId: String, returnDestination: ReturnDestination)` — `@Serializable`, minimal payload per §6 note.
- `ReturnDestination` sealed class: `Home`, `Rewards`, `GamesHub` — captured at the moment of launch from whichever screen initiated the session (Home's Trending Games rail → `Home`; Rewards screen entry → `Rewards`; Games Hub tile → `GamesHub`).
- `GameSessionWrapper` composable: generic loading state (lightweight, per-game-asset-appropriate) → delegates to the game-specific play screen (reused from A.5) → generic `SessionCompletionScreen` → explicit `navigator.navigateTo(returnDestination.toRoute(), popUpTo = GameSessionRoute::class, inclusive = true)` on "Done."
- "Play Again" restarts a fresh session at the same `gameId`/`returnDestination` without leaving the wrapper (no lock, no degraded repeat experience per FR-9).
- Difficulty-adaptive feedback rendered smoothly, no jarring interruption (§2.1) — implemented as a subtle, non-modal visual cue only.

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes `GET /v1/games/{game_id}/manifest` exactly as defined in B-02 §13 (including `403 AGE_BAND_MISMATCH` / `410 GAME_WITHDRAWN` handling — mapped to `AppError.Auth`/a dedicated `AppError.GameUnavailable` variant respectively, falling back gracefully to the Games Hub with a message rather than crashing).

## 14. Database Requirements
N/A directly; local manifest caching for offline play is owned by K-05.

## 15. Validation
`gameId` presence validated before manifest fetch; malformed/missing `gameId` routes back to Games Hub defensively rather than crashing.

## 16. Authentication
Relies on existing child-session-scoped network client; no new auth logic.

## 17. Authorization
Server-side re-validation (B-02) is the actual authorization boundary; this wrapper simply surfaces the resulting `403`/`410` gracefully.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Manifest fetch returns `403 AGE_BAND_MISMATCH` | Return to Games Hub with a brief "this game isn't available right now" message, no crash |
| Manifest fetch returns `410 GAME_WITHDRAWN` | Same graceful fallback |
| A.5 game-play composable throws/errors internally | Wrapper catches at its boundary, logs via `NoorHeroesLogger`, routes to a generic error state with "Try Again"/"Back" options |
| Session completion API call fails (network) | Handled by K-03, not this blueprint — completion screen still shown per FR-7 intent |

## 19. Offline First
`GameSessionWrapper` requests the manifest via `GamesRepository.getManifest()`, which (per K-05) resolves from local cache when offline for downloaded games; non-downloaded games show the offline/download-required notice (PRD §1.14) rather than attempting the wrapper flow.

## 20. Local Data
N/A directly (owned by K-05); this blueprint defines the consumption contract only.

## 21. Localization
All Session Completion Screen text ("Nice work! 🌟", strengths/next-step framing, button labels) localized EN/HI/AR/UR.

## 22. RTL
Completion screen layout mirrors correctly for Arabic/Urdu; "Play Again"/"Done" button order follows RTL convention (not simply mirrored left-right blindly — follow platform RTL button-ordering guidance from `CORE_DESIGNSYSTEM_INSTRUCTIONS.md`).

## 23. Analytics
- `game_session_started` (with `game_id`, `skill_node_ids`, `age_band_tier`) — fired on successful manifest resolution, before play begins.
- `game_difficulty_adapted_in_session` — fired on in-session difficulty shift.
- Completion-related events (`game_session_completed`, `game_evidence_submitted`, `game_reward_awarded`) fired by K-03 upon successful delegation, not here directly, to keep this blueprint focused on navigation/lifecycle.

## 24. Performance
- Loading state kept lightweight and game-asset-appropriate (reuse each game's own existing loading pattern from A.5 where available, per PRD §1.13).
- Navigation to return destination is immediate/synchronous from the UI's perspective (no unnecessary intermediate screens).
- Target: session start p95 < 800ms including manifest resolution (shared target with B-02).

## 25. Security
No new sensitive data surface; relies on B-02's server-side re-validation as the actual security boundary.

## 26. Library Requirements
Jetpack Compose Multiplatform, Koin, Kotlinx Coroutines/Flow, Kotlinx Serialization. No new dependencies.

## 27. Testing
- **Primary navigation test:** all three `ReturnDestination` values (`Home`, `Rewards`, `GamesHub`) verified to route correctly on completion, including when intermediate screens were pushed during the session (simulated back-stack manipulation in test).
- Unit: "Play Again" correctly restarts without navigating away from the wrapper.
- Unit: `403`/`410` manifest errors correctly route to graceful fallback, not a crash.
- Integration: full manifest-fetch → play-screen-delegation → completion → return-navigation round trip (play-screen mocked/stubbed since it's owned by A.5).
- Structural test: confirm `GameSessionWrapper` invokes A.5's existing composables rather than containing duplicated game-mechanic rendering code.

## 28. Documentation
KDoc on `ReturnDestination` and `GameSessionWrapper` explicitly documenting the "explicit navigation, not back-stack pop" contract and why (fragility under pushed intermediate screens).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define ReturnDestination Sealed Class**
- Objective: `sealed class ReturnDestination { object Home; object Rewards; object GamesHub }` with a `toRoute(): Route` mapping function.
- Definition of Done: exhaustive `when` mapping to `Route` compiles with no `else` branch needed.

**Task 02 — Define GameSessionRoute**
- Objective: `@Serializable data class GameSessionRoute(val gameId: String, val returnDestination: ReturnDestination) : Route`.
- Definition of Done: registered in `core-navigation`'s route registry.

**Task 03 — Extend GamesRepository with getManifest()**
- Objective: `suspend fun getManifest(gameId: String): NoorResult<GameManifest>`.
- Existing Files to Reuse: `GamesRepository` interface from K-01.
- Definition of Done: maps B-02's `403`/`410`/`404` responses to distinct `AppError` variants.

**Task 04 — Implement GameSessionViewModel**
- Objective: Fetches manifest, exposes UI state (`Loading`, `Ready`, `Unavailable`, `Error`), holds `returnDestination` for later use.
- Definition of Done: unit tests for all state transitions.

**Task 05 — Build GameSessionWrapper Composable**
- Objective: Loading state → delegate to A.5's existing play composable (selected by `mechanic_type`) → `SessionCompletionScreen`.
- Existing Files to Reuse: A.5's `:feature:learn` composables — invoke via their existing public API, do not copy/reimplement.
- Definition of Done: structural test confirms no duplicated game-mechanic code.

**Task 06 — Implement Explicit Return Navigation**
- Objective: On "Done," call `navigator.navigateTo(returnDestination.toRoute(), popUpTo = GameSessionRoute::class, inclusive = true)`.
- Definition of Done: primary navigation test (Task 09) passes for all three destinations under pushed-intermediate-screen conditions.

**Task 07 — Implement "Play Again" Flow**
- Objective: Restart session in place without leaving the wrapper or triggering return navigation.
- Definition of Done: unit test confirms no navigation event fired on replay.

**Task 08 — Build SessionCompletionScreen**
- Objective: Celebratory-but-calm UI, XP reveal, optional strengths/next-step block (per-game-configurable), "Play Again"/"Done" actions.
- Existing Files to Reuse: A.8/A.9's existing result-screen visual pattern.
- Definition of Done: matches PRD §2.2 component list.

**Task 09 — Add Navigation Tests**
- Objective: Full `ReturnDestination` coverage under pushed-intermediate-screens scenario.
- Files to Create: `GameSessionWrapperNavigationTest.kt`.

**Task 10 — Add Error-Handling Tests**
- Objective: `403`/`410` graceful-fallback paths tested.

**Task 11 — Add Localization/RTL Verification**
- Objective: Completion screen strings and RTL button ordering verified.

**Task 12 — Final Code Review**
- Objective: Confirm no generic back-stack pop is used anywhere in the completion flow; confirm A.5 composable reuse (no mechanic duplication).
- Definition of Done: review checklist (§31) fully checked.

## 30. Definition of Done
- All three `ReturnDestination` values route correctly on completion, verified under pushed-intermediate-screen conditions.
- "Play Again" functions identically to first play, no lock, no degraded experience.
- A.5's existing game-play composables reused, not duplicated.
- Graceful fallback for `403`/`410` manifest errors, no crashes.
- Completion screen matches PRD component/state requirements.

## 31. Final Verification Checklist
- [ ] Explicit navigation (not back-stack pop) verified for Home/Rewards/GamesHub
- [ ] Navigation correctness holds even with intermediate screens pushed during session
- [ ] "Play Again" does not trigger unintended navigation
- [ ] `403 AGE_BAND_MISMATCH`/`410 GAME_WITHDRAWN` both gracefully handled, no crash
- [ ] A.5 game-play composables reused via public interface, not duplicated
- [ ] Completion screen localized EN/HI/AR/UR with correct RTL button ordering
- [ ] Difficulty-adaptive feedback confirmed non-jarring (no modal interruption)
- [ ] No files outside declared scope modified

---

## 32. Cross-Platform Dependencies
- Backend Dependency: B-02 (manifest resolution), B-03 (completion orchestration).
- KMP Dependency: `:feature:learn` (A.5 game-play composables, reused not forked), `:core:mastery-engine` (A.9 `QuizCompletionResultScreen`/`MasteryResultViewModel`, reused per §6 resolution above).
- Admin Dependency: None directly.
- Database Dependency: None directly (stateless wrapper; manifest caching owned by K-05).
- External Service Dependency: None.
- Figma Dependency: Session Completion Screen (generic wrapper) — Figma Required.
