# Final Authentication Prototype — Review handoff

**Superseded by the [Login standardization handoff](Login_Standardization/README.md).** The current implementation uses one active Login, shared processing/snackbar overlays and inline validation. Twenty-one earlier variants are archived. Current verification:1,576saved-action assertions,552routes. The content below records the earlier implementation and must not be used as current layout/state guidance.

Saved 2026-10-19. Implementation is ready for design review; this is not implementation sign-off or production authentication.

## Open the work

- [Final Authentication section](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1355-2564)
- [Start at approved Login](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1355-2696)
- Structure: NoorHeroes V2 Design `1128:2` → Onboarding `1270:140` → Final Authentication `1355:2564`.
- Six groups: Approved Login, Country Selector, Button States, Loading States, Error & Retry States, Connected Prototype Flow.

## Sources and preservation

The current manually corrected Login `1330:5697` and country selector section `1330:5691` are the visual sources. The approved header wordmark, centered gold monogram, form geometry, colors and typography are preserved in the new default. No replacement visual direction was introduced.

Button `1334:678` supplies the disabled appearance (42% opacity); `1334:725` is an enabled Try again reference. The existing language loader `1259:140` supplies the morph and three-dot motion. Outer dimensions adapt to the approved Login button, 342 × 56 px. Login screens use 390 × 844 px.

Functional authority: `PRD_Documents/Child App (1-12)/Feature_A1_Splash_Auth_Onboarding.md`, particularly phone/email OTP, Google and six-digit OTP requirements; aligned with `Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/03-registration-consent-otp-verification-flow.md`. Protected source files were not modified.

Original/reference designs remain available. Superseded generated Login states are grouped outside active V2 in `1358:5860`. The former redesign section is now named Authentication Source References — Approved + Superseded. The old local October 18 companion is not the final UI.

## Implemented interactions

- Existing Intro Skip/final exits open the final Login. Login Back returns to the invoking approved Intro through four guarded branches.
- Phone/Email tabs preserve their separate inputs and readiness. Empty, incomplete, invalid and missing-country cases prevent submission.
- Country selector contains 245 sourced country rows and flags. Selection updates code and actual flag, retains the entered phone and requires revalidation.
- Full button morphs into a centered compact three-dot loader. Processing disables duplicate submissions and conflicting controls. Cancel/Back restores the originating method.
- Failure, offline recovery and a simulated 10-second timeout have matching retry paths and retained input. The loader stays active throughout the timeout wait.
- Google has simulated processing, cancellation and generic failure/retry; no OAuth service is connected.
- Search states, clear, empty results, data-unavailable recovery, selector dismissal and scrolling are connected.
- Longer error layouts can scroll to Register without moving the approved default form layout. Additional small/large/keyboard-viewport frames are inspection aids, not prototype starts.

## Pending boundaries — do not guess destinations

**User decision: leave success destination pending until OTP is approved.** No OTP frame or placeholder route was created. The simulated completed request restores the matching ready Login view; it does not indicate verified authentication. Replace that completion action only after an approved OTP destination exists. Source OTP references conflict with the PRD or contain unapproved additions.

Register also remains unmapped because no approved V2 destination is confirmed. The manually approved default no longer contains Forgot access; it was not reintroduced. Do not create subsequent screens automatically from this handoff.

## How to review the native simulation

Start at Final Authentication — Approved Login. Tap the input to populate a sourced valid example, choose a country, switch methods, and submit. Country changes disable submission until the input is validated again. Examples include US `2015550123`, India `8123456789`, and email `test@example.com`.

Keyboard fixture controls on Login:

| Key | Fixture |
| --- | --- |
| I | Incomplete input |
| F | Invalid format |
| Z | Empty input |
| M | Missing country, Phone mode only |
| S | Completed request scenario; OTP remains pending |
| N | Request failure scenario |
| T | Timeout scenario |
| O | Offline scenario |

Country search fixtures: click Search for `ind`, click again for `+971`; I = `ind`, U = `+971`, X = no results, C = clear, D = data-unavailable. Backdrop and Escape dismiss. Clear/retry keeps the sheet open without replaying its entrance.

These are explicit native prototype fixtures, not arbitrary typed input, country filtering, phone validation or network execution. Code Layers remain unavailable (`code_layers_enabled:false`); no Code Layer was imported.

## Verification and limits

[Saved graph audit](evidence/native-graph-audit.json): **1,256 assertions passed**, including all 245 country selections, exact flag exclusivity, input retention, submit gating, duplicate prevention, method changes, offline recovery, four Intro return origins and processing result branches. **847 node routes**, zero null/missing destinations and zero routes into superseded designs. This count includes repeated routes, not 847 distinct screens.

[Audit source](evidence/native-audit.mjs) evaluates the saved Figma reactions with a model of their variable/action behavior. Its syntax was checked with Node. It is not a live Present test. Static rendered checks cover [empty/disabled Login](evidence/login-empty-disabled.png), [India selected and ready](evidence/login-india-ready.png), [error](evidence/login-error.png), and [country selector](evidence/country-selector.png). Test variable changes were restored afterward.

Motion tracks and durations were inspected, including the 8.1-second compact hold timeline used after initial loading for the 10-second timeout. Actual Present playback was not exercised: browser access to figma.com is denied, and that restriction was not bypassed. Device rendering, actual keyboard avoidance, screen readers, dynamic text and runtime reduced-motion behavior remain unverified. No backend, OTP delivery, account session or real network recovery is implemented by Figma actions.

## Continuation notes

Before any next edit, re-read the live nodes and `../CURRENT_CONTEXT_AND_NEXT_SCREEN.md`; manual changes may have occurred. Keep the approved source frames unchanged and work in the final section. Native CONDITIONAL serialization retained only IF/ELSE in this environment, while nested conditionals were rejected. Multiple branches therefore use separate guarded top-level CONDITIONAL actions. Preserve this structure when updating processing outcomes or Intro return paths. Avoid self-navigation actions; preserve same-frame variable mutations instead.

Next review: inspect native playback when authorized access is available, approve the final Login, then approve the OTP content/layout before connecting success. No future route is authorized merely by this document.
