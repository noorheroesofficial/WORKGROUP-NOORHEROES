# V2 prompts 015–021: missing-content review

Date: 2026-10-23. Figma-only task. Existing file MR9935oQZACMjndzGIUgq5, mobile page928:2, V2 section1128:2.

The user requested a review of existing work, with only one separate screen for missing content. They then approved combining the family summary with the proposed short screen-time/notification primer copy. No application code was edited.

## Coverage and latest decisions

| Prompt | Current coverage / decision |
|---|---|
| 015 Avatar | Existing DOB-filtered, three-visible-avatar carousel1872:3298 reused by Add Child. No duplicate route created. Initial avatar composition inspected. Unavailable-catalog runtime behavior and live scrolling were not tested. |
| 016 Interests | Current approved Learning Focus selections remain inline. Standalone Interests, Daily Goal and Accessibility were explicitly removed by the user earlier; this task does not reintroduce them from older prompts. |
| 017 Learning Level | Existing three-level selection and descriptions remain in Add Child. The new summary reads its existing Level variable. |
| 018 Add Another | Existing footer and family-plan information sheet1965:6718 retained. The new review footer opens that same sheet. The general paid-plan multi-child loop is not supplied by this new screen; current existing direct sheet wiring is not eligibility-gated. |
| 019 Family summary | Added one separate editable review screen, using existing app strings and existing profile variables. Supports the current single-child review fixture. Edit opens existing valid-draft Add Child1806:3639. This is not server-backed saved-family persistence. |
| 020 Primer | Combined into the same screen using the user's newly approved copy below. Informational primer; it does not request OS permission or implement a settings toggle list. |
| 021 Optional path reveal | Not created: no verified recommendation content or approved screen-specific copy was found. The prompt expressly prohibits invented recommendation/religious content. |

## New Figma nodes

- Separate section2137:6634: `015–021 — Missing requirements / Family Summary Review`.
- One mobile screen2137:6635: `NH/V2/Onboarding/019/Learning Setup Summary/Review`,390×844.
- Existing NH Button, StatusBadge, approved avatar artwork, toolbar and shared star field reused; shared typography and palette variables retained.
- Existing nickname/DOB/language/level/Interest0–4 variables are read by the summary. The screen uses the existing review fixture mode, clearly identified by canvas notes outside the application frame.
- New summary-only boolean VariableID:2139:6741 controls the empty-focus dash, computed from the five existing selection booleans. No new colors or global component definitions created.
- Scroll viewport2139:6737 supports longer selected-focus summaries; action footer remains outside it.
- Confirm2137:6721 intentionally remains disabled. There is no approved V2 Profile Picker destination. The new screen is separate and is not inserted into the existing onboarding routes.
- No existing screen nodes were edited; the existing V2 parent expands to include the new section.

## Approved primer copy

Screen time & notifications

Manage screen time in the Parent Area.

Optional notifications are off by default. Safety alerts stay on.

Notification permission will be requested later.

## Sources and checks

Reviewed screen prompts015–021, Feature_A1_Splash_Auth_Onboarding.md (inventory and remaining-screen component table), KMP blueprint06-add-child-profile-flow.md, live V2 section inventory, current Add Child variables/components, and existing English resource strings in `NoorHeroes/core/core-common/src/commonMain/composeResources/values/strings.xml` (Learning Setup Summary / Profiles ready for your family adventure / Ready).

Visual evidence: `2026-10-23_Profile_Review_Before_015_021.png` and `2026-10-23_Combined_Summary_Primer.png`. The latter was re-rendered after correcting the avatar's parent height; avatar is64×64 and fully visible.

Structural checks:390×844, one new screen, confirmed Edit and sheet destination IDs, disabled Confirm, exact approved primer strings, independent scrolling body with footer outside, and all32 focus-selection combinations for the empty-focus expression. Default body498px fits its512px viewport; footer ends at722px within the738px card.

These are canvas, screenshot and stored-expression checks. Live Present playback, Android/iOS runtime, OS permission handling, backend persistence, multiple-child data rendering and production plan eligibility were not verified or implemented by this Figma-only task.
