# K-02 — Language Selection & Intro Onboarding Sequence

> **Status:** ✅ **Implemented & Verified** (Live simulator verified on Android `emulator-5554` with live FastAPI backend)

## 1. Feature Context
First-launch-only Language Selection followed by 4 skippable Intro slides, both pre-auth and pre-network-dependent (bundled fallback content). This is the "value sequence" a new parent sees before any signup pressure.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
2.2 Language Selection & Intro Onboarding Sequence (ID: **K-02**)

## 4. Objective
Build Language Selection (persists immediately on tap) and a 4-slide Compose Pager Intro sequence (skip from slide 1) with bundled-offline fallback, full RTL mirroring, and OS-level language-change resilience mid-flow.

## 5. Business Requirements
- FR-3: Language selection available before/alongside intro; persists locally and to parent profile once authenticated.
- FR-4: Intro is exactly 4 screens; skip available from screen 1; no paywall/subscription screen before intro completes.
- Edge Case: Parent changes device language mid-onboarding (OS-level change while backgrounded) → app re-renders current step in new language on resume, without losing entered data.
- Empty State: Intro slides with no remote content loaded → fallback to bundled offline copies (never block first-launch on network).
- NFR: Full localization + RTL layout mirroring, not just text translation; WCAG 2.1 AA.

## 6. Existing Architecture
`core-common`'s `localization` package (reactive localization provider); `core-datastore`'s `PreferenceManager` for immediate-persist language selection; `core-navigation`'s `Route`; `core-ui`'s `LoadStateContent` for the (rare) remote-intro-content-fetch path.

## 7. Existing Code to Reuse
- `core-common/localization`: reactive localization provider (exact class name to confirm in codebase — reuse, do not build a parallel locale system)
- `core-datastore`: `PreferenceManager.setString()/getString()`
- `core-navigation`: `Navigator`, `Route`
- `core-designsystem`: `NoorHeroesTheme`, RTL-aware `Modifier.noorHeroesSafeArea()`
- `core-ui`: `PrimaryButton`, `TextButton` (for Skip), `LoadStateContent`

## 8. Files to Create
- `feature/onboarding/ui/LanguageSelectionScreen.kt`
- `feature/onboarding/ui/IntroSlidesScreen.kt` (Pager-based, 4 slides)
- `feature/onboarding/viewmodel/LanguageSelectionViewModel.kt`, `IntroSlidesViewModel.kt` (+ State/Event files)
- `feature/onboarding/data/IntroContentRepository.kt` (bundled-asset-first, remote-optional)
- `res/raw or commonMain/resources/intro_slides_bundled.json` (or per-locale bundled string resources, following existing localization resource convention)
- `test/feature/onboarding/LanguageSelectionViewModelTest.kt`, `IntroSlidesViewModelTest.kt`
- `androidTest/feature/onboarding/IntroSlidesScreenTest.kt`

## 9. Files to Modify
- `core-navigation/Route.kt` — add `LanguageSelectionRoute`, `IntroSlidesRoute`

## 10. KMP Requirements
- `LanguageSelectionViewModel`: on tap, immediately calls `PreferenceManager.setString(KEY_LANGUAGE, code)` — no separate "confirm" step; if authenticated later, this selection is also pushed to the parent profile (coordinate with B-02/consent — the persisted language is included in the `locale` field already sent at registration, not a separate API call).
- `IntroSlidesViewModel`: `IntroContentRepository.getSlides()` returns bundled content immediately (synchronously available, no loading spinner needed for the default path); if a remote-content-freshness check succeeds, swap in updated content non-blockingly — never block first-launch on this network call.
- Skip available starting from slide 1 (not just slide 4) — `Skip` button visible on every slide, navigates directly to Login/Registration (K-03).
- OS-level language change while backgrounded: on `onResume`, re-read the active locale from `core-common`'s localization provider and re-render the current step's copy in the new language, preserving any already-entered state (N/A for Intro itself, but the pattern must be established here since K-03/K-06 depend on the same resume-refresh behavior).
- RTL: full mirroring for Arabic — layout direction, icon directionality (back arrows), text alignment; verify Compose `LayoutDirection` propagates correctly through the Pager.

