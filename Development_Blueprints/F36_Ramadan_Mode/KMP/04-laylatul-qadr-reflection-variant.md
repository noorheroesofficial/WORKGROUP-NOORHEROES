# K-04 — Laylatul Qadr Reflection Variant

## 1. Feature Context
The deliberately calmer, non-competitive presentation variant shown on the five Laylatul Qadr nights (21/23/25/27/29) — driven entirely by B-03's server-computed `gamification_suppressed` flag, since manually hardcoding these five nights anywhere client-side would be exactly the "dependent on manual editorial memory" failure mode the PRD explicitly warns against.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
2.4 Laylatul Qadr Reflection Variant (ID: **K-04**)

## 4. Objective
Build the Laylatul Qadr Reflection screen variant and its Night Recap counterpart, rendered conditionally based solely on B-03's `gamification_suppressed` flag.

## 5. Business Requirements
- FR-12: Laylatul Qadr nights deliberately suppress gamification — no leaderboard-style framing, no competitive badge call-outs, a calmer reflection-oriented register.
- §1.18 Screen 8: Laylatul Qadr Reflection (calmer variant).
- §2.1: Laylatul Qadr Calm-Mode Visual Language — deliberately quieter, less saturated treatment.
- §7 Android AI prompt item 3 (mandatory): variant renders based on the server's `gamification_suppressed` flag; UI test for both states.

## 6. Existing Architecture
`:feature:ramadan` module; this is a presentation-layer variant of K-02's/K-03's screens, selected by a single boolean flag from B-03 — not a parallel navigation branch or duplicated business logic.

## 7. Existing Code to Reuse
- K-02's Journey Map/Night Recap base Composables (variant applied via conditional theming, not forked)
- K-03's Mission Detail base Composable
- `:core:design-system`'s token-swap mechanism

## 8. Files to Create
- `feature/ramadan/presentation/laylatulqadr/LaylatulQadrReflectionScreen.kt`
- `feature/ramadan/presentation/laylatulqadr/LaylatulQadrThemeTokens.kt`

## 9. Files to Modify
- K-02's `RamadanJourneyMapViewModel`/Screen — consume `gamification_suppressed` to select the calm-mode node treatment
- K-03's `MissionDetailScreen` — consume the flag to suppress competitive framing/badge call-outs during content display

## 10. KMP Requirements
- **UI/Component:** a quieter, less-saturated visual treatment (per §2.1) applied wherever competitive framing would otherwise appear — no leaderboard styling, no competitive badge call-outs — for exactly the nights B-03 flags.
- **State:** the suppression flag is read directly from the already-fetched mission response (B-03) — no independent computation, no local list of "nights 21/23/25/27/29" anywhere in this sub-feature's code (mandatory structural guarantee, mirrors K-01's §7 item 1 discipline).
- **Screen variant:** dedicated Reflection screen for calmer scholar-approved content, and a calmer Night Recap variant, both selected purely by the flag.
- **Offline First:** consistent with K-02/K-03's existing offline pattern — no special-casing needed since the flag travels with the already-cached mission response.

## 11. NextJS Requirements
N/A.

## 12. API Contract
Consumes `gamification_suppressed` from `GET /v1/ramadan/missions/{night}` (B-03) — no dedicated endpoint of its own.

## 13. Database Requirements
The `gamification_suppressed` boolean is cached as part of the existing mission-content cache entity (K-03) — no separate table.

## 14. Validation
N/A.

## 15. Authentication
N/A beyond the standard session already established by K-02/K-03.

## 16. Authorization
N/A.

## 17. Error Handling
If the flag is unexpectedly absent from a cached/stale response, default to the standard (non-suppressed) presentation rather than guessing — never infer suppression client-side.

## 18. Offline First
Inherits K-02/K-03's offline-first behavior; the flag is part of the same cached payload.

## 19. Local Data
Part of the existing mission-content cache entity (K-03) — no new local storage.

## 20. Localization
Reflection content text fully localized across En/Hi/Ar/Ur via the same content pipeline as standard nights.

## 21. RTL
Full RTL layout for the calmer variant, consistent with the standard variant's RTL handling.

## 22. Analytics
`ramadan_laylatul_qadr_reflection_viewed` per §1.19.

## 23. Performance
Conditional theme-token application must not introduce extra recomposition cost beyond the standard variant's baseline — verified via the same stability annotations used in K-01/K-02.

## 24. Security
N/A beyond standard session handling.

## 26. Library Requirements
Kotlin, Jetpack Compose. No new libraries.

## 27. Testing
UI test: **mandatory** — both `gamification_suppressed = true` and `= false` states render correctly and distinctly (§7 item 3). **Mandatory structural test:** confirm no hardcoded night-number list (e.g. `[21, 23, 25, 27, 29]`) exists anywhere in `:feature:ramadan`'s source outside of test fixtures. Accessibility test: calm-mode content remains fully screen-reader navigable.

## 28. Documentation
KDoc explicitly stating this variant must never independently determine which nights are Laylatul Qadr — the flag is the single source of truth.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define `LaylatulQadrThemeTokens`**
Objective: Quieter, less-saturated token set per §2.1. Files to Create: `presentation/laylatulqadr/LaylatulQadrThemeTokens.kt`. Definition of Done: tokens defined, reviewed against §2.1's visual-language description.

**Task 02 — Wire the Suppression Flag into K-02's Journey Map**
Objective: Calm-mode node treatment when flagged. Files to Modify: K-02's ViewModel/Screen. Dependencies: Task 01. Tests: node-treatment-by-flag test. Definition of Done: test passes.

**Task 03 — Wire the Suppression Flag into K-03's Mission Detail**
Objective: Suppress competitive framing/badge call-outs when flagged. Files to Modify: K-03's `MissionDetailScreen`. Dependencies: Task 01. Tests: content-suppression test. Definition of Done: test passes.

**Task 04 — Build `LaylatulQadrReflectionScreen`**
Objective: Dedicated calmer reflection screen. Files to Create: `presentation/laylatulqadr/LaylatulQadrReflectionScreen.kt`. Dependencies: Task 01. Tests: UI test. Definition of Done: test passes.

**Task 05 — Build the Calmer Night Recap Variant**
Objective: Variant of K-02's Night Recap. Files to Modify: K-02's `NightRecapScreen.kt`. Dependencies: Task 01. Tests: variant-rendering test. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §27, both mandatory tests included. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Grep the entire `:feature:ramadan` module for any hardcoded night-number list; confirm none exists outside test fixtures. Definition of Done: checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] Both suppressed/non-suppressed states render correctly — mandatory test passing
- [ ] No hardcoded Laylatul Qadr night list anywhere in module source — mandatory structural check passing
- [ ] Calm-mode content remains fully accessible via screen reader
- [ ] Suppression flag correctly propagates into both Journey Map and Mission Detail

## 31. Definition of Done
Laylatul Qadr's tonal integrity is enforced automatically and reliably by a server-computed flag alone — never dependent on any client-side editorial memory or hardcoded date list.
