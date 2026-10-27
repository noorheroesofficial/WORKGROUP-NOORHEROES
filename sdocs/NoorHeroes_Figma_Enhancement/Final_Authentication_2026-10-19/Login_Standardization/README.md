# Login standardization — final review handoff

**20 October selector refinement:** target1355:2713now matches reference1355:3070's white bordered container and spacing, with only the selected button dark #0F3333. Unselected labels use #606B72; selected labels are white. Both mode actions and input persistence were checked. This supersedes dark-selector-container descriptions below. The recorded full audit predates this color refinement; its dark-container style assertion is historical.

This update supersedes the earlier 22-screen Login implementation. Work remains in the existing Figma file, under NoorHeroes V2 Design → Onboarding → Final Authentication.

## Review links

- [Standard Login](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1355-2696)
- [Final Authentication section](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1355-2564)
- [Shared buttons and feedback](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1355-2567)
- [Prototype fixture guide](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1391-3057)

## Standardized layout

One active Login screen replaces21duplicate full-screen variations. Their incoming references were checked before they were moved to Reference Only — Superseded Login States `1386:5901`, outside active V2. No source artwork or unrelated screen was deleted.

The approved monogram and wordmark are centered above the card with their original proportions. The card is366px wide on the390×844standard canvas, with12px outer inset and12px horizontal inner padding. Inputs, segmented controls, Send code and Google share342px content width. Vertical card padding is20px; content sections use16px gaps and form controls12px gaps. Auto Layout replaces the legacy negative gaps and fixed content height. The card retains the approved asymmetric corner concept. Its466px height includes a reserved helper line so validation does not move the button.

The bottom prompt is exactly “Don't have an account? Create an account?” with a white prompt and brand-gold action, centered together and able to wrap. Registration is not connected because an approved destination is still unavailable.

## Reference fidelity

Active and Inactive appearance comes from1355:2567:342×56,18px radius, source teal gradient, Poppins SemiBold14/20; inactive opacity42%. The reusable set now has Default, Disabled, Pressed and Loading. The country-flag component was moved out of that button set into the shared-assets group.

The loader reuses1259:140's three10×10dots, white artwork, exact opacity keys, stagger and source teal surface. **The latest brief overrides shrinking behavior: the Login loading button stays342×56.** There is no separate success screen. Google keeps its approved light surface and uses dark dots for contrast.

The Login background uses the original Splash1131:2star artwork, colors and opacity tracks. Only stars in the unobstructed top and bottom bands are retained. The center remains clear. No new star or logo artwork was invented.

## Connected native behavior

- Intro Skip/final exits continue to the same main Login ID. Back still returns to the invoking one of four approved Intro screens.
- Phone/Email switch the same form through variables, preserve separate input values and recalculate readiness.
- Corrected valid fixtures enable Send code; empty, incomplete, malformed and missing-country fixtures disable it. A red outline and one aligned inline message show the current field error. Correction clears that error.
- A fixed button slot prevents collapse when loading starts. Duplicate Send code and Google submissions are guarded. Processing overlays block conflicting input and provide tappable Back cancellation plus Escape.
- Normal processing lasts1.95seconds. Timeout processing continues for8.05more seconds before its snackbar, totaling10seconds. Source dot keys cover the processing interval.
- API failure, offline and timeout feedback use one shared snackbar, preserving the form and entered values. Retry repeats only the failed OTP/Google operation and simulates recovery. An invalid identifier cannot bypass validation through Retry.
- Snackbar Retry and Dismiss are44×44touch targets. The standard390×844composition places the60px snackbar at y772,10px below the registration row and12px above the bottom. It dismisses after6seconds, Escape, Dismiss or a tap outside it.
- All245country rows update the real selected flag/code, retain the phone, clear obsolete country errors, require revalidation and close the picker. The missing country-commit controller was recreated.
- Search, clear, no-results and data-unavailable fixtures remain connected.

## Test controls

Tap an input to populate a sourced valid example. Phone fixtures depend on the selected country's existing example data. Email uses `test@example.com`.

| Key | Action |
| --- | --- |
| I | Incomplete input |
| F | Invalid format |
| Z | Empty required-field validation |
| M | Missing country, Phone only |
| S | Completed request scenario |
| N | API failure scenario |
| T |10-second timeout scenario |
| O | Offline snackbar |
| R | Toggle reduced-motion preview |
| Escape | Back/cancel/dismiss, according to current view |

Select S/N/T before submitting. Retry switches to the completed-request fixture to demonstrate recovery. R hides decorative stars and replaces pulsing dots with static dots; it does not read OS preferences.

Country search: click Search for `ind`, again for `+971`; I/U/X/C/D select the name/code/no-results/clear/data-failure fixtures. These are documented fixtures, not arbitrary live text filtering.

## Pending destinations

The user's instruction to leave OTP success pending remains in force. Completed requests restore the appropriate enabled Login state and close processing; they do not navigate to an invented OTP or create a session. Connect only after OTP content/layout is approved. Registration remains unmapped under the same rule.

## Verification

[Saved-action audit](evidence/saved-action-audit.json): **1,576 assertions passed**, all245country selections,552node routes, zero missing destinations and zero active links into the archive. The [audit source](evidence/saved-action-audit.mjs) evaluates the actual saved reaction graph and variables; it is not live Present playback.

Static checks and evidence:

- [Default390×844](evidence/login-default.png)
- [Small320×568](evidence/login-small-320.png): card296px/content272px; the segmented-control overflow found during inspection was fixed. The page scrolls to lower actions.
- Large430×932was also rendered and inspected: card406px/content382px, with centered branding and aligned controls.
- Inline validation was rendered with identical field/button positions and red outline/helper text.
- [Loading composition](evidence/login-loading-composition.png)
- [Snackbar composition](evidence/login-snackbar-composition.png)

Loading/snackbar composition images temporarily combine their native overlay with the Login for visual inspection; they are not Present screenshots. All preview nodes were removed, variables restored, and the canvas returned to390×844. No persistent QA screen duplicates were added.

## Limits and remaining review

Native input and search use fixtures. No real API, phone validation service, OTP delivery, account session or OAuth was implemented. Code Layers were unavailable in the existing account context; no alternative file/import was created.

Live Present playback remains unverified because browser permission denies figma.com; that restriction was not bypassed. No video render was attempted because no frame extractor was available. Motion was checked through saved tracks and durations.

Small and large static layouts were checked, but actual OS keyboard opening, automatic focus/scroll, device safe areas, screen-reader traversal, text scaling and platform reduced-motion detection are **not verified**. Native loading/snackbar overlays are authored for the standard390×844flow. The snackbar is a dismissible native overlay: it must be dismissed before interacting with the underlying form. It is not a production non-modal toast. Verify keyboard-aware overlay positioning and touch-through behavior in application implementation.

Source PRDs/blueprints/Screens stayed read-only. Future work must read the current handoff and live Figma, preserve original assets, and not promote an unapproved future destination.

