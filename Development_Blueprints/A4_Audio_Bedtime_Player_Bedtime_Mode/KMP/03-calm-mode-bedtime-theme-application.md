# K-03 — Calm Mode & Bedtime Theme Application

## 1. Feature Context
Applies the dimmed, low-stimulation Bedtime visual treatment to K-01's player screen — auto-triggered by the parent-configured window (K-07/B-01) or manually via an explicit Calm Mode toggle exposed from the standard Story Player (A.3). This is deliberately reconciled with, not a duplicate of, A.3/K-05's `BedtimeThemeOverlay`: both must read the same `core-designsystem` calm-mode tokens.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
2.3 Calm Mode & Bedtime Theme Application (ID: **K-03**)

## 4. Objective
Implement `forceCalmMode` as a parameter accepted by `BedtimeAudioPlayerScreen` (K-01), resolved once at entry from the time-window (K-07) or explicit toggle, applying dimmed theme tokens, muted accent overrides, and breathing cover-art animation — sourced from the same `core-designsystem` token set A.3/K-05 already established, not a second parallel theming system.

## 5. Business Requirements
- FR-4: Bedtime Mode is a system-wide state — any content surface entered during the window (or via explicit entry) applies the same dimmed visual treatment.
- FR-5: dims UI, disables stimulating reward effects, ends every session with dua/reflection — zero exceptions.
- FR-14: outside the window, the player functions normally unless the child explicitly opts in via "Calm Mode" toggle — the automatic window-based trigger stays separate from the manual toggle.
- §2.1: Calm Palette Application — dimmed navy/teal gradient, breathing cover art, `gold-bedtime` muted accent override (a deliberate token override, not a hardcoded local color).
- §1.10 Edge Case 10: daytime Calm Mode toggle used, then the actual window begins mid-session — no jarring transition, session continues in the already-calm visual state.
- A.3/K-05 §10: `isBedtimeMode` resolved exactly once at entry, no mid-session flicker on window-boundary crossing — this same discipline applies here, adapted to K-01's screen rather than K-05's overlay.

## 6. Existing Architecture
A.3/K-05 already established the pattern: a pure `BedtimeModeResolver.resolve(entryPoint, currentTime, parentBedtimeWindow)` function and a `core-designsystem` theming-override mechanism for content-context states independent of device light/dark mode. This sub-feature must **reuse A.3/K-05's `BedtimeModeResolver` and its `core-designsystem` token overrides directly** rather than reimplementing an equivalent resolver — the only genuinely new work is wiring `forceCalmMode` into K-01's screen/ViewModel, since K-01 is a different screen than A.3/K-05's overlay target.

## 7. Existing Code to Reuse
- A.3/K-05's `feature/stories/viewmodel/BedtimeModeResolver.kt` — reuse directly (import/depend on it, or confirm it is exposed via a shared module such as `core-bedtime` if the codebase has already extracted it there; if it currently lives inside `:feature:stories` and is not exposed as a shared dependency, this is the one architectural gap to flag and resolve via a small refactor — extracting the resolver to a shared module — rather than duplicating its logic into `:feature:bedtime-audio`)
- A.3/K-05's `core-designsystem` calm-mode theming-override tokens (`gold-bedtime`, dimmed navy/teal palette) — reuse the exact same token names
- K-07's `BedtimeRepository.getConfig()` (window source for this module's resolver input)

## 8. Files to Create
- `feature/bedtime-audio/theme/BedtimeCalmModeResolver.kt` — thin wrapper/adapter calling the shared `BedtimeModeResolver` (A.3/K-05) with K-01's entry-point context, OR a direct dependency on the shared resolver if extraction (per §7) is completed first
- `feature/bedtime-audio/theme/BreathingCoverArt.kt` — the audio player's specific breathing cover-art animation (distinct visual from A.3's video player, since there's no video to watch)
- `test/feature/bedtime-audio/BedtimeCalmModeResolverTest.kt`
- `androidTest/feature/bedtime-audio/CalmModeThemeTest.kt`

