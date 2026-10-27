# Profile Setup refinement — 2026-10-22

Applied to all four existing V2 Add Child states. Removed requested Figma roots 1804:3252 and 1804:3346; duplicate-name recovery is now inline and keeps its disambiguation requirement. Twelve Learning Level cards have 12 px padding on all sides. Five field headings use 18 px icon canvases and 6 px gaps. Learning Focus and Interests are inline. Have multiple children? appears below Save.

## App changes
- AddChildComponents.kt: reusable ProfileSectionHeading and responsive Learning Level cards, equal padding, radio semantics, wrapping text.
- AddChildScreen.kt: five heading rows, inline preferences, IME padding, secondary action using existing validated save flow.
- ChildPreferredLanguageSheet.kt: shared language heading.
- AddChildPreferencesComponents.kt: inline Learning Focus and Interests using existing catalog IDs and selectedInterests persistence; existing daily goal and AI/voice controls retained.
- ProfilePreferenceGroups.kt and ProfilePreferenceGroupsTest.kt: catalog partition and unknown-ID preservation.
- core-common values/strings.xml: labels and multiple-child action.

Reused NoorChip, NoorToggle, existing inputs, native date picker, avatar carousel, language picker, ViewModel validation and save navigation. No DTO or API changes.

## Verification
- RED: grouping tests failed with the initial stub (014_Profile_CMP_RED.log).
- GREEN: :feature:feature-onboarding:testAndroidHostTest BUILD SUCCESSFUL; 311 tests, zero failures (014_Profile_CMP_GREEN.log).
- 116/116 Figma stored-action and structural checks passed; no dangling destinations. This is not live playback evidence.
- Inspected updated default Figma screenshot; lower form sections remain accessible through the existing form scroller with fixed Figma actions.

## Remaining limitations
- Live Figma Present testing remains blocked by browser access denial in this session. No claim of live playback verification.
- Android/iOS physical-device rendering, keyboard, text scaling and safe-area checks were not run. iOS build not run on Windows.
- Figma has no confirmed Add Another destination, so its secondary action remains unmapped; app saves before its existing Add Another prompt.
- Existing Figma accessibility controls do not yet have equivalent controls/state in this app screen. No new accessibility API contract was invented.
- Existing Figma 80-portrait library versus app catalog asset mapping remains unresolved.
- New English labels use resource fallback pending translations.
- Other pre-existing worktree changes were preserved.
