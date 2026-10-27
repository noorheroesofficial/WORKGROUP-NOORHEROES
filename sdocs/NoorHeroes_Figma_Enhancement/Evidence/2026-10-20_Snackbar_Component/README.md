# Reusable Snackbar component

Created 20 October 2026 in the existing NoorHeroes Figma file.

## Open the work

- [NH/Snackbar component](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1420-18)
- [Snackbar library page](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1420-2)
- [Six configuration specimens](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1420-34)
- [Interactive demo starting frame](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1420-89)
- [Bottom overlay demo/template](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1420-98)

## Source fidelity

The live references were1383:3295 and1383:3294. Their current treatment has **square corners**, a dark #1C2B33 surface, 1px white border at12%alpha, Poppins Regular12/18message, light gold Poppins SemiBold12/18action, and a centered × dismissal glyph. This intentionally follows the current square reference rather than earlier rounded snapshots.

Default component size is350×60. Its effective vertical inset is8px, implemented as7px Auto Layout padding plus the1px stroke included in layout. The default message/action/dismiss positions therefore match the reference. Minimum control targets are44×44. The component height grows for wrapped copy; a280px specimen grows to70px without clipping. Long action labels grow their control width.

The390×844overlay reproduces the reference's390×72bar at x0/y772. This edge placement is a prototype template, not device safe-area verification.

## Component API

| Property | Type | Default |
| --- | --- | --- |
| Message | Text | Unable to send the code. Please try again. |
| Action label | Text | Retry |
| Show action | Boolean | true |
| Show dismiss | Boolean | true |

One master covers action+dismiss, dismiss-only, action-only, message-only, narrow wrapping and longer-action-label examples. No semantic tone variants or replacement Toast family were invented. Existing NH/Toast components are unchanged.

Shared message style NH/Intro/Content/Description was reused because its Poppins Regular12/18 and zero letter spacing exactly match. New NH/Snackbar/Action and NH/Snackbar/Dismiss text styles cover the remaining roles. Component-scoped variables alias existing brand ink/white and preserve the reference's exact action gold. Border alpha has its own RGBA token; binding opaque white and separately setting paint alpha was found to overwrite the alpha, so the border token explicitly resolves to12%.

## Interaction ownership

The reusable master carries no Login variables, API logic or destination routes. Its generic Action is intentionally host-owned. Dismiss uses Close Overlay.

The separate demo has a Show snackbar button, local feedback variable, action feedback and dismissal. Retry closes the overlay and records “Retry requested — demo only.” Dismiss, Escape and an outside tap close it; the timeout is6seconds. This is a native prototype simulation and sends no request. The original Login snackbar, failed-operation routing and overlay were not replaced or disconnected.

For a consuming screen, duplicate the overlay template, override Action on that instance with the screen's confirmed retry behavior, and retain its form state. Do not wire a generic snackbar to Login/OTP or another guessed destination. Screen/application logic owns duplicate-request prevention, safe-area/keyboard positioning and accessible announcements.

## Verification

[Audit](audit.json): **55component/interaction checks passed**, plus7source-preservation checks. Tests cover properties, source dimensions/corners/colors/alpha, shared typography, wrapping, absence of clipping, minimum44px controls, optional controls, source-matched overlay placement, valid demo destination, timeout, retry/dismiss feedback and isolation from Login variables.

[Final component review](component-review.png) shows all six configurations. A static host+overlay composition was also visually inspected; temporary preview nodes were removed. Saved reaction definitions and static rendering were verified. Live Present playback, screen readers, actual keyboard/safe-area behavior and backend integration remain unverified.

[State manifest](figma-state.json) and [saved-action audit source](audit.mjs). Source PRD/blueprints/Screens were not modified.