## 9. Files to Modify
- `feature/bedtime-audio/player/BedtimeAudioPlayerScreen.kt` (K-01) — accept `forceCalmMode: Boolean` parameter, apply theme override
- `feature/bedtime-audio/player/BedtimeAudioViewModel.kt` (K-01) — resolve calm-mode state once at entry, expose as immutable state
- A.3's standard Story Player Calm Mode toggle entry point — confirm it can navigate into K-01's `BedtimeAudioPlayerRoute` with a `forceCalmMode=true` param when the content is audio-format (cross-module navigation touchpoint; coordinate with A.3's existing toggle implementation rather than building a second toggle)

## 10. KMP Requirements
- `forceCalmMode` resolved exactly once when `BedtimeAudioPlayerScreen` is composed/launched — passed down as an immutable parameter, never re-evaluated mid-session even if the window boundary is crossed during playback (identical discipline to A.3/K-05).
- Resolution inputs: entry point (Home Bedtime Corner / Stories Bedtime category / explicit Calm Mode toggle / direct deep link) + current time + K-07's cached bedtime window.
- Theme override applies regardless of device light/dark mode: dimmed navy/teal gradient background, `gold-bedtime` muted amber accent (not the vibrant daytime gold), large soft-glow breathing cover art (slow subtle scale pulse loosely synced to playback, never jarring/fast).
- Edge Case 10 handling: if Calm Mode was already manually toggled and the actual window begins mid-session, no re-render/flicker occurs since the visual state was already calm-mode-equivalent — the resolved `forceCalmMode` value simply remains `true` throughout.
- Zero flashing elements under any circumstance within calm-mode visuals — stricter reduced-motion enforcement than the standard (non-bedtime) player state.

## 11. Required API
None directly — reads K-07's cached `BedtimeRepository.getConfig()` (which itself sources from B-01).

## 12. Offline First
Bedtime-window configuration cached locally via K-07 (reused, not duplicated) — calm-mode resolution works fully offline.

## 13. Local Data
Reuses K-07's existing parent-settings local cache — no new local store introduced by this sub-feature.

## 14. Localization
No new localized strings beyond what K-01 already renders; calm-mode is a purely visual/theme state.

## 15. RTL
Breathing cover-art animation is symmetric and requires no directional mirroring; surrounding layout mirroring is inherited from K-01's existing RTL handling.

## 16. Analytics
`BedtimeAnalytics`: `bedtime_mode_auto_applied`, `calm_mode_manually_toggled` — fired exactly once per resolution at screen entry (not re-fired on subsequent recompositions).

## 17. Performance
Reduced-motion enforcement must not introduce jank elsewhere — verify the dimmed-theme recomposition does not cascade into unnecessary re-renders of the underlying audio-player surface (breathing animation should be isolated to the cover-art composable's own recomposition scope).

## 18. Security
No new security surface.

## 19. Testing
- Unit: `BedtimeCalmModeResolver` determinism — mocked time-window boundary cases (mirrors A.3/K-05's boundary test suite), explicit-toggle override cases.
- Unit: Edge Case 10 — Calm Mode already active before window begins mid-session, verify no `forceCalmMode` value change/flicker.
- UI: theme applies identically regardless of device light/dark mode (mocked both).
- UI: reduced-motion assertion — zero flashing elements verified.
- Integration: confirm this module's resolver produces identical results to A.3/K-05's resolver given identical inputs (a cross-module consistency test, given both must agree on what "within the bedtime window" means for the same child at the same instant).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Confirm Reusability of A.3/K-05's `BedtimeModeResolver`**
Objective: Determine whether the existing resolver is accessible as a dependency from `:feature:bedtime-audio` (either already in a shared module, or requiring a small extraction refactor). Why: avoid duplicating the window-boundary resolution logic in two places that could silently drift apart. Follow: existing module-dependency graph conventions. Do Not Change: A.3/K-05's resolver behavior itself — only its location/exposure, if extraction is needed. Definition of Done: `:feature:bedtime-audio` has a confirmed, tested dependency path to the exact same resolver logic A.3/K-05 uses.

**Task 02 — Implement `BedtimeCalmModeResolver` Adapter**
Objective: Thin wrapper supplying K-01's entry-point context to the shared resolver. Files to create: `BedtimeCalmModeResolver.kt`. Dependencies: Task 01. Tests: boundary-case tests mirroring A.3/K-05's suite. Definition of Done: tests pass, results consistent with A.3/K-05 given identical inputs.

**Task 03 — Wire `forceCalmMode` into `BedtimeAudioViewModel`/`BedtimeAudioPlayerScreen`**
Objective: Resolve once at entry, pass down as immutable parameter. Files to modify: K-01's ViewModel and Screen. Dependencies: Task 02. Tests: no-mid-session-flicker regression test (window-boundary crossed during an active session). Definition of Done: test passes.

**Task 04 — Implement `BreathingCoverArt` Composable**
Objective: Slow, subtle scale-pulse animation loosely synced to playback, isolated recomposition scope. Files to create: `BreathingCoverArt.kt`. Follow: `core-designsystem` calm-mode tokens. Dependencies: Task 03. Tests: recomposition-isolation test (verify the animation does not trigger re-renders of sibling composables). Definition of Done: test passes.

**Task 05 — Apply Dimmed Theme Tokens**
Objective: Dimmed navy/teal background, `gold-bedtime` accent override, applied via the same `core-designsystem` mechanism A.3/K-05 uses. Dependencies: Task 01, 03. Tests: theme-independence-from-device-setting test (both light/dark device modes). Definition of Done: test passes.

**Task 06 — Wire the Standard Story Player's Calm Mode Toggle to Navigate into K-01**
Objective: When the toggled content is audio-format, the existing A.3 toggle entry point navigates into `BedtimeAudioPlayerRoute` with `forceCalmMode=true` rather than staying on A.3's own player. Files to modify: A.3's Calm Mode toggle implementation (coordinate cross-module). Dependencies: Task 03. Tests: navigation-routing test for audio-format content. Definition of Done: test passes.

**Task 07 — Add Analytics Instrumentation**
Objective: Two events per §16, fired exactly once per resolution. Tests: fake-tracker assertions. Definition of Done: exactly one call site per event.

**Task 08 — Add Full Test Suite Including Cross-Module Consistency Check**
Objective: Complete coverage per §19, including the resolver-consistency test against A.3/K-05. Definition of Done: all green.

**Task 09 — Final Code Review**
Objective: Confirm zero duplicated resolver logic exists between this module and A.3/K-05; confirm theme tokens are shared, not redefined locally. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] `forceCalmMode` resolved exactly once at K-01's screen entry, never flickers mid-session
- [ ] Resolver logic is genuinely shared with (or provably consistent with) A.3/K-05's `BedtimeModeResolver` — not a silently-drifting duplicate
- [ ] Dimmed theme tokens (`gold-bedtime`, navy/teal palette) sourced from `core-designsystem`, not hardcoded locally
- [ ] Breathing cover-art animation isolated to its own recomposition scope
- [ ] Zero flashing elements under any circumstance
- [ ] Edge Case 10 (Calm Mode already active before window begins) produces no flicker
- [ ] Standard Story Player's Calm Mode toggle correctly routes audio-format content into K-01
- [ ] Both analytics events fire exactly once per resolution

## 22. Definition of Done
K-01's Bedtime Audio Player correctly and consistently applies the dimmed, low-stimulation Bedtime visual treatment — genuinely sharing its resolution logic and design tokens with A.3/K-05 rather than forking a second theming system, with zero mid-session flicker and zero flashing elements.