## 11. Required API
None — this sub-feature is intentionally network-independent for its default path. If a remote intro-content-versioning check exists (per B-01's `remote_config.intro_slides_version`), it is read-only and non-blocking.

## 12. Offline First
Bundled intro slides are the source of truth by default; remote content (if any) is a progressive enhancement only, never a hard dependency for first-launch.

## 13. Local Data
`PreferenceManager` key for selected language (persisted immediately). No other local state at this stage.

## 14. Localization
English, Hindi, Arabic, Urdu — bundled slide copy must exist for all four at ship time (scholar/legal-reviewed where the copy touches consent-adjacent trust messaging, per PRD §2.1 Arabic Support Rules, even though Intro itself isn't legal text — apply the same translation-quality bar for brand consistency).

## 15. RTL
Full mirroring: Pager swipe direction, page indicator dot order, Skip/Next button positions, icon mirroring (chevrons) — explicitly test, not just rely on Compose's automatic mirroring for custom-drawn elements.

## 16. Analytics
Emit `language_selected` (language_code, is_first_launch), `intro_slide_viewed` (slide_number), `intro_skipped` (slide_number_at_skip) via `AnalyticsTracker`.

## 17. Performance
Bundled content must render with zero network-wait — this is a cold-start-adjacent screen, so avoid any synchronous I/O heavier than a `PreferenceManager` read on the critical path.

## 18. Security
No sensitive data on this screen — N/A beyond standard input hygiene.

## 19. Testing
- Unit: language-selection immediate-persist behavior; skip-from-slide-1 navigation target; OS-language-change-on-resume re-render logic.
- UI: Pager swipe/skip/next interactions; RTL layout snapshot tests (Percy/Chromatic-equivalent) for all 4 slides in both LTR and RTL, light and dark theme.
- Accessibility: TalkBack traversal order on Language Selection (list/search if >8 languages) and Intro (headline → body → page indicator → Skip/Next).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Add Routes**
Objective: `LanguageSelectionRoute`, `IntroSlidesRoute`. Follow: existing `Route` pattern. Definition of Done: routes compile, `analyticsName` set.

**Task 02 — Implement `IntroContentRepository` with Bundled-First Strategy**
Objective: Synchronous bundled-content access + optional non-blocking remote freshness check. Follow: `core-data` repository conventions, but explicitly bundled-first (unusual relative to the network-first patterns elsewhere — document why in the class KDoc). Files to Create: repository + bundled resource file(s). Tests: bundled content always available with zero network mock configured. Definition of Done: repository never throws/blocks when network is fully absent.

**Task 03 — Implement `LanguageSelectionViewModel` and Screen**
Objective: Immediate-persist-on-tap language list (with search if >8 languages per PRD). Follow: `BaseViewModel`, `PreferenceManager`. Tests: persist-on-tap-no-confirm-step assertion. Dependencies: Task 01. Definition of Done: selection persists to DataStore within the same tap handler, no intermediate "Confirm" UI state.

**Task 04 — Implement `IntroSlidesViewModel` and Pager Screen**
Objective: 4-slide pager, skip-from-slide-1, page indicator dots. Follow: `BaseViewModel`, Compose `HorizontalPager`. Business Rules: Skip visible and functional on every slide including slide 1. Tests: skip-target-is-K03-login navigation assertion for each slide index. Dependencies: Tasks 01–02. Definition of Done: skip works identically regardless of which slide it's triggered from.

**Task 05 — Implement OS-Language-Change-on-Resume Handling**
Objective: Re-render current step's copy after a backgrounded OS-level language change, establishing the pattern K-03/K-06 will reuse. Follow: lifecycle-aware `onResume` hook re-reading `core-common`'s localization provider. Tests: simulated locale-change-while-backgrounded test. Dependencies: Tasks 03–04. Definition of Done: re-render happens without any data loss (trivial here since Intro has no user-entered data, but the mechanism itself must be verified reusable).

**Task 06 — Full RTL Verification Pass**
Objective: Confirm Pager, indicator dots, Skip/Next, and all icons mirror correctly in Arabic/Urdu. Follow: `core-designsystem`'s RTL utilities. Tests: RTL snapshot tests per §19. Dependencies: Task 04. Definition of Done: visual snapshot baselines captured for both LTR and RTL.

**Task 07 — Add Analytics Instrumentation**
Objective: `language_selected`, `intro_slide_viewed`, `intro_skipped`. Follow: `AnalyticsTracker` injection, ViewModel-only call sites. Tests: fake-tracker assertions. Dependencies: Tasks 03–04. Definition of Done: exactly one call site per event.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green, including accessibility traversal-order tests.

**Task 09 — Final Code Review**
Objective: Confirm zero network dependency on the default first-launch path, RTL correctness, no hardcoded design tokens. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [x] Language selection persists immediately on tap, no separate confirm step
- [x] Intro renders fully from bundled content with zero network calls required
- [x] Skip is available and functional from slide 1 onward
- [x] No paywall/subscription screen reachable before intro completes
- [x] OS-level language change while backgrounded correctly re-renders on resume
- [x] Full RTL mirroring verified for Pager, indicators, buttons, icons
- [x] `language_selected`/`intro_slide_viewed`/`intro_skipped` events emitted correctly
- [x] Bundled copy exists for English, Hindi, Arabic, Urdu

## 22. Definition of Done
Language Selection and the 4-slide Intro sequence are live, fully offline-capable by default, fully RTL-mirrored, and hand off cleanly to K-03 (Registration/OTP) via Skip or natural completion. **(STATUS: IMPLEMENTED & VERIFIED)**
