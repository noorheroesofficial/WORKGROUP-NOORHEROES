# Learning Focus and Interests UI refinement

Applied 2026-10-22 to four existing V2 Figma Profile Setup states and shared CMP source.

- Headings and icons are outside and above separate white cards.
- Figma chip flow wraps with 8 px gaps, growing height, neutral borders, teal selected fills and checkmarks. Existing selection variables remain connected.
- Shared app profile chips use selected Surface semantics, 48 dp minimum height, wrapping text and content-driven height. Existing catalog IDs, selections, validation and save action are unchanged.
- Footer now reads only Add another child later, with teal link text and disabled styling in app.

## Changed source files
- NoorHeroes/feature/feature-onboarding/src/commonMain/kotlin/com/noorheroes/feature/onboarding/ui/AddChildPreferencesComponents.kt
- NoorHeroes/feature/feature-onboarding/src/commonMain/kotlin/com/noorheroes/feature/onboarding/ui/AddChildScreen.kt
- NoorHeroes/core/core-common/src/commonMain/composeResources/values/strings.xml

## Verification and limits
- Inspected Figma screenshots at 338 px and 300 px content widths, including mixed selected/unselected chips. No clipped chip labels in those checks.
- git diff --check passed.
- Android host tests: see 014_Profile_Chip_Fix_Final_Test.log.
- Native Android/iOS visual, keyboard, accessibility scaling and navigation testing not performed; adb unavailable on PATH, and iOS build/device testing unavailable on this Windows host.
- Figma Present playback not verified. The existing unmapped Figma Add Another destination remains unchanged.
- App and Figma retain their existing catalog wording; no unsupported API field was added.
