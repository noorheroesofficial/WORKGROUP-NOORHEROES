# NoorHeroes shared Snackbar — 22 October 2026

Implemented in the existing Figma library, KMP mobile application and existing local authentication review companion. Original reference designs, admin/public-web repositories, PRDs, navigation and API contracts remain unchanged. This is not a production-release certification.

## Source and Figma result

Inspected screen `1654:1428` and library page `1420:2`. The screen already used the approved master `1420:18`; retained that component ID and its exact Error appearance. It now belongs to the single `NH/Snackbar` variant family `1769:53`, alongside Success `1769:35`, Warning `1769:41` and Info `1769:47`. Non-error tones use existing semantic variables; callers supply meaningful messages.

Error contract: square #1C2B33 surface, white 12% one-pixel border, no shadow or leading icon, Poppins Regular 12/18 white message, SemiBold 12/18 gold action. At 390px screen width, the floating surface is 350px wide with 20px side margins and 24px bottom spacing. Minimum height60, padding16/8 horizontal and7 vertical, gap8, minimum44px action/dismiss targets. Text wraps and height grows.

All six active V2 consumers use the retained master. Corrected Login/Registration full-width drift and biometric fixed-height drift. OTP/PIN variable bindings, existing retry/dismiss reactions and navigation were preserved. Four stars overlapping the reference snackbar were hidden for readability. No active V2 Toast instance remains; historical reference pages were preserved.

- [Final node audit](figma/final-audit.json)
- [Reference screenshot](../Evidence/2026-10-22_Snackbar_Reference_Verified.png)
- [Four-tone and long-message previews](../Evidence/2026-10-22_Snackbar_Final_1420-34.png)

## Mobile implementation

One renderer and typed state live in `NoorHeroes/core/core-ui`; shared geometry/colors live in `core-designsystem`. All20 current transient consumers across Onboarding, Stories, Rewards and Bedtime use the shared system. No feature-level default Material SnackbarHost or platform Toast remains. Inline validation, persistent banners and celebration overlays remain in their appropriate roles. Screen-scoped hosts prevent stale feedback after leaving a screen.

The state supports Error/Success/Warning/Info, bounded FIFO admission, duplicate suppression, cancellation cleanup and exactly-once action results. Posting does not block navigation collectors. Actionable messages persist until action/dismissal; passive statuses use Material's accessibility-aware timeout. SafeDrawing/IME insets, wrapping content, localized dismissal and polite accessibility announcements are supported. Tablet widths adapt up to560dp while matching350dp at390dp mobile width.

See [runtime verification](runtime/verification-report.md), [API and usage audit](runtime/API-and-audit.md) and [exact changed-file inventory](runtime/changed-files.txt).

## Local review companion

The existing authentication prototype uses `snackbar-core.cjs`, one DOM renderer and centralized CSS. It supports semantic tones, a bounded queue, duplicates, six-second passive statuses, persistent retry actions, operation-specific retry callbacks, safe-area/visual-viewport placement, modal layering, Escape/dismiss controls and reduced-motion CSS. All message text is assigned through textContent. It remains a loopback mock, not production authentication.

`node --test snackbar.test.cjs auth.test.cjs http.test.cjs`: **9/9 pass**. `node --check app-v2.js`: pass. HTTP coverage exercises controlled status mapping and network/timeout recovery. No live production API requests were made.

## Verification and remaining gates

Figma source/final screenshots were visually inspected; all six current instances and four variants were inspected structurally. Long-message preview at280px grows to142px without clipping and retains44px controls. Native Present playback was not verified.

Mobile core-ui19/19, Onboarding295/295, Stories168/168 and Bedtime144/144 tests pass. Rewards143/147 pass: four unchanged MissionsViewModelTest fixtures dated2026-10-01 now appear expired against the real clock. This diagnosis is grounded in unchanged source, not an independent baseline rerun. Shared Android compilation and common Kotlin metadata compilation passed. A final semantic-border parity correction uses the existing theme border for non-error tones; its rerun is recorded in runtime/evidence/primary-final.log.

Final rerun after the semantic-border correction: **BUILD SUCCESSFUL**, core-ui19/19 and shared Android compilation, recorded in runtime/evidence/primary-final.log. Local9/9 rerun is recorded in local-validation.log; mobile diff whitespace check is clean.

Android/iOS device visuals, real IME/gesture insets, RTL/200% text, TalkBack/VoiceOver, iOS native binary and local browser playback remain unverified. Review these before release. No new production endpoint, authentication or business-rule behavior is introduced.
